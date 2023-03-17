# Arcanoid_Capstone(1).py
# Author: Georgios Lazari (G21065613)
# Email: GLazari@uclan.ac.uk
# Description: The Arcanoid_Capstone(1).py program demonstrates the Arkanoid game which is an arcade game
# from the 1980's. The player controls with the mouse a rectangular craft at the bottom of the screen, moving left
# and right, to deflect a ball and eliminate a number of bricks by hitting them with the ball. The score increase by
# 10 each time a brick breaks. There are two levels the first level is with one ball and the second level it is with
# two balls. The player looses when the ball hits the bottom the window and wins when all the bricks break.
# You can try again when loosing a level or exit the program.


from tkinter import *
from random import randint

# contant variables for width and height of the window(reused from DrawCircle.py in week01, step0104)
WIDTH = 800
HEIGHT = 600
# constant variables for window title and animation delay(reused from DrawCircle.py in week01, step0104)
TITLE = 'Arcanoid Georgios Lazari'
DELAY = 20

# graphical window creation, adding title and dimensions(reused from DrawCircle.py in week01, step0104)
arcanoid = Tk()
arcanoid.title(TITLE)
arcanoid.geometry(str(WIDTH) + 'x' + str(HEIGHT))

# Link the canvas to the 'arcanoid' and set its size(reused from DrawCircle.py in week01, step0104)
window = Canvas(arcanoid, width=WIDTH, height=HEIGHT, bg='pink')
window.pack()


# The definition of the Ball Class is reused from the Collisions.py code provided under Week03, step0306.
class Ball:

    def __init__(self, ball_x, ball_y, speed_x, speed_y, radius, color, ball_outline):
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.radius = radius
        self.color = color
        self.ball_outline = ball_outline
        self.canvas_object = window.create_oval(ball_x - radius, ball_y - radius, ball_x + radius, ball_y + radius,
                                                fill=self.color, outline=self.ball_outline)

    # method to remove a ball object
    def remove(self):
        window.delete(self.canvas_object)

    # method to move the ball object within the window, setting it to deflect on the extremities
    # changing speed of x and y (reused from the Collisions.py code provided under Week03, step0306).
    def move(self):
        self.ball_x = self.ball_x + self.speed_x
        if self.ball_x >= WIDTH - self.radius:
            self.speed_x = -abs(self.speed_x)
        if self.ball_x <= self.radius:
            self.speed_x = abs(self.speed_x)
        self.ball_y = self.ball_y + self.speed_y
        if self.ball_y >= HEIGHT - self.radius:
            self.speed_y = -abs(self.speed_y)
        if self.ball_y <= self.radius:
            self.speed_y = abs(self.speed_y)

    # method to update the coordinates of the ball object(used from Collisions.py in week03, step0306)
    def draw(self):
        window.coords(self.canvas_object, self.ball_x - self.radius, self.ball_y - self.radius,
                      self.ball_x + self.radius,
                      self.ball_y + self.radius)


# Ufo class to create the ufo objects on the main menu, used a similar way as creating a ball
class Ufo:
    def __init__(self, ufo_x, ufo_y, x_radius, y_radius, ufo_speed_x, ufo_speed_y, ufo_fill, ufo_outline):
        self.ufo_x = ufo_x
        self.ufo_y = ufo_y
        self.x_radius = x_radius
        self.y_radius = y_radius
        self.ufo_fill = ufo_fill
        self.ufo_outline = ufo_outline
        self.ufo_speed_y = ufo_speed_y
        self.ufo_speed_x = ufo_speed_x
        self.ufo_object = window.create_oval(ufo_x - x_radius, ufo_y - y_radius, ufo_x + x_radius,
                                             ufo_y + y_radius, fill=ufo_fill, outline=ufo_outline)

    #  method to remove an ufo object from the window
    def remove_ufo(self):
        window.delete(self.ufo_object)


# brick class to create the bricks, same way as making a rectangle
class Brick:
    def __init__(self, brick_left, brick_top, brick_right, brick_bottom, color):
        self.brick_left = brick_left
        self.brick_top = brick_top
        self.brick_right = brick_right
        self.brick_bottom = brick_bottom
        self.color = color
        self.window_object = window.create_rectangle(brick_left, brick_top, brick_right, brick_bottom, fill=self.color,
                                                     outline='black')

    # method to remove a brick object from the window
    def remove_brick(self):
        window.delete(self.window_object)


