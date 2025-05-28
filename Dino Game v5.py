import os
import sys
import pygame
import tkinter as tk
from tkinter import *
import tkinter.messagebox as messagebox

Width = 623
Height = 150

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
            self.gravity = 1.2
            self.onground = True
            self.jumping = False
            self.jump_stop = 10
            self.falling = False
            self.fall_stop = self.y
            self.set_texture()
            self.show()

        def update(self, loops):
            if self.jumping:
                self.y -= self.dy
                if self.y <= self.jump_stop:
                    self.fall()
            elif self.falling:
                self.y += self.gravity + self.dy
                if self.y >= self.fall_stop:
                    self.stop()
            elif self.onground and loops % 4 == 0:
                self.texture_num = (self.texture_num + 1) % 3
                self.set_texture()

        def show(self):
            screen.blit(self.texture, (self.x, self.y))

        def set_texture(self):
            path = os.path.join(f'assets/Images/dino{self.texture_num + 1}.png')
            self.texture = pygame.image.load(path).convert_alpha()
            self.width, self.height = self.texture.get_size()
            self.y = Height - self.height

        def jump(self):
            self.jumping = True
            self.onground = False

        def fall(self):
            self.jumping = False
            self.falling = True

        def stop(self):
            self.falling = False
            self.onground = True

    class BG:
        def __init__(self, x):
            self.x = x
            self.set_texture()

        def update(self, dx):
            self.x += dx
            if self.x <= -self.width:
                self.x = Width

        def show(self):
            screen.blit(self.texture, (self.x, self.y))

        def set_texture(self):
            path = os.path.join('assets/Images/chao.png')
            self.texture = pygame.image.load(path).convert_alpha()
            self.width, self.height = self.texture.get_size()
            self.y = Height - self.height

    class Cactus:
        def __init__(self, x):
            self.width = 34
            self.height = 44
            self.x = x
            self.y = 80
            self.set_texture()
            self.show()

        def update(self, dx):
            self.x += dx

        def show(self):
            screen.blit(self.texture, (self.x, self.y))

        def set_texture(self):
            path = os.path.join('assets/Images/Cactus.png')
            self.texture = pygame.image.load(path)
            self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

    class Game:
        def __init__(self):
            self.bg = [BG(x=0), BG(x=Width)]
            self.dino = Dino()
            self.cactus = Cactus(x=300)
            self.speed = 3

    def main():
        game = Game()
        dino = game.dino
        clock = pygame.time.Clock()
        loops = 0
        while True:
            loops += 1
            screen.fill((255, 255, 255))

            for bg in game.bg:
                bg.update(-game.speed)
                bg.show()

            dino.update(loops)
            dino.show()

            game.cactus.update(-game.speed)
            game.cactus.show()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if dino.onground:
                            dino.jump()

            pygame.display.update()
            clock.tick(80)

    main()

def validate_input(char):
    return char.isalpha()

def tkinter():
    root = tk.Tk()
    root.title("Dino Math Quiz")
    root.geometry("400x300")

    # Title label at the top
    title_label = Label(root, text="MATH DINO GAME", font=("Times New Roman", 20, "bold"))
    title_label.pack(pady=30)

    # Username label and entry
    username_label = Label(root, text="Enter your name:", font=("Times New Roman", 12))
    username_label.pack(pady=5)
    username_entry = Entry(root, font=("Times New Roman", 12))
    username_entry.pack(pady=5)

    # Start button
    def start_game():
        username = username_entry.get()
        if not username.isalpha():
            tk.messagebox.showwarning("Input Required", "Please enter your name before starting the game.")
        else:
            root.destroy()
            run_game()  # You can modify run_game() to accept the username if needed

    start = Button(root, text="Start Dino Math Quiz", font=("Times New Roman", 14), command=start_game)
    start.pack(pady=5)

    # Exit button at bottom-left
    exit_button = Button(root, text="Exit", font=("Times New Roman", 12), command=root.destroy)
    exit_button.place(x=20, y=260)

    # Instructions button at bottom-right
    def show_instructions():
        instruction_window = tk.Toplevel(root)
        instruction_window.title("Instructions")
        instruction_window.geometry("300x200")
        Label(instruction_window, text="Solve the math question displayed at the top of the screen.\nEach cactus represents a possible answer.\nCollide with the cactus displaying the correct answer to score points.\nAvoid incorrect answers by jumping over them.\nBe quick and accurate to achieve the highest score!",
              font=("Times New Roman", 12), justify="left", wraplength=280).pack(pady=20)

    instruction_button = Button(root, text="Instructions", font=("Times New Roman", 12), command=show_instructions)
    instruction_button.place(x=280, y=260)

    root.mainloop()


tkinter()
