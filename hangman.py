import pygame
import random
import sys
import json
import os
import platform

FPS = 60

RESOLUTIONS = [
    (800, 550, "Small"),
    (900, 650, "Medium"),
    (1050, 720, "Large"),
    (1200, 800, "XL"),
]

BG_COLOR = (22, 24, 38)
GALLOW_COLOR = (230, 230, 235)
TEXT_COLOR = (245, 245, 250)
ACCENT = (90, 180, 255)
WRONG_COLOR = (255, 85, 85)
CORRECT_COLOR = (75, 215, 125)
BUTTON_COLOR = (45, 48, 72)
BUTTON_HOVER = (65, 72, 110)
BUTTON_USED = (38, 40, 55)

CATEGORIES = {
    "Tech & Code": [
        "PYTHON", "HANGMAN", "PYGAME", "ALGORITHM", "DATABASE", "FRAMEWORK",
        "JUPYTER", "GITHUB", "VARIABLE", "FUNCTION", "DEVELOPER", "INTERFACE",
        "COMPUTER", "KEYBOARD", "MONITOR", "PROGRAM", "BINARY", "COMPILER",
        "DEBUGGER", "ENCRYPT", "FIREWALL", "KERNEL", "MODULE", "PACKAGE",
        "REFACTOR", "CONTAINER", "MICROSERVICE", "REPOSITORY", "ASYNC", "TYPESCRIPT"
    ],
    "Fantasy & Myths": [
        "WIZARD", "DRAGON", "CASTLE", "KNIGHT", "PIRATE", "ADVENTURE",
        "CHALLENGE", "EXPLORER", "INVENTOR", "TREASURE", "SORCERER",
        "PHOENIX", "UNICORN", "GOBLIN", "TROLL", "MERMAID", "VAMPIRE",
        "WEREWOLF", "DUNGEON", "LEGEND", "MYSTIC", "PROPHECY", "ALCHEMY",
        "GRIFFIN", "VALKYRIE", "HYDRA", "CHIMERA"
    ],
    "Animals & Nature": [
        "ELEPHANT", "KANGAROO", "DINOSAUR", "BUTTERFLY", "MOUNTAIN", "OCEAN",
        "SUNSHINE", "JAGUAR", "PENGUIN", "DOLPHIN", "GIRAFFE", "CHEETAH",
        "OCTOPUS", "TORNADO", "VOLCANO", "RAINFOREST", "WATERFALL", "HURRICANE",
        "BAMBOO", "CACTUS", "CORAL", "DESERT", "AVALANCHE", "MANGROVE", "ORCHID"
    ],
    "Space & Cosmos": [
        "GALAXY", "ROCKET", "PLANET", "ASTRONAUT", "NEBULA", "COMET",
        "METEOR", "JUPITER", "SATURN", "MARS", "VENUS", "PLUTO",
        "QUASAR", "PULSAR", "ORBIT", "COSMIC", "LUNAR", "SOLAR",
        "BLACKHOLE", "ASTEROID", "TELESCOPE", "SPACECRAFT", "SUPERNOVA", "EXOPLANET"
    ],
}

ALL_WORDS = [word for words in CATEGORIES.values() for word in words]

DIFFICULTIES = {
    "Easy": 8,
    "Normal": 6,
    "Hard": 4
}

STATS_FILE = "hangman_stats.json"
SETTINGS_FILE = "hangman_settings.json"
PARTICLE_COUNT = 120
CONFETTI_COLORS = [(255, 105, 180), (100, 200, 255), (255, 215, 0), (144, 238, 144), (255, 160, 122)]


def load_resolution():
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                w = data.get("width", 900)
                h = data.get("height", 650)
                for rw, rh, _ in RESOLUTIONS:
                    if rw == w and rh == h:
                        return w, h
    except:
        pass
    return 900, 650


def save_resolution(w, h):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump({"width": w, "height": h}, f)
    except:
        pass


