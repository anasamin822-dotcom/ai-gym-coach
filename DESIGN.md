---
name: AI Gym Coach
description: Real-time computer vision, 3D digital twin, and voice-guided athletic intelligence
colors:
  bg-dark: "#060B14"
  bg-surface: "#0E1422"
  cyber-green: "#00F59B"
  hud-cyan: "#38BDF8"
  accent-amber: "#F5A623"
  danger-red: "#EF4444"
  text-primary: "#FFFFFF"
  text-secondary: "#94A3B8"
  border-glow: "rgba(0, 245, 155, 0.3)"
typography:
  display:
    fontFamily: "'Space Grotesk', 'Instrument Serif', sans-serif"
    fontSize: "clamp(2.5rem, 6vw, 4.5rem)"
    fontWeight: 900
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  telemetry:
    fontFamily: "'JetBrains Mono', 'Ubuntu', monospace"
    fontSize: "0.85rem"
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: "0.08em"
  body:
    fontFamily: "'Inter', 'Averta', sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
rounded:
  sm: "4px"
  md: "8px"
  lg: "16px"
  pill: "999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "48px"
components:
  button-primary:
    backgroundColor: "{colors.cyber-green}"
    textColor: "#060B14"
    rounded: "{rounded.md}"
    padding: "12px 28px"
  badge-hud:
    backgroundColor: "rgba(0, 245, 155, 0.15)"
    textColor: "{colors.cyber-green}"
    rounded: "{rounded.pill}"
    padding: "4px 12px"
---

## Overview
AI Gym Coach uses an Olympic-grade dark cyberpunk telemetry design language. Built for high legibility from 2–3 meters away, the interface combines deep obsidian backgrounds with high-chroma neon green, cyan, and amber data streams to deliver biomechanical feedback mid-rep.

## Colors
- **Primary Cyber Green (`#00F59B`)**: Signals optimal joint angles, successful reps, and live tracking status.
- **HUD Cyan (`#38BDF8`)**: Secondary metrics, velocity tracking, and joint angle readouts.
- **Warning Amber (`#F5A623`)**: Sub-optimal alignment warnings and rest timers.
- **Danger Red (`#EF4444`)**: Fatigue velocity drop (>35%) and form breakdown alerts.
- **Obsidian Dark Surface (`#060B14` & `#0E1422`)**: Low-glare backdrop preventing eye fatigue in gym settings.

## Typography
- **Display**: High-impact geometric sans/serif for bold hero claims and exercise titles.
- **Telemetry**: Monospace font for numerical angles (88°), rep counters, and sub-second latency tags.
- **Body**: Clean readable sans-serif for exercise explanations and nutritional guidelines.

## Layout
- Grid overlay background with 64px spatial reference lines mimicking a biomechanical motion capture studio.
- Center-stage 3D WebGL Arena and video feed flanked by high-contrast telemetry panels.
- Responsive breakpoints for mobile smartphones propped on gym benches up to ultrawide desktop monitors.

## Elevation & Depth
- Glassmorphism overlays with `backdrop-filter: blur(12px)`.
- Neon green drop-shadow glows (`box-shadow: 0 0 30px rgba(0, 245, 155, 0.25)`).
- Subtle scan-line animation across active exercise cards.

## Shapes
- Rounded rectangles (`8px` to `16px`) for cards and HUD badges.
- Pill badges (`999px`) for live status indicators ("● LIVE DEMO").

## Components
- **3D Digital Twin Arena**: Interactive Three.js WebGL viewport with 33 glowing joint nodes.
- **Exercise Audit Card**: 200px image viewport with scanline overlay and angle tags.
- **Dynamic UPI QR Checkout**: Clean modal display with instantaneous QR scanning for PhonePe/GPay.
- **Session Telemetry Badge**: Real-time rep, angle, and speed counters.

## Do's and Don'ts
- **DO**: Use `#00F59B` exclusively for positive/passing biomechanical thresholds.
- **DO**: Keep text readable from distance during active workouts.
- **DON'T**: Use white backgrounds or high-luminance light modes that cause glare during workouts.
- **DON'T**: Hide critical error/fatigue warnings behind clicks or accordions.
