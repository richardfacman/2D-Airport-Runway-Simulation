import math
import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


WIDTH = 1000
HEIGHT = 700

# Airplane state and movement variables.
plane_x = 205.0
plane_y = 150.0
plane_speed = 2.6
vertical_speed = 3.2
state = "WAITING"
pause = False
day_mode = True
scene_scale_x = 1.0

# Small cloud objects moving slowly across the sky.
clouds = [
    {"x": 280.0, "y": 435.0, "speed": 0.18},
    {"x": 520.0, "y": 455.0, "speed": 0.20},
    {"x": 720.0, "y": 420.0, "speed": 0.16},
    {"x": 930.0, "y": 445.0, "speed": 0.22},
]


def reset_airplane():
    """Return the airplane and animation state to the initial waiting position."""
    global plane_x, plane_y, state, pause
    plane_x = 205.0
    plane_y = 150.0
    state = "WAITING"
    pause = False


# ------------------------------------------------------------
# OpenGL helper functions
# ------------------------------------------------------------

def draw_text(x, y, text, color=(1.0, 1.0, 1.0), font=GLUT_BITMAP_HELVETICA_12):
    """Draw basic text using GLUT bitmap fonts."""
    glColor3f(*color)
    glRasterPos2f(x, y)
    for character in text:
        glutBitmapCharacter(font, ord(character))


def draw_circle(cx, cy, radius, segments=24):
    """Draw a filled circle using GL_POLYGON."""
    glBegin(GL_POLYGON)
    for i in range(segments):
        angle = 2.0 * math.pi * i / segments
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        glVertex2f(x, y)
    glEnd()


# ------------------------------------------------------------
# Scene drawing functions
# ------------------------------------------------------------

def draw_background():
    """Draw the sky. In day mode the sky is blue; in night mode it is dark blue."""
    if day_mode:
        glColor3f(0.38, 0.72, 0.96)
    else:
        glColor3f(0.03, 0.05, 0.18)

    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(WIDTH, 0)
    glVertex2f(WIDTH, HEIGHT)
    glVertex2f(0, HEIGHT)
    glEnd()


def draw_ground():
    """Draw the ground area at the bottom of the screen."""
    if day_mode:
        glColor3f(0.20, 0.68, 0.30)
    else:
        glColor3f(0.14, 0.30, 0.22)

    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(WIDTH, 0)
    glVertex2f(WIDTH, 235)
    glVertex2f(0, 235)
    glEnd()


def draw_runway():
    """Draw runway pavement, edge lines, threshold bars, centerline, and numbers."""
    if day_mode:
        glColor3f(0.25, 0.28, 0.32)
    else:
        glColor3f(0.10, 0.13, 0.19)

    glBegin(GL_QUADS)
    glVertex2f(0, 120)
    glVertex2f(WIDTH, 120)
    glVertex2f(WIDTH, 190)
    glVertex2f(0, 190)
    glEnd()

    # Solid white edge lines.
    glColor3f(1.0, 1.0, 1.0)
    for y in (112, 185):
        glBegin(GL_QUADS)
        glVertex2f(0, y)
        glVertex2f(WIDTH, y)
        glVertex2f(WIDTH, y + 3)
        glVertex2f(0, y + 3)
        glEnd()

    # Dashed centerline and threshold bars at both ends.
    for x in range(125, WIDTH - 125, 105):
        glBegin(GL_QUADS)
        glVertex2f(x, 147)
        glVertex2f(x + 55, 147)
        glVertex2f(x + 55, 153)
        glVertex2f(x, 153)
        glEnd()
    for x in (28, 945):
        for offset in range(0, 48, 14):
            glBegin(GL_QUADS)
            glVertex2f(x + offset, 120)
            glVertex2f(x + offset + 7, 120)
            glVertex2f(x + offset + 7, 178)
            glVertex2f(x + offset, 178)
            glEnd()
    draw_text(112, 159, "09", color=(1.0, 1.0, 1.0))
    draw_text(875, 159, "27", color=(1.0, 1.0, 1.0))


