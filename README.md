
# 🌍 Dristi

### AI-Powered Voice-Controlled Visual Assistant for the Visually Impaired

Dristi is an accessibility-focused AI application that enables blind and visually impaired users to understand their surroundings using voice commands and real-time scene description. The system combines computer vision, speech recognition, multilingual translation, and speech synthesis to create a fully hands-free interaction experience.

---

## 🚀 Overview

Dristi allows users to:

* Capture images using voice commands
* Receive detailed scene descriptions
* Extract and read text from images (OCR)
* Automatically detect spoken language
* Translate captions into the user’s language
* Hear responses through speech synthesis

The goal is to eliminate screen dependency and create a seamless, real-world assistive tool.

---

## 🧠 Core Features

### 🎤 Voice-Controlled Interaction

* Always-on listening system
* Speech-to-text transcription
* Automatic language detection
* No on-screen buttons required

### 📷 AI Scene Captioning

* Real-time image capture
* Advanced image captioning model
* Context-aware descriptions

### 🌐 Multilingual Support

* Automatic language detection
* Caption translation
* Speech output in detected language

### 🔎 OCR Text Reading

* Extracts visible text from captured images
* Reads text aloud in user’s language

---

## 🏗️ Architecture

Dristi uses a modular AI-driven pipeline:

User Voice → Speech-to-Text → Command Detection → Image Capture →
Image Captioning → Translation → Text-to-Speech Output

---

## 🛠️ Tech Stack

### Frontend

* HTML, CSS, JavaScript
* Web Speech API / MediaRecorder
* Progressive Web App (PWA)

### Backend

* Python (Flask)
* REST API endpoints

### AI Models

* Whisper (Speech-to-Text)
* Qwen2-VL 7B (Image Captioning)
* Helsinki-NLP Translation Models
* OCR Engine (Tesseract / similar)

---

## 📂 Project Structure

```
Dristi/
│
├── backend/
│   ├── app.py
│   ├── models/
│   └── utils/
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── styles.css
│
├── static/
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/divya32704/dristi-main.git
cd dristi-main
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Backend

```bash
python app.py
```

### 5️⃣ Open Frontend

Open `index.html` in browser or run via local server.

---

## 🌿 Git Workflow (PowerShell)

Use these commands to create a branch, commit, and push changes.

### Create and switch to a new branch

```powershell
git checkout -b unika
```

or

```powershell
git switch -c unika
```

Note: do not use angle brackets in PowerShell. Use `unika`, not `<unika>`.

### Commit your changes

```powershell
git add .
git commit -m "some minor changes"
```

### Push branch to GitHub

```powershell
git push -u origin unika
```

---

## 🔐 Environment Variables

Create a `.env` file:

```
OPENAI_API_KEY=your_key_here
```

Make sure `.env` is included in `.gitignore`.

---

## 🎯 Impact

Dristi is designed to:

* Increase independence for visually impaired individuals
* Provide real-time environmental awareness
* Remove dependency on physical interaction with devices
* Support multilingual global accessibility

---

## 🏆 Recognition

* 3rd Place – Nexus Technology Cup 2025 (Statewide Competition)
* Featured in university innovation showcase
* Ulm 2025 Hackathon 2nd place


---

## 👩‍💻 Author

**Unika Bista**
Computer Science | AI & Accessibility Research
University of Louisiana Monroe

LinkedIn: https://www.linkedin.com/in/unika-bista-50139033a/

---

# 💡 Future Improvements

* Real-time object detection
* Continuous streaming caption mode
* Offline model optimization
* Mobile native deployment
* Edge AI acceleration

---

