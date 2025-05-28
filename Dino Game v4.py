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
        self.dy = 3
        self.gravity = 1.2
        self.onground = True
        self.jumping = False
        self.jump_stop = 10
        self.falling = False
        self.fall_stop = self.y
        self.set_texture()
        self.show()

    def update(self,loops):
        # jumping
        if self.jumping:
            self.y -= self.dy
            if self.y <= self.jump_stop:
                self.fall()

        # falling
        elif self.falling:
            self.y += self.gravity + self.dy
            if self.y >= self.fall_stop:
                self.stop()

        # Walking
        elif  self.onground and loops % 4 ==0:
            self.texture_num = (self.texture_num + 1) % 3
            self.set_texture()


    def show(self):
        screen.blit(self.texture,(self.x,self.y))

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
        path = os.path.join('assets/Images/chao.png')  # Make sure this path is correct
        self.texture = pygame.image.load(path).convert_alpha()
        self.width, self.height = self.texture.get_size()
        self.y = Height - self.height

class Cactus:

    def __init__(self,x):
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
        path = os.path.join('assets/Images/Cactus.png')  # Make sure this path is correct
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture,(self.width, self.height) )

class Game:

    def __init__(self):
        self.bg = [BG(x=0), BG(x=Width)]
        self.dino= Dino()
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

        #events
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
