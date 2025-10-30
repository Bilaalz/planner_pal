/**
 * Main App component for Planner Pal.
 * 
 * This is the root component that manages the overall application state and
 * coordinates between the calendar view, event modal, and PDF upload functionality.
 * It handles all API communication with the backend and manages the event data.
 */

import React, { useState, useEffect } from "react";
import CalendarView from "./CalendarView";
import EventModal from "./EventModal";
import "./App.css";

function App() {
  // State management for events and UI
  const [file, setFile] = useState(null); // Selected PDF file
  const [uploadStatus, setUploadStatus] = useState(""); // Status message for uploads
  const [events, setEvents] = useState([]); // Array of all calendar events
  const [showEventModal, setShowEventModal] = useState(false); // Controls event modal visibility
  const [editingEvent, setEditingEvent] = useState(null); // Event being edited (null for new events)
  const [loading, setLoading] = useState(false); // Loading state for PDF processing

  // Load events from backend on component mount
  useEffect(() => {
    fetchEvents();
  }, []);

  /**
   * Fetches all events from the backend API.
   * Called on component mount and after successful operations.
   */
  const fetchEvents = async () => {
    try {
      const response = await fetch("http://localhost:5000/events");
      const data = await response.json();
      if (response.ok) {
        setEvents(data.events);
      }
    } catch (error) {
      console.error("Error fetching events:", error);
    }
  };

  /**
   * Handles file selection for PDF upload.
   * 
   * @param {Event} e - File input change event
   */
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setUploadStatus("");
  };

  /**
   * Handles PDF file upload and deadline extraction.
   * 
   * @param {Event} e - Form submit event
   */
  const handlePdfUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setUploadStatus("Please select a PDF file first.");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5000/upload-pdf", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        setUploadStatus(`Success: ${data.message}`);
        // Add new events to existing events instead of replacing them
        setEvents(prevEvents => [...prevEvents, ...data.events]);
        setFile(null);
        // Reset file input
        e.target.reset();
      } else {
        setUploadStatus(`Error: ${data.error}`);
      }
    } catch (error) {
      console.error('Error uploading PDF:', error);
      setUploadStatus(`Error uploading file: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Opens the event modal for creating a new event.
   */
  const handleCreateEvent = () => {
    setEditingEvent(null);
    setShowEventModal(true);
  };

  /**
   * Opens the event modal for editing an existing event.
   * 
   * @param {Object} event - The event to edit
   */
  const handleEditEvent = (event) => {
    setEditingEvent(event);
    setShowEventModal(true);
  };

  /**
   * Deletes an event after user confirmation.
   * 
   * @param {number} eventId - ID of the event to delete
   */
  const handleDeleteEvent = async (eventId) => {
    if (window.confirm("Are you sure you want to delete this event?")) {
      try {
        const response = await fetch(`http://localhost:5000/events/${eventId}`, {
          method: "DELETE",
        });
        
        if (response.ok) {
          setEvents(events.filter(e => e.id !== eventId));
          setUploadStatus("Event deleted successfully");
        } else {
          setUploadStatus("Error deleting event");
        }
      } catch (error) {
        setUploadStatus("Error deleting event");
      }
    }
  };

  /**
   * Saves an event (either new or updated) to the backend.
   * 
   * @param {Object} eventData - The event data to save
   */
  const handleSaveEvent = async (eventData) => {
    try {
      let response;
      if (editingEvent) {
        // Update existing event
        response = await fetch(`http://localhost:5000/events/${editingEvent.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(eventData),
        });
      } else {
        // Create new event
        response = await fetch("http://localhost:5000/events", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(eventData),
        });
      }

      const data = await response.json();
      if (response.ok) {
        await fetchEvents(); // Refresh events
        setShowEventModal(false);
        setUploadStatus(editingEvent ? "Event updated successfully" : "Event created successfully");
      } else {
        setUploadStatus(`Error: ${data.error}`);
      }
    } catch (error) {
      setUploadStatus("Error saving event");
    }
  };

  /**
   * Exports all events as an ICS calendar file.
   * Downloads a .ics file that can be imported into any calendar application.
   */
  const handleExportICS = async () => {
    try {
      const response = await fetch('http://localhost:5000/export/ics');
      
      if (response.ok) {
        // Create blob and download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'planner_pal_calendar.ics';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        setUploadStatus('Calendar exported successfully!');
      } else {
        const errorData = await response.json();
        setUploadStatus(`Error: ${errorData.error}`);
      }
    } catch (error) {
      console.error('Error exporting calendar:', error);
      setUploadStatus('Error exporting calendar');
    }
  };

  return (
    <div className="app">
      {/* Application header with title and description */}
      <header className="app-header">
        <h1>Planner Pal</h1>
        <p>Transform your course syllabus into a beautiful, organized calendar</p>
      </header>

      <main className="app-main">
        {/* PDF upload section */}
        <div className="upload-section">
          <div className="upload-card">
            <h2>Upload Syllabus</h2>
            <p>Upload a PDF syllabus to automatically extract assignment deadlines</p>
            
            <form onSubmit={handlePdfUpload} className="upload-form">
              <div className="file-input-container">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileChange}
                  className="file-input"
                  id="pdf-upload"
                />
                <label htmlFor="pdf-upload" className="file-input-label">
                  {file ? file.name : "Choose PDF file"}
                </label>
              </div>
              
              <button 
                type="submit" 
                className="upload-button"
                disabled={!file || loading}
              >
                {loading ? "Processing..." : "Extract Deadlines"}
              </button>
            </form>

            {/* Status message for upload feedback */}
            {uploadStatus && (
              <div className={`status-message ${uploadStatus.includes('Error') ? 'error' : 'success'}`}>
                {uploadStatus}
              </div>
            )}
          </div>

          {/* Manual event creation and export section */}
          <div className="actions-section">
            <button 
              onClick={handleCreateEvent}
              className="add-event-button"
            >
              Add Manual Event
            </button>
            
            <button 
              onClick={handleExportICS}
              className="export-button"
              disabled={events.length === 0}
            >
              📅 Export Calendar
            </button>
          </div>
        </div>

        {/* Calendar display section */}
        <div className="calendar-section">
          <CalendarView 
            events={events} 
            onEditEvent={handleEditEvent}
            onDeleteEvent={handleDeleteEvent}
          />
        </div>
      </main>

      {/* Event creation/editing modal */}
      {showEventModal && (
        <EventModal
          event={editingEvent}
          onSave={handleSaveEvent}
          onClose={() => setShowEventModal(false)}
        />
      )}
    </div>
  );
}

export default App;