def draw_runway_lights():
    """Place small lights along the runway edges in both scene modes."""
    if day_mode:
        glColor3f(0.92, 0.95, 0.80)
    else:
        glColor3f(1.0, 0.82, 0.20)
    for x in range(60, WIDTH, 90):
        draw_circle(x, 108, 4 if not day_mode else 3, 12)
        draw_circle(x, 192, 4 if not day_mode else 3, 12)


def draw_airport():
    """Draw a terminal with roof, glass facade, sign, entrance, and details."""
    if day_mode:
        building_color = (0.82, 0.86, 0.89)
        roof_color = (0.20, 0.31, 0.40)
        glass_color = (0.20, 0.62, 0.78)
    else:
        building_color = (0.38, 0.45, 0.55)
        roof_color = (0.13, 0.19, 0.29)
        glass_color = (0.20, 0.42, 0.61)

    glColor3f(*building_color)
    glBegin(GL_QUADS)
    glVertex2f(650, 235)
    glVertex2f(950, 235)
    glVertex2f(950, 410)
    glVertex2f(650, 410)
    glEnd()

    # Wide roof cap.
    glColor3f(*roof_color)
    glBegin(GL_TRIANGLES)
    glVertex2f(630, 410)
    glVertex2f(970, 410)
    glVertex2f(950, 440)
    glEnd()
    glBegin(GL_QUADS)
    glVertex2f(630, 410)
    glVertex2f(950, 410)
    glVertex2f(950, 425)
    glVertex2f(630, 425)
    glEnd()

    # Three broad glass panels with simple frames.
    for x in (675, 765, 855):
        glColor3f(*glass_color)
        glBegin(GL_QUADS)
        glVertex2f(x, 285)
        glVertex2f(x + 70, 285)
        glVertex2f(x + 70, 365)
        glVertex2f(x, 365)
        glEnd()
        glColor3f(0.88, 0.92, 0.94)
        glBegin(GL_LINES)
        glVertex2f(x + 35, 285)
        glVertex2f(x + 35, 365)
        glVertex2f(x, 325)
        glVertex2f(x + 70, 325)
        glEnd()

    # Entrance doors and airport sign.
    glColor3f(0.14, 0.22, 0.30)
    glBegin(GL_QUADS)
    glVertex2f(770, 235)
    glVertex2f(825, 235)
    glVertex2f(825, 280)
    glVertex2f(770, 280)
    glEnd()
    glColor3f(0.25, 0.65, 0.82)
    glBegin(GL_QUADS)
    glVertex2f(765, 375)
    glVertex2f(845, 375)
    glVertex2f(845, 403)
    glVertex2f(765, 403)
    glEnd()
    draw_text(775, 385, "AIRPORT", color=(1.0, 1.0, 1.0))


def draw_control_tower():
    """Draw a narrow control tower with an observation room and glass windows."""
    if day_mode:
        base_color = (0.74, 0.79, 0.83)
        roof_color = (0.18, 0.27, 0.35)
        glass_color = (0.12, 0.55, 0.72)
    else:
        base_color = (0.38, 0.43, 0.51)
        roof_color = (0.13, 0.18, 0.25)
        glass_color = (0.15, 0.37, 0.53)

    glColor3f(*base_color)
    glBegin(GL_QUADS)
    glVertex2f(550, 235)
    glVertex2f(585, 235)
    glVertex2f(585, 405)
    glVertex2f(550, 405)
    glEnd()

    # Observation room sits on the narrow tower shaft.
    glColor3f(*base_color)
    glBegin(GL_QUADS)
    glVertex2f(525, 405)
    glVertex2f(610, 405)
    glVertex2f(610, 455)
    glVertex2f(525, 455)
    glEnd()
    glColor3f(*glass_color)
    glBegin(GL_QUADS)
    glVertex2f(533, 414)
    glVertex2f(602, 414)
    glVertex2f(602, 444)
    glVertex2f(533, 444)
    glEnd()

    glColor3f(*roof_color)
    glBegin(GL_QUADS)
    glVertex2f(518, 455)
    glVertex2f(617, 455)
    glVertex2f(610, 468)
    glVertex2f(525, 468)
    glEnd()

    glColor3f(0.35, 0.39, 0.43)
    glBegin(GL_QUADS)
    glVertex2f(535, 235)
    glVertex2f(600, 235)
    glVertex2f(600, 250)
    glVertex2f(535, 250)
    glEnd()


