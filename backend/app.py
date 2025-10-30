"""
Main Flask application for Planner Pal.

- models.py: Data models and storage
- extractor.py: PDF text extraction and deadline parsing
- routes.py: API route handlers
"""

from flask import Flask
from flask_cors import CORS

from routes import (
    upload_pdf_handler, get_events_handler, create_event_handler,
    update_event_handler, delete_event_handler, health_check_handler,
    export_ics_handler
)

# Create Flask application instance
app = Flask(__name__)

# Configure CORS to allow frontend connections (any localhost port)
CORS(
    app,
    resources={r"/*": {"origins": [
        "http://localhost",
        r"http://localhost:*",
        "http://127.0.0.1",
        r"http://127.0.0.1:*",
        "http://0.0.0.0",
        r"http://0.0.0.0:*",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000"
    ]}}
)

# Register API routes
@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    """Upload and process PDF syllabus to extract deadlines"""
    return upload_pdf_handler()

@app.route('/events', methods=['GET'])
def get_events():
    """Get all events"""
    return get_events_handler()

@app.route('/events', methods=['POST'])
def create_event():
    """Create a new event"""
    return create_event_handler()

@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """Update an existing event"""
    return update_event_handler(event_id)

@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Delete an event"""
    return delete_event_handler(event_id)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return health_check_handler()

@app.route('/export/ics', methods=['GET'])
def export_ics():
    """Export calendar as ICS file"""
    return export_ics_handler()

if __name__ == '__main__':
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)