# craft class to create the craft, same way as making a rectangle
class Craft:
    def __init__(self, left, top, right, bottom, color_of_craft):
        self.left = left  # in Python, it's enough to declare a class value implicitly (in this case 'self.x' etc.)
        self.top = top
        self.right = right
        self.bottom = bottom
        self.color_of_craft = color_of_craft
        self.window_object = window.create_rectangle(left, top, right, bottom, fill=self.color_of_craft)

    # method to update the coordinates of the craft (used from Collisions.py in week03, step0306)
    def draw_craft(self):
        window.coords(self.window_object, self.left, self.top, self.right, self.bottom)

    # method to remove the craft
    def remove_craft(self):
        window.delete(self.window_object)


# Final score class to create the message of either loosing or winning along with the final score points
class FinalScore:
    def __init__(self, score_x, score_y, text, font, colour_fill, score_points):
        self.score_x = score_x
        self.score_y = score_y
        self.text = text
        self.font = font
        self.colour_fill = colour_fill
        self.score_points = score_points
        self.window_object = window.create_text(score_x, score_y, text=self.text + str(self.score_points),
                                                font=self.font, fill=self.colour_fill)

    # method to change the colour and text of the Final Score(used from ShowingTextOnCanvas.py in week03, step0303)
    def change_score_colour(self, new_colour):
        window.itemconfig(self.window_object, fill=new_colour, text=self.text + str(score.score_points))

    # method to change the text of a Final Score object from the window
    def remove_final_score(self):
        window.itemconfig(self.window_object, text="")


# ScoreBoard class to create the changing score while the game is played
class Score_Board:
    def __init__(self, score_x, score_y, text, font, colour_fill, score_points):
        self.score_x = score_x
        self.score_y = score_y
        self.text = text
        self.font = font
        self.colour_fill = colour_fill
        self.score_points = score_points
        self.window_object = window.create_text(score_x, score_y, text=self.text + str(self.score_points),
                                                font=self.font, fill=self.colour_fill)

    # method to update the points of the score(used from ShowingTextOnCanvas.py in week03, step0303)
    def draw_new_score(self):
        window.itemconfig(self.window_object, text=self.text + str(self.score_points))


# Main menu title class to create the main menu title and instructions
class Main_menu_title:
    def __init__(self, title_x, title_y, title_text, title_fill, title_font):
        self.title_x = title_x
        self.title_y = title_y
        self.title_text = title_text
        self.title_fill = title_fill
        self.title_font = title_font
        self.title_object = window.create_text(title_x, title_y, text=title_text, fill=title_fill, font=title_font)

    # method to remove a main menu title object from the window
    def remove_title(self):
        window.delete(self.title_object)


# Background class to create the building objects, same way as making a rectangle
class Background:
    def __init__(self, building_x1, building_y1, building_x2, building_y2, colour, outline):
        self.building_x1 = building_x1
        self.building_y1 = building_y1
        self.building_x2 = building_x2
        self.building_y2 = building_y2
        self.colour = colour
        self.outline = outline
        self.building_object = window.create_rectangle(building_x1, building_y1, building_x2,
                                                       building_y2, fill=colour, outline=outline)

    # method to create the building windows according to the coordinates of the building
    def windows(self):
        window_height = 0
        window_width = 0
        # 3 rows of two windows each
        for j in range(3):
            for h in range(2):
                window.create_rectangle(self.building_x1 + 25 + window_width, self.building_y1 + 50 + window_height,
                                        self.building_x2 - 125 + window_width, self.building_y2 - 200 + window_height,
                                        fill='black')
                window_width += 100
            window_width = 0
            window_height += 60

    # method to create the building door according to the coordinates of the building
    def building_door(self):
        window.create_rectangle(self.building_x1 + 85, self.building_y1 + 225, self.building_x2 - 90, self.building_y2,
                                fill='brown')


# creating the main menu game title and instruction for the levels, restarting and exiting the game
the_arcanoid = Main_menu_title(400, 50, title_text='THE ARCANOID GAME', title_fill='black',
                               title_font=('Arial Bold', 50))
