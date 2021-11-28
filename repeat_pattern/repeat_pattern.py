# repeat pattern
import random

import pygame

from typing import List
from typing import Tuple


WIDTH = 600
HEIGHT = 600
NUMBER_OF_BUTTONS = 4  # not sure if needed
BUTTON_START = 0
BUTTON1 = 1
BUTTON2 = 2
BUTTON3 = 3
BUTTON4 = 4
BACKGROUND_COLOR = (40, 40, 40)
COLORS_DICT = {
    "green": (0, 128, 0),
    "red": (128, 0, 0),
    "blue": (0, 0, 128),
    "yellow": (128, 128, 0),
    "bright green": (0, 255, 0),
    "bright red": (255, 0, 0),
    "bright blue": (0, 0, 255),
    "bright yellow": (255, 255, 0),
    "white": (255, 255, 255),
    "grey": (128, 128, 128),
    "black": (0, 0, 0),
}
CONGRATS_TEXT = ["Nice", "Good Job", "Great", "Good Work"]
color_type = Tuple[int, int, int]


class Levels:
    def __init__(self):
        self.level = 1
        self.seq_data = [
            (2, 0), (3, 0), (3, 0), (4, 0), (4, 0),
            (4, 1), (4, 1), (5, 1), (5, 2), (6, 2),
            (7, 3),
        ]  # if level 12 + len = level - 4, any number of dup

    def get_level(self) -> int:
        return self.level

    def increment_level(self) -> None:
        self.level += 1

    def get_sequence_data(self) -> Tuple[int, int]:
        if self.level <= 11:
            return self.seq_data[self.level - 1]
        else:
            return self.level - 4, -1

    def reset_level(self) -> None:
        self.level = 1

    def set_level(self, num: int) -> None:
        self.level = num


class GameSequence:
    def __init__(self, game_level: Levels):
        self.game_level = game_level
        self.number_of_buttons = NUMBER_OF_BUTTONS

    def get_sequence(self) -> list:
        seq_len, total_num_dup = self.game_level.get_sequence_data()
        seq = []
        dup_num = 0
        for _ in range(seq_len):
            while True:
                button_num = random.randint(1, self.number_of_buttons)
                if total_num_dup == -1:
                    seq.append(button_num)
                    break
                if total_num_dup == 0 and button_num in seq:
                    continue
                elif button_num in seq and dup_num < total_num_dup:
                    dup_num += 1
                    seq.append(button_num)
                    break
                elif button_num in seq and dup_num >= total_num_dup:
                    continue
                else:
                    seq.append(button_num)
                    break

        return seq


class Button:
    def __init__(self, win: pygame.Surface,
                 name: str,
                 button_number: int,
                 size: Tuple[int, int, int, int],
                 default_color: color_type,
                 select_color: color_type,
                 text: str,
                 font: pygame.font.Font):
        self.size = size
        self.win = win
        self.name = name
        self.button_number = button_number
        self.default_color = default_color
        self.select_color = select_color
        self.color = default_color
        self.font = font
        self.text = text
        self.button = pygame.rect.Rect(size)

    def display(self) -> None:
        pygame.draw.rect(self.win, self.color, self.button)
        text = self.font.render(self.text, True, COLORS_DICT["black"])
        tx = (self.size[0] + self.size[2] / 2) - text.get_width() / 2
        ty = (self.size[1] + self.size[3] / 2) - text.get_height() / 2
        self.win.blit(text, (tx, ty))  # make better

    def check_if_clicked(self, x: int, y: int, show_click: bool) -> bool:
        if self.button.collidepoint(x, y):
            if show_click:
                self.color = self.select_color
            return True
        else:
            return False

    def set_selected(self):
        self.color = self.select_color

    def reset_color(self) -> None:
        self.color = self.default_color

    def get_number(self) -> int:
        return self.button_number

    def set_text(self, text: str) -> None:
        self.text = text

    def get_pygame_rect(self) -> pygame.rect.Rect:
        # not sure if needed
        return self.button


