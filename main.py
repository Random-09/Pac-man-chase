import pygame

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 900, 1000  # 480, 480 для "simple_map.txt"
FPS = 16                                              # 900, 1000 для "orig_map.txt"
TILE_SIZE = 32
GAME_EVENT_TYPE = pygame.USEREVENT + 6


class Labyrinth:
    def __init__(self, filename, free_tiles, finish_tile):
        self.map = []
        with open(f'{filename}') as input_file:
            for line in input_file:
                self.map.append(list(map(int, line.split())))
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.tile_size = TILE_SIZE
        self.free_tiles = free_tiles
        self.finish_tile = finish_tile

    def render(self, screen):
        colors = {0: (0, 0, 0), 1: (120, 120, 120), 2: (50, 50, 50)}
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size,
                                   self.tile_size, self.tile_size)
                screen.fill(colors[self.get_tile_id((x, y))], rect)

    def get_tile_id(self, position):
        return self.map[position[1]][position[0]]

    def is_free(self, position):
        return self.get_tile_id(position) in self.free_tiles

    def find_path_step(self, start, target, direction):  # сократить (по возможности)
        x, y = start
        xt, yt = target
        tile_list = []
        distance = []
        if direction == 'up':
            if self.is_free((x, y - 1)):  # up
                tile_list.append((x, y - 1))
            if self.is_free((x - 1, y)):  # left
                tile_list.append((x - 1, y))
            if self.is_free((x + 1, y)):  # right
                tile_list.append((x + 1, y))
        if direction == 'down':
            if self.is_free((x - 1, y)):  # left
                tile_list.append((x - 1, y))
            if self.is_free((x, y + 1)):  # down
                tile_list.append((x, y + 1))
            if self.is_free((x + 1, y)):  # right
                tile_list.append((x + 1, y))
        if direction == 'right':
            if self.is_free((x, y - 1)):  # up
                tile_list.append((x, y - 1))
            if self.is_free((x, y + 1)):  # down
                tile_list.append((x, y + 1))
            if self.is_free((x + 1, y)):  # right
                tile_list.append((x + 1, y))
        if direction == 'left':
            if self.is_free((x, y - 1)):  # up
                tile_list.append((x, y - 1))
            if self.is_free((x - 1, y)):  # left
                tile_list.append((x - 1, y))
            if self.is_free((x, y + 1)):  # down
                tile_list.append((x, y + 1))
        for tile in tile_list:
            xn, yn = tile
            distance.append(abs(xn - xt) ** 2 + abs(yn - yt) ** 2)
        return tile_list[distance.index(min(distance))]


class Pacman:
    def __init__(self, position):
        self.next_direction = ''
        self.current_direction = 'left'
        self.x, self.y = position

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def get_curr_dir(self):
        return self.current_direction

    def get_next_dir(self):
        return self.next_direction

    def set_next_dir(self, direction):
        self.next_direction = direction

    def set_curr_dir(self, direction):
        self.current_direction = direction
        self.next_direction = ''

    def render(self, screen):
        center = self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, (255, 255, 0), center, TILE_SIZE // 2)


class Red:
    def __init__(self, position):
        self.direction = 'up'
        self.x, self.y = position
        self.delay = 200
        pygame.time.set_timer(GAME_EVENT_TYPE, self.delay)

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def get_direction(self):
        return self.direction

    def set_direction(self, direction):
        self.direction = direction

    def render(self, screen):
        center = self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, pygame.Color('red'), center, TILE_SIZE // 2)


class Pink:
    def __init__(self, position):
        self.direction = 'up'
        self.x, self.y = position
        self.delay = 200
        pygame.time.set_timer(GAME_EVENT_TYPE, self.delay)

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def get_direction(self):
        return self.direction

    def set_direction(self, direction):
        self.direction = direction

    def render(self, screen):
        center = self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, pygame.Color('pink'), center, TILE_SIZE // 2)


class Blue:
    def __init__(self, position):
        self.direction = 'up'
        self.x, self.y = position
        self.delay = 100
        pygame.time.set_timer(GAME_EVENT_TYPE, self.delay)

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def get_direction(self):
        return self.direction

    def set_direction(self, direction):
        self.direction = direction

    def render(self, screen):
        center = self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, pygame.Color('blue'), center, TILE_SIZE // 2)


class Orange:
    def __init__(self, position):
        self.direction = 'up'
        self.x, self.y = position
        self.delay = 200
        pygame.time.set_timer(GAME_EVENT_TYPE, self.delay)

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def get_direction(self):
        return self.direction

    def set_direction(self, direction):
        self.direction = direction

    def render(self, screen):
        center = self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, pygame.Color('orange'), center, TILE_SIZE // 2)


