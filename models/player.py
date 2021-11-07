from models.ship import *
import random

# Player player
NAVE_JUGADOR = pygame.transform.scale(pygame.image.load(os.path.join("assets", "ship2_recortado.png")), (101,78))
NAVE_JUGADOR_IZQ = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Nave frontal izq.png")), (101,78))
NAVE_JUGADOR_DER = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Nave frontal der.png")), (101,78))

SONIDO_EXPLOSION_JUGADOR = pygame.mixer.Sound(os.path.join("assets", "sonido_explosion_jugador.wav"))
SONIDO_EXPLOSION = pygame.mixer.Sound(os.path.join("assets", "sonido_explosion.wav"))

YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

class Player(Ship):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.ship_img = NAVE_JUGADOR
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.vidas = 3
        self.invulnerabilidad = False
        self.contadorInvulneravilidad = 0
        self.score = 0

    def move_left(self):
        self.ship_img = NAVE_JUGADOR_IZQ

    def move_right(self):
        self.ship_img = NAVE_JUGADOR_DER

    def stand_by(self):
        self.ship_img = NAVE_JUGADOR

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):   ## Colision del laser con el enemigo
                        SONIDO_EXPLOSION.play()
                        objs.remove(obj)
                        self.score += random.randrange(100, 200)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def recibir_golpe(self):
        SONIDO_EXPLOSION_JUGADOR.play()
        self.invulnerabilidad = True
        self.contadorInvulneravilidad = 180
        self.x=300
        self.y=680
        self.vidas -= 1