class Display:
    def __init__(self, win: pygame.Surface, game_seq: GameSequence, game_level: Levels):
        self.win = win
        self.game_sequence = game_seq
        self.game_level = game_level
        self.font = pygame.font.SysFont("comicsans", 30)
        self.button_list = [
            Button(win, "start", BUTTON_START, (220, 325, 80, 40),
                   COLORS_DICT["white"], COLORS_DICT["white"], "Start", self.font),
            Button(win, "button 1", BUTTON1, (50, 50, 150, 150),
                   COLORS_DICT["blue"], COLORS_DICT["bright blue"], "", self.font),
            Button(win, "button 2", BUTTON2, (WIDTH - 200, 50, 150, 150),
                   COLORS_DICT["green"], COLORS_DICT["bright green"], "", self.font),
            Button(win, "button 3", BUTTON3, (WIDTH - 200, HEIGHT - 200, 150, 150),
                   COLORS_DICT["yellow"], COLORS_DICT["bright yellow"], "", self.font),
            Button(win, "button 4", BUTTON4, (50, HEIGHT - 200, 150, 150),
                   COLORS_DICT["red"], COLORS_DICT["bright red"], "", self.font)
        ]
        self.text_display = pygame.rect.Rect((220, 240, 160, 65))
        self.text_on_display = ""

    def display_game(self) -> None:
        self.win.fill(color=BACKGROUND_COLOR)
        for button in self.button_list:
            button.display()
        text = self.font.render(self.text_on_display, True, COLORS_DICT["black"])
        pygame.draw.rect(self.win, COLORS_DICT["grey"], self.text_display)
        ty = (self.text_display.y + self.text_display.height / 2) - text.get_height() / 2
        tx = (self.text_display.x + self.text_display.width / 2) - text.get_width() / 2
        self.win.blit(text, (tx, ty))
        pygame.display.update()

    def get_clicked(self, x: int, y: int, show_click: bool) -> int:
        for button in self.button_list:
            if button.check_if_clicked(x, y, show_click):
                return button.get_number()
        return -1

    def display_sequence(self, seq: List[int]) -> bool:
        clock = pygame.time.Clock()
        i = 0
        self.display_game()
        pygame.time.wait(2000)
        run = True
        while run:
            clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
            self.button_list[seq[i]].set_selected()
            self.display_game()
            pygame.time.wait(500)
            self.button_list[seq[i]].reset_color()
            self.display_game()
            pygame.time.wait(500)
            i += 1
            if i >= len(seq):
                run = False
        return True

    def reset_button_colors(self) -> None:
        for button in self.button_list:
            button.reset_color()

    def set_display_text(self, text: str) -> None:
        self.text_on_display = text


def get_sequence_from_player(game_display: Display, seq: List[int]) -> str:
    # correct, incorrect, quit
    clock = pygame.time.Clock()
    game_display.display_game()
    pygame.time.wait(2000)
    game_display.set_display_text("GO")
    pygame.time.set_timer(1, 3000)
    i = 0
    while i <= len(seq) - 1:
        clock.tick(10)
        game_display.display_game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                clicked = game_display.get_clicked(mouse_x, mouse_y, True)
                if clicked == seq[i]:
                    i += 1
                    pygame.time.set_timer(1, 3000)
                elif clicked == -1 or clicked == 0:
                    continue
                else:
                    game_display.display_game()
                    pygame.time.wait(300)
                    game_display.reset_button_colors()
                    pygame.time.set_timer(1, 0)
                    return "incorrect"
                game_display.display_game()
                pygame.time.wait(100)
            elif event.type == pygame.MOUSEBUTTONUP:
                game_display.reset_button_colors()
            elif event.type == 1:
                game_display.reset_button_colors()
                pygame.time.set_timer(1, 0)
                return "incorrect"
    else:
        game_display.reset_button_colors()
        pygame.time.set_timer(1, 0)
        return "correct"


def game_over(game_display: Display) -> bool:
    # False - quit, True - start_game
    clock = pygame.time.Clock()
    game_display.set_display_text("Game Over")
    run = True
    while run:
        clock.tick(10)
        game_display.display_game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                clicked = game_display.get_clicked(mouse_x, mouse_y, False)
                if clicked == BUTTON_START:
                    return True


def start_game(game_display: Display) -> bool:
    # True - play, False - exit
    clock = pygame.time.Clock()
    game_display.set_display_text("Press Start")
    run = True
    while run:
        clock.tick(10)
        game_display.display_game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                clicked = game_display.get_clicked(mouse_x, mouse_y, False)
                if clicked == BUTTON_START:
                    return True


def play_the_game(game_display: Display,
                  game_seq: GameSequence,
                  game_level: Levels) -> None:
    run = True
    while run:
        game_display.set_display_text(f"Level: {game_level.get_level()}")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # get sequence
        seq = game_seq.get_sequence()
        # display sequence
        if game_display.display_sequence(seq):
            # get the sequence from player
            result = get_sequence_from_player(game_display, seq)
            if result == "quit":
                run = False
            elif result == "incorrect":
                if game_over(game_display):
                    game_level.reset_level()
                else:
                    run = False
            elif result == "correct":
                game_display.set_display_text(random.choice(CONGRATS_TEXT))
                game_display.display_game()
                pygame.time.wait(1100)
                game_level.increment_level()
        else:
            run = False
    # increase level
    # rinse and repeat
    ...


def main_game() -> None:
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    game_level = Levels()
    game_sequence = GameSequence(game_level)
    game_display = Display(win, game_sequence, game_level)
    if start_game(game_display):
        play_the_game(game_display, game_sequence, game_level)


if __name__ == "__main__":
    main_game()