class HangmanGame:
    def __init__(self):
        self.current_category = "Random"
        self.current_difficulty = "Normal"
        self.stats = {"games": 0, "wins": 0, "streak": 0, "best_streak": 0}
        self.load_stats()
        self.reset()

    def load_stats(self):
        try:
            if os.path.exists(STATS_FILE):
                with open(STATS_FILE, "r") as f:
                    data = json.load(f)
                    self.stats.update(data)
        except:
            pass

    def save_stats(self):
        try:
            with open(STATS_FILE, "w") as f:
                json.dump(self.stats, f)
        except:
            pass

    def update_stats(self, won):
        self.stats["games"] += 1
        if won:
            self.stats["wins"] += 1
            self.stats["streak"] += 1
            if self.stats["streak"] > self.stats["best_streak"]:
                self.stats["best_streak"] = self.stats["streak"]
        else:
            self.stats["streak"] = 0
        self.save_stats()

    def reset(self, category=None, difficulty=None):
        if category is not None:
            self.current_category = category
        if difficulty is not None:
            self.current_difficulty = difficulty

        if self.current_category == "Random":
            pool = ALL_WORDS
        else:
            pool = CATEGORIES.get(self.current_category, ALL_WORDS)

        self.secret_word = random.choice(pool)
        self.guessed = set()
        self.wrong_guesses = 0
        self.game_over = False
        self.won = False
        self.message = ""
        self.hints_used = 0
        self.max_hints = 1
        self.max_wrong = DIFFICULTIES[self.current_difficulty]
        self.start_ticks = pygame.time.get_ticks()
        self.correct_count = 0
        self.wrong_count = 0
        self.duration = 0

    def guess_letter(self, letter):
        if self.game_over or letter in self.guessed:
            return False
        self.guessed.add(letter)
        if letter in self.secret_word:
            self.correct_count += 1
        else:
            self.wrong_guesses += 1
            self.wrong_count += 1
        self._check_game_state()
        return True

    def _check_game_state(self):
        if self.wrong_guesses >= self.max_wrong:
            self.game_over = True
            self.won = False
            self.duration = (pygame.time.get_ticks() - self.start_ticks) // 1000
            self.message = "You lost! The word was " + self.secret_word
            self.update_stats(False)
        elif all(c in self.guessed for c in self.secret_word):
            self.game_over = True
            self.won = True
            self.duration = (pygame.time.get_ticks() - self.start_ticks) // 1000
            self.message = "You won!"
            self.update_stats(True)

    def get_display_word(self):
        return " ".join(c if c in self.guessed else "_" for c in self.secret_word)

    def get_wrong_letters(self):
        return sorted([l for l in self.guessed if l not in self.secret_word])

    def use_hint(self):
        if self.game_over or self.hints_used >= self.max_hints:
            return False
        unguessed = [c for c in self.secret_word if c not in self.guessed]
        if not unguessed:
            return False
        hint_letter = random.choice(unguessed)
        self.guessed.add(hint_letter)
        self.correct_count += 1
        self.hints_used += 1
        self._check_game_state()
        return True

    def get_accuracy(self):
        total = self.correct_count + self.wrong_count
        if total == 0:
            return 100
        return int((self.correct_count / total) * 100)

    def get_elapsed(self):
        if self.game_over:
            return self.duration
        return (pygame.time.get_ticks() - self.start_ticks) // 1000

    def give_up(self):
        if self.game_over:
            return False
        self.game_over = True
        self.won = False
        self.duration = (pygame.time.get_ticks() - self.start_ticks) // 1000
        self.message = "You gave up. The word was " + self.secret_word
        self.update_stats(False)
        return True


def draw_gallows(surface, x, y):
    pygame.draw.rect(surface, GALLOW_COLOR, (x - 85, y + 185, 210, 14), border_radius=4)
    pygame.draw.rect(surface, GALLOW_COLOR, (x + 20, y - 125, 11, 310), border_radius=2)
    pygame.draw.rect(surface, GALLOW_COLOR, (x + 20, y - 125, 155, 11), border_radius=2)
    pygame.draw.line(surface, GALLOW_COLOR, (x + 160, y - 120), (x + 160, y - 72), 5)
    pygame.draw.line(surface, GALLOW_COLOR, (x + 25, y - 120), (x + 78, y - 72), 7)
    pygame.draw.circle(surface, GALLOW_COLOR, (x + 160, y - 65), 6, 3)


