# Hangman

A clean, modern Hangman game with multiple categories, difficulty levels, hints, and persistent statistics.

## Features

- Four themed word categories with over 100 words
- Three difficulty levels (Easy, Normal, Hard)
- One hint per round
- Give up option that reveals the word
- Live timer and accuracy tracking
- Persistent win streaks and best streak
- Satisfying confetti animation on wins
- Full keyboard and mouse support
- Smooth animated loading screen
- Linux-friendly runtime (Wayland/X11 hints, HiDPI scaling, reliable fullscreen)

## Installation

This game supports **Windows, Linux, and macOS**.

### All Platforms (Recommended)

1. Make sure you have Python 3.8 or newer.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the game:

```bash
python hangman.py
```

### Linux (Ubuntu / Debian / Pop!_OS)

```bash
sudo apt update
sudo apt install python3-pip python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python hangman.py
```

### Linux (Fedora)

```bash
sudo dnf install python3-pip python3-virtualenv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python hangman.py
```

### Linux (Arch / Manjaro)

```bash
sudo pacman -S python-pip python-virtualenv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python hangman.py
```

**Note:** On some minimal Linux installs you may also need `sudo apt install libsdl2-2.0-0` or equivalent if Pygame fails to start. Most modern distributions work out of the box with the pip method above.

## How to Play

- A secret word is chosen based on your selected category and difficulty.
- Click letters or type on your keyboard to guess.
- Each incorrect guess adds a part to the hangman.
- Run out of guesses and you lose. Guess the full word and you win.
- Use the **Hint** button (or press **H**) once per game for help.
- Use **Give Up** (or press **G**) if you want to end the round and see the word.
- Change category or difficulty at any time before the round ends.
- Your streak and statistics are saved automatically between sessions.

## Controls

- **A–Z** — Guess a letter
- **H** — Use hint (if available)
- **G** — Give up and reveal the word
- **R** — Restart / new round
- **ESC** — Quit the game
- **F11** — Toggle fullscreen (recommended on Linux)
- Mouse — Click letters, category buttons, difficulty buttons, hint, give up, and play again

## Difficulty Levels

- **Easy** — 8 wrong guesses allowed
- **Normal** — 6 wrong guesses allowed
- **Hard** — 4 wrong guesses allowed

## Linux Notes

The game includes several Linux-specific improvements:

- Auto-detects best video driver (prefers Wayland when available, falls back to X11)
- SDL environment hints for better Wayland and X11 compatibility
- `pygame.SCALED` mode for proper HiDPI / fractional scaling support
- Graceful error handling when entering fullscreen (automatically falls back if the driver refuses)
- Reliable fullscreen toggle via **F11**
- Cross-platform font fallback using DejaVu, Liberation, Noto, and Free fonts

Most modern distributions (Ubuntu 22.04+, Fedora 38+, Arch, etc.) should work without extra configuration when using a Python virtual environment.

## Credits

Made by ritepro

---

Enjoy the game!