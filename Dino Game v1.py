# Creating a parallax Infinite Scrolling Background for the Dino game
import os
import sys
import pygame

Width = 623
Height = 150

pygame.init()
screen = pygame.display.set_mode( (Width,Height) )
pygame.display.set_caption('Dino')

class BG:

    def __init__(self, x,):
        self.width = Width
        self. height = Height
        self.x = x
        self.y = 0
        self.set_texture()
        self.show()

    def update(self, dx):
        self.x += dx
        if self.x <= -Width:
            self.x=Width

    def show(self):
        screen.blit(self.texture,(self.x,self.y))

    def set_texture(self):
        path = os.path.join('assets/images/bg.png')
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture,(self.width, self.height))




class Game:

    def __init__(self):
        self.bg = [BG(x=0),BG(x=Width)]
        self.speed=3

def main():

    game = Game()

    clock = pygame.time.Clock()
    # main loop
    while True:

        for bg in game.bg:
            bg.update(-game.speed)
            bg.show()

        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()

        clock.tick(80)
        pygame.display.update()

main()