def draw_cloud(x, y, scale=1.0):
    """Draw a simple white cloud using circles (GL_POLYGON)."""
    glColor3f(1.0, 1.0, 1.0)
    draw_circle(x, y, 30 * scale, 24)
    draw_circle(x + 35 * scale, y + 12 * scale, 26 * scale, 24)
    draw_circle(x + 70 * scale, y, 24 * scale, 24)
    draw_circle(x + 22 * scale, y - 12 * scale, 24 * scale, 24)


def draw_clouds():
    """Display moving clouds in day mode."""
    for cloud in clouds:
        draw_cloud(cloud["x"], cloud["y"], 1.0)


def draw_stars():
    """Draw static stars in night mode using points."""
    glColor3f(1.0, 1.0, 1.0)
    glPointSize(3.0)
    glBegin(GL_POINTS)
    star_positions = [
        (90, 630), (150, 580), (220, 650), (330, 610),
        (470, 620), (560, 660), (700, 610), (840, 650),
        (910, 600), (790, 560), (670, 590), (390, 650)
    ]
    for x, y in star_positions:
        glVertex2f(x, y)
    glEnd()
    glPointSize(1.0)


def draw_vehicle():
    """Draw a compact yellow airport service van with cabin, lights, and wheels."""
    if day_mode:
        body_color = (0.95, 0.62, 0.12)
    else:
        body_color = (0.72, 0.45, 0.12)

    glColor3f(*body_color)
    glBegin(GL_QUADS)
    glVertex2f(805, 55)
    glVertex2f(910, 55)
    glVertex2f(910, 90)
    glVertex2f(805, 90)
    glEnd()

    # Sloped cabin shape, facing to the right.
    glColor3f(0.88, 0.56, 0.12)
    glBegin(GL_POLYGON)
    glVertex2f(825, 88)
    glVertex2f(840, 112)
    glVertex2f(887, 112)
    glVertex2f(902, 88)
    glEnd()

    # Blue windshield and side window.
    glColor3f(0.18, 0.58, 0.78)
    glBegin(GL_QUADS)
    glVertex2f(845, 94)
    glVertex2f(865, 94)
    glVertex2f(865, 106)
    glVertex2f(841, 106)
    glVertex2f(870, 94)
    glVertex2f(894, 94)
    glVertex2f(886, 106)
    glVertex2f(870, 106)
    glEnd()

    # Bumper, headlights, and two dark wheels with gray hubs.
    glColor3f(0.25, 0.28, 0.30)
    glBegin(GL_QUADS)
    glVertex2f(800, 53)
    glVertex2f(915, 53)
    glVertex2f(915, 60)
    glVertex2f(800, 60)
    glEnd()
    glColor3f(1.0, 0.96, 0.65)
    draw_circle(910, 76, 5, 12)
    glColor3f(0.12, 0.14, 0.16)
    for wheel_x in (830, 892):
        draw_circle(wheel_x, 55, 10, 16)
        glColor3f(0.70, 0.72, 0.74)
        draw_circle(wheel_x, 55, 4, 12)
        glColor3f(0.12, 0.14, 0.16)


def draw_tree(x, y, scale=1.0):
    """Draw a small tree from a brown trunk and two green foliage circles."""
    glColor3f(0.38, 0.20, 0.10)
    glBegin(GL_QUADS)
    glVertex2f(x - 5 * scale, y)
    glVertex2f(x + 5 * scale, y)
    glVertex2f(x + 5 * scale, y + 28 * scale)
    glVertex2f(x - 5 * scale, y + 28 * scale)
    glEnd()
    if day_mode:
        glColor3f(0.10, 0.43, 0.18)
    else:
        glColor3f(0.08, 0.28, 0.16)
    draw_circle(x, y + 38 * scale, 17 * scale, 20)
    draw_circle(x - 10 * scale, y + 31 * scale, 12 * scale, 20)