def draw_hangman(surface, x, y, stage):
    head_center = (x + 155, y - 40)
    head_radius = 28

    if stage >= 1:
        pygame.draw.circle(surface, WRONG_COLOR, head_center, head_radius, 4)
        pygame.draw.circle(surface, WRONG_COLOR, (x + 145, y - 48), 4, 2)
        pygame.draw.circle(surface, WRONG_COLOR, (x + 165, y - 48), 4, 2)
        pygame.draw.arc(surface, WRONG_COLOR, (x + 142, y - 35, 26, 18), 3.5, 5.8, 3)

    if stage >= 2:
        pygame.draw.line(surface, WRONG_COLOR, (x + 155, y - 12), (x + 155, y + 55), 5)

    if stage >= 3:
        pygame.draw.line(surface, WRONG_COLOR, (x + 155, y + 5), (x + 110, y + 35), 5)

    if stage >= 4:
        pygame.draw.line(surface, WRONG_COLOR, (x + 155, y + 5), (x + 200, y + 35), 5)

    if stage >= 5:
        pygame.draw.line(surface, WRONG_COLOR, (x + 155, y + 55), (x + 120, y + 110), 5)

    if stage >= 6:
        pygame.draw.line(surface, WRONG_COLOR, (x + 155, y + 55), (x + 190, y + 110), 5)


def draw_text(surface, text, font, color, x, y, center=True):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(img, rect)
    return rect


