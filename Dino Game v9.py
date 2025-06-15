import os
import sys
import math
import pygame
import tkinter as tk
from tkinter import *
import tkinter.messagebox as messagebox
import random

Width = 623
Height = 300


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption('Dino')
    

    class Dino:
        def __init__(self):
            self.width = 44
            self.height = 44
            self.x = 10
            self.y = 80
            self.texture_num = 0
            self.dy = 3
            self.onground = True
            self.jumping = False
            self.falling = False
            self.fall_stop = self.y
            self.velocity = 0
            self.gravity = 0.5
            self.jump_strength = -10
            self.set_texture()
            self.show()

        def update(self, loops):
            if not self.onground:
                self.velocity += self.gravity
                self.y += self.velocity

                if self.y >= Height - self.height - 65:
                    self.y = Height - self.height - 65
                    self.velocity = 0
                    self.onground = True
            elif loops % 8 == 0:
                self.texture_num = (self.texture_num + 1) % 3
                self.set_texture()

        def show(self):
            screen.blit(self.texture, (self.x, self.y))

        def set_texture(self):
            path = os.path.join(f'assets/Images/Noob{self.texture_num + 1}.png')
            image = pygame.image.load(path).convert_alpha()
            self.texture = pygame.transform.scale(image, (self.width, self.height))
            self.y = Height - self.height - 65

        def jump(self):
            if self.onground:
                self.velocity = self.jump_strength
                self.onground = False

    class BG:
        def __init__(self, x):
            self.width = Width
            self.height = Height
            self.x = x
            self.y = 0
            self.set_texture()

        def update(self, dx):
            self.x += dx
            if self.x <= -self.width:
                self.x += Width * 2

        def show(self):
            screen.blit(self.texture, (int(self.x), int(self.y)))

        def set_texture(self):
            path = os.path.join('assets/Images/BG.png')
            image = pygame.image.load(path)
            self.texture = pygame.transform.scale(image, (self.width, self.height))

    class Cactus:
        def __init__(self, x):
            self.width = 34
            self.height = 34
            self.x = x
            self.y = 80
            self.set_texture()
            self.show()

        def update(self, dx):
            self.x += dx

        def show(self):
            screen.blit(self.texture, (self.x, self.y))

        def set_texture(self):
            path = os.path.join('assets/Images/Obstacle.png')
            image = pygame.image.load(path).convert_alpha()
            self.texture = pygame.transform.scale(image, (self.width, self.height))
            self.y = Height - self.height - 70

    class Collision:

        def between(self,obj1,obj2):
            distance = math.sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)
            return distance < 35

    class Score:

        def __init__(self, hs):
            self.hs = hs
            self.act = 0
            self. font = pygame.font.SysFont('Times New Roman', 18)
            self.color = (0,0,0)
            self.show()

        def update(self, loops):
            self.act = loops // 10
            self.check_hs()

        def show(self):
            self.lbl = self.font.render(f'Hi {self.hs} {self.act}', 1, self.color)
            lbl_width = self.lbl.get_rect().width
            screen.blit(self.lbl,(Width - lbl_width - 10, 10))

        def check_hs(self):
            if self.act >= self.hs:
                self.hs = self.act

        def reset(self):
            self.act = 0
            
    class Question:
        def __init__(self):
            self.font = pygame.font.SysFont('Times New Roman', 24)
            self.question_data = {"question": "1 + 1", "answer": 2}
            self.question_text = self.question_data["question"]

        def show(self):
            text_surface = self.font.render(self.question_text, True, (0, 0, 0))
            screen.blit(text_surface, (Width // 2 - text_surface.get_width() // 2, 20))

    class Game:
        def __init__(self):
            self.bg = [BG(x=0), BG(x=Width)]
            self.dino = Dino()
            self.obstacles = []
            self.collision = Collision()
            self.score = Score(hs=0)
            self.speed = 3
            self.playing = False
            self.question = Question()
            self.set_labels()

        def set_labels(self):
            big_font = pygame.font.SysFont('Times New Roman', 24, bold = True)
            small_font = pygame.font.SysFont('Times New Roman', 18)
            self.big_lbl = big_font.render(f'G A M E O V E R', 1, (0, 0, 0))
            self.small_lbl = small_font.render(f'press r to restart', 1, (0, 0, 0))

        def start(self):
            self.playing = True

        def over(self):
            screen.blit(self.big_lbl, (Width // 2 - self.big_lbl.get_width() // 2, Height // 4))
            screen.blit(self.small_lbl, (Width // 2 - self.small_lbl.get_width() // 2, Height // 2))
            self.playing = False 

        

        def tospawn(self, loops):
            return loops % 100 == 0


        def spawn_cactus(self):
            if len(self.obstacles) > 0:
                prev_cactus=self.obstacles[-1]
                x = random.randint(prev_cactus.x + self.dino.width + 84, Width + prev_cactus.x + self.dino.width + 84)

            else:
                x = random.randint(Width + 100,1000)

            cactus = Cactus(x=x)
            self.obstacles.append(cactus)

        
        def restart(self):
            self.__init__()
            
    def main():
        game = Game()
        dino = game.dino

        
        clock = pygame.time.Clock()
        loops = 0
        
        while True:

            if game.playing:

                loops += 1

                for bg in game.bg:
                    bg.update(-game.speed)
                    bg.show()

                dino.update(loops)
                dino.show()
                game.question.show()

                if game.tospawn(loops):
                    game.spawn_cactus()

                for cactus in game.obstacles:
                    cactus.update(-game.speed)
                    cactus.show()

                    if game.collision.between(dino, cactus):
                        game.over()

                game.score.update(loops)
                game.score.show()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if dino.onground:
                            dino.jump()

                        if not game.playing:
                            game.start()
                        
                    if event.key == pygame.K_r:
                        game.restart()
                        dino = game.dino
                        loops = 0

            pygame.display.update()
            clock.tick(80)

    main()


def validate_input(char):
    return char.isalpha()


def tkinter():
    root = tk.Tk()
    root.title("Dino Math Quiz")
    root.geometry("400x300")

    title_label = Label(root, text="MATH DINO GAME", font=("Times New Roman", 20, "bold"))
    title_label.pack(pady=30)

    username_label = Label(root, text="Enter your name:", font=("Times New Roman", 12))
    username_label.pack(pady=5)
    username_entry = Entry(root, font=("Times New Roman", 12))
    username_entry.pack(pady=5)

    def start_game():
        username = username_entry.get()
        if not username.isalpha():
            tk.messagebox.showwarning("Input Required", "Please enter your name before starting the game.")
        else:
            root.destroy()
            run_game()

    start = Button(root, text="Start Dino Math Quiz", font=("Times New Roman", 14), command=start_game)
    start.pack(pady=5)

    exit_button = Button(root, text="Exit", font=("Times New Roman", 12), command=root.destroy)
    exit_button.place(x=20, y=260)

    def show_instructions():
        instruction_window = tk.Toplevel(root)
        instruction_window.title("Instructions")
        instruction_window.geometry("300x200")
        Label(instruction_window,
              text="Solve the math question displayed at the top of the screen.\nEach cactus represents a possible answer.\nCollide with the cactus displaying the correct answer to score points.\nAvoid incorrect answers by jumping over them.\nBe quick and accurate to achieve the highest score!",
              font=("Times New Roman", 12), justify="left", wraplength=280).pack(pady=20)

    instruction_button = Button(root, text="Instructions", font=("Times New Roman", 12), command=show_instructions)
    instruction_button.place(x=280, y=260)

    root.mainloop()


tkinter()
