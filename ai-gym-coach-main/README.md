# 🏋️ AI Gym Coach: Real-Time Computer Vision & Voice-Guided Fitness Coach

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit Cloud](https://img.shields.io/badge/Streamlit%20Cloud-Deployed-FF4B4B?logo=streamlit&logoColor=white)](https://ai-gym-coach-bndhslamytm6wpyg5beqeo.streamlit.app/)
[![MediaPipe Tasks](https://img.shields.io/badge/MediaPipe-Tasks%200.10-0078D4?logo=google&logoColor=white)](https://developers.google.com/mediapipe)
[![WebRTC](https://img.shields.io/badge/WebRTC-Real--Time%20Stream-333333?logo=webrtc&logoColor=white)](https://webrtc.org/)
[![Groq Llama-3](https://img.shields.io/badge/Groq-Llama--3%20Ultra--Low%20Latency-F55036?logo=groq&logoColor=white)](https://groq.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Local%20Persistence-003B57?logo=sqlite&logoColor=white)](https://sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Instant UPI QR](https://img.shields.io/badge/Payments-Instant%20UPI%20QR-00F59B?logo=googlepay&logoColor=white)](https://ai-gym-coach-bndhslamytm6wpyg5beqeo.streamlit.app/)
[![Live Landing Page](https://img.shields.io/badge/Landing%20Page-Live-00F59B?logo=githubpages&logoColor=white)](https://anasamin822-dotcom.github.io/ai-gym-coach/)

> **Empowering solo athletes with computer-vision kinematic joint analysis, real-time muscular fatigue detection, live XP combo gamification, sub-second LLM voice coaching, and instant dynamic UPI checkout.**

[🌐 **Visit Live Landing Page**](https://anasamin822-dotcom.github.io/ai-gym-coach/) • [🚀 **Launch Live App on Streamlit Cloud**](https://ai-gym-coach-bndhslamytm6wpyg5beqeo.streamlit.app/) • [📑 **Architecture Overview**](#-system-architecture) • [⚡ **Hackathon Innovations**](#-hackathon-winning-innovations) • [💻 **Local Setup**](#-installation--local-setup)

---

## 🎯 The Problem
Traditional fitness apps either rely on manual logging (which is inaccurate and passive) or expensive wearable sensors (which fail to evaluate posture and joint biomechanics). Exercising with improper form or lifting through severe muscular velocity exhaustion leads to acute joint injuries, chronic back pain, and stalled strength progression.

## 💡 The Solution
**AI Gym Coach** turns any ordinary laptop or mobile webcam into an edge-accelerated, biomechanical personal trainer. Using client-side WebRTC and Google MediaPipe 33-point 3D PoseLandmarkers, it computes angular joint geometry at 30+ FPS, warns athletes of form breakdown, tracks eccentric/concentric rep velocity, gamifies workouts with dynamic XP streaks, and delivers real-time voice coaching powered by **Groq Llama 3**.

---

## ⚡ Hackathon-Winning Innovations

### 1. ⚡ Real-Time Muscular Fatigue & Velocity Drop Engine
- Continuously calculates rep duration and movement speed across concentric and eccentric phases.
- Calibrates a dynamic baseline pace from the initial reps of each set.
- Automatically flags **Muscular Fatigue (-35% Velocity Drop)** when concentric speed significantly degrades, warning users before form failure or injury occurs.

### 2. 🎮 Live Form Gamification & XP Combo Multiplier
- Analyzes joint stability on every repetition.
- **Strict Form** rewards athletes with consecutive **Combo Streaks** (1.5x -> 2.0x -> 3.0x Live XP Multipliers).
- Any form deviation (e.g., shallow squat depth, hip sagging, excessive curl swing) triggers an instant **"Combo Break"**, encouraging rigorous exercise execution.

### 3. 🎙️ Sub-Second Groq Llama-3 Voice Pipeline
- Real-time event dispatching connects rep milestones and biomechanical warnings to Groq's `llama-3.1-8b-instant`.
- Voice synthesis communicates form cues and encouragement through your speakers with sub-second response times.
- Resilient fallback layer guarantees continuous coaching even when offline or during network drops.

### 4. 🧘 Smart Rest Interval Manager
- Set completion triggers an athletic recovery state with an SVG circular countdown ring (configurable 15s to 180s, default 45s).
- Features dynamic `+15s` / `-15s` micro-adjustments and an instant **"Skip Rest"** trigger.
- Sounds a dual-tone athletic Web Audio chime and spoken prompt when rest concludes.

### 5. 📄 1-Click Certified Session Report (PDF & CSV)
- Generates a certified single-page vector PDF workout report powered by `fpdf2`.
- Formats kinematic accuracy, bilateral joint symmetry, rep cadence, fatigue resistance scores, and XP tier badges.
- Includes clean CSV exports for offline fitness logging.

### 6. 📱 Mobile OTP Auth & Instant Dynamic UPI QR Payments
- Frictionless 10-digit mobile number login with OTP verification (Fast2SMS/Twilio carrier integration + resilient sandbox fallback).
- Automatic **7-Day Free Starter Trial** activation with live remaining-days counter.
- Instant Dynamic UPI QR Code generator supporting PhonePe, Google Pay, Paytm, and BHIM with NPCI intent links.
- 12-digit UTR reference validation for instant **Pro Athlete** feature unlocking.

---

## 🏗️ System Architecture

```text
======================================================================================
                              CLIENT-SIDE (Web Browser)
======================================================================================
  [Webcam Stream] -----> HTML5 Canvas -----> WebRTC SENDRECV PeerConnection
         ^                                               |
         | (Visual Overlay & Video Feed)                 v
  +----------------------------------------------------------------------------------+
  |  CYBER-ATHLETIC STREAMLIT HUD: Live XP Combo Multiplier | Velocity Fatigue Meter  |
  +----------------------------------------------------------------------------------+

======================================================================================
                           SERVER-SIDE AI WORKER PIPELINE
======================================================================================
                 WebRTC Video Frame (30+ FPS)
                              |
                              v
             +----------------------------------+
             |   MediaPipe Tasks PoseLandmarker |
             |   (33 Full-Body 3D Landmarks)    |
             +----------------------------------+
                              |
                              v
             +----------------------------------+
             |     Vector Biomechanics Engine   |
             |  - Joint Angle Trigonometry      |
             |  - Depth & Hip Stability Checks  |
             |  - Rep Counter & Cadence Timing  |
             +----------------------------------+
                              |
             +----------------+----------------+
             |                                 |
             v                                 v
  +-----------------------+       +------------------------------------+
  |  Velocity & Fatigue   |       |  Live Form Gamification            |
  |  - Baseline Speed     |       |  - Perfect Form = XP Combo Streak  |
  |  - Velocity Drop %    |       |  - Form Slip = Combo Break         |
  +-----------------------+       +------------------------------------+
             |                                 |
             +----------------+----------------+
                              |
                              v
             +----------------------------------+
             |     Event Dispatch & Coaching    |
             +----------------------------------+
               /              |               \
              /               |                \
             v                v                 v
   +------------------+ +-------------+ +--------------------+
   |  Groq Llama-3    | |   SQLite    | |   Reporting Engine |
   |  Voice Pipeline  | | Session DB  | | (fpdf2 PDF & CSV)  |
   +------------------+ +-------------+ +--------------------+
```

---

## 📐 Biomechanical Standards & Kinematic Rules

| Exercise | Tracked Joints | Strict Biomechanical Criteria |
| :--- | :--- | :--- |
| **Squats** | Hip, Knee, Ankle, Torso | Depth threshold (<95 deg), upright torso angle (>70 deg), knee lockout prevention |
| **Bicep Curls** | Shoulder, Elbow, Wrist | Full elbow flexion (<45 deg), full extension (>155 deg), strict torso stability (<15 deg swing) |
| **Push-ups** | Shoulder, Elbow, Hip, Ankle | Chest-to-floor depth (<90 deg elbow), straight body plane (no hip sag or pike) |
| **Shoulder Press** | Elbow, Shoulder, Spine | Overhead vertical lockout (>160 deg), stable lumbar curvature (no hyper-extension) |
| **Lunges** | Hip, Front Knee, Ankle | 90 deg knee flexion, vertical torso balance, controlled deceleration |

---

## 💻 Installation & Local Setup

### 1. Clone Repository
```bash
git clone https://github.com/anasamin822-dotcom/ai-gym-coach.git
cd ai-gym-coach
```

### 2. Create Virtual Environment
- **Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
- **Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Secrets
Create a `.env` file in the root directory:
```ini
GROQ_API_KEY=gsk_your_groq_api_key_here
```
> *Note: If `GROQ_API_KEY` is omitted, the app smoothly falls back to rule-based deterministic coaching.*

### 5. Launch the Application
```bash
streamlit run MainApp/main.py
```
Visit `http://localhost:8501` in your browser.

---

## ☁️ Cloud Deployment Guardrails (Streamlit Cloud)

To deploy to **Streamlit Community Cloud** without issues:

1. **Python Version**: Set runtime to **Python 3.10** or **Python 3.11**.
2. **Debian Packages (`packages.txt`)**: Ensure `packages.txt` exists at root containing:
   ```text
   libgl1
   libegl1
   libgles2
   libglvnd0
   libgbm1
   libglib2.0-0
   ```
3. **Application Entry Point**: Set Main file path to:
   ```text
   ai-gym-coach-main/MainApp/main.py
   ```
4. **Secrets Configuration**: Add your `GROQ_API_KEY` in Streamlit Cloud Secrets.
5. **WebRTC STUN Servers**: STUN servers (`stun:stun.l.google.com:19302`) are pre-configured for global NAT traversal.

---

## 📂 Repository File Structure

```text
ai-gym-coach/
├── packages.txt                    # System runtime libraries for Cloud GPU/GL
├── requirements.txt                # Production dependencies (including fpdf2)
├── README.md                       # Hackathon presentation documentation
├── static/
│   └── style.css                   # Cyber-athletic design & mobile media queries
└── MainApp/
    ├── main.py                     # Main application entry point & WebRTC loop
    ├── core/                       # Geometric mathematics & angle calculation
    ├── detectors/                  # MediaPipe PoseLandmarker exercise algorithms
    ├── ml_models/                  # pose_landmarker_full.task model bundle
    ├── services/
    │   ├── auth/                   # SQLite authentication & user state
    │   ├── coaching/               # Groq LLM & text-to-speech voice pipeline
    │   ├── config/                 # Biomechanical thresholds & system prompts
    │   ├── nutrition/              # BMI assessment & personalized meal engine
    │   ├── persistence/            # SQLite repository for workout history
    │   ├── reporting/              # fpdf2 single-page PDF & CSV export engine
    │   ├── state/                  # Session defaults & state machine
    │   ├── tracking/               # Rep cadence, velocity & combo telemetry
    │   ├── ui/                     # SVG circular rest timer & summary view
    │   └── vision/                 # WebRTC VideoProcessorClass with Cyber HUD
    └── static/
        └── style.css               # Embedded UI stylesheet
```

---

## 📜 License
Distributed under the **MIT License**. See `LICENSE` for details.

---

## 🏆 Hackathon Acknowledgments
- **Google MediaPipe**: Edge pose landmark inference.
- **Streamlit**: Interactive cyber-athletic interface.
- **Groq**: Lightning-fast Llama-3 coaching intelligence.
- **Streamlit-WebRTC**: Browser-to-server video streaming.
