import os
import sys
import pygame

Width = 623
Height = 150

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
        self.set_texture()
        self.show()

    def update(self):
        self.texture_num = (self.texture_num + 1) % 3
        self.set_texture()


    def show(self):
        screen.blit(self.texture,(self.x,self.y))

    def set_texture(self):
        path = os.path.join(f'assets/Images/dino{self.texture_num + 1}.png')
        self.texture = pygame.image.load(path).convert_alpha()
        self.width, self.height = self.texture.get_size()
        self.y = Height - self.height

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
        path = os.path.join('assets/Images/chao.png')  # Make sure this path is correct
        self.texture = pygame.image.load(path).convert_alpha()
        self.width, self.height = self.texture.get_size()
        self.y = Height - self.height

class Game:

    def __init__(self):
        self.bg = [BG(x=0), BG(x=Width)]
        self.dino= Dino()
        self.speed = 3

def main():
    game = Game()
    dino = game.dino

    clock = pygame.time.Clock()


    while True:



        screen.fill((255, 255, 255))

        for bg in game.bg:
            bg.update(-game.speed)
            bg.show()

        dino.update()
        dino.show()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(80)

main()
