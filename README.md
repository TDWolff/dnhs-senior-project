# DNHS Senior Project — 3D Blender Presentation

An interactive 3D presentation built with Blender, Three.js, and Flask. You navigate through animated slides using the arrow keys, spacebar, or mouse click — the camera and scene animations are driven entirely from a Blender `.glb` export.

---

## Table of Contents

1. [Running the App](#running-the-app)
2. [How the Presentation Works](#how-the-presentation-works)
3. [Blender Workflow — Step by Step](#blender-workflow--step-by-step)
   - [Scene Setup](#1-scene-setup)
   - [Animating the Camera](#2-animating-the-camera)
   - [Creating Animation Clips with NLA](#3-creating-animation-clips-with-the-nla-editor)
   - [Naming Conventions](#4-naming-conventions)
   - [Exporting to GLB](#5-exporting-to-glb)
4. [Adding the GLB to the Project](#adding-the-glb-to-the-project)
5. [Controls](#controls)
6. [Project Structure](#project-structure)

---

## Running the App

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/).

```bash
# Build and start the server
docker compose up --build

# Open in browser
http://localhost:8090
```

To stop: `Ctrl+C` in the terminal, then `docker compose down`.

Logs are saved automatically to `logs/YYYY-MM-DD.log` and also printed to the terminal.

---

## How the Presentation Works

- The Flask server serves a Three.js page at `/presentation`
- Three.js loads `static/models/presentation.glb` — your exported Blender file
- Each **NLA strip** in Blender becomes one "slide" (an animation clip)
- The camera exported from Blender is used directly, so all your camera moves play exactly as authored
- Pressing next/previous plays the corresponding animation clip in order

---

## Blender Workflow — Step by Step

### 1. Scene Setup

1. Open Blender and start a new project (or open an existing one)
2. Build all the objects, materials, and lights for your entire presentation in **one single Blender file** — every "slide" lives in the same scene
3. Keep your scene origin at `(0, 0, 0)` — this makes camera paths predictable
4. Set your **frame rate**: go to `Properties → Output Properties → Frame Rate`. 24fps is standard for cinematic feel; 30fps works too. Be consistent — pick one and don't change it

### 2. Animating the Camera

The website uses your Blender camera directly, so every position, rotation, and focal length change you animate will appear in the browser exactly as you see it in Blender.

1. In the 3D viewport, press `Numpad 0` to look through your camera
2. Select the camera in the outliner or by clicking it in the viewport
3. Press `I` to insert a keyframe — choose **Location & Rotation** to lock in the starting position
4. Move to a later frame on the timeline, reposition the camera (press `G` to grab, `R` to rotate), and press `I` again to insert another keyframe
5. Repeat for every camera move in your presentation
6. To make camera cuts (instant jump to a new position), insert two keyframes on consecutive frames with different positions — Blender will jump instead of interpolate
7. To get smooth easing on moves, select all keyframes in the **Graph Editor**, press `T`, and choose **Ease In/Out** or **Bezier**

> **Tip:** parent the camera to an **Empty** object if you want to do complex orbiting moves. Animate the Empty's rotation and the camera's local offset separately — it gives much more control than animating the camera directly.

### 3. Creating Animation Clips with the NLA Editor

This is the most important step. Each "slide" must be a separate **NLA Action Strip**.

**Step A — Create the first action:**

1. Open the **Timeline** at the bottom of Blender (or switch an area to **Nonlinear Animation**)
2. Select your camera (and any objects that move during this slide)
3. Animate the keyframes for slide 1 within a specific frame range, e.g. frames 1–60
4. In the **NLA Editor** (top menu: `Editor Type → Nonlinear Animation`), find the camera track
5. Click the **Push Down** button (the downward arrow icon next to the action name in the NLA track header) — this converts the active action into an NLA strip
6. The strip will appear as a colored bar in the NLA editor. **Double-click its name** and rename it to something like `01_intro`

**Step B — Create the next action:**

1. In the NLA Editor, click the **"+" button** on the camera's track (or press `N` to open the properties panel and create a new action)
2. Go back to the **Action Editor** (switch an editor area to `Action Editor`)
3. Click the action name dropdown and select `New` — this creates a blank action
4. Name it something like `02_overview`
5. Now animate the camera for this slide in a **different frame range** (e.g. frames 1–90 — frame ranges don't need to be unique across actions since each action is isolated)
6. Push down this action in the NLA Editor the same way as before

**Step C — Repeat for every slide:**

Repeat Step B for each slide in your presentation. Each one should be pushed down into its own NLA strip with a numbered name.

**Quick NLA cheat sheet:**

| Action | How |
|--------|-----|
| Push action down to NLA | Click the ↓ arrow in NLA track header |
| Rename a strip | Double-click the strip name |
| Edit a strip's frames | Tab into the strip in NLA editor |
| Mute a strip (for testing) | Click the checkmark on the strip |
| Change strip timing | Drag the strip left/right in NLA editor |

### 4. Naming Conventions

The website sorts clips **alphabetically by name** to determine playback order. Use zero-padded numbers at the start of every action name:

```
01_intro
02_overview
03_detail_shot
04_conclusion
```

Do **not** use names like `intro`, `slide1`, `final` without numbers — alphabetical sort will put `final` before `intro` and `slide1` before `slide10`.

If you have more than 9 slides, use two digits: `01_`, `02_`, ..., `09_`, `10_`, `11_`.

### 5. Exporting to GLB

Once all your animations are pushed down into named NLA strips:

1. Go to `File → Export → glTF 2.0 (.glb/.gltf)`
2. In the export dialog on the right side, configure these settings:

   **Format:** `GLB` (single binary file — easier to move around)

   **Include:**
   - ✅ Selected Objects: OFF (export everything)
   - ✅ Custom Properties: ON (preserves extra metadata if you add any)

   **Transform:**
   - ✅ Y Up: ON (Three.js uses Y-up coordinates, same as glTF standard)

   **Data → Mesh:**
   - ✅ Apply Modifiers: ON

   **Data → Armature:** (if you have rigged characters)
   - ✅ Export Deformation Bones Only: OFF unless you specifically want this

   **Animation:**
   - ✅ Animation: ON
   - ✅ Export NLA Strips: **ON** ← this is the critical one
   - ✅ Export All Actions: OFF (you only want the NLA strips, not every loose action)
   - ✅ Group by NLA Track: OFF
   - ✅ Optimize Animation Size: ON (reduces file size)

   **Camera:**
   - ✅ Export Cameras: **ON** ← required for the website to use your camera

   **Lighting:**
   - Export Lights: ON if you want Blender lights in the scene (optional — the website adds its own ambient and directional lights)

3. Navigate to your project folder and name the file exactly `presentation.glb`
4. Click **Export glTF 2.0**

---

## Adding the GLB to the Project

1. Copy `presentation.glb` into the project at:
   ```
   static/models/presentation.glb
   ```
2. If the server is already running, just refresh the browser — it loads the GLB fresh on each page load
3. If the file is missing or has no animations, the page shows an error message explaining what's wrong

---

## Controls

| Input | Action |
|-------|--------|
| `→` Arrow key | Next slide |
| `←` Arrow key | Previous slide |
| `Space` | Next slide |
| Left click | Next slide |
| On-screen `←` `→` buttons | Navigate |

The slide counter in the bottom center shows your current position (e.g. `2 / 5`).

---

## Project Structure

```
dnhs-senior-project/
├── Blend Model/          # Blender source files (.blend)
├── static/
│   └── models/
│       └── presentation.glb   # ← your exported file goes here
├── templates/
│   ├── base.html         # redirects to /presentation
│   └── presentation.html # Three.js presentation page
├── logs/                 # auto-generated daily log files
├── main.py               # Flask server
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```
