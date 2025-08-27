from ColabTurtlePlus.Turtle import *
import time

# Initialize Turtle
initializeTurtle()
pensize(4)
pencolor("green")
speed(6)

# ==============================
# Parameters
# ==============================
vertical_height = 100
horizontal_length = 40
vertical_x = 0
vertical_bottom_y = 0
vertical_top_y = vertical_height

pause_time = 0.5  # pause between strokes

# ==============================
# Helper function: draw base step by step
# ==============================
def draw_base_live():
    # Draw main vertical line
    penup()
    goto(vertical_x, vertical_bottom_y)
    pendown()
    setheading(90)
    forward(vertical_height)
    time.sleep(pause_time)

    # Draw top horizontal line going left
    setheading(180)
    forward(horizontal_length)
    time.sleep(pause_time)

# ==============================
# Column-specific functions
# ==============================
def draw_ge():  # Column 1
    draw_base_live()

def draw_gu():  # Column 2 - small horizontal on right middle
    draw_base_live()
    penup()
    goto(vertical_x, vertical_height / 2)
    pendown()
    setheading(0)
    forward(20)
    time.sleep(pause_time)

def draw_gi():  # Column 3 - small horizontal on right bottom
    draw_base_live()
    penup()
    goto(vertical_x, vertical_bottom_y)
    pendown()
    setheading(0)
    forward(20)
    time.sleep(pause_time)

def draw_ga():  # Column 4 - horizontal line left at bottom
    draw_base_live()
    penup()
    goto(vertical_x, vertical_bottom_y)
    pendown()
    setheading(180)
    forward(30)
    time.sleep(pause_time)

def draw_gee():  # Column 5 - circle attached to the right edge of vertical line, upward
    draw_base_live()
    penup()
    # Right edge of vertical line, slightly above bottom
    goto(vertical_x + 15, vertical_bottom_y + 10)
    pendown()
    circle(15)
    time.sleep(pause_time)

def draw_ge2():  # Column 6 - circle at left end of horizontal line
    draw_base_live()
    penup()
    goto(vertical_x - horizontal_length, vertical_top_y)
    pendown()
    circle(15)
    time.sleep(pause_time)

def draw_go():  # Column 7 - vertical line on top middle of horizontal line
    draw_base_live()
    penup()
    goto(vertical_x - (horizontal_length / 2), vertical_top_y)
    pendown()
    setheading(90)
    forward(30)
    time.sleep(pause_time)

# ==============================
# Draw all 7 columns sequentially, live animation
# ==============================
columns = [draw_ge, draw_gu, draw_gi, draw_ga, draw_gee, draw_ge2, draw_go]
labels = ["ገ (ge)", "ጉ (gu)", "ጊ (gi)", "ጋ (ga)", "ጌ (gē)", "ግ (gə)", "ጎ (go)"]

for i, col in enumerate(columns):
    clear()
    col()  # Live drawing for that column
    penup()
    goto(0, -70)
    write(labels[i], align="center", font=("Arial", 18, "normal"))
    time.sleep(1.5)