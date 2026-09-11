# Product

<!-- impeccable:product-schema 1 -->

## Platform
web

## Users
- Primary users: Solo gym-goers, student athletes, physical training candidates, and home fitness practitioners who need real-time postural guidance and injury prevention without paying expensive personal trainer fees (₹3,000–₹10,000/month).
- Secondary users: Remote physiotherapy and orthopedic rehabilitation patients tracking joint recovery angles; physical education teachers and defense recruiters evaluating standardized physical drills at scale.

## Product Purpose
AI Gym Coach turns any ordinary smartphone or laptop camera into an Olympic-grade biomechanical training station without wearables or sensors. It calculates real-time 3D joint angles, counts strict repetitions, detects muscular fatigue before injury occurs, and provides instant voice coaching. Success means safe, independent, injury-free strength training accessible to anyone with a browser.

## Positioning
Unlike wearable fitness trackers (smartwatches) that only measure heart rate and approximate steps, and unlike gym mirrors that cannot quantify anatomical angles, AI Gym Coach extracts 33 3D skeletal landmarks in real time directly inside browser RAM, calculates joint kinematics, alerts on concentric velocity breakdown (>35% drop), and provides sub-second voice cues with zero cloud video transmission.

## Operating Context
- User workout environment: Solo gym sessions, home workouts, dorm rooms, or hostel setups.
- Device: Desktop laptop webcam, tablet, or smartphone propped against a water bottle/stand.
- Lighting: Often mixed or dim gym/bedroom lighting; requires robust spatial landmark interpolation.
- Network: Intermittent mobile data / Wi-Fi; requires offline sports science fallback when cloud APIs lag.

## Capabilities and Constraints
Confirmed capabilities:
- Real-time 33 3D joint detection at 30 FPS using MediaPipe Tasks (purely in volatile memory).
- Live 3D Biomechanical Digital Twin avatar (Three.js WebGL) with 360° OrbitControls.
- Dual-Path AI Agent: Sub-90ms Groq Llama-3 LPU voice feedback + Offline Sports Science reasoning engine.
- Velocity-Based Fatigue Engine: Auto-warning upon >35% concentric speed drop (González-Badillo standard).
- Resilient Mobile OTP Authentication: 10-digit Indian phone validation, Fast2SMS/Twilio pipeline, Sandbox mode, Judge Master OTP 999999.
- 7-Day Free Starter Trial auto-activation with real-time countdown badge.
- Dynamic UPI QR Code Paywall: Direct NPCI deep-links for PhonePe, GPay, Paytm, and BHIM (₹0 Trial, ₹19 Day Pass, ₹199 Pro Monthly) with 12-digit UTR audit verification.
- High-Concurrency SQLite WAL Mode: Multi-thread safe Write-Ahead Logging with 30s timeout and UPSERT protection.
- Downloadable 1-page clinical PDF session workout reports with bilateral symmetry scores.

Technical constraints:
- Must run in modern browsers (Chrome, Edge, Safari, Brave) with zero external hardware or sensor requirements.
- Privacy constraint: Video frames are analyzed in RAM and never written to disk or transmitted to a cloud server.

## Brand Commitments
- Name: AI Gym Coach
- Aesthetic & Visual Identity: Dark cyberpunk athletic aesthetic (#060B14 deep navy background, #00F59B neon cyber-green accents, #38BDF8 HUD cyan, crisp monospace telemetry badges).
- Tagline: 'Train Smarter. Not Harder.' / 'Olympic-Grade Form Feedback. Zero Hardware Required.'

## Evidence on Hand
- Live Streamlit Web App: https://ai-gym-coach-bndhslamytm6wpyg5beqeo.streamlit.app/
- Live Cyberpunk Landing Page: https://anasamin822-dotcom.github.io/ai-gym-coach/
- Open-Source GitHub Repository: https://github.com/anasamin822-dotcom/ai-gym-coach
- Visual Assets: High-precision exercise HUD screenshots in docs/IMGs/ (i1.png to i6.png covering squats, curls, pushups, shoulder presses, voice coach, and PDF reports).

## Product Principles
1. Zero Hardware Barrier: If it requires an Apple Watch, special sensor, or expensive GPU, it violates our core mission.
2. Uncompromising Privacy: An athlete's workout video never leaves their device's RAM.
3. Sub-Second Feedback: A form correction delivered after the rep is finished is useless; auditory cues must arrive mid-rep (<90ms).
4. Scientifically Grounded: Every angle threshold, rep boundary, and fatigue warning is anchored in clinical biomechanics (Escamilla) and velocity-based training (González-Badillo).
5. Accessible Economics: Transparent, commission-free Indian micro-payments (UPI QR) with generous free trials for students.

## Accessibility & Inclusion
- High-contrast neon-on-dark HUD elements for legibility from 2–3 meters away while exercising.
- Auditory cues (synthesized speech + chimes) so the athlete doesn't have to look at the screen while executing squats or pushups.
- Language: English & Hinglish colloquial fitness terminology for broad adoption across Tier-1, Tier-2, and Tier-3 Indian fitness communities.
