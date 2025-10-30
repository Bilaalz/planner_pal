# 📚 Planner Pal - AI-Powered Syllabus Deadline Extractor

A full-stack web application that automatically extracts assignment deadlines from course syllabi PDFs and displays them in an interactive calendar. Built with React.js frontend and Flask Python backend.

## ✨ Features

- **📄 PDF Upload**: Upload course syllabus PDFs to automatically extract deadlines
- **🤖 AI-Powered Extraction**: Advanced NLP algorithm that identifies various deadline formats and assignment types
- **📅 Interactive Calendar**: Clean, modern calendar interface with multiple viewing modes (month, week, day, agenda)
- **✏️ Event Management**: Create, edit, and delete events manually
- **🎨 Modern UI**: Clean, responsive design with intuitive user experience
- **🔍 Smart Detection**: Automatically categorizes events (Assignments, Exams, Projects, Labs)

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Flask server:
```bash
python app.py
```

The backend will start on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will start on `http://localhost:5173`

## 🎯 How to Use

1. **Upload Syllabus**: Click "Choose PDF file" and select your course syllabus
2. **Extract Deadlines**: Click "Extract Deadlines" to process the PDF and automatically extract assignment deadlines
3. **View Calendar**: See all deadlines displayed in the interactive calendar
4. **Manage Events**: Click on events to view details, edit, or delete them
5. **Add Manual Events**: Use the "Add Manual Event" button to create custom events

## 🧠 AI Algorithm Features

The deadline extraction algorithm uses advanced pattern matching and NLP techniques to identify:

- **Deadline Keywords**: due, deadline, submit, assignment, project, exam, quiz, final, midterm, paper, presentation, lab, homework
- **Date Formats**: 
  - Full dates: "January 15, 2024", "Jan 15, 2024"
  - Numeric dates: "01/15/2024", "2024-01-15"
  - Day + date: "Monday, January 15, 2024"
- **Assignment Types**: Automatically categorizes as Assignment, Exam, Project, or Lab
- **Context Awareness**: Looks for dates within 100 characters of deadline keywords

## 🛠️ Technical Stack

### Backend
- **Flask**: Python web framework
- **PyPDF2**: PDF text extraction
- **python-dateutil**: Advanced date parsing
- **spacy**: Natural language processing
- **Flask-CORS**: Cross-origin resource sharing

### Frontend
- **React.js**: Modern JavaScript library
- **React Big Calendar**: Interactive calendar component
- **date-fns**: Date manipulation library
- **CSS3**: Modern styling with gradients and animations

## 📁 Project Structure

```
planner_pal/
├── backend/
│   ├── app.py              # Flask API server
│   ├── parse_csv.py        # Legacy CSV parser
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main application component
│   │   ├── App.css         # Application styles
│   │   ├── CalendarView.jsx # Calendar component
│   │   └── EventModal.jsx  # Event creation/editing modal
│   ├── package.json        # Node.js dependencies
│   └── vite.config.js      # Vite configuration
└── README.md
```

## 🔧 API Endpoints

- `POST /upload-pdf` - Upload and process PDF syllabus
- `GET /events` - Retrieve all events
- `POST /events` - Create new event
- `PUT /events/<id>` - Update existing event
- `DELETE /events/<id>` - Delete event
- `GET /health` - Health check

## 🎨 UI Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern Aesthetics**: Gradient backgrounds, smooth animations, clean typography
- **Interactive Elements**: Hover effects, smooth transitions, intuitive controls
- **Event Categorization**: Color-coded events by type
- **Modal Dialogs**: Clean popups for event management
- **Status Messages**: Clear feedback for user actions

## 🚀 Future Enhancements

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User authentication and multiple calendars
- [ ] Email notifications for upcoming deadlines
- [ ] Calendar export (iCal format)
- [ ] Mobile app (React Native)
- [ ] Advanced NLP with machine learning models
- [ ] Bulk PDF processing
- [ ] Calendar sharing features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- React Big Calendar for the calendar component
- Flask for the backend framework
- PyPDF2 for PDF processing
- The open-source community for inspiration and tools

---

**Built with ❤️ for students who want to stay organized and never miss a deadline!**
