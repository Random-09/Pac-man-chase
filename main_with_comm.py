import sys
import pygame
import pygame_gui  # необходимые библиотеки

MENU_SIZE = 430, 430
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 670, 800
TILE_SIZE = 24
GAME_EVENT_TYPE = pygame.USEREVENT + 1
pygame.time.set_timer(GAME_EVENT_TYPE, 150)
PACMAN_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(PACMAN_EVENT, 170)
SONG_END = pygame.USEREVENT + 3  # константы и события

POSITIONS = {
    'first_map.txt': {
        'pacman': (5, 15),
        'red': (9, 9),
        'pink': (18, 19),
        'blue': (26, 21),
        'orange': (2, 30)},
    'second_map.txt': {
        'pacman': (2, 19),
        'red': (21, 18),
        'pink': (9, 27),
        'blue': (9, 2),
        'orange': (2, 8)},
    'third_map.txt': {
        'pacman': (1, 27),
        'red': (26, 20),
        'pink': (12, 9),
        'blue': (4, 8),
        'orange': (1, 14)},
    'fourth_map.txt': {
        'pacman': (14, 30),
        'red': (26, 18),
        'pink': (1, 7),
        'blue': (6, 28),
        'orange': (7, 9)},
    'fifth_map.txt': {
        'pacman': (1, 30),
        'red': (12, 18),
        'pink': (21, 9),
        'blue': (15, 30),
        'orange': (5, 12)},
}  # Положения персонажей в зависимости от уровня


class Labyrinth:  # Класс, выстраивающий лабиринт и отвечающий за навигацию в нём
    def __init__(self, filename, free_tiles, finish_tile):
        """инициализатор класса"""
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
        """построение лабиринта"""
        colors = {0: (0, 0, 0), 1: (5, 5, 190), 2: (50, 50, 50)}
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size,
                                   self.tile_size, self.tile_size)
                screen.fill(colors[self.get_tile_id((x, y))], rect)

    def get_tile_id(self, position):
        """вспомогательный метод, возвращающий id тайла"""
        return self.map[position[1]][position[0]]

    def is_free(self, position):
        """вспомогательный метод, возвращающий True/False если клетка свободна/занята"""
        return self.get_tile_id(position) in self.free_tiles

    def find_path_step(self, start, target, direction):
        """алгоритм построения маршрута для призраков (поиск следующего тайла)"""
        x, y = start
        xt, yt = target
        tile_list = []
        distance = []
        if direction == 'up':
            if self.is_free((x, y - 1)):
                tile_list.append((x, y - 1))
            if self.is_free((x - 1, y)):
                tile_list.append((x - 1, y))
            if self.is_free((x + 1, y)):
                tile_list.append((x + 1, y))
        if direction == 'down':
            if self.is_free((x - 1, y)):
                tile_list.append((x - 1, y))
            if self.is_free((x, y + 1)):
                tile_list.append((x, y + 1))
            if self.is_free((x + 1, y)):
                tile_list.append((x + 1, y))
        if direction == 'right':
            if self.is_free((x, y - 1)):
                tile_list.append((x, y - 1))
            if self.is_free((x, y + 1)):
                tile_list.append((x, y + 1))
            if self.is_free((x + 1, y)):
                tile_list.append((x + 1, y))
        if direction == 'left':
            if self.is_free((x, y - 1)):
                tile_list.append((x, y - 1))
            if self.is_free((x - 1, y)):
                tile_list.append((x - 1, y))
            if self.is_free((x, y + 1)):
                tile_list.append((x, y + 1))
        for tile in tile_list:
            xn, yn = tile
            distance.append(abs(xn - xt) ** 2 + abs(yn - yt) ** 2)
        return tile_list[distance.index(min(distance))]


class Pacman:  # класс Пакмена
    def __init__(self, position):
        """инициализатор класса"""
        self.next_direction = ''
        self.current_direction = 'left'
        self.x, self.y = position

    # вспомогательные методы, возвращающие информацию о положении Пакмена / выставляющие эти значения
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
        """метод рендера героя на экран"""
        center = self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, (255, 255, 0), center, TILE_SIZE // 2)


