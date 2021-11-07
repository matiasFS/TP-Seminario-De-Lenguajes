import random
from models.ship import *
from models.laser import *

NAVE_ENEMIGO_1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "enemy1_recortado.png")) , (76,70))

RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))

SONIDO_LASER_ENEMIGO = pygame.mixer.Sound(os.path.join("assets", "sonido_laser3.wav"))

BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
GREEN_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "enemy3.png")) , (60,72))
BLUE_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Enemy2-recortado.png")) , (50,82))



class Enemy(Ship):
    COLOR_MAP = {
                "red": (NAVE_ENEMIGO_1, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
                }

    def __init__(self, x, y, color):
        super().__init__(x, y)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.cool_down_counter = random.randrange(0, 59)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        #if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            #self.cool_down_counter = 1

