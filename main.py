import pygame
import os
import time
import random

from pygame.constants import KEYDOWN
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 750, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GALAGA")

#Colores
NEGRO   = (0, 0, 0)
BLANCO  = (255, 255, 255)
VERDE   = (0, 255, 0)
ROJO    = (255, 0, 0)
AZUL    = (0, 0, 255)
VIOLETA = (117, 53, 228)

#Fuente
fuente = pygame.font.SysFont(None, 50)

# Reloj para la funcion Pausa
clock = pygame.time.Clock()

# Load images
NAVE_ENEMIGO_1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "enemy1_recortado.png")) , (76,70))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player player
NAVE_JUGADOR = pygame.transform.scale(pygame.image.load(os.path.join("assets", "ship2_recortado.png")), (101,78))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

# Sonidos
SONIDO_LASER_JUGADOR = pygame.mixer.Sound(os.path.join("assets", "sonido_laser2.wav"))
SONIDO_LASER_ENEMIGO = pygame.mixer.Sound(os.path.join("assets", "sonido_laser3.wav"))
SONIDO_EXPLOSION = pygame.mixer.Sound(os.path.join("assets", "sonido_explosion.wav"))
SONIDO_EXPLOSION_JUGADOR = pygame.mixer.Sound(os.path.join("assets", "sonido_explosion_jugador.wav"))

# Musica
pygame.mixer.music.load(os.path.join("assets", "freedom_squad.mp3" ))
pygame.mixer.music.set_volume(0.5)

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


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


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def puntajeAlto():
    WIN.fill(NEGRO)
    puntaje_font = pygame.font.SysFont("comicsans", 50)
    cartel_puntaje = puntaje_font.render("1. " + max_score(), 1, (255,255,255))
    WIN.blit(cartel_puntaje, (WIDTH/2 - cartel_puntaje.get_width()/2, 350))
    pygame.display.update()
    time.sleep(4)
############## ARCHIVO DE PUNTAJE MÁS ALTO ########################
def update_score(nscore):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))
def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score
######## FIN ARCHIVO DE PUNTAJE MÁS ALTO ##########

def pausa():

    pausado = True

    while pausado:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pausado = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.set_volume(0.5)
                    pausado = False
                if event.key == pygame.K_q:
                    pausado = False
                    pygame.quit()
                    exit()  

        WIN.fill(NEGRO)
        pygame.draw.rect(WIN,NEGRO, (110,160,550,200))
        mensaje("PAUSA", VIOLETA, 300, 200)
        mensaje("Presiona ESC para continuar", BLANCO, 150, 270)
        mensaje("Presiona Q para salir", BLANCO, 150, 320)
        pygame.display.update()                
        

def main():
    run = True
    FPS = 60
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 5

    player = Player(300, 680)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0
    global score
    nave_visible = True

    def redraw_window():
        WIN.blit(BG, (0,0))
        # draw text
        cartel_vidas = main_font.render(f"Vidas: {player.vidas}", 1, (255,255,255))
        cartel_score = main_font.render(f"Puntaje: {player.score}", 1, (255,255,255))
        WIN.blit(cartel_vidas, (10, 10))
        WIN.blit(cartel_score, (420,10))
        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("Fin Del Juego", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
            update_score(player.score)
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if player.vidas <= 0:
            lost = True
            pygame.mixer.music.stop()
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)



        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()    


        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

           # if random.randrange(0, 2*60) == 1:
            #    enemy.shoot()

            if enemy.cool_down_counter==0:
                enemy.shoot()
                enemy.cool_down_counter = 120
            else :
                enemy.cool_down_counter -= 1


            if (collide(enemy, player))and(player.invulnerabilidad==False):
                enemies.remove(enemy)
                player.recibir_golpe()
            if enemy.y + enemy.get_height() > HEIGHT:
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.set_volume(0.2)
                    pausa()


        if (player.contadorInvulneravilidad==0 and player.invulnerabilidad==True):
            player.invulnerabilidad = False
        elif (player.contadorInvulneravilidad>0):
            player.contadorInvulneravilidad-=1

        


def mensaje(msg, color, txt_x, txt_y):
    txt_pantalla = fuente.render(msg, True, color)
    WIN.blit(txt_pantalla, [txt_x, txt_y])


def menu_Comienzo():
    WIN.fill(NEGRO)
    mensaje("JUEGO GALAGA", VIOLETA, 200, 110)
    mensaje("[1] Comenzar a Jugar", BLANCO, 200, 200)
    mensaje("[2] Instrucciones", BLANCO, 200, 300)
    mensaje("[3] Puntaje más alto", BLANCO, 200, 400)
    mensaje("[4] Salir", BLANCO, 200, 500)


    pygame.display.update()


def instrucciones():
    WIN.fill(NEGRO)
    mensaje("INSTRUCCIONES", VIOLETA, 200, 100)
    mensaje("- Teclas de acción: [W][A][S][D][ESPACIO].", BLANCO, 20, 200)
    mensaje("- Presionar ESC para pausar.", BLANCO, 20, 300)
    mensaje("- Si una bala te impacta, perdés vida.", BLANCO, 20, 400)
    pygame.display.update()
    time.sleep(5)


fin_Juego = False
while not fin_Juego:
    menu_Comienzo()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                fin_Juego = True     
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                pygame.mixer.music.play(loops=-1)
                main()
            if event.key == pygame.K_2:
                 instrucciones()    
            if event.key == pygame.K_3:
                puntajeAlto()
            if event.key == pygame.K_4:
                pygame.display.quit()
                fin_Juego = True

          
pygame.display.quit()                 