# 2D Airport Runway Simulation

A small interactive airport scene built with Python, PyOpenGL, and GLUT. The project demonstrates 2D drawing primitives, orthographic projection, keyboard input, and timer-based animation.

## Features

- Airport scene with a runway, terminal, control tower, service vehicle, trees, and airplane
- Taxi and takeoff animation with ready, taxiing, and takeoff status
- Day and night scenes with moving clouds or stars
- Pause, reset, and keyboard controls
- Resizable window with an orthographic 2D view

## Requirements

- Python 3
- PyOpenGL and PyOpenGL_accelerate
- A working GLUT implementation (freeglut is commonly used)
- A graphics driver that supports OpenGL

On Windows, install freeglut if GLUT cannot create a window. Ensure its DLL is available on `PATH`.

## Setup and run

From this directory, create a virtual environment and install the dependencies:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python airport_simulation.py
```

If PowerShell blocks virtual environment activation, run the executable directly:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe airport_simulation.py
```

On macOS or Linux, use the platform's Python executable to create and activate `.venv`, then run `python -m pip install -r requirements.txt` and `python airport_simulation.py`. GLUT must also be installed using the operating system's package manager.

## Controls

| Key | Action |
| --- | --- |
| `S` | Start the airplane |
| `P` | Pause or resume |
| `R` | Reset to the starting position |
| `D` | Switch to day mode |
| `N` | Switch to night mode |
| `Esc` | Exit |

## Project structure

```text
airport_simulation.py  Main application and scene drawing code
requirements.txt       Python package dependencies
README.md              Setup, controls, and project overview
```

## Implementation overview

The scene is drawn from basic OpenGL primitives using a 2D orthographic projection. GLUT creates the window and dispatches keyboard and timer callbacks. Each timer update advances the airplane and clouds, then requests a redraw. The airplane progresses through `WAITING`, `RUNWAY`, and `TAKEOFF` states; day and night modes change the scene colors and sky details.

This is an educational visual demonstration. It does not model real aircraft physics or airport operations.
