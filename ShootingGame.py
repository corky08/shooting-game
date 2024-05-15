import tkinter as tk
import random
import math

### constants of window ###
frame_h = 400       # range of target moving
frame_w = 690

### variables of PLAYER ###
px = frame_w / 2        # coordinates of PLAYER
py = 500
p_speed = 4

### variables of BULLET ###
bx = 0                  # coordinates of BULLET
by = 0
b_speed = 6
shot = 0                # BULLET has been shot or not.  0 is 'not'

### variables of TARGET ###
tx = frame_w / 2                 # coordinates of TARGET
ty = frame_h / 2
t_speed = 5
radius = 35
angle = random.randint(0, 360)   # direction of TARGET moving
count = 0                        # The number of counter that will be increased each time function 'main()' is run
counter = 0

### others ###
mspf = 15      # running function 'main()' once per (ms) (constants)
key = ""       # keyboad input (variable)
scene = 0      # BULLET hits TARGET or not.   0 is 'not',   1 is 'game over' (variable)


def key_down(e):
    global key
    key = e.keysym

def key_up(e):
    global key
    key = ""

def player_move():
    global px, py, p_speed, key
    game_canvas.delete("PLAYER")
    if key == "a" and px > 30:               # the player moves left
        px -= p_speed
    if key == "d" and px < (frame_w - 20):   # the player moves right
        px += p_speed
    game_canvas.create_rectangle(px-5, py, px+5, py+20, fill = "black", tag = "PLAYER")
    game_canvas.create_polygon(px-5,py, px+5,py, px, py-5, fill = "black", tag = "PLAYER")

def shooting(e):
    global px, py, bx, by, shot
    bullet_num = left_bullet.get()
    if shot == 0 and bullet_num != 0:
        bx = px                               # set BULLET location
        by = py - 15
        shot = 1
        hit.set("")                           # initialize widget variables
        o_score.set("")
        bullet_num -= 1                       # update the number of left bullet
        left_bullet.set(bullet_num)
        game_canvas.create_line(bx,by, bx,by+10, width = 2, fill = "red", tag = "BULLET")
        

def bullet_move():
    global bx, by, shot, scene
    if scene == 0:
        game_canvas.delete("BULLET")
        if shot == 1:
            by -= b_speed
            if by < 10:    # if BULLET is out of canvas, delete BULLET and initialize the variables
                shot = 0
                bx = 0
                by = 0
                hit.set("Miss")
                o_score.set("0 Point")
                bullet_num = left_bullet.get()
                if bullet_num == 0:             # if the number of left bullet is 0, Gameover
                    scene = 1
            else:
                game_canvas.create_line(bx,by, bx,by+10, width = 2, fill = "red", tag = "BULLET")
                
def target_move():
    global tx, ty, angle, counter
    if scene == 0:
        game_canvas.delete("TARGET")
        tx += t_speed * math.cos(math.radians(angle))     # TARGET moving
        ty += t_speed * math.sin(math.radians(angle))
        counter += count
        if tx >= frame_w - radius:   # bounce on the right wall
            angle = 180 - angle
            tx = frame_w - radius
        if tx <= 10 + radius:        # bounce on the left wall
            angle = 180 - angle
            tx = 10 + radius
        if ty <= 10 + radius:        # bounce on the wall above
            angle = -angle
            ty = 10 + radius
        if ty >= frame_h - radius:   # bounce on the wall below
            angle = -angle
            ty = frame_h - radius
        if angle < 0:
            angle += 360
        if counter > 1000:
            angle = random.randint(0, 360)
            counter = 0
        elif counter > 800:          # The color of TARGET changes just before the direction of movement changes
            game_canvas.create_oval(tx-radius,ty-radius, tx+radius,ty+radius, fill = "red", tag = "TARGET")
            game_canvas.create_oval(tx-(2*radius/3),ty-(2*radius/3), tx+(2*radius/3),ty+(2*radius/3), fill = "white", tag = "TARGET")
            game_canvas.create_oval(tx-(radius/3),ty-(radius/3), tx+(radius/3),ty+(radius/3), fill = "red", tag = "TARGET")
        else:
            game_canvas.create_oval(tx-radius,ty-radius, tx+radius,ty+radius, fill = "green", tag = "TARGET")
            game_canvas.create_oval(tx-(2*radius/3),ty-(2*radius/3), tx+(2*radius/3),ty+(2*radius/3), fill = "white", tag = "TARGET")
            game_canvas.create_oval(tx-(radius/3),ty-(radius/3), tx+(radius/3),ty+(radius/3), fill = "green", tag = "TARGET")