class Red:  # Класс красного призрака
    def __init__(self, position):
        """инициализатор класса"""
        self.direction = 'up'
        self.x, self.y = position
        self.delay = 200
        self.image = pygame.image.load(f'characters/red/{self.direction}1.png')
        self.image1 = pygame.transform.scale(self.image, (24, 24))
        self.count = 0
        pygame.time.set_timer(GAME_EVENT_TYPE, self.delay)

    # вспомогательные методы, возвращающие информацию о положении призрака / выставляющие эти значения
    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def get_direction(self):
        return self.direction

    def set_direction(self, direction):
        self.direction = direction

    def update_image(self):
        """метод обновления текстуры призрака"""
        self.image = pygame.image.load(f'characters/red/{self.direction}{self.count % 2}.png')
        self.image1 = pygame.transform.scale(self.image, (24, 24))
        self.count += 1

    def render(self, screen):
        """метод рендера призрака на экран"""
        delta = (self.image1.get_width() - TILE_SIZE) // 2
        screen.blit(self.image1, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))


class Pink:  # Класс розового призрака
    def __init__(self, position):
        """инициализатор класса"""
        self.direction = 'up'
        self.x, self.y = position
        self.delay = 200
        self.image = pygame.image.load(f'characters/pink/{self.direction}1.png')
        self.image1 = pygame.transform.scale(self.image, (24, 24))
        self.count = 0
        pygame.time.set_timer(GAME_EVENT_TYPE, self.delay)

    # вспомогательные методы, возвращающие информацию о положении призрака / выставляющие эти значения
    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def get_direction(self):
        return self.direction

    def set_direction(self, direction):
        self.direction = direction

    def update_image(self):
        """метод обновления текстуры призрака"""
        self.image = pygame.image.load(f'characters/pink/{self.direction}{self.count % 2}.png')
        self.image1 = pygame.transform.scale(self.image, (24, 24))
        self.count += 1

    def render(self, screen):
        """метод рендера призрака на экран"""
        delta = (self.image1.get_width() - TILE_SIZE) // 2
        screen.blit(self.image1, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))


class Blue:  # Класс голубого призрака
    def __init__(self, position):
        """инициализатор класса"""
        self.direction = 'up'
        self.x, self.y = position
        self.delay = 100
        self.image = pygame.image.load(f'characters/blue/{self.direction}1.png')
        self.image1 = pygame.transform.scale(self.image, (24, 24))
        self.count = 0
        pygame.time.set_timer(GAME_EVENT_TYPE, self.delay)

    # вспомогательные методы, возвращающие информацию о положении призрака / выставляющие эти значения
    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def get_direction(self):
        return self.direction

    def set_direction(self, direction):
        self.direction = direction

    def update_image(self):
        """метод обновления текстуры призрака"""
        self.image = pygame.image.load(f'characters/blue/{self.direction}{self.count % 2}.png')
        self.image1 = pygame.transform.scale(self.image, (24, 24))
        self.count += 1

    def render(self, screen):
        """метод рендера призрака на экран"""
        delta = (self.image1.get_width() - TILE_SIZE) // 2
        screen.blit(self.image1, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))


class Orange:  # Класс оранжевого призрака
    def __init__(self, position):
        """инициализатор класса"""
        self.direction = 'up'
        self.x, self.y = position
        self.delay = 200
        self.image = pygame.image.load(f'characters/orange/{self.direction}1.png')
        self.image1 = pygame.transform.scale(self.image, (24, 24))
        self.count = 0
        pygame.time.set_timer(GAME_EVENT_TYPE, self.delay)

    # вспомогательные методы, возвращающие информацию о положении призрака / выставляющие эти значения
    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def get_direction(self):
        return self.direction

    def set_direction(self, direction):
        self.direction = direction

    def update_image(self):
        """метод обновления текстуры призрака"""
        self.image = pygame.image.load(f'characters/orange/{self.direction}{self.count % 2}.png')
        self.image1 = pygame.transform.scale(self.image, (24, 24))
        self.count += 1

    def render(self, screen):
        """метод рендера призрака на экран"""
        delta = (self.image1.get_width() - TILE_SIZE) // 2
        screen.blit(self.image1, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))