press_1 = Main_menu_title(400, 350, title_text='Press 1 for level 1', title_fill='blue', title_font=('Arial Bold', 30))
press_2 = Main_menu_title(400, 400, title_text='Press 2 for level 2', title_fill='yellow',
                          title_font=('Arial Bold', 30))
press_r = Main_menu_title(400, 500, title_text='Press r to restart the level', title_fill='orange',
                          title_font=('Arial Bold', 25))
press_x = Main_menu_title(400, 550, title_text='Press x to exit the game', title_fill='purple',
                          title_font=('Arial Bold', 25))

# creating the first hotel with windows and door
hotel_1 = Background(0, 300, 200, 600, 'grey', 'black')
hotel_1.windows()
hotel_1.building_door()
# creating the second hotel with windows and door
hotel_2 = Background(600, 300, 800, 600, 'grey', 'black')
hotel_2.windows()
hotel_2.building_door()

# list where crafts are put when created
drawn_crafts = []
# if more than number of size, crafts are created then the first craft is deleted
size = 1

# craft object
craft = Craft(400, 590, 490, 580, color_of_craft='cyan')
craft.draw_craft()

# center coordinates of the window
x = WIDTH / 2
y = HEIGHT / 2


# function that changes the coordinates of the craft according to x and y, and deletes the new craft object created if
# more than 1
def delete_previous_craft():
    global craft
    craft = Craft(x, y, x + 90, y - 10, color_of_craft='cyan')
    craft_id = craft.window_object
    drawn_crafts.append(craft_id)
    # if crafts created are more than 1 delete the first craft created (reused from ManyCircles.py in week02, step0206)
    if len(drawn_crafts) > size:
        id_of_craft_to_be_deleted = drawn_crafts.pop(0)
        window.delete(id_of_craft_to_be_deleted)


#  function to move the craft according to mouse motion (used from CoordinatesWithTuples.py in week02, step0205)
def move_craft(event):
    global x, y
    # delete the craft you made before
    craft.remove_craft()
    coordinates = (event.x, event.y)
    mouse_x = coordinates[0]
    # assign x to x coordinates of mouse
    x = mouse_x
    # make y stable to height 590
    y = 590
    # restrict the craft x from going less than 0
    if x < 0:
        x = 0
    # restrict craft x from going more than 710 since 90 is its width
    if x > 710:
        x = 710
    # calling delete_previous_craft so that 1 craft is always displayed in the window
    delete_previous_craft()


# bind mouse motion to move_craft function
window.bind('<Motion>', move_craft)

DEFAULT_RADIUS = 10
DEFAULT_SPEED = 7
# ball object for level 1
b_level1 = Ball(WIDTH / 2, HEIGHT / 2, 0, DEFAULT_SPEED, DEFAULT_RADIUS, 'red', ball_outline='black')

# list for level 2 balls
level_2_balls = []

second_ball_xcoord_diff = 0
num_of_balls = 3
speed_diff = 0
height_diff = 0
# for loop to create the balls for level 2 using the above variables (used from TwoBalls.py in week 03, step 0305)
for r in range(1, num_of_balls):
    ball_2 = Ball(300 + second_ball_xcoord_diff, 200 + height_diff, 0, DEFAULT_SPEED + speed_diff,
                  DEFAULT_RADIUS,
                  'red',
                  ball_outline='black')
    second_ball_xcoord_diff = 200
    speed_diff += 2
    height_diff += 50
    level_2_balls.append(ball_2)


# function to detect if there is a collision of q ball with a brick using Pythagoras theorem
def collision_ball_bricks(ball1, brick1):
    distance_x = int((ball1.ball_x - (brick1.brick_left + 20))) ** 2
    distance_y = int((ball1.ball_y - (brick1.brick_top + 10))) ** 2
    distance = int((distance_x + distance_y)) ** 0.5
    if distance <= ball1.radius + 20:
        return True