class Game:
    def __init__(self, labyrinth, pacman, red, pink, blue, orange):
        self.labyrinth = labyrinth
        self.pacman = pacman
        self.red = red
        self.pink = pink
        self.blue = blue
        self.orange = orange

    def render(self, screen):
        self.labyrinth.render(screen)
        self.pacman.render(screen)
        self.red.render(screen)
        self.pink.render(screen)
        self.blue.render(screen)
        self.orange.render(screen)

    def direct_pacman(self):
        if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
            self.pacman.set_next_dir('left')
        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
            self.pacman.set_next_dir('right')
        if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
            self.pacman.set_next_dir('up')
        if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
            self.pacman.set_next_dir('down')

    def update_direct_pacman(self):  # Требуется оптимизация кода и скорости реагирования
        next_x, next_y = self.pacman.get_position()
        if self.pacman.get_next_dir() == 'up':
            if self.labyrinth.is_free((next_x, next_y - 1)):
                self.pacman.set_curr_dir('up')
        if self.pacman.get_next_dir() == 'down':
            if self.labyrinth.is_free((next_x, next_y + 1)):
                self.pacman.set_curr_dir('down')
        if self.pacman.get_next_dir() == 'right':
            if self.labyrinth.is_free((next_x + 1, next_y)):
                self.pacman.set_curr_dir('right')
        if self.pacman.get_next_dir() == 'left':
            if self.labyrinth.is_free((next_x - 1, next_y)):
                self.pacman.set_curr_dir('left')

        if self.pacman.get_curr_dir() == 'up':
            next_y -= 1
        if self.pacman.get_curr_dir() == 'down':
            next_y += 1
        if self.pacman.get_curr_dir() == 'right':
            next_x += 1
        if self.pacman.get_curr_dir() == 'left':
            next_x -= 1
        if self.labyrinth.is_free((next_x, next_y)):
            self.pacman.set_position((next_x, next_y))

    def move_red(self):
        next_position = self.labyrinth.find_path_step(self.red.get_position(), self.pacman.get_position(),
                                                      self.red.get_direction())
        self.red.set_direction(find_direction(self.red.get_position(), next_position))
        self.red.set_position(next_position)

    def move_pink(self):
        direction = self.pacman.get_curr_dir()
        target = ()
        if direction == 'up':
            target = self.pacman.get_position()[0] - 4, self.pacman.get_position()[1] - 4
        if direction == 'down':
            target = self.pacman.get_position()[0], self.pacman.get_position()[1] + 4
        if direction == 'right':
            target = self.pacman.get_position()[0] + 4, self.pacman.get_position()[1]
        if direction == 'left':
            target = self.pacman.get_position()[0] - 4, self.pacman.get_position()[1]
        next_position = self.labyrinth.find_path_step(self.pink.get_position(), target,
                                                      self.pink.get_direction())
        self.pink.set_direction(find_direction(self.pink.get_position(), next_position))
        self.pink.set_position(next_position)

    def move_blue(self):
        direction = self.pacman.get_curr_dir()
        center = ()
        if direction == 'up':
            center = self.pacman.get_position()[0] - 2, self.pacman.get_position()[1] - 2
        if direction == 'down':
            center = self.pacman.get_position()[0], self.pacman.get_position()[1] + 2
        if direction == 'right':
            center = self.pacman.get_position()[0] + 2, self.pacman.get_position()[1]
        if direction == 'left':
            center = self.pacman.get_position()[0] - 2, self.pacman.get_position()[1]
        xc, yc = center
        xr, yr = self.red.get_position()
        target = 2 * xc - xr, 2 * yc - yr
        print(target)
        next_position = self.labyrinth.find_path_step(self.blue.get_position(), target,
                                                      self.blue.get_direction())
        self.blue.set_direction(find_direction(self.blue.get_position(), next_position))
        self.blue.set_position(next_position)

    def move_orange(self):
        x = abs(self.pacman.get_position()[0] - self.orange.get_position()[0])
        y = abs(self.pacman.get_position()[1] - self.orange.get_position()[1])
        distance = round((x ** 2 + y ** 2) ** 0.5)
        if distance >= 8:
            next_position = self.labyrinth.find_path_step(self.orange.get_position(),
                                                          self.pacman.get_position(),
                                                          self.orange.get_direction())
        else:
            next_position = self.labyrinth.find_path_step(self.orange.get_position(),
                                                          (1, 13), self.orange.get_direction())
        self.orange.set_direction(find_direction(self.orange.get_position(), next_position))
        self.orange.set_position(next_position)

    def check_win(self):
        return self.labyrinth.get_tile_id(self.pacman.get_position()) == self.labyrinth.finish_tile

    def check_lose(self):
        return self.pacman.get_position() == self.red.get_position() or\
               self.pacman.get_position() == self.orange.get_position()


def find_direction(start, target):
    x, y = start
    xn, yn = target
    if xn - x == 1:
        return 'right'
    if xn - x == -1:
        return 'left'
    if yn - y == 1:
        return 'down'
    if yn - y == - 1:
        return 'up'


def show_message(screen, message):
    font = pygame.font.Font(None, 50)
    text = font.render(message, True, (50, 70, 0))
    text_x = WINDOW_WIDTH // 2 - text.get_width() // 2
    text_y = WINDOW_HEIGHT // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (200, 150, 50), (text_x - 10, text_y - 10,
                                              text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    labyrinth = Labyrinth('orig_map.txt', [0, 2], 2)
    pacman = Pacman((1, 1))
    red = Red((14, 14))
    pink = Pink((1, 7))
    blue = Blue((14, 2))
    orange = Orange((2, 7))
    game = Game(labyrinth, pacman, red, pink, blue, orange)

    clock = pygame.time.Clock()
    running = True
    game_over = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == GAME_EVENT_TYPE and not game_over:
                game.update_direct_pacman()
                # game.move_red()
                # game.move_pink()
                game.move_blue()
                # game.move_orange()
        game.direct_pacman()
        screen.fill((0, 0, 0))
        game.render(screen)
        if game.check_win():
            game_over = True
            show_message(screen, 'You won!')
        if game.check_lose():
            game_over = True
            show_message(screen, 'You lost!')
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()


# TODO (для себя)
# Сделать алгоритм передвижения призраков как в оригинальном пакмане (СДЕЛАНО, ВЕРСИЯ 1.1 (приоритет поворотов,
#                                                                                          неоптимизированная))
# По возможности сократить и оптимизировать алгоритм

# Доделать других призраков

# Сделать персонажей спрайтами
# Сделать плавное перемещение всех персонажей

# Улучшить управление Пакмана, т.к. не всегда срабатывают повороты