class Game:  # Класс, управляющий игрой
    def __init__(self, labyrinth, pacman, red, pink, blue, orange):
        """инициализвтор класса"""
        self.labyrinth = labyrinth
        self.pacman = pacman
        self.red = red
        self.pink = pink
        self.blue = blue
        self.orange = orange

    def render(self, screen):
        """рендер персонажей на экран"""
        self.labyrinth.render(screen)
        self.pacman.render(screen)
        self.red.render(screen)
        self.pink.render(screen)
        self.blue.render(screen)
        self.orange.render(screen)

    def direct_pacman(self):
        """метод, изменяющий следующее направление движения пакмена"""
        if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
            self.pacman.set_next_dir('left')
        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
            self.pacman.set_next_dir('right')
        if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
            self.pacman.set_next_dir('up')
        if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
            self.pacman.set_next_dir('down')

    def update_direct_pacman(self):
        """метод, выставляющий следующее направление пакмена, если такой поворот возможен"""
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
        """метод перемещения красного призрака"""
        target = self.pacman.get_position()
        next_position = self.labyrinth.find_path_step(self.red.get_position(), target,
                                                      self.red.get_direction())
        self.red.set_direction(find_direction(self.red.get_position(), next_position))
        self.red.set_position(next_position)
        self.red.update_image()

    def move_pink(self):
        """метод перемещения розового призрака"""
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
        self.pink.update_image()

    def move_blue(self):
        """метод перемещения голубого призрака"""
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
        next_position = self.labyrinth.find_path_step(self.blue.get_position(), target,
                                                      self.blue.get_direction())
        self.blue.set_direction(find_direction(self.blue.get_position(), next_position))
        self.blue.set_position(next_position)
        self.blue.update_image()

    def move_orange(self):
        """метод перемещения оранжевого призрака"""
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
        self.orange.update_image()

    def check_win(self):
        """проверка на победу"""
        return self.labyrinth.get_tile_id(self.pacman.get_position()) == self.labyrinth.finish_tile

    def check_lose(self):
        """проверка на поражение"""
        return self.pacman.get_position() == self.red.get_position() or \
               self.pacman.get_position() == self.orange.get_position() or \
               self.pacman.get_position() == self.pink.get_position() or \
               self.pacman.get_position() == self.blue.get_position()


def find_direction(start, target):
    """Функция, определяющая направление движения призрака, исходя из текущего и следующего положения"""
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


def show_message(screen, message1, message2):
    """Фунция вывода сообщеня на экран в конце игры"""
    font = pygame.font.Font(None, 50)
    text1 = font.render(message1, True, (50, 70, 0))
    text2 = font.render(message2, True, (50, 70, 0))
    text_x = WINDOW_WIDTH // 2 - text1.get_width() // 2
    text_y = WINDOW_HEIGHT // 2 - text1.get_height() // 2
    text_w = text1.get_width()
    text_h = text1.get_height()
    pygame.draw.rect(screen, (200, 150, 50), (text_x - 10, text_y - 10,
                                              text_w + 20, text_h + 20))
    screen.blit(text1, (text_x, text_y))

    text_x1 = WINDOW_WIDTH // 2 - text2.get_width() // 2
    text_y1 = WINDOW_HEIGHT // 2 - text2.get_height() // 2
    text_w1 = text2.get_width()
    text_h1 = text2.get_height()
    pygame.draw.rect(screen, (200, 150, 50), (text_x1 - 10, text_y1 + 40,
                                              text_w1 + 20, text_h1 + 20))

    screen.blit(text2, (text_x1, text_y1 + 50))


def terminate():
    """Функция закрытия игры"""
    pygame.quit()
    sys.exit()


def load_menu():
    """Функция загрузки и обработки меню"""
    pygame.init()
    pygame.display.set_caption('Pac-man: chase!')
    manager = pygame_gui.UIManager(MENU_SIZE)
    screen = pygame.display.set_mode(MENU_SIZE)
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("Pac-man: chase!", True, (254, 254, 34))
    text_x = 20
    text_y = 20
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (254, 254, 34), (text_x - 10, text_y - 10,
                                              text_w + 20, text_h + 20), 1)

    instrusction_font = pygame.font.SysFont('Comic Sans MS', 18)
    instruction1 = instrusction_font.render('Проведите пакмена через', True, (65, 65, 190))
    instruction2 = instrusction_font.render('систему лабиринтов на свободу.', True, (65, 65, 190))
    instruction3 = instrusction_font.render('Чтобы пройти лабиринт нужно', True, (65, 65, 190))
    instruction4 = instrusction_font.render('дойти до серой клетки, избегая', True, (65, 65, 190))
    instruction5 = instrusction_font.render('призраков. Для управления', True, (65, 65, 190))
    instruction6 = instrusction_font.render('используйте клавиши со стрелками', True, (65, 65, 190))
    instruction7 = instrusction_font.render('или AWSD. Смена уровня возможна', True, (65, 65, 190))
    instruction8 = instrusction_font.render('только в меню. Приятной игры!', True, (65, 65, 190))
    screen.blit(instruction1, (12, 70))
    screen.blit(instruction2, (12, 90))
    screen.blit(instruction3, (12, 120))
    screen.blit(instruction4, (12, 140))
    screen.blit(instruction5, (12, 160))
    screen.blit(instruction6, (12, 180))
    screen.blit(instruction7, (12, 200))
    screen.blit(instruction8, (12, 220))

    select = pygame.mixer.Sound('sounds/button.wav')

    but1 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((340, 70), (90, 50)),
        text='1 уровень',
        manager=manager
    )
    but2 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((340, 130), (90, 50)),
        text='2 уровень',
        manager=manager
    )
    but3 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((340, 190), (90, 50)),
        text='3 уровень',
        manager=manager
    )
    but4 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((340, 250), (90, 50)),
        text='4 уровень',
        manager=manager
    )
    but5 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((340, 310), (90, 50)),
        text='5 уровень',
        manager=manager
    )

    running = True
    clock = pygame.time.Clock()

    while running:  # цикл меню
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    select.play()
                    if event.ui_element == but1:
                        main('first_map.txt')
                        running = False
                    if event.ui_element == but2:
                        main('second_map.txt')
                        running = False
                    if event.ui_element == but3:
                        main('third_map.txt')
                        running = False
                    if event.ui_element == but4:
                        main('fourth_map.txt')
                        running = False
                    if event.ui_element == but5:
                        main('fifth_map.txt')
                        running = False
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
    pygame.quit()