# creating a ball to make the ufo ships according to these coordinates
ball_for_ufo = Ball(WIDTH / 2, HEIGHT / 2, 0, DEFAULT_SPEED, DEFAULT_RADIUS, 'red', ball_outline='black')
# creating the ufo ship1, cabin 1 and windows according to the ball_for_ufo x and y
ufo_ship1 = Ufo(ball_for_ufo.ball_x, ball_for_ufo.ball_y - 30, 50, 20, ufo_speed_x=3, ufo_speed_y=0, ufo_fill='blue',
                ufo_outline='black')
ufo_cabin1 = Ufo(ball_for_ufo.ball_x, ball_for_ufo.ball_y - 50, 20, 10, ufo_speed_x=3, ufo_speed_y=0, ufo_fill='white',
                 ufo_outline='black')
ufo_window_distance = 0

ufo_windows1 = []
# for loop to make 4 circle windows for the ufo ship, inserting them into the ufo_windows1 list
for i in range(4):
    ufo_window = Ufo(ball_for_ufo.ball_x - 30 + ufo_window_distance, ball_for_ufo.ball_y - 22, 4, 4, ufo_speed_x=3,
                     ufo_speed_y=0,
                     ufo_fill='yellow', ufo_outline='')
    ufo_window_distance += 20
    ufo_windows1.append(ufo_window)

# list for level 2 ufo ships
ufo_ships2 = []
# list for level 2 ufo cabins
ufo_cabins2 = []
# list for level 2 uf windows
ufo_windows2 = []

# nested for-loops to make the level 2 ufo ships, cabins and windows using the x and y coordinated of the level 2
# balls in the level_2_balls list
for k in range(len(level_2_balls)):
    ufo_window_distance = 0
    ufo_ship2 = Ufo(level_2_balls[k].ball_x, level_2_balls[k].ball_y - 30, 50, 20, ufo_speed_x=3, ufo_speed_y=0,
                    ufo_fill='blue', ufo_outline='black')
    ufo_ships2.append(ufo_ship2)
    ufo_cabin2 = Ufo(level_2_balls[k].ball_x, level_2_balls[k].ball_y - 50, 20, 10, ufo_speed_x=3, ufo_speed_y=0,
                     ufo_fill='white',
                     ufo_outline='black')
    ufo_cabins2.append(ufo_cabin2)
    for l in range(4):
        ufo_window2 = Ufo(level_2_balls[k].ball_x - 30 + ufo_window_distance, level_2_balls[k].ball_y - 22, 4, 4,
                          ufo_speed_x=3, ufo_speed_y=0,
                          ufo_fill='yellow', ufo_outline='')
        ufo_window_distance += 20
        ufo_windows2.append(ufo_window2)
    ufo_window_distance = 0

# creating the score object setting the score points to 0
points = 0
score = Score_Board(40, 580, text='Score: ', font=('Arial Bold', 10), colour_fill='white', score_points=points)

# final score object to display the loosing message
final_score = FinalScore(400, 360, text='YOU LOST!!\nPress r to TRY AGAIN\nPress x to EXIT\nFinal Score: ',
                         font=('Arial Bold', 20),
                         colour_fill='', score_points=score.score_points)
# final score object to display the winning message
winning_message = FinalScore(400, 350, text='YOU WON!!!\nPress r to PLAY AGAIN\nPress x to EXIT\nFinal Score: ',
                             font=('Arial Bold', 20),
                             colour_fill='', score_points=score.score_points)
# list for bricks
bricks = []
# x1,y1 cordinates of first brick
initial_brick_width = 2
initial_brick_height = 2
change = 0
# list for colours of bricks for each row
colors_of_bricks = ['red', 'yellow', 'green', 'blue', 'purple']

# boolean variable set to determine if a level is accessed
game_control = False
# variable changing to 1 if level 1 is played and to 2 if level 2 is played
level = 0