def collision():
    global bx, by, tx, ty, scene
    if abs(ty-by) <= (b_speed/2 + max(0, t_speed*math.sin(math.radians(angle)))):   # prevent BULLET from slipping through by adding width to the y-axis of the hit detection.
        if abs(tx-bx) < (radius/3):             # get score based on the distance between BULLET hit location and the center of TARGET
            hit.set("Hit")
            o_score.set("50 Point")             # score that this shot gets
            new_score = t_score.get() + 50
            t_score.set(new_score)              # update total score
            bullet_num = left_bullet.get()
            if bullet_num == 0:                 # if the number of left bullet is 0, Gameover
                scene = 1
            restart()
        elif abs(tx-bx) < (2*radius/3):
            hit.set("Hit")
            o_score.set("30 Point")
            new_score = t_score.get() + 30
            t_score.set(new_score)
            bullet_num = left_bullet.get()
            if bullet_num == 0:
                scene = 1
            restart()
        elif abs(tx-bx) < radius:
            hit.set("Hit")
            o_score.set("10 Point")
            new_score = t_score.get() + 10
            t_score.set(new_score)
            bullet_num = left_bullet.get()
            if bullet_num == 0:
                scene = 1
            restart()

def restart():                                     # initialize the variables
    global bx, by, shot, tx, ty, scene, angle, counter
    if scene == 0:
        bx = 0
        by = 0
        shot = 0
        tx = frame_w / 2
        ty = frame_h / 2
        counter = 0
        angle = random.randint(0, 360)

def gameover():
    global scene
    if scene == 1:
        game_canvas.delete("TARGET")
        game_canvas.delete("BULLET")
        game_canvas.delete("GAMEOVER")
        game_canvas.config(bg = "black")
        total_score = str(t_score.get())
        game_canvas.create_text(350, 100, text = "Game over", font = 'Times 50', fill = 'white', tag = "GAMEOVER")
        game_canvas.create_text(350, 200, text = "Your Score is", font = 'Times 30', fill = 'white', tag = "GAMEOVER")
        game_canvas.create_text(350, 300, text = total_score, font = 'Times 80', fill = 'white', tag = "GAMEOVER")
        game_canvas.create_text(350, 500, text = "Press space key to restart", font = 'Times 40', fill = 'white', tag = "GAMEOVER")
        if key == "space":
            game_canvas.delete("GAMEOVER")           # initialize the variables and restart main() function
            game_canvas.config(bg = defaultbg)
            scene = 0
            left_bullet.set(10)
            t_score.set(0)
            o_score.set("")
            hit.set("")
            restart()
            main()
        win.after(mspf, gameover)


### function to change PLAYER speed ###
def pspeed_slow():
    global p_speed
    p_speed = 2

def pspeed_normal():
    global p_speed
    p_speed = 4

def pspeed_fast():
    global p_speed
    p_speed = 6

### function to change BULLET speed ###
def bspeed_slow():
    global b_speed
    b_speed = 4

def bspeed_normal():
    global b_speed
    b_speed = 8

def bspeed_fast():
    global b_speed
    b_speed = 12

### function to change TARGET speed ###
def tspeed_slow():
    global t_speed
    t_speed = 2

def tspeed_normal():
    global t_speed
    t_speed = 5

def tspeed_fast():
    global t_speed
    t_speed = 10

### function to change TARGET size ###
def tsize_big():
    global radius
    radius = 50

def tsize_normal():
    global radius
    radius = 35

def tsize_small():
    global radius
    radius = 25

### function to change interval count ###
def tinterval_none():
    global count, counter
    count = 0
    counter = 0

def tinterval_normal():
    global count, counter
    count = 3
    counter = 0

def tinterval_short():
    global count, counter
    count = 6
    counter = 0


def main():
    global key
    player_move()
    target_move()
    bullet_move()
    collision()
    if scene == 0:
        win.after(mspf, main)
    if scene == 1:
        gameover()
    
    
win = tk.Tk()
win.geometry("1000x600")
win.title("shooting game")
defaultbg = win.cget('bg')

game_canvas = tk.Canvas(win, height = 600, width = frame_w + 10)
game_canvas.pack(anchor=tk.NW)


### show the range in which TARGET can move ###
game_canvas.create_rectangle(10, 10, frame_w, frame_h, outline = "black")

