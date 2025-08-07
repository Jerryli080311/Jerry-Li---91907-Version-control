# Author: Jerry Li
# Date: 2/5/2025
# Purpose: Design and develop an math quiz program to help students improve their mathematical skills through interactive learning.

# Import libraries needed to run the program
import os 
import sys 
import math 
import pygame 
import tkinter as tk 
from tkinter import * 
import tkinter.messagebox as messagebox 
import random 
import json 



# Set the width and the height of the game window
Width = 623
Height = 300

# Set constant for ranking window background colour
RANKING_BG_COLOR = "#cceaf6"

# Declare global variables
basic_level_ranking = "rankings_basic.json" 
moderate_level_ranking = "rankings_moderate.json" 
advanced_level_ranking = "rankings_advanced.json" 

# Create a class for the character   
class Character: 
   # Create initialised properties for the character
   def __init__(self):
       self.width = 44 
       self.height = 44 
       self.xPos = 10 
       self.yPos  = Height - self.height - 65 
       self.image_num = 0 
       self.onground = True 
       self.jumping = False 
       self.falling = False 
       self.fall_stop = self.yPos 
       self.velocity = 0 
       self.gravity = 0.5 
       self.initial_velocity = -10 
       self.set_texture() 
       self.show() 

   # Update the character's velocity and image
   def update(self, loops):
       # Check if the character is not on the ground
       if not self.onground: 
           # Let character stop at ground level and set vertical velocity to 0
           self.velocity += self.gravity 
           self.yPos += self.velocity 
           if self.yPos >= Height - self.height - 65: 
               self.yPos = Height - self.height - 65 
               self.velocity = 0 
               self.onground = True 
       # Update the image of the charatcer based on loops
       elif loops % 8 == 0: 
           self.image_num = (self.image_num + 1) % 3 
           self.set_texture() 

   # Load the image of the character
   def set_texture(self):
       path = os.path.join(f'assets/Images/Noob{self.image_num + 1}.png') 
       image = pygame.image.load(path)
       self.texture = pygame.transform.scale(image, (self.width, self.height)) 

   # Show the character on the screen
   def show(self):
      screen.blit(self.texture, (self.xPos, self.yPos)) 

   # The property of the character when jumping
   def jump(self):
       if self.onground: 
           self.velocity = self.initial_velocity 
           self.onground = False 

# Create a class for the background
class BG:
   # Create inisilised properties for the background
   def __init__(self, x):
       self.width = Width 
       self.height = Height 
       self.xPos = x 
       self.yPos = 0 
       self.image() 

   # Update new position of the background
   def update(self, dx):
       self.xPos += dx 
       if self.xPos <= -self.width: 
           self.xPos += Width * 2 

# Load the image of the background
   def image(self):
       path = os.path.join('assets/Images/BG.png') 
       image = pygame.image.load(path) 
       self.image = pygame.transform.scale(image, (self.width, self.height)) 

   # Show the background on the screen 
   def show(self):
       screen.blit(self.image, (int(self.xPos), int(self.yPos))) 

   
