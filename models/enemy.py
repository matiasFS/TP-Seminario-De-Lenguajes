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
        self.tipo_de_nave = None
        self.cooldown_movimiento = 0
        self.lado = None
        if (x<350):
            self.lado=1
        else:
            self.lado=2
        if (color=="red"):
            self.tipo_de_nave = 1
        elif (color=="green"):
            self.tipo_de_nave = 2
        else:
            self.tipo_de_nave = 3


    def move(self, vel):
        if (self.tipo_de_nave==1):
            self.y += vel*3
        elif (self.tipo_de_nave==2):
            self.cooldown_movimiento += 1
            self.y += vel
            if (self.lado==1):
                if (self.cooldown_movimiento==3):    
                    self.x += vel
                    self.cooldown_movimiento=0
            else:
                if (self.cooldown_movimiento==3):    
                    self.x -= vel
                    self.cooldown_movimiento=0
        else:
            self.y += vel

    def shoot(self):
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)


