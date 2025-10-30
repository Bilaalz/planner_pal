/**
 * EventModal component for creating and editing calendar events.
 * 
 * This modal provides a form interface for users to create new events or edit
 * existing ones. It handles both all-day and timed events with proper date/time
 * input handling and validation.
 */

import React, { useState, useEffect } from 'react';

/**
 * EventModal component that provides a form for event creation and editing.
 * 
 * @param {Object} props - Component props
 * @param {Object|null} props.event - Event to edit (null for new events)
 * @param {Function} props.onSave - Callback when event is saved
 * @param {Function} props.onClose - Callback when modal is closed
 */
function EventModal({ event, onSave, onClose }) {
  // Form state management
  const [formData, setFormData] = useState({
    title: '',
    type: 'Assignment',
    start: '',
    end: '',
    allDay: true,
    description: '',
    course: ''
  });

  // Initialize form data when event prop changes
  useEffect(() => {
    if (event) {
      // Convert dates to local format for input fields
      const startDate = new Date(event.start);
      const endDate = new Date(event.end);
      
      setFormData({
        title: event.title || '',
        type: event.type || 'Assignment',
        start: startDate.toISOString().slice(0, 16), // YYYY-MM-DDTHH:MM format
        end: endDate.toISOString().slice(0, 16),
        allDay: event.allDay !== false,
        description: event.description || '',
        course: event.course || ''
      });
    } else {
      // Reset form for new event with default values
      const now = new Date();
      const tomorrow = new Date(now);
      tomorrow.setDate(tomorrow.getDate() + 1);
      
      setFormData({
        title: '',
        type: 'Assignment',
        start: now.toISOString().slice(0, 16),
        end: tomorrow.toISOString().slice(0, 16),
        allDay: true,
        description: '',
        course: ''
      });
    }
  }, [event]);

  /**
   * Handles input field changes for all form fields.
   * 
   * @param {Event} e - Input change event
   */
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  /**
   * Handles form submission and converts data to API format.
   * 
   * @param {Event} e - Form submit event
   */
  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Convert to ISO format for API consumption
    const eventData = {
      ...formData,
      start: new Date(formData.start).toISOString(),
      end: new Date(formData.end).toISOString()
    };
    
    onSave(eventData);
  };

  /**
   * Handles all-day checkbox changes and adjusts form accordingly.
   * 
   * @param {Event} e - Checkbox change event
   */
  const handleAllDayChange = (e) => {
    const isAllDay = e.target.checked;
    setFormData(prev => ({
      ...prev,
      allDay: isAllDay,
      // If switching to all day, set end to same day as start
      end: isAllDay ? prev.start : prev.end
    }));
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        {/* Modal header with title and close button */}
        <div className="modal-header">
          <h2>{event ? 'Edit Event' : 'Add New Event'}</h2>
          <button className="close-button" onClick={onClose}>
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          {/* Event title input */}
          <div className="form-group">
            <label htmlFor="title">Event Title *</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              placeholder="Enter event title"
            />
          </div>

          {/* Event type selection */}
          <div className="form-group">
            <label htmlFor="type">Event Type</label>
            <select
              id="type"
              name="type"
              value={formData.type}
              onChange={handleChange}
            >
              <option value="Assignment">Assignment</option>
              <option value="Exam">Exam</option>
              <option value="Project">Project</option>
              <option value="Lab">Lab</option>
              <option value="Other">Other</option>
            </select>
          </div>

          {/* Optional course field */}
          <div className="form-group">
            <label htmlFor="course">Course (optional)</label>
            <input
              type="text"
              id="course"
              name="course"
              value={formData.course}
              onChange={handleChange}
              placeholder="e.g., CS101"
            />
          </div>

          {/* All-day event checkbox */}
          <div className="form-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={formData.allDay}
                onChange={handleAllDayChange}
              />
              <span>All Day Event</span>
            </label>
          </div>

          {/* Start date/time input */}
          <div className="form-group">
            <label htmlFor="start">Start Date & Time *</label>
            <input
              type={formData.allDay ? "date" : "datetime-local"}
              id="start"
              name="start"
              value={formData.allDay ? formData.start.slice(0, 10) : formData.start}
              onChange={handleChange}
              required
              step={formData.allDay ? undefined : "60"}
            />
          </div>

          {/* End date/time input (only shown for timed events) */}
          {!formData.allDay && (
            <div className="form-group">
              <label htmlFor="end">End Date & Time *</label>
              <input
                type="datetime-local"
                id="end"
                name="end"
                value={formData.end}
                onChange={handleChange}
                required
                step="60"
              />
            </div>
          )}

          {/* Optional description field */}
          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="3"
              placeholder="Optional description"
            />
          </div>

          {/* Form action buttons */}
          <div className="form-actions">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              {event ? 'Update Event' : 'Create Event'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default EventModal;
