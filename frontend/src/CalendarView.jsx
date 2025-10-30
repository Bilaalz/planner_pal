/**
 * CalendarView component for displaying and managing calendar events.
 * 
 * This component uses react-big-calendar to display events in multiple views
 * (month, week, day, agenda) and provides functionality for event interaction
 * including viewing details, editing, and deleting events.
 */

import React, { useState } from 'react';
import { Calendar, dateFnsLocalizer } from 'react-big-calendar';
import format from 'date-fns/format';
import parse from 'date-fns/parse';
import startOfWeek from 'date-fns/startOfWeek';
import getDay from 'date-fns/getDay';
import enUS from 'date-fns/locale/en-US';
import 'react-big-calendar/lib/css/react-big-calendar.css';

// Configure date-fns localizer for react-big-calendar
const locales = { 'en-US': enUS };
const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
});

/**
 * CalendarView component that displays events in an interactive calendar.
 * 
 * @param {Object} props - Component props
 * @param {Array} props.events - Array of event objects to display
 * @param {Function} props.onEditEvent - Callback for editing an event
 * @param {Function} props.onDeleteEvent - Callback for deleting an event
 */
function CalendarView({ events, onEditEvent, onDeleteEvent }) {
  // State management for calendar view and interactions
  const [view, setView] = useState('month'); // Current calendar view (month, week, day, agenda)
  const [date, setDate] = useState(new Date()); // Currently displayed date
  const [selectedEvent, setSelectedEvent] = useState(null); // Event selected for popup

  // Convert backend events to calendar format with proper Date objects
  const calendarEvents = events.map(ev => ({
    ...ev,
    start: typeof ev.start === 'string' ? new Date(ev.start) : ev.start,
    end: typeof ev.end === 'string' ? new Date(ev.end) : ev.end,
  }));

  /**
   * Handles event selection when user clicks on a calendar event.
   * 
   * @param {Object} event - The selected event object
   */
  const handleSelectEvent = (event) => {
    setSelectedEvent(event);
  };

  /**
   * Closes the event details popup.
   */
  const handleClosePopup = () => {
    setSelectedEvent(null);
  };

  /**
   * Handles editing the selected event.
   * Calls the parent component's onEditEvent callback.
   */
  const handleEdit = () => {
    if (selectedEvent) {
      onEditEvent(selectedEvent);
      setSelectedEvent(null);
    }
  };

  /**
   * Handles deleting the selected event after user confirmation.
   * Calls the parent component's onDeleteEvent callback.
   */
  const handleDelete = () => {
    if (selectedEvent && window.confirm('Are you sure you want to delete this event?')) {
      onDeleteEvent(selectedEvent.id);
      setSelectedEvent(null);
    }
  };

  /**
   * Determines the styling for calendar events based on their type.
   * 
   * @param {Object} event - The event object
   * @returns {Object} Style object for the event
   */
  const eventStyleGetter = (event) => {
    const type = event.type?.toLowerCase() || 'assignment';
    let backgroundColor = '#4299e1'; // Default blue for assignments
    
    // Color coding based on event type
    switch (type) {
      case 'exam':
        backgroundColor = '#e53e3e'; // Red for exams
        break;
      case 'project':
        backgroundColor = '#38a169'; // Green for projects
        break;
      case 'lab':
        backgroundColor = '#d69e2e'; // Yellow for labs
        break;
      default:
        backgroundColor = '#4299e1'; // Blue for assignments
    }

    return {
      style: {
        backgroundColor,
        borderRadius: '6px',
        border: 'none',
        color: 'white',
        fontSize: '0.85rem',
        fontWeight: '500',
        padding: '2px 6px',
      }
    };
  };

  /**
   * Custom event component for displaying event details in calendar cells.
   * 
   * @param {Object} props - Component props
   * @param {Object} props.event - The event object
   */
  const CustomEvent = ({ event }) => (
    <div className="rbc-event-content">
      <strong>{event.title}</strong>
      {event.course && <div style={{ fontSize: '0.75rem', opacity: 0.9 }}>{event.course}</div>}
      {event.type && <div style={{ fontSize: '0.75rem', opacity: 0.9 }}>{event.type}</div>}
    </div>
  );

  return (
    <div className="calendar-container">
      {/* Calendar header with title and description */}
      <div className="calendar-header">
        <h2>Academic Calendar</h2>
        <p>View and manage your deadlines and events</p>
      </div>
      
      {/* Main calendar component */}
      <div className="calendar-wrapper">
        <Calendar
          localizer={localizer}
          events={calendarEvents}
          startAccessor="start"
          endAccessor="end"
          style={{ height: 500 }}
          views={['month', 'week', 'day', 'agenda']}
          view={view}
          onView={setView}
          date={date}
          onNavigate={setDate}
          onSelectEvent={handleSelectEvent}
          eventPropGetter={eventStyleGetter}
          components={{
            event: CustomEvent
          }}
          popup
        />
      </div>

      {/* Event Details Popup - shown when user clicks on an event */}
      {selectedEvent && (
        <div className="event-popup-overlay" onClick={handleClosePopup}>
          <div className="event-popup" onClick={(e) => e.stopPropagation()}>
            {/* Popup header with event title and close button */}
            <div className="event-popup-header">
              <h3>{selectedEvent.title}</h3>
              <button className="close-popup" onClick={handleClosePopup}>×</button>
            </div>
            
            {/* Event details content */}
            <div className="event-popup-content">
              <div className="event-detail">
                <strong>Type:</strong> {selectedEvent.type || 'Assignment'}
              </div>
              
              <div className="event-detail">
                <strong>Date:</strong> {selectedEvent.start.toLocaleDateString()}
              </div>
              
              {/* Show time only if not an all-day event */}
              {!selectedEvent.allDay && (
                <div className="event-detail">
                  <strong>Time:</strong> {selectedEvent.start.toLocaleTimeString()} - {selectedEvent.end.toLocaleTimeString()}
                </div>
              )}
              
              {/* Optional description field */}
              {selectedEvent.description && (
                <div className="event-detail">
                  <strong>Description:</strong> {selectedEvent.description}
                </div>
              )}
              
              {/* Optional course field */}
              {selectedEvent.course && (
                <div className="event-detail">
                  <strong>Course:</strong> {selectedEvent.course}
                </div>
              )}
              
              {/* Show extraction source for PDF-imported events */}
              {selectedEvent.source === 'pdf_upload' && selectedEvent.extracted_from && (
                <div className="event-detail">
                  <strong>Extracted from:</strong> 
                  <div className="extracted-text">"{selectedEvent.extracted_from}"</div>
                </div>
              )}
            </div>
            
            {/* Action buttons for edit and delete */}
            <div className="event-popup-actions">
              <button className="btn btn-secondary" onClick={handleEdit}>
                ✏️ Edit
              </button>
              <button className="btn btn-danger" onClick={handleDelete}>
                🗑️ Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default CalendarView;