def draw_letter_buttons(surface, font, game, start_x, start_y, button_w, button_h, spacing):
    buttons = []
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cols = 9
    rows = 3

    for i, letter in enumerate(letters):
        row = i // cols
        col = i % cols
        bx = start_x + col * (button_w + spacing)
        by = start_y + row * (button_h + spacing)

        used = letter in game.guessed
        color = BUTTON_USED if used else BUTTON_COLOR

        rect = pygame.Rect(bx, by, button_w, button_h)
        pygame.draw.rect(surface, color, rect, border_radius=8)
        pygame.draw.rect(surface, ACCENT if not used else (80, 80, 100), rect, width=2, border_radius=8)

        text_color = (160, 160, 170) if used else TEXT_COLOR
        draw_text(surface, letter, font, text_color, bx + button_w // 2, by + button_h // 2)

        buttons.append((rect, letter))
    return buttons


def draw_category_selector(surface, fonts, game, start_x, start_y):
    buttons = []
    categories = list(CATEGORIES.keys()) + ["Random"]
    btn_w, btn_h = 130, 30
    spacing = 5

    for i, cat in enumerate(categories):
        by = start_y + i * (btn_h + spacing)
        is_selected = cat == game.current_category
        color = (70, 130, 180) if is_selected else BUTTON_COLOR
        border_color = ACCENT if is_selected else (80, 80, 100)

        rect = pygame.Rect(start_x, by, btn_w, btn_h)
        pygame.draw.rect(surface, color, rect, border_radius=6)
        pygame.draw.rect(surface, border_color, rect, width=2, border_radius=6)

        text_color = (255, 255, 255) if is_selected else TEXT_COLOR
        draw_text(surface, cat, fonts["small"], text_color, rect.centerx, rect.centery)
        buttons.append((rect, cat))
    return buttons


def draw_difficulty_selector(surface, fonts, game, start_x, start_y):
    buttons = []
    btn_w, btn_h = 130, 30
    spacing = 5

    for i, (diff, wrongs) in enumerate(DIFFICULTIES.items()):
        by = start_y + i * (btn_h + spacing)
        is_selected = diff == game.current_difficulty
        color = (180, 120, 60) if is_selected else BUTTON_COLOR
        border_color = ACCENT if is_selected else (80, 80, 100)

        rect = pygame.Rect(start_x, by, btn_w, btn_h)
        pygame.draw.rect(surface, color, rect, border_radius=6)
        pygame.draw.rect(surface, border_color, rect, width=2, border_radius=6)

        label = diff + " (" + str(wrongs) + ")"
        text_color = (255, 255, 255) if is_selected else TEXT_COLOR
        draw_text(surface, label, fonts["small"], text_color, rect.centerx, rect.centery)
        buttons.append((rect, diff))
    return buttons


def create_confetti(particles, x, y):
    for _ in range(PARTICLE_COUNT):
        particles.append({
            "x": x + random.randint(-60, 60),
            "y": y + random.randint(-20, 40),
            "vx": random.uniform(-3.5, 3.5),
            "vy": random.uniform(-4.5, 1.5),
            "color": random.choice(CONFETTI_COLORS),
            "size": random.randint(5, 9),
            "life": random.randint(45, 85)
        })


def update_draw_particles(surface, particles):
    alive = []
    for p in particles:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vy"] += 0.12
        p["life"] -= 1
        if p["life"] > 0:
            alpha = max(40, int(255 * (p["life"] / 70)))
            s = pygame.Surface((p["size"], p["size"]), pygame.SRCALPHA)
            pygame.draw.circle(s, (*p["color"], alpha), (p["size"]//2, p["size"]//2), p["size"]//2)
            surface.blit(s, (int(p["x"]), int(p["y"])))
            alive.append(p)
    particles[:] = alive


def draw_game_ui(surface, fonts, game, particles):
    surface.fill(BG_COLOR)

    draw_text(surface, "HANGMAN", fonts["title"], ACCENT, WIDTH // 2, 32)

    streak_text = "Streak: " + str(game.stats["streak"]) + "   Best: " + str(game.stats["best_streak"])
    draw_text(surface, streak_text, fonts["small"], ACCENT, 95, 28)

    time_text = "Time: " + str(game.get_elapsed()) + "s"
    draw_text(surface, time_text, fonts["small"], (200, 200, 210), WIDTH // 2 + 60, int(HEIGHT * 0.29))

    gallows_x = int(WIDTH * 0.22)
    gallows_y = int(HEIGHT * 0.26)
    draw_gallows(surface, gallows_x, gallows_y)
    draw_hangman(surface, gallows_x, gallows_y, game.wrong_guesses)

    info_x = int(WIDTH * 0.38)
    word = game.get_display_word()
    draw_text(surface, word, fonts["word"], TEXT_COLOR, info_x, int(HEIGHT * 0.32))

    draw_text(surface, "Category: " + game.current_category, fonts["small"], ACCENT, info_x, int(HEIGHT * 0.36))
    draw_text(surface, "Word length: " + str(len(game.secret_word)), fonts["small"], (180, 180, 200), info_x, int(HEIGHT * 0.39))

    wrong_letters = game.get_wrong_letters()
    draw_text(surface, "Wrong guesses: " + str(game.wrong_guesses) + " / " + str(game.max_wrong), fonts["medium"], WRONG_COLOR, info_x, int(HEIGHT * 0.44))

    if wrong_letters:
        draw_text(surface, "Used: " + " ".join(wrong_letters), fonts["medium"], (200, 140, 140), info_x, int(HEIGHT * 0.48))

    button_start_x = int(WIDTH * 0.13)
    button_start_y = HEIGHT - 195
    btn_w, btn_h = 58, 52
    spacing = 8
    buttons = draw_letter_buttons(surface, fonts["button"], game, button_start_x, button_start_y, btn_w, btn_h, spacing)

    hint_rect = None
    give_up_rect = None
    diff_buttons = []
    cat_buttons = []

    if not game.game_over:
        hints_left = game.max_hints - game.hints_used
        hint_color = (80, 160, 120) if hints_left > 0 else BUTTON_USED
        hint_rect = pygame.Rect(WIDTH - 165, int(HEIGHT * 0.19), 130, 34)
        pygame.draw.rect(surface, hint_color, hint_rect, border_radius=8)
        pygame.draw.rect(surface, ACCENT, hint_rect, width=2, border_radius=8)
        hint_text = "HINT (" + str(hints_left) + " left)" if hints_left > 0 else "NO HINTS"
        draw_text(surface, hint_text, fonts["small"], TEXT_COLOR if hints_left > 0 else (140,140,150), hint_rect.centerx, hint_rect.centery)

        give_up_rect = pygame.Rect(WIDTH - 165, int(HEIGHT * 0.25), 130, 34)
        pygame.draw.rect(surface, (160, 70, 70), give_up_rect, border_radius=8)
        pygame.draw.rect(surface, (220, 120, 120), give_up_rect, width=2, border_radius=8)
        draw_text(surface, "GIVE UP", fonts["small"], TEXT_COLOR, give_up_rect.centerx, give_up_rect.centery)

        right_x = WIDTH - 175
        diff_buttons = draw_difficulty_selector(surface, fonts, game, right_x, int(HEIGHT * 0.32))
        cat_buttons = draw_category_selector(surface, fonts, game, right_x, int(HEIGHT * 0.48))
    else:
        cat_buttons = []
        diff_buttons = []

    draw_text(surface, "Click letters or press H for hint • R to restart • G for give up • F11 fullscreen", fonts["small"], (140, 140, 160), WIDTH // 2, HEIGHT - 32)
    draw_text(surface, "Made by ritepro", fonts["small"], (90, 90, 110), 70, HEIGHT - 32)

    size_rect = pygame.Rect(WIDTH - 95, HEIGHT - 46, 80, 26)
    pygame.draw.rect(surface, (60, 65, 95), size_rect, border_radius=6)
    pygame.draw.rect(surface, ACCENT, size_rect, width=2, border_radius=6)
    draw_text(surface, "Size", fonts["small"], TEXT_COLOR, size_rect.centerx, size_rect.centery)

    if game.game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((20, 20, 35, 210))
        surface.blit(overlay, (0, 0))

        if game.won and not particles:
            create_confetti(particles, WIDTH // 2, HEIGHT // 2 - 60)

        update_draw_particles(surface, particles)

        msg_color = CORRECT_COLOR if game.won else WRONG_COLOR
        draw_text(surface, game.message, fonts["medium"], msg_color, WIDTH // 2, int(HEIGHT * 0.45))

        stats_line = "Time: " + str(game.duration) + "s   Accuracy: " + str(game.get_accuracy()) + "%"
        draw_text(surface, stats_line, fonts["small"], (210, 210, 220), WIDTH // 2, int(HEIGHT * 0.48))

        play_rect = pygame.Rect(WIDTH // 2 - 120, int(HEIGHT * 0.52), 240, 55)
        pygame.draw.rect(surface, ACCENT, play_rect, border_radius=12)
        draw_text(surface, "PLAY AGAIN", fonts["button"], BG_COLOR, play_rect.centerx, play_rect.centery)

        return buttons, play_rect, cat_buttons, diff_buttons, hint_rect, give_up_rect, size_rect

    update_draw_particles(surface, particles)
    return buttons, None, cat_buttons, diff_buttons, hint_rect, give_up_rect, size_rect


def show_loading_screen(screen, fonts, clock):
    start = pygame.time.get_ticks()
    duration = 1600
    loading_done = False

    while not loading_done:
        current = pygame.time.get_ticks()
        progress = min((current - start) / duration, 1.0)

        screen.fill(BG_COLOR)

        draw_text(screen, "HANGMAN", fonts["title"], ACCENT, WIDTH // 2, HEIGHT // 2 - 80)

        subtitle = "Guess the word. Master the categories."
        draw_text(screen, subtitle, fonts["small"], (180, 180, 200), WIDTH // 2, HEIGHT // 2 - 25)

        bar_width = int(WIDTH * 0.42)
        bar_height = 8
        bar_x = WIDTH // 2 - bar_width // 2
        bar_y = HEIGHT // 2 + 45

        pygame.draw.rect(screen, (55, 55, 75), (bar_x, bar_y, bar_width, bar_height), border_radius=4)
        fill_width = int(bar_width * progress)
        if fill_width > 0:
            pygame.draw.rect(screen, ACCENT, (bar_x, bar_y, fill_width, bar_height), border_radius=4)

            shine_x = bar_x + fill_width - 25
            if shine_x > bar_x:
                pygame.draw.rect(screen, (180, 230, 255), (shine_x, bar_y, 22, bar_height), border_radius=4)

        pct = int(progress * 100)
        draw_text(screen, str(pct) + "%", fonts["small"], TEXT_COLOR, WIDTH // 2, bar_y + 25)

        draw_text(screen, "Made by ritepro", fonts["small"], (130, 130, 150), WIDTH // 2, HEIGHT - 55)

        pygame.display.flip()
        clock.tick(60)

        if progress >= 1.0:
            loading_done = True

    for _ in range(8):
        clock.tick(60)


def _create_display(fullscreen):
    try:
        flags = pygame.FULLSCREEN | pygame.SCALED if fullscreen else pygame.SCALED
        return pygame.display.set_mode((WIDTH, HEIGHT), flags)
    except:
        try:
            return pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
        except:
            return pygame.display.set_mode((WIDTH, HEIGHT))


def main():
    global WIDTH, HEIGHT

    if platform.system() == "Linux" and "SDL_VIDEODRIVER" not in os.environ:
        if os.environ.get("XDG_SESSION_TYPE") == "wayland" or os.environ.get("WAYLAND_DISPLAY"):
            os.environ.setdefault("SDL_VIDEODRIVER", "wayland")
        else:
            os.environ.setdefault("SDL_VIDEODRIVER", "x11")

    os.environ.setdefault("SDL_HINT_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR", "0")
    os.environ.setdefault("SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS", "0")

    pygame.init()
    pygame.display.set_caption("Hangman")

    WIDTH, HEIGHT = load_resolution()

    screen = _create_display(False)
    clock = pygame.time.Clock()
    display = {"screen": screen, "fullscreen": False, "show_settings": False}

    sans_fonts = ["arial", "helvetica", "dejavu sans", "liberation sans", "freesans", "noto sans", "sans"]
    mono_fonts = ["consolas", "dejavu sans mono", "liberation mono", "freemono", "menlo", "monaco", "courier new", "monospace"]

    def make_fonts(w, h):
        scale = min(w / 900, h / 650)
        return {
            "title": pygame.font.SysFont(sans_fonts, int(52 * scale), bold=True),
            "word": pygame.font.SysFont(mono_fonts, int(48 * scale), bold=True),
            "medium": pygame.font.SysFont(sans_fonts, int(28 * scale)),
            "button": pygame.font.SysFont(sans_fonts, int(26 * scale), bold=True),
            "small": pygame.font.SysFont(sans_fonts, int(18 * scale)),
        }

    fonts = make_fonts(WIDTH, HEIGHT)

    show_loading_screen(display["screen"], fonts, clock)

    game = HangmanGame()
    particles = []
    running = True

    while running:
        buttons, play_again_rect, cat_buttons, diff_buttons, hint_rect, give_up_rect, size_rect = draw_game_ui(display["screen"], fonts, game, particles)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    particles.clear()
                    game.reset()
                elif event.key == pygame.K_h and not game.game_over:
                    game.use_hint()
                elif event.key == pygame.K_g and not game.game_over:
                    game.give_up()
                elif event.key == pygame.K_F11:
                    display["fullscreen"] = not display["fullscreen"]
                    display["screen"] = _create_display(display["fullscreen"])
                elif event.unicode.isalpha() and not game.game_over:
                    game.guess_letter(event.unicode.upper())

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                for rect, letter in buttons:
                    if rect.collidepoint(mx, my) and not game.game_over:
                        game.guess_letter(letter)

                if hint_rect and hint_rect.collidepoint(mx, my) and not game.game_over:
                    game.use_hint()

                if give_up_rect and give_up_rect.collidepoint(mx, my) and not game.game_over:
                    game.give_up()

                for rect, cat in cat_buttons:
                    if rect.collidepoint(mx, my) and not game.game_over:
                        if cat != game.current_category:
                            particles.clear()
                            game.reset(category=cat)

                for rect, diff in diff_buttons:
                    if rect.collidepoint(mx, my) and not game.game_over:
                        if diff != game.current_difficulty:
                            particles.clear()
                            game.reset(difficulty=diff)

                if game.game_over and play_again_rect and play_again_rect.collidepoint(mx, my):
                    particles.clear()
                    game.reset()

                if size_rect and size_rect.collidepoint(mx, my):
                    current = (WIDTH, HEIGHT)
                    idx = 0
                    for i, (rw, rh, _) in enumerate(RESOLUTIONS):
                        if rw == current[0] and rh == current[1]:
                            idx = i
                            break
                    new_idx = (idx + 1) % len(RESOLUTIONS)
                    new_w, new_h, _ = RESOLUTIONS[new_idx]
                    WIDTH, HEIGHT = new_w, new_h
                    save_resolution(WIDTH, HEIGHT)
                    display["screen"] = _create_display(display["fullscreen"])
                    fonts = make_fonts(WIDTH, HEIGHT)

        if not game.game_over:
            mx, my = pygame.mouse.get_pos()
            for rect, _ in buttons:
                if rect.collidepoint(mx, my):
                    pygame.draw.rect(display["screen"], BUTTON_HOVER, rect, border_radius=8, width=0)

            if hint_rect and hint_rect.collidepoint(mx, my) and (game.max_hints - game.hints_used) > 0:
                pygame.draw.rect(display["screen"], (100, 190, 140), hint_rect, border_radius=8, width=0)

            if give_up_rect and give_up_rect.collidepoint(mx, my):
                pygame.draw.rect(display["screen"], (190, 90, 90), give_up_rect, border_radius=8, width=0)

            for rect, _ in cat_buttons:
                if rect.collidepoint(mx, my):
                    pygame.draw.rect(display["screen"], (90, 150, 200), rect, border_radius=6, width=0)

            for rect, _ in diff_buttons:
                if rect.collidepoint(mx, my):
                    pygame.draw.rect(display["screen"], (200, 140, 80), rect, border_radius=6, width=0)

            if size_rect and size_rect.collidepoint(mx, my):
                pygame.draw.rect(display["screen"], (80, 90, 130), size_rect, border_radius=6, width=0)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()