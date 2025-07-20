from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
from io import StringIO

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://localhost:3000"])

# In-memory storage for events
events = []

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'File must be a CSV'}), 400
    try:
        stream = StringIO(file.stream.read().decode('utf-8'))
        reader = csv.DictReader(stream)
        parsed_events = []
        for row in reader:
            event = {
                'name': row.get('Name', '').strip(),
                'type': row.get('Type', '').strip(),
                'due_date': row.get('Due_Date', '').strip(),
                'course': row.get('Course', '').strip(),
                'weight': row.get('Weight', '').strip()
            }
            parsed_events.append(event)
        events.extend(parsed_events)
        return jsonify({'message': f'{len(parsed_events)} events uploaded', 'events': parsed_events}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/events', methods=['GET'])
def get_events():
    return jsonify({'events': events}), 200

@app.route('/health')
def health_check():
    return {'status': 'healthy', 'message': 'Planner Pal API is running'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
