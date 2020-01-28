import sys
import pygame
import os
import copy
pygame.init()
new_game_button = 'new'
records_button = 'records'
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        block = pygame.Surface((12, 12))
        block.fill(pygame.Color('blue'))
        self.image = block
        self.rect = self.image.get_rect()
        self.rect.x = x * 12
        self.rect.y = y * 12


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        ball = pygame.Surface((12, 12))
        pygame.draw.circle(ball, (255, 255, 255), (6, 6), 3)
        self.image = ball
        self.rect = self.image.get_rect()
        self.rect.x = x * 12
        self.rect.y = y * 12


class Energizer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        ball = pygame.Surface((24, 24))
        pygame.draw.circle(ball, (255, 255, 255), (12, 12), 6)
        self.image = ball
        self.rect = self.image.get_rect()
        self.rect.x = x * 12
        self.rect.y = y * 12


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def main_menu():
    menu = pygame.display.set_mode((800, 600))
    menu.blit(pygame.transform.scale(load_image('menu_logo.jpg'), (800, 450)), (0, -100))
    font = pygame.font.Font(os.path.join('data', 'PAC-FONT.TTF'), 35)
    text = font.render('New game', 1, (0, 0, 255))
    text_x = 800 // 2 - text.get_width() // 2
    text_y = 250
    menu.blit(text, (text_x, text_y))
    text2 = font.render('Records', 1, (0, 0, 255))
    text_x2 = 800 // 2 - text2.get_width() // 2
    text_y2 = 350
    menu.blit(text2, (text_x2, text_y2))
    button = new_game_button
    pygame.display.flip()
    menu_run = True
    while menu_run:
        menu.fill((0, 0, 0))
        menu.blit(pygame.transform.scale(load_image('menu_logo.jpg'), (800, 450)), (0, -100))
        menu.blit(text, (text_x, text_y))
        menu.blit(text2, (text_x2, text_y2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if button == new_game_button:
                        button = records_button
                elif event.key == pygame.K_UP:
                    if button == records_button:
                        button = new_game_button
                elif event.key == pygame.K_RETURN:
                    menu_run = False
                    if button == new_game_button:
                        new_game()
                    elif button == records_button:
                        records()
        if button == new_game_button:
            pygame.draw.polygon(menu, (0, 0, 255),
                                ((text_x - 30, text_y + 5), (text_x - 10, text_y + 15), (text_x - 30, text_y + 25)))
        elif button == records_button:
            pygame.draw.polygon(menu, (0, 0, 255), ((text_x2 - 30, text_y2 + 5),
                                                    (text_x2 - 10, text_y2 + 15), (text_x2 - 30, text_y2 + 25)))
        pygame.display.flip()


def new_game():
    red_death = 0
    blue_death = 0
    pink_death = 0
    orange_death = 0
    right = 'right'
    left = 'left'
    up = 'up'
    down = 'down'
    game = True
    score = 0
    boost = 'boost'
    simple = 'simple'
    state = simple
    timer = 150
    ghosts = pygame.sprite.Group()
    red_ghost = pygame.sprite.Sprite()
    block = pygame.Surface((24, 24))
    block.fill(pygame.Color('red'))
    red_ghost.image = block
    red_ghost.rect = red_ghost.image.get_rect()
    red_ghost.rect.x = 12
    red_ghost.rect.y = 12
    pink_ghost = pygame.sprite.Sprite()
    block = pygame.Surface((24, 24))
    block.fill(pygame.Color('pink'))
    pink_ghost.image = block
    pink_ghost.rect = pink_ghost.image.get_rect()
    pink_ghost.rect.x = 444
    pink_ghost.rect.y = 12
    orange_ghost = pygame.sprite.Sprite()
    block = pygame.Surface((24, 24))
    block.fill(pygame.Color('orange'))
    orange_ghost.image = block
    orange_ghost.rect = orange_ghost.image.get_rect()
    orange_ghost.rect.x = 12
    orange_ghost.rect.y = 444
    blue_ghost = pygame.sprite.Sprite()
    block = pygame.Surface((24, 24))
    block.fill((50, 50, 255))
    blue_ghost.image = block
    blue_ghost.rect = blue_ghost.image.get_rect()
    blue_ghost.rect.x = 444
    blue_ghost.rect.y = 444
    ghosts.add(red_ghost)
    ghosts.add(blue_ghost)
    ghosts.add(pink_ghost)
    ghosts.add(orange_ghost)
    all_sprites = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    balls = pygame.sprite.Group()
    energizers = pygame.sprite.Group()
    pacman = pygame.sprite.Sprite()
    block = pygame.Surface((12, 12))
    block.fill(pygame.Color('yellow'))
    pacman.image = block
    pacman.rect = pacman.image.get_rect()
    pacman_direction = right
    pacman.rect.x = 12 * 19 + 4
    pacman.rect.y = 12 * 30 + 4
    all_sprites.add(pacman)
    fps = 30
    size = (480, 530)
    screen = pygame.display.set_mode(size)
    f = open(os.path.join('data', 'map'))
    lines = f.read().split()
    for a in range(40):
        for b in range(40):
            if lines[b][a] == '1':
                walls.add(Wall(a, b))
            elif lines[b][a] == '0':
                balls.add(Ball(a, b))
            elif lines[b][a] == '2' and lines[b + 1][a + 1] == '2':
                energizers.add(Energizer(a, b))
    walls.draw(screen)
    balls.draw(screen)
    energizers.draw(screen)
    font = pygame.font.Font(None, 30)
    text = font.render(f'Score: {score}', 1, (0, 0, 255))
    text_x = 10
    text_y = 490
    screen.blit(text, (text_x, text_y))
    pygame.display.flip()
    clock = pygame.time.Clock()
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = False
                elif event.key == pygame.K_RIGHT:
                    pacman.rect.x += 3
                    if pygame.sprite.spritecollideany(pacman, walls):
                        pacman.rect.x -= 3
                    else:
                        pacman_direction = right
                        pacman.rect.x -= 3
                elif event.key == pygame.K_LEFT:
                    pacman_direction = left
                    pacman.rect.x -= 3
                    if pygame.sprite.spritecollideany(pacman, walls):
                        pacman.rect.x += 3
                    else:
                        pacman_direction = left
                        pacman.rect.x += 3
                elif event.key == pygame.K_UP:
                    pacman_direction = up
                    pacman.rect.y -= 3
                    if pygame.sprite.spritecollideany(pacman, walls):
                        pacman.rect.y += 3
                    else:
                        pacman_direction = up
                        pacman.rect.y += 3
                elif event.key == pygame.K_DOWN:
                    pacman_direction = down
                    pacman.rect.y += 3
                    if pygame.sprite.spritecollideany(pacman, walls):
                        pacman.rect.y -= 3
                    else:
                        pacman_direction = down
                        pacman.rect.y -= 3
        screen.fill((0, 0, 0))
        if pacman_direction == right:
            pacman.rect.x += 3
            if pygame.sprite.spritecollideany(pacman, walls):
                pacman.rect.x -= 3
            elif pygame.sprite.spritecollideany(pacman, balls):
                pygame.sprite.groupcollide(all_sprites, balls, dokilla=False, dokillb=True)
                score += 10
            elif pygame.sprite.spritecollideany(pacman, energizers):
                pygame.sprite.groupcollide(all_sprites, energizers, dokilla=False, dokillb=True)
                score += 50
                state = boost
                timer = 150
        elif pacman_direction == left:
            pacman.rect.x -= 3
            if pygame.sprite.spritecollideany(pacman, walls):
                pacman.rect.x += 3
            if pygame.sprite.spritecollideany(pacman, balls):
                pygame.sprite.groupcollide(all_sprites, balls, dokilla=False, dokillb=True)
                score += 10
            if pygame.sprite.spritecollideany(pacman, energizers):
                pygame.sprite.groupcollide(all_sprites, energizers, dokilla=False, dokillb=True)
                score += 50
                state = boost
                timer = 150
        elif pacman_direction == up:
            pacman.rect.y -= 3
            if pygame.sprite.spritecollideany(pacman, walls):
                pacman.rect.y += 3
            if pygame.sprite.spritecollideany(pacman, balls):
                pygame.sprite.groupcollide(all_sprites, balls, dokilla=False, dokillb=True)
                score += 10
            if pygame.sprite.spritecollideany(pacman, energizers):
                pygame.sprite.groupcollide(all_sprites, energizers, dokilla=False, dokillb=True)
                score += 50
                state = boost
                timer = 150
        elif pacman_direction == down:
            pacman.rect.y += 3
            if pygame.sprite.spritecollideany(pacman, walls):
                pacman.rect.y -= 3
            if pygame.sprite.spritecollideany(pacman, balls):
                pygame.sprite.groupcollide(all_sprites, balls, dokilla=False, dokillb=True)
                score += 10
            if pygame.sprite.spritecollideany(pacman, energizers):
                pygame.sprite.groupcollide(all_sprites, energizers, dokilla=False, dokillb=True)
                score += 50
                state = boost
                timer = 150
        pacman.rect.x = pacman.rect.x % 480
        if timer != 150 and timer != 0:
            timer -= 1
        elif timer == 150 and state == boost:
            timer -= 1
        elif timer == 0:
            state = simple
            timer = 150
        if pygame.sprite.spritecollideany(pacman, ghosts) and state == simple:
            game = False
        all_sprites.draw(screen)
        walls.draw(screen)
        balls.draw(screen)
        energizers.draw(screen)
        if state == boost:
            block = pygame.Surface((24, 24))
            block.fill(pygame.Color('green'))
            red_ghost.image = block
            block = pygame.Surface((24, 24))
            block.fill(pygame.Color('green'))
            pink_ghost.image = block
            block = pygame.Surface((24, 24))
            block.fill(pygame.Color('green'))
            orange_ghost.image = block
            block = pygame.Surface((24, 24))
            block.fill(pygame.Color('green'))
            blue_ghost.image = block
            if pygame.sprite.spritecollide(pacman, ghosts, dokill=False) == [red_ghost]:
                red_ghost.rect.x = -24
                red_ghost.rect.y = -24
                red_death += 1
                score += 200
            if pygame.sprite.spritecollide(pacman, ghosts, dokill=False) == [blue_ghost]:
                blue_ghost.rect.x = -24
                blue_ghost.rect.y = -24
                blue_death += 1
                score += 200
            if pygame.sprite.spritecollide(pacman, ghosts, dokill=False) == [pink_ghost]:
                pink_ghost.rect.x = -24
                pink_ghost.rect.y = -24
                pink_death += 1
                score += 200
            if pygame.sprite.spritecollide(pacman, ghosts, dokill=False) == [orange_ghost]:
                orange_ghost.rect.x = -24
                orange_ghost.rect.y = -24
                orange_death += 1
                score += 200
        else:
            block = pygame.Surface((24, 24))
            block.fill(pygame.Color('red'))
            red_ghost.image = block
            block = pygame.Surface((24, 24))
            block.fill(pygame.Color('pink'))
            pink_ghost.image = block
            block = pygame.Surface((24, 24))
            block.fill(pygame.Color('orange'))
            orange_ghost.image = block
            block = pygame.Surface((24, 24))
            block.fill((50, 50, 255))
            blue_ghost.image = block
            if red_ghost.rect.y == pacman.rect.y:
                if red_ghost.rect.x > pacman.rect.x:
                    red_ghost.rect.x -= 2
                    if pygame.sprite.spritecollideany(red_ghost, walls):
                        red_ghost.rect.x += 2
                else:
                    red_ghost.rect.x += 2
                    if pygame.sprite.spritecollideany(red_ghost, walls):
                        red_ghost.rect.x -= 2
            elif red_ghost.rect.y > pacman.rect.y:
                red_ghost.rect.y -= 2
                if pygame.sprite.spritecollideany(red_ghost, walls):
                    red_ghost.rect.y += 2
                    if red_ghost.rect.x > pacman.rect.x:
                        red_ghost.rect.x -= 2
                        if pygame.sprite.spritecollideany(red_ghost, walls):
                            red_ghost.rect.x += 2
                    else:
                        red_ghost.rect.x += 2
                        if pygame.sprite.spritecollideany(red_ghost, walls):
                            red_ghost.rect.x -= 2
            elif red_ghost.rect.y < pacman.rect.y:
                red_ghost.rect.y += 2
                if pygame.sprite.spritecollideany(red_ghost, walls):
                    red_ghost.rect.y -= 2
                    if red_ghost.rect.x > pacman.rect.x:
                        red_ghost.rect.x -= 2
                        if pygame.sprite.spritecollideany(red_ghost, walls):
                            red_ghost.rect.x += 2
                    else:
                        red_ghost.rect.x += 2
                        if pygame.sprite.spritecollideany(red_ghost, walls):
                            red_ghost.rect.x -= 2
            if blue_ghost.rect.y == pacman.rect.y:
                if blue_ghost.rect.x > pacman.rect.x:
                    blue_ghost.rect.x -= 2
                    if pygame.sprite.spritecollideany(blue_ghost, walls):
                        blue_ghost.rect.x += 2
                else:
                    blue_ghost.rect.x += 2
                    if pygame.sprite.spritecollideany(blue_ghost, walls):
                        blue_ghost.rect.x -= 2
            elif blue_ghost.rect.y > pacman.rect.y:
                blue_ghost.rect.y -= 2
                if pygame.sprite.spritecollideany(blue_ghost, walls):
                    blue_ghost.rect.y += 2
                    if blue_ghost.rect.x > pacman.rect.x:
                        blue_ghost.rect.x -= 2
                        if pygame.sprite.spritecollideany(blue_ghost, walls):
                            blue_ghost.rect.x += 2
                    else:
                        blue_ghost.rect.x += 2
                        if pygame.sprite.spritecollideany(blue_ghost, walls):
                            blue_ghost.rect.x -= 2
            elif blue_ghost.rect.y < pacman.rect.y:
                blue_ghost.rect.y += 2
                if pygame.sprite.spritecollideany(blue_ghost, walls):
                    blue_ghost.rect.y -= 2
                    if blue_ghost.rect.x > pacman.rect.x:
                        blue_ghost.rect.x -= 2
                        if pygame.sprite.spritecollideany(blue_ghost, walls):
                            blue_ghost.rect.x += 2
                    else:
                        blue_ghost.rect.x += 2
                        if pygame.sprite.spritecollideany(blue_ghost, walls):
                            blue_ghost.rect.x -= 2
            if pink_ghost.rect.y == pacman.rect.y:
                if pink_ghost.rect.x > pacman.rect.x:
                    pink_ghost.rect.x -= 2
                    if pygame.sprite.spritecollideany(pink_ghost, walls):
                        pink_ghost.rect.x += 2
                else:
                    pink_ghost.rect.x += 2
                    if pygame.sprite.spritecollideany(pink_ghost, walls):
                        pink_ghost.rect.x -= 2
            elif pink_ghost.rect.y > pacman.rect.y:
                pink_ghost.rect.y -= 2
                if pygame.sprite.spritecollideany(pink_ghost, walls):
                    pink_ghost.rect.y += 2
                    if pink_ghost.rect.x > pacman.rect.x:
                        pink_ghost.rect.x -= 2
                        if pygame.sprite.spritecollideany(pink_ghost, walls):
                            pink_ghost.rect.x += 2
                    else:
                        pink_ghost.rect.x += 2
                        if pygame.sprite.spritecollideany(pink_ghost, walls):
                            pink_ghost.rect.x -= 2
            elif pink_ghost.rect.y < pacman.rect.y:
                pink_ghost.rect.y += 2
                if pygame.sprite.spritecollideany(pink_ghost, walls):
                    pink_ghost.rect.y -= 2
                    if pink_ghost.rect.x > pacman.rect.x:
                        pink_ghost.rect.x -= 2
                        if pygame.sprite.spritecollideany(pink_ghost, walls):
                            pink_ghost.rect.x += 2
                    else:
                        pink_ghost.rect.x += 2
                        if pygame.sprite.spritecollideany(pink_ghost, walls):
                            pink_ghost.rect.x -= 2
            if orange_ghost.rect.y == pacman.rect.y:
                if orange_ghost.rect.x > pacman.rect.x:
                    orange_ghost.rect.x -= 2
                    if pygame.sprite.spritecollideany(orange_ghost, walls):
                        orange_ghost.rect.x += 2
                else:
                    orange_ghost.rect.x += 2
                    if pygame.sprite.spritecollideany(orange_ghost, walls):
                        orange_ghost.rect.x -= 2
            elif orange_ghost.rect.y > pacman.rect.y:
                orange_ghost.rect.y -= 2
                if pygame.sprite.spritecollideany(orange_ghost, walls):
                    orange_ghost.rect.y += 2
                    if orange_ghost.rect.x > pacman.rect.x:
                        orange_ghost.rect.x -= 2
                        if pygame.sprite.spritecollideany(orange_ghost, walls):
                            orange_ghost.rect.x += 2
                    else:
                        orange_ghost.rect.x += 2
                        if pygame.sprite.spritecollideany(orange_ghost, walls):
                            orange_ghost.rect.x -= 2
            elif orange_ghost.rect.y < pacman.rect.y:
                orange_ghost.rect.y += 2
                if pygame.sprite.spritecollideany(orange_ghost, walls):
                    orange_ghost.rect.y -= 2
                    if orange_ghost.rect.x > pacman.rect.x:
                        orange_ghost.rect.x -= 2
                        if pygame.sprite.spritecollideany(orange_ghost, walls):
                            orange_ghost.rect.x += 2
                    else:
                        orange_ghost.rect.x += 2
                        if pygame.sprite.spritecollideany(orange_ghost, walls):
                            orange_ghost.rect.x -= 2
        if 91 > red_death > 0:
            red_death += 1
        elif red_death == 91:
            red_ghost.rect.x = 12
            red_ghost.rect.y = 12
            red_death = 0
        if 91 > blue_death > 0:
            blue_death += 1
        elif blue_death == 91:
            blue_ghost.rect.x = 444
            blue_ghost.rect.y = 444
            blue_death = 0
        if 91 > pink_death > 0:
            pink_death += 1
        elif pink_death == 91:
            pink_ghost.rect.x = 444
            pink_ghost.rect.y = 12
            pink_death = 0
        if 91 > orange_death > 0:
            orange_death += 1
        elif orange_death == 91:
            orange_ghost.rect.x = 12
            orange_ghost.rect.y = 444
            orange_death = 0
        ghosts.draw(screen)
        clock.tick(fps)
        font = pygame.font.Font(None, 30)
        text = font.render(f'Score: {score}', 1, (0, 0, 255))
        text_x = 10
        text_y = 490
        screen.blit(text, (text_x, text_y))
        if len(balls) == 0 and len(energizers) == 0:
            game = False
        pygame.display.flip()
    game = True
    font = pygame.font.Font(os.path.join('data', 'PAC-FONT.TTF'), 15)
    text = font.render('Game over', 1, (255, 255, 255))
    text_x = 174
    text_y = 216
    screen.blit(text, (text_x, text_y))
    pygame.display.flip()
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = False
    f.close()
    with open(os.path.join('data', 'records_list'), 'r') as f:
        records = list(map(int, f.read().split()))
        records.append(score)
        records = sorted(records, reverse=True)[:10]
    with open(os.path.join('data', 'records_list'), 'w') as f:
        data = ''
        for r in records:
            data += str(r)
            data += '\n'
        f.truncate()
        f.write(data)
    main_menu()


def records():
    with open(os.path.join('data', 'records_list')) as f:
        record_list = f.read().split()
        record_menu = True
        width = 600
        records_screen = pygame.display.set_mode((600, 700))
        font = pygame.font.Font(os.path.join('data', 'PAC-FONT.TTF'), 50)
        text = font.render('Top records', 1, (0, 0, 255))
        text_x = width // 2 - text.get_width() // 2
        text_y = 20
        records_screen.blit(text, (text_x, text_y))
        k = 0
        for t in record_list:
            font = pygame.font.Font(None, 40)
            text = font.render(t, 1, (0, 0, 255))
            text_x = width // 2 - text.get_width() // 2
            text_y = 90 + k * 40
            records_screen.blit(text, (text_x, text_y))
            k += 1
        pygame.display.flip()
        while record_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        record_menu = False
        main_menu()


main_menu()
