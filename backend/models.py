"""
Data models and constants for the Planner Pal application.

This module contains the data structures, constants, and helper functions
used throughout the application for managing events and configuration.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

# Event types allowed in the system
ALLOWED_TYPES = ["Lab", "Assignment", "Exam", "Midterm", "Quiz", "Project", "Other"]

# In-memory storage for events (in production, use a database)
events: List[Dict[str, Any]] = []
next_event_id: int = 1

class Event:
    """
    Represents a calendar event with all necessary properties.
    
    Attributes:
        id (int): Unique identifier for the event
        title (str): Display name of the event
        type (str): Type of event (Lab, Assignment, Exam, etc.)
        start (str): ISO format start datetime
        end (str): ISO format end datetime
        allDay (bool): Whether the event spans the entire day
        source (str): How the event was created ('pdf_upload' or 'manual')
        description (str, optional): Additional details about the event
        course (str, optional): Course name associated with the event
        extracted_from (str, optional): Original text that generated this event
    """
    
    def __init__(self, 
                 id: int,
                 title: str,
                 start: str,
                 end: str,
                 type: str = "Assignment",
                 allDay: bool = True,
                 source: str = "manual",
                 description: str = "",
                 course: str = "",
                 extracted_from: str = ""):
        self.id = id
        self.title = title
        self.type = type
        self.start = start
        self.end = end
        self.allDay = allDay
        self.source = source
        self.description = description
        self.course = course
        self.extracted_from = extracted_from
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the event to a dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'start': self.start,
            'end': self.end,
            'allDay': self.allDay,
            'source': self.source,
            'description': self.description,
            'course': self.course,
            'extracted_from': self.extracted_from
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Event':
        """Create an Event instance from a dictionary."""
        return cls(
            id=data.get('id', 0),
            title=data.get('title', ''),
            start=data.get('start', ''),
            end=data.get('end', ''),
            type=data.get('type', 'Assignment'),
            allDay=data.get('allDay', True),
            source=data.get('source', 'manual'),
            description=data.get('description', ''),
            course=data.get('course', ''),
            extracted_from=data.get('extracted_from', '')
        )

def get_next_event_id() -> int:
    """Get the next available event ID and increment the counter."""
    global next_event_id
    current_id = next_event_id
    next_event_id += 1
    return current_id

def add_event(event: Event) -> None:
    """Add an event to the in-memory storage."""
    events.append(event.to_dict())

def add_event_dict(event_dict: Dict[str, Any]) -> None:
    """Add an event dictionary directly to the in-memory storage."""
    events.append(event_dict)

def get_all_events() -> List[Dict[str, Any]]:
    """Get all events from storage."""
    return events

def get_event_by_id(event_id: int) -> Optional[Dict[str, Any]]:
    """Get a specific event by its ID."""
    return next((e for e in events if e['id'] == event_id), None)

def update_event(event_id: int, updates: Dict[str, Any]) -> bool:
    """
    Update an event with new data.
    
    Args:
        event_id: ID of the event to update
        updates: Dictionary of fields to update
        
    Returns:
        bool: True if event was found and updated, False otherwise
    """
    event = get_event_by_id(event_id)
    if not event:
        return False
    
    for key, value in updates.items():
        if key != 'id':  # Don't allow changing the ID
            event[key] = value
    
    return True

def delete_event(event_id: int) -> bool:
    """
    Delete an event by its ID.
    
    Args:
        event_id: ID of the event to delete
        
    Returns:
        bool: True if event was found and deleted, False otherwise
    """
    global events
    original_length = len(events)
    events = [e for e in events if e['id'] != event_id]
    return len(events) < original_length
