import os
from models.laser import *

pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = 750, 800
# Sonidos
SONIDO_LASER_JUGADOR = pygame.mixer.Sound(os.path.join("assets", "sonido_laser2.wav"))


class Ship:
    COOLDOWN = 30

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        #self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif (laser.collision(obj)) and (obj.invulnerabilidad==False):
                obj.recibir_golpe()
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x+3, self.y, self.laser_img)
            SONIDO_LASER_JUGADOR.play()
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