def draw_airplane(x, y, scale=1.0):
    """Draw the red, orange, and cyan passenger jet used by this simulation."""
    glPushMatrix()
    glTranslatef(x, y, 0.0)
    glScalef(scale, scale, 1.0)

    # Far wing, tailplane, and tall swept tail fin.
    glColor3f(0.04, 0.48, 0.75)
    glBegin(GL_POLYGON)
    glVertex2f(-65, 6)
    glVertex2f(-5, 10)
    glVertex2f(35, 49)
    glVertex2f(12, 47)
    glVertex2f(-28, 15)
    glEnd()
    glColor3f(0.06, 0.58, 0.82)
    glBegin(GL_POLYGON)
    glVertex2f(-73, 2)
    glVertex2f(-112, 8)
    glVertex2f(-69, 13)
    glVertex2f(-47, 9)
    glEnd()
    glColor3f(0.05, 0.62, 0.86)
    glBegin(GL_POLYGON)
    glVertex2f(-74, 8)
    glVertex2f(-88, 64)
    glVertex2f(-82, 72)
    glVertex2f(-72, 70)
    glVertex2f(-51, 19)
    glEnd()

    # Near wing, visible under the fuselage, with two blue engine nacelles.
    glColor3f(0.06, 0.39, 0.68)
    glBegin(GL_POLYGON)
    glVertex2f(-25, 2)
    glVertex2f(22, -38)
    glVertex2f(68, -42)
    glVertex2f(42, -17)
    glVertex2f(3, 5)
    glEnd()
    for engine_x, engine_y in ((-8, -28), (53, -30)):
        glColor3f(0.05, 0.38, 0.70)
        draw_circle(engine_x, engine_y, 12, 24)
        glColor3f(0.08, 0.70, 0.90)
        draw_circle(engine_x + 1, engine_y + 1, 7, 20)
        glColor3f(0.08, 0.18, 0.28)
        draw_circle(engine_x + 2, engine_y + 1, 4, 16)

    # Long rounded fuselage, with the bright red lower body and orange crown.
    glColor3f(0.83, 0.06, 0.04)
    glBegin(GL_POLYGON)
    glVertex2f(-82, 7)
    glVertex2f(-74, -6)
    glVertex2f(-49, -15)
    glVertex2f(4, -17)
    glVertex2f(55, -10)
    glVertex2f(83, 2)
    glVertex2f(94, 11)
    glVertex2f(79, 18)
    glVertex2f(46, 24)
    glVertex2f(-26, 21)
    glVertex2f(-68, 15)
    glEnd()
    glColor3f(0.98, 0.23, 0.08)
    glBegin(GL_POLYGON)
    glVertex2f(-79, 8)
    glVertex2f(-70, 15)
    glVertex2f(-24, 22)
    glVertex2f(25, 39)
    glVertex2f(58, 34)
    glVertex2f(79, 19)
    glVertex2f(48, 18)
    glVertex2f(-24, 15)
    glEnd()

    # Blue cockpit glazing and a bright cyan row of cabin windows.
    glColor3f(0.02, 0.20, 0.38)
    glBegin(GL_POLYGON)
    glVertex2f(54, 27)
    glVertex2f(71, 24)
    glVertex2f(84, 16)
    glVertex2f(53, 18)
    glEnd()
    glColor3f(0.12, 0.72, 0.90)
    for window_x, window_y in ((-53, 14), (-42, 16), (-31, 18), (-20, 20),
                               (-9, 22), (2, 25), (13, 28), (24, 31), (35, 33)):
        draw_circle(window_x, window_y, 2.5, 12)

    # Landing gear and twin wheels remain visible during taxi and takeoff.
    glColor3f(0.12, 0.14, 0.16)
    glBegin(GL_LINES)
    glVertex2f(-45, -12)
    glVertex2f(-45, -25)
    glVertex2f(40, -10)
    glVertex2f(40, -24)
    glEnd()
    draw_circle(-45, -26, 5, 14)
    draw_circle(40, -25, 6, 14)

    glPopMatrix()


def draw_title():
    """Show the simulation title at the top of the screen."""
    draw_text(350, 670, "2D AIRPORT RUNWAY SIMULATION", color=(1.0, 1.0, 1.0),
              font=GLUT_BITMAP_HELVETICA_18)


