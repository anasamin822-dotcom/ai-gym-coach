# 🏋️ AI Gym Coach

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0078D4?logo=google&logoColor=white)](https://developers.google.com/mediapipe)
[![WebRTC](https://img.shields.io/badge/WebRTC-333333?logo=webrtc&logoColor=white)](https://webrtc.org/)
[![Groq Llama-3](https://img.shields.io/badge/Groq-Llama--3-F55036?logo=groq&logoColor=white)](https://groq.com/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)](https://sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Real-Time Computer Vision & Voice-Guided AI Fitness Coach**

AI Gym Coach is an intelligent, edge-accelerated personal fitness trainer built with **Streamlit**, **Google MediaPipe Tasks**, **WebRTC**, and **Groq-powered Llama 3**. It tracks human biomechanics through your webcam in real-time, validates joint angles, counts reps, enforces set cadences with automated rest intervals, delivers audio feedback, and exports certified session reports in PDF & CSV.

---

## ⚡ Key Features

- **Real-Time Edge Pose Estimation**: High-performance 33-landmark 3D pose extraction via Google MediaPipe Tasks (`pose_landmarker_full.task`) over low-latency browser WebRTC video streams.
- **Biometric Joint Angle Tracking & HUD Overlay**: Live mathematical angle computation for elbows, shoulders, hips, and knees. Renders visual angle telemetry and color-coded status cues directly onto webcam video frames.
- **Low-Latency LLM Voice Coaching**: Integrates Groq Llama 3 (`llama-3.1-8b-instant`) and text-to-speech to provide immediate spoken coaching tips, form warnings, and rep encouragement with zero lag.
- **Automated Rest Timer Between Sets**: Auto-detects completed sets, triggering a visual recovery countdown (configurable 15–180s) with Web Audio API chime notifications and a 1-tap **"Skip Rest"** button (`btn_skip_rest`).
- **Workout Summary Export (PDF & CSV)**: Zero-dependency pure-Python PDF 1.4 generator and CSV export detailing total reps, sets, avg tempo (s/rep), form accuracy (%), and gamified XP rank badges (e.g. *🏆 Elite Iron Titan*).
- **Personalized BMI & Nutrition Routine**: Built-in biometric assessment engine calculating BMI, maintenance calories, macro breakdown, and complete daily meal & exercise routines.
- **Local SQLite Persistence**: Automatic session logging, rep counting, and historical trend analysis across past workouts.
- **Responsive Mobile & Viewport UX**: Cyber-Athletic neon UI designed to stack seamlessly on mobile screens, tablets, and desktop displays.

---

## 🏗️ System Architecture

```text
+-----------------------------------------------------------------------------------+
|                                CLIENT (Browser)                                   |
|   +--------------------------+                     +--------------------------+   |
|   |   Webcam Video Stream    |                     |  Cyber-Athletic Web UI   |   |
|   |      (HTML5 Canvas)      |                     | (Streamlit + Custom CSS) |   |
|   +------------+-------------+                     +------------^-------------+   |
+----------------|------------------------------------------------|-----------------+
                 | WebRTC SENDRECV                                | UI State & HUD
                 v                                                |
+-----------------------------------------------------------------|-----------------+
|                           AI GYM COACH ENGINE (Server)          |                 |
|                                                                 |                 |
|   +--------------------------+      Raw Frames      +-----------+-------------+   |
|   |  streamlit-webrtc        | -------------------> |    MediaPipe Tasks      |   |
|   |  VideoTransformer Worker |                      | (PoseLandmarker Full)   |   |
|   +--------------------------+                      +-----------+-------------+   |
|                                                                 |                 |
|                                                     33 3D Pose Landmarks          |
|                                                                 v                 |
|   +--------------------------+      Angles & Reps   +-------------------------+   |
|   |    Session State &       | <------------------- | Exercise Heuristic Core |   |
|   | SQLite Persistence Layer |                      |  (Knee/Elbow/Hip Math)  |   |
|   +------------+-------------+                      +-----------+-------------+   |
|                |                                                |                 |
|       Metrics  |                                    Form Events | (Warning/Rep)   |
|                v                                                v                 |
|   +--------------------------+                      +-------------------------+   |
|   | PDF/CSV Summary Engine   |                      |  Groq Llama-3 LLM       |   |
|   | (Pure Python PDF 1.4)    |                      |  Ultra-Low Latency TTS  |   |
|   +--------------------------+                      +-------------------------+   |
+-----------------------------------------------------------------------------------+
```

---

## 🛠️ Supported Exercises & Biomechanical Checks

| Exercise | Monitored Joints | Strict Form Validations |
| :--- | :--- | :--- |
| **Squats** | Hip, Knee, Ankle | Depth threshold (<95°), upright torso, knee lockout prevention |
| **Bicep Curls** | Shoulder, Elbow, Wrist | Full elbow flexion (<45°), full extension (>155°), no torso swing |
| **Push-ups** | Shoulder, Elbow, Hip, Ankle | Chest-to-floor depth, body plane alignment (no sagging or piking) |
| **Shoulder Press** | Elbow, Shoulder, Spine | Overhead vertical extension, back arch stabilization |
| **Lateral Raises** | Shoulder, Elbow, Torso | Arm elevation to parallel (80–100°), elbow stability |

---

## 💻 Installation & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/anasamin822-dotcom/ai-gym-coach.git
cd ai-gym-coach
```

### 2. Create and Activate Virtual Environment
- **On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
- **On Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```ini
GROQ_API_KEY=your_groq_api_key_here
```
> *Note: If `GROQ_API_KEY` is not provided, the coach gracefully falls back to deterministic rule-based coaching feedback.*

### 5. Launch the Application
```bash
streamlit run ai-gym-coach-main/MainApp/main.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ Cloud Deployment Guardrails (Streamlit Cloud)

When deploying to **Streamlit Community Cloud**, observe the following production constraints:

1. **Python Runtime**:
   - Ensure the runtime environment is set to **Python 3.10** or **Python 3.11** (MediaPipe Tasks requires >= 3.10).

2. **System Dependencies (`packages.txt`)**:
   - The root directory **must** contain `packages.txt` with required OpenGL/EGL and GLib runtime binaries for headless OpenCV and MediaPipe:
     ```text
     libgl1
     libegl1
     libgles2
     libglib2.0-0
     ```

3. **Application Entry Point**:
   - Set the Main file path in Streamlit Cloud settings to:
     ```text
     ai-gym-coach-main/MainApp/main.py
     ```

4. **Secrets Management**:
   - Under Streamlit Cloud Settings > **Secrets**, configure:
     ```toml
     GROQ_API_KEY = "gsk_your_actual_groq_api_key"
     ```

5. **WebRTC NAT Traversal (STUN/TURN)**:
   - For client-server WebRTC handshakes over cellular or restricted networks, ensure Google STUN servers are configured in the RTCConfiguration:
     ```python
     RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
     ```

---

## 📊 Directory Structure

```text
ai-gym-coach/
├── packages.txt                    # Debian system packages for Cloud deployment
├── requirements.txt                # Python dependencies
├── README.md                       # Comprehensive documentation
├── static/
│   └── style.css                   # Cyber-Athletic styling & responsive media queries
└── ai-gym-coach-main/
    └── MainApp/
        ├── main.py                 # Core Streamlit app & WebRTC streamer loop
        ├── core/                   # Mathematical calculations & angle geometry
        ├── detectors/              # MediaPipe PoseLandmarker & exercise trackers
        ├── ml_models/              # pose_landmarker_full.task model binaries
        ├── services/
        │   ├── auth/               # User authentication & credentials
        │   ├── coaching/           # Groq LLM & Text-to-Speech voice pipeline
        │   ├── config/             # Prompts & exercise configuration
        │   ├── nutrition/          # BMI calculation & diet generation
        │   ├── persistence/        # SQLite workout database models
        │   ├── reporting/          # Pure-Python PDF & CSV export engine
        │   ├── state/              # Streamlit session state management
        │   ├── tracking/           # Metrics aggregation & rest cadence
        │   ├── ui/                 # Rest countdown overlays & summary views
        │   └── vision/             # Frame processing & camera pipeline
        └── static/
            └── style.css
```

---

## 📜 License
Distributed under the **MIT License**. See `LICENSE` for more information.

---

## 🙏 Acknowledgments
- [Google MediaPipe](https://developers.google.com/mediapipe) for pose landmark detection.
- [Streamlit WebRTC](https://github.com/whitphx/streamlit-webrtc) for seamless real-time browser video streaming.
- [Groq](https://groq.com/) for lightning-fast Llama-3 model inference.
