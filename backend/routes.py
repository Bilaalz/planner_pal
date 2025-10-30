"""
API routes for the Planner Pal application.

This module contains all the Flask route handlers for the REST API,
including file upload, event CRUD operations, and health checks.
"""

from flask import request, jsonify, Response
import PyPDF2
import io
from typing import Dict, Any
from datetime import datetime
import pytz
from icalendar import Calendar, Event as ICalEvent

from models import (
    get_next_event_id, get_all_events, 
    get_event_by_id, update_event, delete_event, events, next_event_id
)
from extractor import extract_deadlines_from_text

def extract_text_from_pdf(file) -> str:
    """
    Extract text content from an uploaded PDF file.
    
    Args:
        file: Flask file object containing the PDF
        
    Returns:
        str: Extracted text content
        
    Raises:
        Exception: If PDF reading fails
    """
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

def upload_pdf_handler():
    """
    Handle PDF upload and extract academic deadlines.
    
    This endpoint:
    1. Validates the uploaded file
    2. Extracts text from the PDF
    3. Parses deadlines using the advanced algorithm
    4. Converts them to calendar events
    5. Stores them in memory
    
    Returns:
        JSON response with extracted events or error message
    """
    # Validate file upload
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'File must be a PDF'}), 400
    
    try:
        # Extract text from PDF
        text = extract_text_from_pdf(file)
        print(f"Extracted text length: {len(text)}")  # Debug
        
        # Extract deadlines using the advanced algorithm
        extracted_events = extract_deadlines_from_text(text)
        print(f"Extracted {len(extracted_events)} events")  # Debug
        
        # Convert to calendar events and store
        new_events = []
        global next_event_id
        
        for event_data in extracted_events:
            event = {
                'id': next_event_id,
                'title': event_data['title'],
                'type': event_data['type'],
                'start': event_data['start'],
                'end': event_data['end'],
                'allDay': event_data['allDay'],
                'source': 'pdf_upload',
                'extracted_from': event_data['extracted_from'],
                'description': '',
                'course': ''
            }
            
            # Add event directly to the events list
            events.append(event)
            new_events.append(event)
            next_event_id += 1
        
        print(f"Successfully processed {len(new_events)} events")  # Debug
        return jsonify({
            'message': f'Successfully extracted {len(new_events)} deadlines from syllabus',
            'events': new_events,
            'total_events': len(get_all_events())
        }), 200
        
    except Exception as e:
        print(f"Error in PDF upload: {str(e)}")  # Debug
        return jsonify({'error': str(e)}), 500

def get_events_handler():
    """
    Retrieve all events from storage.
    
    Returns:
        JSON response containing all events
    """
    return jsonify({'events': get_all_events()}), 200

def create_event_handler():
    """
    Create a new manual event.
    
    Expected JSON payload:
    {
        "title": "Event title",
        "start": "2024-01-01T00:00:00",
        "end": "2024-01-01T23:59:00",
        "type": "Assignment",
        "allDay": true,
        "description": "Optional description",
        "course": "Optional course name"
    }
    
    Returns:
        JSON response with created event or error message
    """
    data = request.get_json()
    required_fields = ['title', 'start', 'end']
    
    # Validate required fields
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create new event
    global next_event_id
    event = {
        'id': next_event_id,
        'title': data['title'],
        'type': data.get('type', 'Assignment'),
        'start': data['start'],
        'end': data['end'],
        'allDay': data.get('allDay', True),
        'source': 'manual',
        'description': data.get('description', ''),
        'course': data.get('course', ''),
        'extracted_from': ''
    }
    
    # Add event directly to the events list
    events.append(event)
    next_event_id += 1
    
    return jsonify({'message': 'Event created successfully', 'event': event}), 201

def update_event_handler(event_id: int):
    """
    Update an existing event.
    
    Args:
        event_id: ID of the event to update
        
    Returns:
        JSON response with updated event or error message
    """
    # Check if event exists
    event = get_event_by_id(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    data = request.get_json()
    
    # Update event fields
    success = update_event(event_id, data)
    
    if success:
        updated_event = get_event_by_id(event_id)
        return jsonify({'message': 'Event updated successfully', 'event': updated_event}), 200
    else:
        return jsonify({'error': 'Failed to update event'}), 500

def delete_event_handler(event_id: int):
    """
    Delete an event by ID.
    
    Args:
        event_id: ID of the event to delete
        
    Returns:
        JSON response with success/error message
    """
    global events
    original_length = len(events)
    events = [e for e in events if e['id'] != event_id]
    
    if len(events) < original_length:
        return jsonify({'message': 'Event deleted successfully'}), 200
    else:
        return jsonify({'error': 'Event not found'}), 404

def export_ics_handler():
    """
    Export all events as an ICS (iCalendar) file.
    
    This function creates a standard iCalendar file that can be imported
    into Google Calendar, Outlook, Apple Calendar, and other calendar applications.
    
    Returns:
        ICS file download response
    """
    try:
        # Create a new calendar
        cal = Calendar()
        cal.add('prodid', '-//Planner Pal//Academic Calendar//EN')
        cal.add('version', '2.0')
        cal.add('calscale', 'GREGORIAN')
        cal.add('method', 'PUBLISH')
        cal.add('X-WR-CALNAME', 'Planner Pal Academic Calendar')
        cal.add('X-WR-CALDESC', 'Academic events and deadlines extracted from syllabi')
        
        # Add all events to the calendar
        for event in events:
            ical_event = ICalEvent()
            
            # Set event properties
            ical_event.add('summary', event['title'])
            ical_event.add('description', event.get('description', ''))
            ical_event.add('location', event.get('course', ''))
            
            # Convert dates to datetime objects
            start_dt = datetime.fromisoformat(event['start'].replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(event['end'].replace('Z', '+00:00'))
            
            # Set start and end times
            ical_event.add('dtstart', start_dt)
            ical_event.add('dtend', end_dt)
            
            # Add event type as categories
            ical_event.add('categories', [event.get('type', 'Assignment')])
            
            # Add unique identifier
            ical_event.add('uid', f"planner-pal-{event['id']}@plannerpal.com")
            
            # Add creation timestamp
            ical_event.add('dtstamp', datetime.now(pytz.UTC))
            
            # Add to calendar
            cal.add_component(ical_event)
        
        # Generate ICS content
        ics_content = cal.to_ical()
        
        # Create response
        response = Response(
            ics_content,
            mimetype='text/calendar',
            headers={
                'Content-Disposition': 'attachment; filename=planner_pal_calendar.ics',
                'Content-Type': 'text/calendar; charset=utf-8'
            }
        )
        
        return response
        
    except Exception as e:
        return jsonify({'error': f'Failed to export calendar: {str(e)}'}), 500

def health_check_handler():
    """
    Health check endpoint to verify API status.
    
    Returns:
        JSON response with API status
    """
    return jsonify({
        'status': 'healthy', 
        'message': 'Planner Pal API is running',
        'total_events': len(get_all_events())
    })
