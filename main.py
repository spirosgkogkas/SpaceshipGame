import pygame,random,os,sys

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1920, 900
BACKGROUND_IMAGES = (pygame.transform.scale(pygame.image.load(os.path.join("Background","space.jpg")),(WIDTH,HEIGHT)),
    pygame.transform.scale(pygame.image.load(os.path.join("Background","space2.jpg")),(WIDTH,HEIGHT)),
    pygame.transform.scale(pygame.image.load(os.path.join("Background", "space3.jpg")),(WIDTH, HEIGHT)))
ICON = pygame.image.load(os.path.join("Assets", "icon.png"))
FPS = 60
BORDER = pygame.Rect(WIDTH//2 - 10, 0, 10, HEIGHT)
RED_SPACESHIP_WIDTH, RED_SPACESHIP_HEIGHT = 75, 75
BLACK_SPACESHIP_WIDTH, BLACK_SPACESHIP_HEIGHT = 75, 75
RED_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("Assets", "red_spaceship.png")),
    (RED_SPACESHIP_WIDTH, RED_SPACESHIP_HEIGHT)),90)
BLACK_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("Assets", "black_spaceship.png")),
    (BLACK_SPACESHIP_WIDTH, BLACK_SPACESHIP_HEIGHT)),180)
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 3
P1_SCORE, P2_SCORE = 0, 0
PLAYER1_HIT = pygame.USEREVENT + 1
PLAYER2_HIT = pygame.USEREVENT + 2
FONT = pygame.font.SysFont("comicsans", 30)
FIRE_SOUND = pygame.mixer.Sound(os.path.join("Music", "laser-beam.mp3"))
HIT_SOUND = pygame.mixer.Sound(os.path.join("Music", "boom.mp3"))
FIRE_SOUND.set_volume(0.5)
HIT_SOUND.set_volume(0.7)

#RGB
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255 ,255)

pygame.display.set_icon(ICON)
pygame.display.set_caption("Spaceship Game!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def display_window(red, black, red_bullets, black_bullets, red_health, black_health, Round_is_ended, num):
    red_health_text = FONT.render(f"Player 1 Health:{red_health}",True,WHITE)
    black_health_text = FONT.render(f"Player 2 Health:{black_health}",True,WHITE)
    red_score = FONT.render(f"P1 Score: {P1_SCORE}", True, WHITE)
    black_score = FONT.render(f"P2 Score: {P2_SCORE}", True, WHITE)
    change_background = random.randint(0,2)

    if Round_is_ended:
        screen.blit(BACKGROUND_IMAGES[change_background].convert_alpha(), (0, 0))
    else:
        screen.blit(BACKGROUND_IMAGES[num].convert_alpha(), (0, 0))
    
    screen.blit(red_health_text, (10,10))
    screen.blit(black_health_text,(WIDTH - black_health_text.get_width() - 10,10))
    screen.blit(red_score, (10,35))
    screen.blit(black_score, (WIDTH - black_score.get_width() - 20, 35))
    screen.blit(RED_SPACESHIP_IMAGE.convert_alpha(), (red.x, red.y))
    screen.blit(BLACK_SPACESHIP_IMAGE.convert_alpha(), (black.x, black.y))
    # pygame.draw.rect(screen, BLACK, BORDER)
    
    for bullet in red_bullets:
        pygame.draw.rect(screen, RED, bullet)
    for bullet in black_bullets:
        pygame.draw.rect(screen, BLACK, bullet)
    pygame.display.update()

def handle_movement(keys, red, black):
    if keys[pygame.K_a] and red.x > VEL:
        red.x -= VEL
    if keys[pygame.K_d] and red.x + red.width + VEL < BORDER.x:
        red.x += VEL
    if keys[pygame.K_w] and red.y > VEL:
        red.y -= VEL
    if keys[pygame.K_s] and red.y + red.height < HEIGHT:
        red.y += VEL

    if keys[pygame.K_LEFT] and black.x - VEL > BORDER.x:
        black.x -= VEL
    if keys[pygame.K_RIGHT] and black.x + black.width + VEL < WIDTH:
        black.x += VEL
    if keys[pygame.K_UP] and black.y > VEL:
        black.y -= VEL
    if keys[pygame.K_DOWN] and black.y + black.height < HEIGHT:
        black.y += VEL

def handle_bullets(red, black, red_bullets, black_bullets):
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if black.colliderect(bullet):
            HIT_SOUND.play()
            red_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(PLAYER2_HIT))
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)
    
    for bullet in black_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            HIT_SOUND.play()
            black_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(PLAYER1_HIT))
        elif bullet.x < 0:
            black_bullets.remove(bullet)

def draw_winner(winner_text):
    font_obj = pygame.font.SysFont("impact",100)
    surface_obj = font_obj.render(winner_text, True,WHITE)
    screen.blit(surface_obj,(WIDTH//2 - surface_obj.get_width()//2,HEIGHT//2 - surface_obj.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    global P1_SCORE, P2_SCORE
    pygame.mixer.music.unload()
    soundtrack = os.listdir(r".\Music\SoundTracks") [random.randint(0, 1)]
    pygame.mixer.music.load(os.path.join("Music", "SoundTracks", soundtrack))
    pygame.mixer.music.play(-1,0.0)
    red = pygame.Rect(0, HEIGHT // 2 - RED_SPACESHIP_HEIGHT, RED_SPACESHIP_WIDTH, RED_SPACESHIP_HEIGHT)
    black = pygame.Rect(WIDTH - BLACK_SPACESHIP_WIDTH, HEIGHT // 2 - BLACK_SPACESHIP_HEIGHT, BLACK_SPACESHIP_WIDTH, BLACK_SPACESHIP_HEIGHT)
    red_bullets = []
    black_bullets = []
    red_health = 10
    black_health = 10
    winner_text = ""
    num = random.randint(0, 2)
    round_finished = 0

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets) < MAX_BULLETS:
                    FIRE_SOUND.play()
                    red_bullets.append(pygame.Rect(red.x + red.width, red.y + red.height//2 - 2, 10, 5))
                if event.key == pygame.K_RCTRL and len(black_bullets) < MAX_BULLETS:
                    FIRE_SOUND.play()
                    black_bullets.append(pygame.Rect(black.x, black.y + black.height // 2 - 2, 10, 5))
            if event.type == PLAYER1_HIT:
                red_health-= 1
            if event.type == PLAYER2_HIT:
                black_health -= 1
        
        if red_health <= 0:
            round_finished = 1
            P2_SCORE += 1
            winner_text = "Player 2 WINS!!!"
        elif black_health <= 0:
            round_finished = 1
            P1_SCORE += 1
            winner_text = "Player 1 WINS!!!"

        if len(winner_text) > 0:
            draw_winner(winner_text)
            break
        
        keys = pygame.key.get_pressed()
        handle_movement(keys, red, black)
        handle_bullets(red,black,red_bullets,black_bullets)
        display_window(red, black,red_bullets,black_bullets,red_health,black_health,round_finished,num)
   
    main()

if __name__ == '__main__':
    main()