### show the range in which PLAYER can move ###
game_canvas.create_line(30,py+10, (frame_w-20),py+10)
game_canvas.create_line(30,py+15, 30,py+5)
game_canvas.create_line((frame_w-20),py+15, (frame_w-20),py+5)

### widget variable ###
hit = tk.StringVar()       # display charactors of "Hit"
o_score = tk.StringVar()   # score for one shot
t_score = tk.IntVar()      # total score
left_bullet = tk.IntVar()  # the number of left bullet
left_bullet.set(10)

### widget frame that shows information for one shot ### 
shot_frame = tk.Frame(win, relief = "ridge", bd = 3, padx = 5, pady = 5)
hit_marker = tk.Label(shot_frame, relief = "sunken", height = 1, width = 5, textvariable = hit, font = 'Times 50', fg = 'pink')
hit_marker.pack()
point_display = tk.Label(shot_frame, relief = "groove", height = 1, width = 10, textvariable = o_score, font = 'Times 25', fg = 'pink')
point_display.pack()
shot_frame.place(x = 750, y = 20)

### widget frame that shows the number of left bullet ###
bullet_frame = tk.Frame(win, relief = "ridge", bd = 3, padx = 5, pady = 5)
left_label = tk.Label(bullet_frame, relief = "groove", height = 1, width = 10, text ='Left bullet', font = 'Times 25')
left_label.pack()
bullet_number = tk.Label(bullet_frame, relief = "sunken", height = 1, width = 4, textvariable = left_bullet, font = 'Times 40')
bullet_number.pack()
bullet_frame.place(x = 750, y = 180)

### widget frame that shows total score ###
score_frame = tk.Frame(win, relief = "ridge", bd = 3, padx = 5, pady = 5)
score_label = tk.Label(score_frame, relief = "groove", height = 1, width = 10, text ='Total Score', font = 'Times 25')
score_label.pack()
total_score = tk.Label(score_frame, relief = "sunken", height = 1, width = 5, textvariable = t_score, text = 'Point',font = 'Times 50')
total_score.pack()
score_frame.place(x = 750, y = 420)

win.bind("<KeyPress>", key_down)
win.bind("<KeyRelease>", key_up)
win.bind("<Button>", shooting)

mainmenu = tk.Menu(win)
playermenu = tk.Menu(mainmenu)
p_speedmenu = tk.Menu(mainmenu)
bulletmenu = tk.Menu(mainmenu)
b_speedmenu = tk.Menu(mainmenu)
targetmenu = tk.Menu(mainmenu)
t_speedmenu = tk.Menu(mainmenu)
t_sizemenu = tk.Menu(mainmenu)
t_intervalmenu = tk.Menu(mainmenu)

mainmenu.add_cascade(label = "Player", menu = playermenu)
playermenu.add_cascade(label = "Speed", menu = p_speedmenu)
p_speedmenu.add_command(label = "slow", command = pspeed_slow)
p_speedmenu.add_command(label = "normal", command = pspeed_normal)
p_speedmenu.add_command(label = "fast", command = pspeed_fast)

mainmenu.add_cascade(label = "Bullet", menu = bulletmenu)
bulletmenu.add_cascade(label = "Speed", menu = b_speedmenu)
b_speedmenu.add_command(label = "slow", command = bspeed_slow)
b_speedmenu.add_command(label = "normal", command = bspeed_normal)
b_speedmenu.add_command(label = "fast", command = bspeed_fast)

mainmenu.add_cascade(label = "Target", menu = targetmenu)
targetmenu.add_cascade(label = "Speed", menu = t_speedmenu)
targetmenu.add_cascade(label = "Size", menu = t_sizemenu)
targetmenu.add_cascade(label = "Random", menu = t_intervalmenu)

t_speedmenu.add_command(label = "slow", command = tspeed_slow)
t_speedmenu.add_command(label = "normal", command = tspeed_normal)
t_speedmenu.add_command(label = "fast", command = tspeed_fast)

t_sizemenu.add_command(label = "big", command = tsize_big)
t_sizemenu.add_command(label = "medium", command = tsize_normal)
t_sizemenu.add_command(label = "small", command = tsize_small)

t_intervalmenu.add_command(label = "none", command = tinterval_none)
t_intervalmenu.add_command(label = "normal", command = tinterval_normal)
t_intervalmenu.add_command(label = "frequent", command = tinterval_short)

win.config(menu = mainmenu)
main()

win.mainloop()
