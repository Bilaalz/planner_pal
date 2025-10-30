# 🧠 Planner Pal  
*AI-Powered Academic Calendar Assistant*

![Planner Pal Demo](https://img.youtube.com/vi/Hcf7YQEoXfg/0.jpg)](https://youtu.be/Hcf7YQEoXfg)

> **Transform your syllabus into a smart, interactive calendar — powered by intelligent text extraction and natural language understanding.**

---

## 📘 Overview

**Planner Pal** is a full-stack web application designed to help students stay organized by automatically converting academic course syllabi into structured, interactive calendars.  
Simply upload a syllabus PDF, and Planner Pal extracts all key academic events — including assignments, labs, exams, and projects — and maps them into an intuitive calendar view.

Planner Pal aims to eliminate the manual hassle of tracking due dates across multiple courses, empowering students to focus more on learning and less on logistics.

---

## ✨ Key Features

- 🗂️ **AI-Powered PDF Parsing** — Extracts deadlines, event names, and times from even messy syllabi.  
- 📅 **Interactive Calendar Interface** — View events in **month**, **week**, **day**, or **agenda** mode.  
- 🧭 **Event Categorization** — Detects event types such as *Assignment*, *Lab*, *Exam*, and *Project*.  
- ⚡ **Smart Context Extraction** — Associates events with surrounding course text for better accuracy.  
- ✏️ **Manual Event Management** — Add, edit, or delete custom events anytime.  
- 🪄 **Real-Time Feedback** — Loading and success/error states for smooth user experience.  
- 📱 **Responsive Modern UI** — Built with **React** and styled with a clean, glassmorphism aesthetic.  

---

## 🧩 Tech Stack

### 🖥️ Frontend
- **React.js**
- **React Big Calendar**
- **TailwindCSS** (for styling)
- **Axios** (for API communication)

### ⚙️ Backend
- **Flask (Python)** — RESTful API for PDF text processing and event generation  
- **PyPDF2** — For extracting raw text from syllabus PDFs  
- **Regex-based Event Parser** — Handles complex date/time patterns, contextual titles, and event grouping  

### 🗄️ Database (In Progress)
- **Supabase (PostgreSQL + Auth)** — Currently being integrated  
  - Migration from temporary backend-based event storage  
  - Will enable persistent user accounts and real-time syncing  

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Bilaalz/planner-pal.git
cd planner-pal