# event function for detecting when you press 1 for level 1, 2 for level 2, r or R for repeating the level and x or X
# for exiting the game (used from MoreKeyboardInput.py week02, step0202)
def on_key_press(event):
    global initial_brick_height, level_2_balls, level, game_control, change, initial_brick_width, b_level1, the_arcanoid, \
        press_1, press_2, press_x, score, final_score, bricks
    # level 1
    if event.char == '1' and game_control == False:
        # level changes to 1 and game control becomes true so that when you press 1 again nothing changes
        game_control = True
        level = 1
        # remove the ball used to make the level1 ufo
        ball_for_ufo.remove()
        # remove title and instructions of main menu
        the_arcanoid.remove_title()
        press_1.remove_title()
        press_2.remove_title()
        press_x.remove_title()
        press_r.remove_title()

        # for-loops to remove the level2 balls and the levels2 ufo ships from the starting window
        for i in range(len(level_2_balls)):
            level_2_balls[i].remove()

        for j in range(len(ufo_ships2)):
            ufo_ships2[j].remove_ufo()

        for c in range(len(ufo_cabins2)):
            ufo_cabins2[c].remove_ufo()

        for n in range(len(ufo_windows2)):
            ufo_windows2[n].remove_ufo()

        # animation level 1 call
        animation_level1()

        # nested for-loops to create 5 rows of 19 bricks per row of different colour
        for i in range(5):
            for j in range(19):
                initial_brick_width = 2
                brick = Brick(initial_brick_width + change, initial_brick_height, 40 + initial_brick_width + change,
                              20 + initial_brick_height, colors_of_bricks[i])
                bricks.append(brick)
                change += 42
            initial_brick_height += 22
            change = 0
    # if statement for repeating level 1
    if (event.char == 'r' or event.char == 'R') and game_control == True and level == 1:
        # ball coordinates and x,y speeds are changed to starting ones
        b_level1.ball_x = 400
        b_level1.ball_y = 290
        b_level1.speed_x = 0
        b_level1.speed_y = 7

        # final score text is removed and points changed to zero
        final_score.remove_final_score()
        final_score.score_points = 0
        score.score_points = 0
        # score in the bottom-left corner is updated
        score.draw_new_score()
        # winning message text is removed and points changed to zero
        winning_message.remove_final_score()
        winning_message.score_points = 0

        # for-loop to remove the bricks left
        for k in range(0, len(bricks)):
            bricks[k].remove_brick()
            bricks[k].brick_left += 1000

        change = 0
        initial_brick_height = 2
        # nested for-loops to make new rows of bricks
        for i in range(5):
            for j in range(19):
                initial_brick_width = 2
                brick = Brick(initial_brick_width + change, initial_brick_height, 40 + initial_brick_width + change,
                              20 + initial_brick_height, colors_of_bricks[i])
                bricks.append(brick)
                change += 42
            initial_brick_height += 22
            change = 0
    # level 2
    if event.char == '2' and game_control == False:
        # game control changes to True and level to 2 so that when you press 2 again nothing happens
        game_control = True
        level = 2
        # remove main menu title and instructions
        the_arcanoid.remove_title()
        press_1.remove_title()
        press_2.remove_title()
        press_x.remove_title()
        press_r.remove_title()
        # remove level 1 ball
        b_level1.remove()
        # remove ball used to make level 1 ufo
        ball_for_ufo.remove()
        # remove level 1 ufo ship, cabin and windows
        ufo_ship1.remove_ufo()
        ufo_cabin1.remove_ufo()
        for j in range(len(ufo_windows1)):
            ufo_windows1[j].remove_ufo()

        # call for level 2 animation function
        animation_level2()

        # nested for-loops to create 5 rows of 19 bricks per row of different colour
        for i in range(5):
            for j in range(19):
                initial_brick_width = 2
                brick = Brick(initial_brick_width + change, initial_brick_height, 40 + initial_brick_width + change,
                              20 + initial_brick_height, colors_of_bricks[i])
                bricks.append(brick)
                change += 42
            initial_brick_height += 22
            change = 0
    # if statement for repeating level 2
    if (event.char == 'r' or event.char == 'R') and game_control == True and level == 2:

        second_ball_xcoord_diff_repeat = 0
        height_diff_repeat = 0
        speed_diff_repeat = 0
        #  for loop for returning the two balls to their starting positions
        for i in range(len(level_2_balls)):
            level_2_balls[i].ball_x = 300 + second_ball_xcoord_diff_repeat
            level_2_balls[i].ball_y = 190 + height_diff_repeat
            level_2_balls[i].speed_x = 0
            level_2_balls[i].speed_y = DEFAULT_SPEED + speed_diff_repeat
            second_ball_xcoord_diff_repeat += 200
            height_diff_repeat += 50
            speed_diff_repeat += 2

        # final score text is removed and points changed to zero
        final_score.remove_final_score()
        score.score_points = 0
        final_score.score_points = 0
        # score in the bottom-left corner is updated
        score.draw_new_score()
        # winning message text removed and points changed to zero
        winning_message.remove_final_score()
        winning_message.score_points = 0

        # for loop to remove the bricks left
        for k in range(0, len(bricks)):
            bricks[k].remove_brick()
            bricks[k].brick_left += 1000

        change = 0
        initial_brick_height = 2
        # nested for-loops to make new bricks
        for i in range(5):
            for j in range(19):
                initial_brick_width = 2
                brick = Brick(initial_brick_width + change, initial_brick_height, 40 + initial_brick_width + change,
                              20 + initial_brick_height, colors_of_bricks[i])
                bricks.append(brick)
                change += 42
            initial_brick_height += 22
            change = 0
    # exiting the game
    if event.char == 'x' or event.char == 'X':  # handle small or capital X
        quit()