def main(map):
    """Главный игровой цикл"""
    pygame.init()
    pygame.display.set_caption('Pac-man: chase!')
    screen = pygame.display.set_mode(WINDOW_SIZE)

    manager = pygame_gui.UIManager(WINDOW_SIZE)

    labyrinth = Labyrinth(f'maps/{map}', [0, 2], 2)
    pacman = Pacman(POSITIONS[map]['pacman'])
    red = Red(POSITIONS[map]['red'])
    pink = Pink(POSITIONS[map]['pink'])
    blue = Blue(POSITIONS[map]['blue'])
    orange = Orange(POSITIONS[map]['orange'])
    game = Game(labyrinth, pacman, red, pink, blue, orange)

    pygame.mixer.music.set_endevent(SONG_END)
    pygame.mixer.music.load('sounds/start-up.wav')
    pygame.mixer.music.play()

    victory = pygame.mixer.Sound('sounds/victory.wav')
    lose = pygame.mixer.Sound('sounds/lose.wav')
    sound_not_played1 = True
    sound_not_played2 = True

    menu_but = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((250, 0), (50, 40)),
        text='Меню',
        manager=manager
    )
    revert_but = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((305, 0), (120, 40)),
        text='Начать заново',
        manager=manager
    )

    clock = pygame.time.Clock()
    running = True
    game_over = False
    game_start = False
    game_start_time = pygame.time.get_ticks() + 4500
    while running:
        current_time = pygame.time.get_ticks()
        time_delta = clock.tick(60) / 1000.0
        if current_time > game_start_time:
            game_start = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == SONG_END:
                pygame.mixer.music.load('sounds/siren.wav')
                pygame.mixer.music.play(-1)
            elif event.type == GAME_EVENT_TYPE and not game_over and game_start:
                game.move_red()
                game.move_pink()
                game.move_blue()
                game.move_orange()
            elif event.type == PACMAN_EVENT and not game_over and game_start:
                game.update_direct_pacman()
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == menu_but:
                        running = False
                        game_start = False
                        pygame.mixer.music.pause()
                        lose.stop()
                        victory.stop()
                        load_menu()
                    elif event.ui_element == revert_but:
                        game_start = False
                        lose.stop()
                        victory.stop()
                        main(map)
            manager.process_events(event)
        game.direct_pacman()
        screen.fill((0, 0, 0))
        game.render(screen)
        manager.update(time_delta)
        manager.draw_ui(screen)
        if game.check_win():
            if map != 'fifth_map.txt':
                game_over = True
                show_message(screen, 'Вы выиграли!', 'Попробуйте и другие уровни')
            else:
                game_over = True
                show_message(screen, 'Вы прошли последний уровень!', 'Поздравляем с победой!')
            pygame.mixer.music.pause()
            if sound_not_played1:
                victory.play(0)
                sound_not_played1 = False
        if game.check_lose():
            game_over = True
            show_message(screen, 'Вы проиграли!', 'Попробуйте снова')
            pygame.mixer.music.pause()
            if sound_not_played2:
                sound_not_played2 = False
                lose.play(0)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':  # Запуск меню
    load_menu()
