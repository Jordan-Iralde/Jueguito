import pygame
import random

# Inicializar Pygame
pygame.init()

# Constantes de pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Fuentes
font = pygame.font.SysFont("Arial", 40)

# Clase Jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.health = 100
        self.mana = 50
        self.speed = 5
        self.attack_cooldown = 0
        self.attack_radius = 30  # Rango de ataque físico reducido

    def update(self, keys):
        # Movimiento del jugador
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

        # Limitar el movimiento del jugador a la ventana
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

        # Ataques
        if keys[pygame.K_SPACE] and self.attack_cooldown == 0:  # Ataque físico (puñetazo)
            print("Ataque físico realizado")
            self.attack_cooldown = 10  # Cooldown entre ataques
            return True, False  # Indicar que se realizó un ataque físico

        elif keys[pygame.K_LSHIFT] and self.attack_cooldown == 0 and self.mana > 0:  # Ataque mágico (proyectil)
            print("Ataque mágico realizado")
            mouse_x, mouse_y = pygame.mouse.get_pos()  # Obtener la posición del mouse
            projectile = Projectile(self.rect.centerx, self.rect.centery, mouse_x, mouse_y)
            all_sprites.add(projectile)
            projectiles.add(projectile)
            self.mana -= 5  # Disminuye el mana
            self.attack_cooldown = 15  # Cooldown entre ataques
            return False, True  # Indicar que se realizó un ataque mágico

        # Enfriar ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        return False, False  # No se realizó ataque

    def draw_health_mana(self, screen):
        # Dibujar barra de vida
        pygame.draw.rect(screen, RED, (20, 20, self.health * 2, 20))
        # Dibujar barra de mana
        pygame.draw.rect(screen, BLUE, (20, 50, self.mana * 2, 20))

# Clase Proyectil
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10

        # Calcular la dirección hacia el cursor
        self.direction = pygame.math.Vector2(target_x - x, target_y - y)
        self.direction.normalize_ip()  # Normaliza el vector para que tenga longitud 1

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        if self.rect.x > SCREEN_WIDTH or self.rect.x < 0 or self.rect.y > SCREEN_HEIGHT or self.rect.y < 0:
            self.kill()

# Clase Enemigo
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 40)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 40)
        self.speed = random.randint(1, 3)
        self.health = 20  # Salud del enemigo
        self.hit_timer = 0  # Para el efecto de daño visual
    
    def update(self):
        # Movimiento hacia el jugador
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > player.rect.x:
            self.rect.x -= self.speed
        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > player.rect.y:
            self.rect.y -= self.speed
        
        # Colisión con el jugador
        if pygame.sprite.collide_rect(self, player):
            player.health -= 1
            if player.health <= 0:
                print("El jugador ha muerto")
                pygame.quit()

        # Temporizador para el efecto de golpe
        if self.hit_timer > 0:
            self.hit_timer -= 1
            if self.hit_timer == 0:
                self.image.fill(RED)  # Volver al color original

    def take_damage(self, damage):
        global score  # Acceder a la variable de puntuación global
        self.health -= damage
        self.hit_timer = 20  # Temporizador para el efecto de daño
        self.image.fill(GREEN)  # Cambiar color al recibir daño
        if self.health <= 0:
            self.kill()  # Elimina al enemigo cuando su salud llega a 0
            score += 10  # Incrementar la puntuación al eliminar al enemigo

# Clase Door
class Door(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2)

# Variables para los niveles y la puerta
level = 1
door = None

def spawn_door():
    global door
    door = Door()
    all_sprites.add(door)

# Función para mostrar el menú principal
def show_menu():
    while True:
        screen.fill(BLACK)

        # Dibujar botones
        start_button = pygame.Rect(300, 200, 200, 50)
        controls_button = pygame.Rect(300, 300, 200, 50)

        pygame.draw.rect(screen, WHITE, start_button)
        pygame.draw.rect(screen, WHITE, controls_button)

        # Dibujar texto
        start_text = font.render("Start", True, BLACK)
        controls_text = font.render("Controls", True, BLACK)

        screen.blit(start_text, (start_button.x + 50, start_button.y + 10))
        screen.blit(controls_text, (controls_button.x + 30, controls_button.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return  # Iniciar el juego
                if controls_button.collidepoint(event.pos):
                    show_controls()  # Mostrar los controles

# Función para mostrar los controles
def show_controls():
    controls_screen = True
    while controls_screen:
        screen.fill(BLACK)

        # Mostrar texto de controles
        controls_text = font.render("Use W/A/S/D to move", True, WHITE)
        attack_text = font.render("Press SPACE to attack", True, WHITE)
        magic_text = font.render("Press LSHIFT for magic", True, WHITE)

        screen.blit(controls_text, (150, 200))
        screen.blit(attack_text, (150, 250))
        screen.blit(magic_text, (150, 300))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                controls_screen = False  # Salir de la pantalla de controles
# Inicializar el juego
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juego con Pygame y P.O.O")

# Mostrar menú principal
show_menu()

# Crear grupos de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

# Crear jugador
player = Player()
all_sprites.add(player)

# Generar enemigos aleatoriamente
for _ in range(5):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Variable de puntuación
score = 0

# Función para mostrar la puntuación en pantalla
def draw_score(screen):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH - 150, 20))

# Bucle principal del juego
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)  # 60 FPS
    screen.fill(BLACK)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Obtener el estado de las teclas
    keys = pygame.key.get_pressed()
    
    # Actualizar el jugador con las teclas
    attack_physical, attack_magic = player.update(keys)  # Se detecta si se realizó un ataque

    # Detectar colisiones del ataque físico
    if attack_physical:
        # Crear un área de ataque circular alrededor del jugador
        attack_area = pygame.Rect(player.rect.centerx - player.attack_radius, 
                                   player.rect.centery - player.attack_radius, 
                                   player.attack_radius * 3, 
                                   player.attack_radius * 3)

        # Detectar colisiones con enemigos
        for enemy in enemies:
            if attack_area.colliderect(enemy.rect):
                enemy.take_damage(10)  # Cada ataque físico hace 10 de daño

    # Actualizar otros sprites
    enemies.update()
    projectiles.update()

    # Detectar colisiones entre proyectiles y enemigos
    hits = pygame.sprite.groupcollide(enemies, projectiles, False, True)  # False no elimina enemigos, True elimina proyectiles
    for enemy, projectiles_hit in hits.items():
        for projectile in projectiles_hit:
            enemy.take_damage(10) 

    # Dibujar sprites y puntuación
    all_sprites.draw(screen)
    # Dibujar el área de ataque (opcional, para depuración)
    if attack_physical:
        pygame.draw.circle(screen, GREEN, player.rect.center, player.attack_radius, 2)
    draw_score(screen)
    player.draw_health_mana(screen)

    def spawn_enemies(level):
        for _ in range(5 + (level - 1) * 2):  # Más enemigos por nivel
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

    def advance_level():
        global level, door
        level += 1
        door.kill()  # Elimina la puerta
        spawn_enemies(level)  # Aumenta la dificultad agregando más enemigos

    # En el bucle principal del juego, después de derrotar a todos los enemigos:
    if not enemies and not door:
        spawn_door()  # Aparece la puerta cuando no quedan enemigos

    # Detectar colisión entre el jugador y la puerta
    if door and pygame.sprite.collide_rect(player, door):
        advance_level()
    pygame.display.flip()

pygame.quit()
  