arcanoid.bind('<KeyPress>', on_key_press)

# list for the trail of balls
shadow_balls = []


# animation function for level 1 (used from Collisions.py week03, step 0306)
def animation_level1():
    global craft, bricks, points, score, shadow_balls, b, final_score
    # ball moves and the coordinates are updated
    b_level1.move()
    b_level1.draw()

    # shadow ball has the same coordinates as the ball in the levels, we just make the radius less
    shadow = Ball(b_level1.ball_x, b_level1.ball_y, b_level1.speed_x, b_level1.speed_y, 3, b_level1.color, '')
    shadow_id = shadow.canvas_object
    shadow_balls.append(shadow_id)
    # we put the shadow balls in a list until length is more than 7 and then the next one created is always removed
    # from the window (ManyCircles.py week02, step0206)
    if len(shadow_balls) > 7:
        delete_shadow = shadow_balls.pop(0)
        window.delete(delete_shadow)
    # if statement if the ball touches the lowest point on the window it stops and the loosing message with the final
    # score appears
    if b_level1.ball_y + b_level1.radius >= HEIGHT:
        b_level1.speed_x = 0
        b_level1.speed_y = 0
        final_score.change_score_colour('red')
    # check if the ball hits the top of the craft and it is within its width
    if b_level1.ball_y + b_level1.radius >= craft.bottom and craft.left <= b_level1.ball_x <= craft.right:
        b_level1.speed_y = -abs(b_level1.speed_y)
        # nested if statements to assign different speed.x to the ball according to where it hits the craft
        # most right point
        if b_level1.ball_x >= craft.left + 72:
            b_level1.speed_x = 10
        # intermediate right point
        elif b_level1.ball_x >= craft.left + 54:
            # speed is assigned to a random number between 2, 8
            b_level1.speed_x = randint(2, 8)
        # middle point
        elif b_level1.ball_x >= craft.left + 36:
            b_level1.speed_x = 0
        # intermediate left point
        elif b_level1.ball_x >= craft.left + 18:
            # speed is assigned to a random number between 2, 8
            b_level1.speed_x = randint(-8, -2)
        # most left point
        elif b_level1.ball_x >= craft.left:
            b_level1.speed_x = -10
    # for-loop for detecting collision of the ball with the bricks
    for num in range(0, len(bricks)):
        if collision_ball_bricks(b_level1, bricks[num]):
            # nested if statements to change the speed x of the ball when it hits left or right of the brick
            if b_level1.ball_x <= bricks[num].brick_left:
                b_level1.speed_x = -b_level1.speed_x
            elif b_level1.ball_x >= bricks[num].brick_right:
                b_level1.speed_x = -b_level1.speed_x
            # if the ball hits anywhere else than left or right then change the y speed
            else:
                b_level1.speed_y = -b_level1.speed_y
            # when collision happens remove a brick
            bricks[num].remove_brick()
            # make the bricks.left coordinate +1000 so it leaves the window
            bricks[num].brick_left += 1000
            # points are increased by 10
            score.score_points += 10
            # score is updated
            score.draw_new_score()
            # if the score points reach 950 then change the colour of the winning message to red and display it
            if score.score_points == 950:
                winning_message.change_score_colour('red')
                # stop the ball
                b_level1.speed_x = 0
                b_level1.speed_y = 0

    window.after(DELAY, animation_level1)