def draw_status_panel():
    """Show the current aircraft state, runway number, and selected scene mode."""
    if state == "WAITING":
        aircraft_status = "READY"
    elif state == "RUNWAY":
        aircraft_status = "TAXIING"
    else:
        aircraft_status = "TAKEOFF"
    if pause:
        aircraft_status += " / PAUSED"

    panel_color = (0.07, 0.12, 0.20) if day_mode else (0.02, 0.04, 0.11)
    glColor3f(*panel_color)
    glBegin(GL_QUADS)
    glVertex2f(20, 505)
    glVertex2f(225, 505)
    glVertex2f(225, 625)
    glVertex2f(20, 625)
    glEnd()
    draw_text(34, 603, "FLIGHT STATUS", color=(0.45, 0.82, 1.0))
    draw_text(34, 579, "Aircraft: " + aircraft_status)
    draw_text(34, 555, "Runway: 09 / 27")
    mode_text = "DAY" if day_mode else "NIGHT"
    draw_text(34, 531, "Mode: " + mode_text)


def draw_controls():
    """Display keyboard instructions at the bottom of the screen."""
    controls = "[S] Start   [P] Pause   [R] Reset   [D] Day   [N] Night   [ESC] Exit"
    draw_text(130, 25, controls, color=(1.0, 1.0, 1.0))


def display():
    """Main display loop: clear the buffer, draw the scene, then swap buffers."""
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH * scene_scale_x, 0, HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glScalef(scene_scale_x, 1.0, 1.0)

    draw_background()
    draw_ground()

    if day_mode:
        draw_clouds()
    else:
        draw_stars()

    draw_airport()
    draw_control_tower()
    draw_tree(80, 235, 1.2)
    draw_tree(450, 235, 1.0)
    draw_tree(975, 235, 1.15)
    draw_runway()
    draw_runway_lights()
    draw_vehicle()
    draw_airplane(plane_x, plane_y)
    draw_title()
    draw_status_panel()
    draw_controls()

    glutSwapBuffers()


# ------------------------------------------------------------
# Animation and keyboard handling
# ------------------------------------------------------------

def update(value):
    """Timer-based animation update."""
    global plane_x, plane_y, state

    if not pause:
        if state == "RUNWAY":
            plane_x += plane_speed
            if plane_x >= 650:
                state = "TAKEOFF"

        elif state == "TAKEOFF":
            # Move forward more slowly while climbing so the airplane stays
            # visible in the sky instead of disappearing off the right edge.
            plane_x += plane_speed * 0.6
            plane_y += vertical_speed
            # Reset at the top edge after the complete airplane has been visible.
            if plane_x > WIDTH + 120 or plane_y >= HEIGHT - 25:
                reset_airplane()

        # Move clouds slowly from left to right.
        for cloud in clouds:
            cloud["x"] += cloud["speed"]
            if cloud["x"] > WIDTH + 120:
                cloud["x"] = -120

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


def keyboard(key, x, y):
    """Respond to keyboard input for start, pause, reset, day/night, and exit."""
    global state, pause, day_mode

    key = key.decode('ascii')

    if key == 's' or key == 'S':
        if state == "WAITING":
            state = "RUNWAY"

    elif key == 'p' or key == 'P':
        pause = not pause

    elif key == 'r' or key == 'R':
        reset_airplane()

    elif key == 'd' or key == 'D':
        day_mode = True

    elif key == 'n' or key == 'N':
        day_mode = False

    elif key == '\x1b':
        sys.exit(0)

    glutPostRedisplay()


# ------------------------------------------------------------
# OpenGL setup and program entry
# ------------------------------------------------------------

def init_opengl():
    """Initialize OpenGL and set the orthographic projection."""
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, 0, HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def reshape(width, height):
    """Fill a resized window while keeping the scene and shapes proportional."""
    global scene_scale_x
    if height == 0:
        height = 1
    if width == 0:
        width = 1

    # Stretch the virtual x range and all x coordinates by the same amount.
    # This uses the full window without changing the physical shape of objects.
    scene_scale_x = (width / height) / (WIDTH / HEIGHT)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH * scene_scale_x, 0, HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    """Create the GLUT window and start the simulation."""
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow(b"2D Airport Runway Simulation")

    init_opengl()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(16, update, 0)
    glutMainLoop()


if __name__ == "__main__":
    main()