# Create a class for the obstacle
class Obstacle:
   # Create inisilised properties for the obstacle
   def __init__(self, x, value):
       self.width = 34 
       self.height = 34 
       self.xPos = x 
       self.yPos = Height - self.height - 70
       self.value = value 
       self.font = pygame.font.SysFont('Press Start 2P', 14) 
       self.load_image() 
       self.show() 

   # Update the position of the obstacle
   def update(self, dx):
       self.xPos += dx 

   # Show the obstacle on the screen based on updated position
   def show(self):
       screen.blit(self.texture, (self.xPos, self.yPos)) 
       text = self.font.render(str(self.value), 1, (0, 0, 0)) 
       text_position = text.get_rect(center=(self.xPos + self.width // 2, self.yPos - 10)) 
       screen.blit(text, text_position) 

   # Load the image of the obstacle
   def load_image(self):
       path = os.path.join('assets/Images/wood.png') 
       img = pygame.image.load(path)
       self.texture = pygame.transform.scale(img, (self.width, self.height)) 

# Create a class for the collision
class Collision:
   # Calculate the distance between two object and determine if they are colliding
   def collision(self, obj1, obj2):
        distance = math.sqrt((obj1.xPos - obj2.xPos) ** 2 + (obj1.yPos - obj2.yPos) ** 2)
        return distance < 25 

# Create a class for the score
class Score:
   # Create inisilised properties for the score
   def __init__(self):
       self.current_score = 0 
       self.font = pygame.font.SysFont('Press Start 2P', 10) 
       self.text_color = (0, 0, 0)
       self.show() 

   # Show the score on the screen
   def show(self):
       self.score = self.font.render(f' Score : {self.current_score}', 1, self.text_color) 
       score_width = self.score.get_rect().width 
       screen.blit(self.score, (Width - score_width - 10, 10)) 

# Create a class for the question
class Question:
   # Create inisilised properties for the question
   def __init__(self):
       self.font = pygame.font.SysFont('Press Start 2P', 14) 
       self.level = "basic" 
       self.generate_question() 

   # Generate a random question based on the level
   def generate_question(self):
       # If basic level
       if self.level == "basic":
           # Randomly select question type
           question_type = random.randint(1, 4) 
           if question_type == 1:
                # Addition
               rand_num1 = random.randint(1, 20)
               rand_num2 = random.randint(1, 20)
               self.answer = rand_num1 + rand_num2
                # Create question text and instruction text
               self.question_text = str(rand_num1) + " + " + str(rand_num2)
               self.instruction_text = "Calculate the result"
           elif question_type == 2:
               rand_num1 = random.randint(2, 20)
               rand_num2 = random.randint(1, rand_num1 - 1)
               self.answer = rand_num1 - rand_num2
                # Create question text and instruction text
               self.question_text = str(rand_num1) + " - " + str(rand_num2)
               self.instruction_text = "Calculate the result"
           elif question_type == 3:
               rand_num1 = random.randint(1, 10)
               rand_num2 = random.randint(1, 10)
               self.answer = rand_num1 * rand_num2
                # Create question text and instruction text
               self.question_text = str(rand_num1) + " × " + str(rand_num2)
               self.instruction_text = "Calculate the result"
           else:
               rand_num1 = random.randint(1, 10) 
               rand_num2 = random.randint(1, 10) 
               dividend = rand_num1 * rand_num2
               self.answer = rand_num2
                # Create question text and instruction text
               self.question_text = str(dividend) + " ÷ " + str(rand_num1)
               self.instruction_text = "Calculate the result"
       
       # If the difficulty is moderate
       elif self.level == "moderate":
           # Use a random number to determine the type of question
           question_type = random.randint(1, 3)
           if question_type == 1:
               # Simple linear equation
               # With random to generate the sign of the eequation
               sign = random.randint(1, 2)
               if sign == 1:
                    # The equation is ax + b = c
                    x_value = random.randint(1, 10) 
                    rand_num1 = random.randint(1, 10) 
                    rand_num2 = random.randint(1, 10) 
                    RHS = rand_num1 * x_value + rand_num2
                    self.answer = x_value
                     # Create question text and instruction text
                    self.question_text = str(rand_num1)+ "x" + " + " + str(rand_num2) + " = " + str(RHS)
                    self.instruction_text = "Solve for x"
               else:
                    # The equation is ax - b = c
                    x_value = random.randint(1, 10) 
                    rand_num1 = random.randint(1, 10) 
                    rand_num2 = random.randint(1, 10) 
                    RHS = rand_num1 * x_value - rand_num2
                    self.answer = x_value
                    # Create question text and instruction text
                    self.question_text = str(rand_num1)+ "x" + " - " + str(rand_num2) + " = " + str(RHS)
                    self.instruction_text = "Solve for x"
              
               
           elif question_type == 2:
                # Find the median of three numbers
                # Generate three random numbers， if any numbers are the same, regenerate
                rand_num1 = random.randint(1, 10)
                rand_num2 = random.randint(1, 10)
                rand_num3 = random.randint(1, 10)
               
                while rand_num2 == rand_num1:
                   rand_num2 = random.randint(1, 10)
                while rand_num3 == rand_num1 or rand_num3 == rand_num2:
                   rand_num3 = random.randint(1, 10)
               
                # Calculate the median number
                if rand_num1 >= rand_num2 and rand_num2 >= rand_num3:
                   self.answer = rand_num2
                elif rand_num1 >= rand_num3 and rand_num3 >= rand_num2:
                    self.answer = rand_num3
                elif rand_num2 >= rand_num1 and rand_num1 >= rand_num3:
                    self.answer = rand_num1
                elif rand_num2 >= rand_num3 and rand_num3 >= rand_num1:
                    self.answer = rand_num3
                elif rand_num3 >= rand_num1 and rand_num1 >= rand_num2:
                    self.answer = rand_num1
                else:
                    self.answer = rand_num2
                # Create question text and instruction text
                self.question_text = "Find the median of " + str(rand_num1) + "," + str(rand_num2) + "," + str(rand_num3)
                self.instruction_text = "Find the middle number"
           
           elif question_type == 3:
               # Find the highest common factor of two numbers
               rand_num1 = random.randint(1, 20)
               rand_num2 = random.randint(1, 20)
               a_value = rand_num1
               b_value = rand_num2
               # Calculate the highest common factor of the two numbers
               while b_value != 0:
                   temp = b_value
                   b_value = a_value % b_value
                   a_value = temp
               self.answer = a_value
               # Create question text and instruction text
               self.question_text = "Find the HCF of " + str(rand_num1) + " and " + str(rand_num2)
               self.instruction_text = "Find the Highest Common Factor"
      
       # If advanced level
       elif self.level == "advanced":
           # Use a random number to determine the type of question
           question_type = random.randint(1, 3) 
           if question_type == 1:
                # Find the derivative of a linear function
                # With random to generate the sign of the function
                question_sign = random.randint(1, 2)
                if question_sign == 1:
                    # The function is f(x) = ax + b
                    rand_num1 = random.randint(1, 8)
                    rand_num2 = random.randint(1, 10)
                    self.answer = rand_num1 
                    # Create question text and instruction text
                    self.question_text = "f(x) = " + str(rand_num1) + "x" + " + " + str(rand_num2)
                    self.instruction_text = "Solve for dy/dx"
                else:
                    # The function is f(x) = ax - b
                    rand_num1 = random.randint(1, 8)
                    rand_num2 = random.randint(1, 10)
                    self.answer = rand_num1
                    # Create question text and instruction text
                    self.question_text = "f(x) = " + str(rand_num1) + "x" + " - " + str(rand_num2)
                    self.instruction_text = "Solve for dy/dx"
           
           elif question_type == 2:
                # Find the derivative of a quadratic function
                # With random to generate the first sign of the function
                question_sign = random.randint(1, 2)
                if question_sign == 1:
                    # Generate the second sign of the function
                    question_sign2 = random.randint(1, 2)
                    if question_sign2 == 1:
                        # The function is f(x) = ax^2 + bx + c
                        rand_num1 = random.randint(1, 10)
                        rand_num2 = random.randint(1, 10)
                        rand_num3 = random.randint(1, 10)
                        x_value = random.randint(1, 10) 
                        self.answer = 2 * rand_num1 * x_value + rand_num2
                        # Create question text and instruction text
                        self.question_text = "f(x) = " + str(rand_num1) + "x^2" + " + " + str(rand_num2) + "x" + " + " + str(rand_num3)
                        self.instruction_text = "find dy/dx at x = " + str(x_value)
                    else:
                        # The function is f(x) = ax^2 + bx - c
                        rand_num1 = random.randint(1, 10)
                        rand_num2 = random.randint(1, 10)
                        rand_num3 = random.randint(1, 10)
                        x_value = random.randint(1, 10) 
                        self.answer = 2 * rand_num1 * x_value + rand_num2
                        # Create question text and instruction text
                        self.question_text = "f(x) = " + str(rand_num1) + "x^2" + " + " + str(rand_num2) + "x" + " - " + str(rand_num3)
                        self.instruction_text = "find dy/dx at x = " + str(x_value)
                else:
                    # Generate the second sign of the function
                    question_sign2 = random.randint(1, 2)
                    if question_sign2 == 1:
                        # The function is f(x) = ax^2 - bx + c
                        rand_num1 = random.randint(1, 10)
                        rand_num2 = random.randint(1, 10)
                        rand_num3 = random.randint(1, 10)
                        x_value = random.randint(1, 10) 
                        self.answer = 2 * rand_num1 * x_value - rand_num2
                        # Create question text and instruction text
                        self.question_text = "f(x) = " + str(rand_num1) + "x^2" + " - " + str(rand_num2) + "x" + " + " + str(rand_num3)
                        self.instruction_text = "find dy/dx at x = " + str(x_value)
                    else:
                        # The function is f(x) = ax^2 - bx - c
                        rand_num1 = random.randint(1, 10)
                        rand_num2 = random.randint(1, 10)
                        rand_num3 = random.randint(1, 10)
                        x_value = random.randint(1, 10) 
                        self.answer = 2 * rand_num1 * x_value - rand_num2
                        # Create question text and instruction text
                        self.question_text = "f(x) = " + str(rand_num1) + "x^2" + " - " + str(rand_num2) + "x" + " - " + str(rand_num3)
                        self.instruction_text = "find dy/dx at x = " + str(x_value)
                    
                    
           elif question_type == 3 :
                # Find the derivative of a cubic function
                # With random to generate the first sign of the function
                question_sign1 = random.randint(1, 2)
                if question_sign1 == 1:
                    # Generate the second sign of the function
                    question_sign2 = random.randint(1, 2)
                    if question_sign2 == 1:
                        # Generate the third sign of the function
                        question_sign3 = random.randint(1, 2)
                        if question_sign3 == 1:
                            # The function is f(x) = ax^3 + bx^2 + cx + d
                            first_num = random.randint(1, 5)
                            second_num = random.randint(1, 5)
                            third_num = random.randint(1, 5)
                            fourth_num = random.randint(1, 5)
                            x_value = random.randint(1, 5) 
                            x_squared = x_value * x_value
                            self.answer = 3 * first_num * x_squared + 2 * second_num * x_value + third_num
                            # Create question text and instruction text
                            self.question_text = "f(x) = " + str(first_num) + "x^3" + " + " + str(second_num) + "x^2" + " + " + str(third_num) + "x" + " + " + str(fourth_num)
                            self.instruction_text = "find dy/dx at x = " + str(x_value)
                        else:
                            # The function is f(x) = ax^3 + bx^2 + cx - d
                            first_num = random.randint(1, 5)
                            second_num = random.randint(1, 5)
                            third_num = random.randint(1, 5)
                            fourth_num = random.randint(1, 5)
                            x_value = random.randint(1, 5) 
                            x_squared = x_value * x_value
                            self.answer = 3 * first_num * x_squared + 2 * second_num * x_value + third_num
                            # Create question text and instruction text
                            self.question_text = "f(x) = " + str(first_num) + "x^3" + " + " + str(second_num) + "x^2" + " + " + str(third_num) + "x" + " - " + str(fourth_num)
                            self.instruction_text = "find dy/dx at x = " + str(x_value)
                    else:
                        # Generate the third sign of the function
                        question_sign3 = random.randint(1, 2)
                        if question_sign3 == 1:
                            # The function is f(x) = ax^3 + bx^2 - cx + d
                            first_num = random.randint(1, 5)
                            second_num = random.randint(1, 5)
                            third_num = random.randint(1, 5)
                            fourth_num = random.randint(1, 5)
                            x_value = random.randint(1, 5) 
                            x_squared = x_value * x_value
                            self.answer = 3 * first_num * x_squared + 2 * second_num * x_value - third_num
                            # Create question text and instruction text
                            self.question_text = "f(x) = " + str(first_num) + "x^3" + " + " + str(second_num) + "x^2" + " - " + str(third_num) + "x" + " + " + str(fourth_num)
                            self.instruction_text = "find dy/dx at x = " + str(x_value)
                            
                        else:
                            # The function is f(x) = ax^3 + bx^2 - cx - d
                            first_num = random.randint(1, 5)
                            second_num = random.randint(1, 5)
                            third_num = random.randint(1, 5)
                            fourth_num = random.randint(1, 5)
                            x_value = random.randint(1, 5) 
                            x_squared = x_value * x_value
                            self.answer = 3 * first_num * x_squared + 2 * second_num * x_value - third_num
                            # Create question text and instruction text
                            self.question_text = "f(x) = " + str(first_num) + "x^3" + " + " + str(second_num) + "x^2" + " - " + str(third_num) + "x" + " - " + str(fourth_num)
                            self.instruction_text = "find dy/dx at x = " + str(x_value)
                else:
                    # Generate the second sign of the function
                    question_sign2 = random.randint(1, 2)
                    if question_sign2 == 1:
                        # Generate the third sign of the function
                        question_sign3 = random.randint(1, 2)
                        if question_sign3 == 1:
                            # The function is f(x) = ax^3 - bx^2 + cx + d
                            first_num = random.randint(1, 10)
                            second_num = random.randint(1, 10)
                            third_num = random.randint(1, 10)
                            fourth_num = random.randint(1, 10)
                            x_value = random.randint(1, 10) 
                            x_squared = x_value * x_value
                            self.answer = 3 * first_num * x_squared - 2 * second_num * x_value + third_num
                            # Create question text and instruction text
                            self.question_text = "f(x) = " + str(first_num) + "x^3" + " - " + str(second_num) + "x^2" + " + " + str(third_num) + "x" + " + " + str(fourth_num)
                            self.instruction_text = "find dy/dx at x = " + str(x_value)
                        else:
                            # The function is f(x) = ax^3 - bx^2 + cx - d
                            first_num = random.randint(1, 10)
                            second_num = random.randint(1, 10)
                            third_num = random.randint(1, 10)
                            fourth_num = random.randint(1, 10)
                            x_value = random.randint(1, 10) 
                            x_squared = x_value * x_value
                            self.answer = 3 * first_num * x_squared - 2 * second_num * x_value + third_num
                            # Create question text and instruction text
                            self.question_text = "f(x) = " + str(first_num) + "x^3" + " - " + str(second_num) + "x^2" + " + " + str(third_num) + "x" + " - " + str(fourth_num)
                            self.instruction_text = "find dy/dx at x = " + str(x_value)
                    else:
                        # Generate the third sign of the function
                        question_sign3 = random.randint(1, 2)
                        if question_sign3 == 1:
                            # The function is f(x) = ax^3 - bx^2 - cx + d
                            first_num = random.randint(1, 10)
                            second_num = random.randint(1, 10)
                            third_num = random.randint(1, 10)
                            fourth_num = random.randint(1, 10)
                            x_value = random.randint(1, 10) 
                            x_squared = x_value * x_value
                            self.answer = 3 * first_num * x_squared - 2 * second_num * x_value - third_num
                            # Create question text and instruction text
                            self.question_text = "f(x) = " + str(first_num) + "x^3" + " - " + str(second_num) + "x^2" + " - " + str(third_num) + "x" + " + " + str(fourth_num)
                            self.instruction_text = "find dy/dx at x = " + str(x_value)
                            
                        else:
                            # The function is f(x) = ax^3 - bx^2 - cx - d
                            first_num = random.randint(1, 10)
                            second_num = random.randint(1, 10)
                            third_num = random.randint(1, 10)
                            fourth_num = random.randint(1, 10)
                            x_value = random.randint(1, 10) 
                            x_squared = x_value * x_value
                            self.answer = 3 * first_num * x_squared - 2 * second_num * x_value - third_num
                            # Create question text and instruction text
                            self.question_text = "f(x) = " + str(first_num) + "x^3" + " - " + str(second_num) + "x^2" + " - " + str(third_num) + "x" + " - " + str(fourth_num)
                            self.instruction_text = "find dy/dx at x = " + str(x_value)



   # Show the question and the instruction text
   def show(self):
       question_text = self.font.render(self.question_text, 1, (0, 0, 0))
       instruction_font = pygame.font.SysFont('Press Start 2P', 10)
       instruction_text = instruction_font.render(self.instruction_text, 1, (0, 0, 0))
       screen.blit(question_text, (Width // 2 - question_text.get_width() // 2, 20))
       screen.blit(instruction_text, (Width // 2 - instruction_text.get_width() // 2, 50))

# Create a class for the game
class Game:
   # Create inisilised properties for the game
   def __init__(self, level):
       self.bg = [BG(x=0), BG(x=Width)] 
       self.character = Character() 
       self.obstacles = [] 
       self.collision = Collision() 
       self.score = Score() 
       self.speed = 3 
       self.playing = False 
       self.question = Question() 
       self.question.level = level
       self.question.generate_question() 
       self.correct_ans_prob = 0.3 
       self.incorr_ans_count = 0 
       self.guaranteed_num = 3 
       self.set_labels()
      
   # Set the labels for the game
   def set_labels(self):
       big_font = pygame.font.SysFont('Press Start 2P', 14, bold=True)
       small_font = pygame.font.SysFont('Press Start 2P', 10)
       self.big_lbl_over = big_font.render(f'G A M E O V E R', 1, (0, 0, 0))
       self.ranking_lbl = small_font.render(f'Press R to view rankings', 1, (0, 0, 0))
       self.Start_lbl= big_font.render(f'Press Space to Start', 1, (0, 0, 0))

   # Condition to start the game
   def start(self):
       self.playing = True

   # Condition to end the game
   def over(self):
       screen.blit(self.big_lbl_over, (Width // 2 - self.big_lbl_over.get_width() // 2, Height // 3))
       screen.blit(self.ranking_lbl, (Width // 2 - self.ranking_lbl.get_width() // 2, Height // 2))
       self.playing = False

   # Call ranking window function show the ranking window
   def show_ranking_window(self):
       show_ranking_window(player_name, self.score.current_score, self.question.level)

   # Show the start label
   def Show_start_lbl(self):
       screen.blit(self.Start_lbl, (Width // 2 - self.Start_lbl.get_width() // 2, Height // 4))

   # Create a function to decide when to create the obstacle
   def tospawn(self, loops):
       return loops % 100 == 0

   # Create a function to create the obstacle
   def spawn_obstacle(self):
       create_correct_ans = False
      
       # If the number of obstacles created with incorrect answer is equal to the guaranteed number, the next obstacle must be with the correct answer
       if self.incorr_ans_count >= self.guaranteed_num:
           create_correct_ans = True 
       else:
           # Generate a random number between 0 and 1
           rand_num = random.random()
           # If the random number is less than the correct answer probability, the next obstacle must be with the correct answer
           if rand_num < self.correct_ans_prob:
               create_correct_ans = True
           # If the random number is greater than the correct answer probability, the next obstacle must be with the incorrect answer
           else:
               create_correct_ans = False
      
       # Get the correct answer from the question class
       correct_ans = self.question.answer
       
       # Generate the range of incorrect answers, the range is from correct answer - 2 to correct answer + 2
       min_incorr = correct_ans - 2
       max_incorr = correct_ans + 2
      
       # Generate the list of incorrect answers
       incorr_options = []
       for num in range(min_incorr, max_incorr + 1):
           if num != correct_ans:
               incorr_options.append(num)
       # Randomly decide how many obstacles to be created
       num_obs = random.randint(1, 3)
        # Go through each obstacle
       for i in range(num_obs):
           # Check if there are already obstacles exist
           if len(self.obstacles) > 0:
               # Get the last obstacle that was created
               last_obstacle = self.obstacles[-1]
               # Create new one after the last on 
               x = random.randint(last_obstacle.xPos + self.character.width + 84,
                                  Width + last_obstacle.xPos + self.character.width + 84)
           else:
               # Otherwise, randomly generate from the right
               x = random.randint(Width + 100, 1000)
          
           # What value to put on top of the obstacle
           if create_correct_ans: 
               value = correct_ans
               create_correct_ans = False 
           else:
               rand_index = random.randint(0, len(incorr_options) - 1)
               value = incorr_options[rand_index]
          
           # Create obstacles with value
           obst = Obstacle(x=x, value=value)
           self.obstacles.append(obst)
      
       # Check if we successfully created an obstacle with the correct answer
       correct_ans_spawned = False
       start_index = len(self.obstacles) - num_obs  
       for j in range(start_index, len(self.obstacles)):
           obst = self.obstacles[j]
           if obst.value == correct_ans:
               correct_ans_spawned = True
               break
      
       # Update the probability
       if correct_ans_spawned == True:
           # If correct answer was created, reset the count and probability
           self.incorr_ans_count = 0
           self.correct_ans_prob = 0.3
       else:
           # If no correct answer was created, increase the probability for next time
           self.incorr_ans_count = self.incorr_ans_count + 1
           new_probability = self.correct_ans_prob + 0.15
           if new_probability > 0.9:
               self.correct_ans_prob = 0.9  
           else:
               self.correct_ans_prob = new_probability

# Run the game
def game_start():
   # Get the selected level and call game class 
   level = game_level
   game = Game(level)
   character = game.character

   # Declarevariables
   clock = pygame.time.Clock()  
   loops = 0                   
   over = False                 

   # Show game background
   for bg in game.bg:
       bg.show()                

   # Show character
   character.show()             
   # Show start label
   game.Show_start_lbl()        

   # Loop until game over
   while True:
       if game.playing:
           loops += 1           

           # Show infinity scrolling background
           for bg in game.bg:
               bg.update(-game.speed)  
               bg.show()               

           # Show animation of character
           character.update(loops)     
           character.show()            
           game.question.show()        

           # Create obstacles
           if game.tospawn(loops):
               game.spawn_obstacle()   

           # Reset probability if user miss the correct answer
           for obstacle in game.obstacles[:]:  
               if obstacle.xPos < -50:    
                   if obstacle.value == game.question.answer:
                       game.incorr_ans_count += 1
                       game.correct_ans_prob = min(0.9, game.correct_ans_prob + 0.2)
                   game.obstacles.remove(obstacle)  
              
           # Show obstacles
           for obstacle in game.obstacles:
               obstacle.update(-game.speed)  
               obstacle.show()               

               # When colliding with the obstacle
               if game.collision.collision(character, obstacle):
                   if obstacle.value == game.question.answer:
                       # Clear obstacle, increase score, generate new question, reset counters, and keep playing
                       game.obstacles.remove(obstacle)           
                       game.score.current_score += 10           
                       game.question.generate_question()        
                       game.obstacles.clear()                   
                       game.incorr_ans_count = 0          
                       game.correct_ans_prob = 0.3    
                       over = False                             
                   else:
                       # Game over
                       over = True

        
           if over:
                # Save user detail to the file
               if player_name:
                   add_score(player_name, game.score.current_score, game.question.level)
               game.over()  

           # Show score
           game.score.show()

       # What happens when user press the certain keys
       for event in pygame.event.get():
           # Close game when user press x on the window
           if event.type == pygame.QUIT:
               pygame.quit()    
               sys.exit()       
            # Jump when user press space while on ground
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_SPACE:
                   if not over:
                       if character.onground:
                           character.jump()  
                        # Start the game if not already playing
                       if not game.playing:
                           game.start()    

           # Show ranking window when game is over
               if event.key == pygame.K_r and over:
                    game.show_ranking_window()  

       pygame.display.update()  
       clock.tick(80)    

# Main function
def main():
   # Create the main window
   main_window = tk.Tk()
   main_window.title("Math Game")
   main_window.geometry("600x400")
   main_window.resizable(False, False)
  
   # Set background image
   bg_img = tk.PhotoImage(file="assets/Images/Math_Game_bg_Main.png")
   bg_lbl = tk.Label(main_window, image=bg_img)
   bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)
  
   # Set a function to the start game button
   def start_game():
       main_window.withdraw()
       name_window()

   # Create the game instructions window
   def instructions_window():
       game_instructions = tk.Toplevel(main_window)
       game_instructions.title("Instructions")
       game_instructions.geometry("500x400")
       game_instructions.resizable(False, False)

       # Set background image for the instruction window 
       game_instruction_bg = tk.PhotoImage(file="assets/Images/Instruction.png")
       game_instruction_bg_lbl = tk.Label(game_instructions, image=game_instruction_bg)
       game_instruction_bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)
       game_instructions.game_instruction_bg = game_instruction_bg  
       

   # Create start game button for the main window
   start_btn = Button(main_window, text="Start Game", font=("Press Start 2P", 10),command=start_game, width=20, height=2, bg='lightgreen')
   start_btn.place(relx=0.5, rely=0.45, anchor='center')

   # Create instruction button for the main window
   instruction_btn = Button(main_window, text="Instructions", font=("Press Start 2P", 10), command=instructions_window, width=15, height=2, bg='lightyellow')
   instruction_btn.place(relx=0.5, rely=0.6, anchor='center')

   # Create exit button for the main window
   exit_btn = Button(main_window, text="Exit", font=("Press Start 2P", 10), command=main_window.destroy, width=15, height=2, bg='lightcoral')
   exit_btn.place(relx=0.5, rely=0.75, anchor='center')

   # Create the name window
   def name_window():
       name_window = tk.Toplevel()
       name_window.title("Enter Your Name")
       name_window.geometry("600x400")
       name_window.resizable(False, False)
    
       # Set background image 
       name_bg_img = tk.PhotoImage(file="assets/Images/Math_Game_bg_Name.png")
       name_bg_lbl = tk.Label(name_window, image=name_bg_img)
       name_bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)
       name_window.name_bg_img = name_bg_img 
      
       # Create the input field for user to enter their name
       name_input = Entry(name_window, font=("Press Start 2P", 8), width=25)
       name_input.place(relx=0.5, rely=0.45, anchor='center')

       # Create the function for the continue button x
       def continue_button():
           # Send error message if the input is not alphabets
           if not name_input.get().isalpha():
               tk.messagebox.showwarning("Invalid Input", "Please enter only alphabets.")
           else:  
               global player_name
               player_name = name_input.get()
               name_window.destroy()
               difficulty_selection_window()
                           

       # Create the function for the back button for player to return to the main window
       def back_button():
           name_window.destroy()
           main_window.deiconify()

       # Create the continue and back button 
       continue_btn = Button(name_window, text="Continue", font=("Press Start 2P", 10), command=continue_button, width=20, height=2, bg = 'lightgreen')
       continue_btn.place(relx=0.5, rely=0.60, anchor='center')

       back_btn = Button(name_window, text="←", font=("Press Start 2P", 12), command=back_button, width=3, height=1, bg = 'lightyellow')
       back_btn.place(x=20, y=20)

       # Set the focus to the input field
       name_input.focus()

   # Create the difficulty selection window
   def difficulty_selection_window():
       global difficulty_window
       
       difficulty_window = tk.Toplevel()
       difficulty_window.title("Select Difficulty")
       difficulty_window.geometry("600x400")
       difficulty_window.resizable(False, False)
      
       # Set background image 
       difficulty_bg = tk.PhotoImage(file="assets/Images/Math_Game_bg_Difficulty.png")
       difficulty_bg_lbl = tk.Label(difficulty_window, image=difficulty_bg)
       difficulty_bg_lbl.place(relwidth=1, relheight=1)
       difficulty_window.difficulty_bg_img = difficulty_bg 
      
       # Create buttons 
       basic_btn = tk.Button(difficulty_window, text="Basic", font=("Press Start 2P", 10), fg='black', width=15, height=2, command=select_basic, bg='lightgreen')
       basic_btn.place(relx=0.5, rely=0.42, anchor='center')
      
       moderate_btn = tk.Button(difficulty_window, text="Moderate", font=("Press Start 2P", 10), fg='black', width=15, height=2, command=select_moderate, bg='lightyellow')
       moderate_btn.place(relx=0.5, rely=0.57, anchor='center')
      
       advanced_btn = tk.Button(difficulty_window, text="Advanced", font=("Press Start 2P", 10), fg='black', width=15, height=2, command=select_advanced, bg='lightcoral')
       advanced_btn.place(relx=0.5, rely=0.72, anchor='center')
      
       back_btn = tk.Button(difficulty_window, text="←", font=("Press Start 2P", 12), command=back_button_difficulty_window, width=3, height=1, bg = 'lightyellow')
       back_btn.place(x=20, y=20)
  
      # Create the function for the basic button 
   def select_basic():
       difficulty_window.destroy()
       main_window.destroy()
       run_game("basic")
  
   # Create the function for the moderate button 
   def select_moderate():
       difficulty_window.destroy()
       main_window.destroy()
       run_game("moderate")
  
   # Create the function for the advanced button 
   def select_advanced():
       difficulty_window.destroy()
       main_window.destroy()
       run_game("advanced")
  
   # Create the function for the back button for the user to return to the name window
   def back_button_difficulty_window():
       difficulty_window.destroy()
       name_window() 

   main_window.mainloop()       

# Return file based on the level
def Player_rank_file(level):
   if level == "basic":
    return basic_level_ranking
   elif level == "moderate":
    return moderate_level_ranking    
   else:
    return advanced_level_ranking
    
# Read the file and return the data
def Read_rankings_file(level):
   ranking_file = Player_rank_file(level) 
   if os.path.exists(ranking_file):
       f = open(ranking_file, 'r')
       data = json.load(f)
       f.close()
       return data
   return []

# Save the data to the file
def save_rankings(rankings, level):
   file = Player_rank_file(level) 
   opend_file = open(file, 'w')
   json.dump(rankings, opend_file, indent=1)
   opend_file.close()

# Add the score to the file
def add_score(Player_name, Player_score, level):
   rankings = Read_rankings_file(level) 
   found = False
   new_score = {"name": Player_name, "score": Player_score}
   # Check if there is a exact same data in the file
   for entry in rankings: 
        if entry["name"] == Player_name and entry["score"] == Player_score:
            found = True
            break
   # If there is no exact same data, add the new score to the file
   if not found:
       rankings.append(new_score)
   # Sort the data
   num_of_data = len(rankings)
   for i in range(num_of_data):
       for j in range(i + 1, num_of_data):
           if rankings[i]["score"] < rankings[j]["score"]:
               temp = rankings[i]
               rankings[i] = rankings[j]
               rankings[j] = temp
   # Only keep the top 10
   if len(rankings) > 10:   
       top_10 = []
       for x in range(min(10, len(rankings))):
           top_10.append(rankings[x])
       rankings = top_10
   
   save_rankings(rankings, level)
  

# Find out player's rank
def Player_rank(Player_name, Player_score, level):
   rankings = Read_rankings_file(level) 
   list_size = len(rankings)
   for position in range(list_size): 
       current_player = rankings[position]
       player_name_check = current_player["name"]
       player_score_check = current_player["score"]
       
       if player_name_check == Player_name and player_score_check == Player_score: 
           player_rank = position + 1
           return player_rank
   
   return None

# Create the ranking window to display top 10 players
def show_ranking_window(player_name, score, level):
   # Close pygame and switch to tkinter for the ranking window
   pygame.quit()
   
   # Create the main ranking window
   ranking_window = tk.Tk()
   ranking_window.title("Math Game - Rankings")
   ranking_window.geometry("550x650")
   ranking_window.resizable(False, False)
   ranking_window.configure(bg=RANKING_BG_COLOR)  
  

    # Create a main frame for the window
   main_frame = tk.Frame(ranking_window, bg=RANKING_BG_COLOR)
   main_frame.pack(expand=True, fill='both', padx=20, pady=20)
   
   # Create label frame for titles and player info
   lbls_frame = tk.Frame(main_frame, bg=RANKING_BG_COLOR)
   lbls_frame.pack(pady=20)
   
   # Create labels for titles and player info 
   level_text = level.capitalize()
   title_lbl = tk.Label(lbls_frame, text=f" TOP 10 RANKINGS - {level_text.upper()} ",font=("Times New Roman", 24, "bold"), bg=RANKING_BG_COLOR)
   title_lbl.pack(pady=10)
   player_info = tk.Label(lbls_frame, text=f"Player: {player_name} | Score: {score}", font=("Times New Roman", 16, "bold"), bg=RANKING_BG_COLOR)
   player_info.pack(pady=5)
 
   # Show player's rank 
   player_rank = Player_rank(player_name, score, level)
   if player_rank:
       rank_lbl = tk.Label(lbls_frame, text=f"Your Rank: #{player_rank}",font=("Times New Roman", 14, "bold"), fg='green', bg= RANKING_BG_COLOR)
       rank_lbl.pack(pady=5)
  
   # Load rankings data from file
   rankings = Read_rankings_file(level)
   # Create ranking frame for leaderboard
   rankings_frame = tk.Frame(main_frame, bg=RANKING_BG_COLOR)
   rankings_frame.pack(pady=20, fill='both', expand=True)
   # Create frame for  headers
   header_frame = tk.Frame(rankings_frame, bg=RANKING_BG_COLOR)
   header_frame.pack(fill='x', pady=(0, 10))
  
   # Use grid to align the header with the leaderboard
   header_frame.grid_columnconfigure(0, weight=1)  
   header_frame.grid_columnconfigure(1, weight=2)  
   header_frame.grid_columnconfigure(2, weight=1)  
   # Create labels for header 
   tk.Label(header_frame, text="Rank", font=("Times New Roman", 12, "bold"),
           anchor='center', bg=RANKING_BG_COLOR).grid(row=0, column=0, sticky='ew')
   tk.Label(header_frame, text="Player", font=("Times New Roman", 12, "bold"),
           anchor='center', bg=RANKING_BG_COLOR).grid(row=0, column=1, sticky='ew')
   tk.Label(header_frame, text="Score", font=("Times New Roman", 12, "bold"),
           anchor='center', bg=RANKING_BG_COLOR).grid(row=0, column=2, sticky='ew')
  
   # Add a line below the header
   seprate_line = tk.Frame(rankings_frame, height=2, bg='black')
   seprate_line.pack(fill='x', pady=5)
  
   # Create leaderboard
   for i, entry in enumerate(rankings):
       rank_frame = tk.Frame(rankings_frame, bg=RANKING_BG_COLOR)
       rank_frame.pack(fill='x', pady=2)
      
       # Use grid to align with the header
       rank_frame.grid_columnconfigure(0, weight=1)  
       rank_frame.grid_columnconfigure(1, weight=2)  
       rank_frame.grid_columnconfigure(2, weight=1)  
      
       # Highlight current player
       if entry["name"] == player_name and entry["score"] == score:
           bg_color = '#fffacd'  
       else:
           bg_color = 'white'    
      
       # Create rank number label
       rank_lbl = tk.Label(rank_frame, text=f"#{i+1}", font=("Times New Roman", 12, "bold"), bg=bg_color, anchor='center')
       rank_lbl.grid(row=0, column=0, sticky='ew')
      
       # Create name label
       name_lbl = tk.Label(rank_frame, text=entry["name"], font=("Times New Roman", 12), bg=bg_color, anchor='center')
       name_lbl.grid(row=0, column=1, sticky='ew')
      
       # Create score label
       score_lbl = tk.Label(rank_frame, text=str(entry["score"]), font=("Times New Roman", 12, "bold"), bg=bg_color, anchor='center')
       score_lbl.grid(row=0, column=2, sticky='ew')
  
   # Function for play again button
   def play_again():
       ranking_window.destroy()
       run_game(level)
  
   # Function to return to main menu button
   def back_to_menu():
       ranking_window.destroy()
       main()
  
   # Function to exit button
   def exit_game():
       ranking_window.destroy()
       
  
   # Create buttons
   play_again_btn = tk.Button(main_frame, text="Play Again", font=("Times New Roman", 14, "bold"), command=play_again, width=15, height=2, bg='lightgreen')
   play_again_btn.pack(side='left', padx=10, pady=20)
   back_to_menu_btn = tk.Button(main_frame, text="Main Menu", font=("Times New Roman", 14, "bold"), command=back_to_menu, width=15, height=2, bg='lightyellow')
   back_to_menu_btn.pack(side='left', padx=10, pady=20)
   exit_game_btn = tk.Button(main_frame, text="Exit", font=("Times New Roman", 14, "bold"), command=exit_game, width=15, height=2, bg='lightcoral')
   exit_game_btn.pack(side='left', padx=10, pady=20)
  
   
   ranking_window.mainloop() 


# Start the game 
def run_game(level):
   # Start pygame and declare variables
   pygame.init()  
   global screen
   global game_level
   screen = pygame.display.set_mode((Width, Height)) 
   pygame.display.set_caption('Math Runner')   
   game_level = level 
   # Start the game
   game_start() 


# Start the application
main()