# list for trail of balls of level 2
level_2_shadows = []


# animation function for level 2 (used from Collisions.py week03, step 0306)
def animation_level2():
    global craft, bricks, level_2_balls, score, level_2_shadows
    # ball moves and the coordinates are updated
    for i in range(len(level_2_balls)):
        level_2_balls[i].move()
        level_2_balls[i].draw()
        # shadow balls following the two balls of level 2
        shadow = Ball(level_2_balls[i].ball_x, level_2_balls[i].ball_y, level_2_balls[i].speed_x,
                      level_2_balls[i].speed_y, 3, level_2_balls[i].color, '')
        shadow_id = shadow.canvas_object
        # insert the shadows into the list
        level_2_shadows.append(shadow_id)
        # check if the list's length is more than 15, then delete the first shadow created
        # (ManyCircles.py week02, step0206)
        if len(level_2_shadows) > 15:
            delete_shadow_2 = level_2_shadows.pop(0)
            window.delete(delete_shadow_2)
        # check if one of the balls hits the lowest y point in the window, then make both of them stop
        if level_2_balls[i].ball_y + level_2_balls[i].radius >= HEIGHT:
            level_2_balls[i].speed_x = 0
            level_2_balls[i].speed_y = 0
            level_2_balls[i - 1].speed_x = 0
            level_2_balls[i - 1].speed_y = 0
            # display loosing message and final score
            final_score.change_score_colour('red')
        # check if the other ball hits the lowest y point of the window and do the same
        if level_2_balls[i - 1].ball_y + level_2_balls[i].radius >= HEIGHT:
            level_2_balls[i - 1].speed_y = 0
            level_2_balls[i - 1].speed_x = 0
            level_2_balls[i].speed_x = 0
            level_2_balls[i].speed_y = 0
            final_score.change_score_colour('red')
        # check for collision with the craft as done in animation level 1 but now we use indexes of the
        # level_2_balls list
        if level_2_balls[i].ball_y + level_2_balls[i].radius >= craft.bottom and craft.left <= level_2_balls[
            i].ball_x <= craft.right:
            level_2_balls[i].speed_y = -abs(level_2_balls[i].speed_y)
            if level_2_balls[i].ball_x >= craft.left + 72:
                level_2_balls[i].speed_x = 10
            elif level_2_balls[i].ball_x >= craft.left + 54:
                level_2_balls[i].speed_x = randint(2, 8)
            elif level_2_balls[i].ball_x >= craft.left + 36:
                level_2_balls[i].speed_x = 0
            elif level_2_balls[i].ball_x >= craft.left + 18:
                level_2_balls[i].speed_x = randint(-8, -2)
            elif level_2_balls[i].ball_x >= craft.left:
                level_2_balls[i].speed_x = -10
        # for-loop with nested if statements to check collisions of the two balls with bricks
        for num in range(0, len(bricks)):
            # change speed x if the collision is left or right, otherwise change speed y
            if collision_ball_bricks(level_2_balls[i], bricks[num]):

                if level_2_balls[i].ball_x <= bricks[num].brick_left:
                    level_2_balls[i].speed_x = -level_2_balls[i].speed_x
                elif level_2_balls[i].ball_x >= bricks[num].brick_right:
                    level_2_balls[i].speed_x = -level_2_balls[i].speed_x
                else:
                    level_2_balls[i].speed_y = -level_2_balls[i].speed_y
                # remove brick, change brick's position to go out of th window
                bricks[num].remove_brick()
                bricks[num].brick_left += 1000
                score.score_points += 10
                # update score
                score.draw_new_score()
                # if points reach 950 display winning message and make the balls stop
                if score.score_points == 950:
                    winning_message.change_score_colour('red')
                    for i in range(len(level_2_balls)):
                        level_2_balls[i].speed_x = 0
                        level_2_balls[i].speed_y = 0
                        level_2_balls[i - 1].speed_x = 0
                        level_2_balls[i - 1].speed_y = 0

    window.after(DELAY, animation_level2)


arcanoid.mainloop()
