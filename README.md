# 👕 V-Mirror Draft v1

A Virtual Fashion Try-On web application that allows users to upload their images and preview clothing virtually using AI-powered body pose detection. This project is an early draft of the V-Mirror system developed as part of an MCA Semester Project.

---

## 📌 Project Overview

V-Mirror aims to provide an interactive virtual dressing experience by combining computer vision and pose estimation. Instead of physically trying on clothes, users can upload their photo and visualize how different outfits look on them.

This repository contains the first working draft of the project with user authentication, Flask backend, and AI-based clothing overlay.

---

## ✨ Features

- 🔐 User Login & Signup Authentication
- 🖥️ Responsive User Interface
- 📤 Upload Image Functionality
- 🤖 AI Pose Detection using MediaPipe
- 👕 Virtual Shirt Overlay
- ⚡ Flask Backend
- 💾 SQLite Database for User Management
- 🎨 Modern HTML, CSS & JavaScript Frontend

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask

### AI / Computer Vision
- OpenCV
- MediaPipe Pose Landmarker
- NumPy

### Database
- SQLite

---

## 📂 Project Structure

```
V-Mirror_Draft_v1/
│
├── ai_engine/
│   ├── pose_detector.py
│   ├── tryon_engine.py
│   └── pose_landmarker.task
│
├── database/
│   └── users.db
│
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── shirts/
│   └── templates/
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

### Run the Application

```bash
python app.py
```

The application will start on:

```
http://127.0.0.1:5000
```

---

## 🚀 Current Functionalities

- User Registration
- User Login
- Session Handling
- Image Upload
- Pose Detection
- Clothing Overlay
- Responsive UI

---

## 📈 Future Improvements

- Live Webcam Try-On
- Multiple Clothing Categories
- AI Size Recommendation
- Background Removal
- 3D Garment Visualization
- User Wardrobe Management
- Product Recommendation System
- Mobile Responsive Improvements

---

## 🎯 Project Objective

The objective of V-Mirror is to simplify online apparel shopping by enabling users to virtually try on clothes using AI-powered computer vision techniques, reducing uncertainty before purchasing.

---

## 👨‍💻 Author

**Shubranil Pandit**

MCA (Data Science)

MIT Vishwaprayag University

GitHub: https://github.com/Shubranilpandit

---

## ⭐ Support

If you found this project helpful, consider giving it a ⭐ on GitHub.

Feedback and suggestions are always welcome!
