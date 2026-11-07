# THE LAST ORDER

A playable local split-screen co-op prototype inspired by the project brief. The project now includes a real Windows EXE launcher and an actual installer EXE generated using Wine + Inno Setup in this environment.

## Deliverables

- `dist/TheLastOrder.exe` — standalone Windows game executable
- `build/installer-output/TheLastOrder_Setup.exe` — Windows installer executable
- `assets/TheLastOrder.ico` — custom Windows icon asset
- `README.md` — usage notes

## What is included

- Two-player split-screen local co-op prototype with independent first-person views
- Six mission states and objective briefings
- Offline save progress stored in the user profile
- A custom icon asset generated as a valid Windows `.ico` file
- A Windows installer that creates a Start Menu shortcut and desktop shortcut

## Play locally on Linux

Prerequisites:

- Python 3.12+
- `pygame` and `Pillow`

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
/usr/bin/python3 main.py
# or: ./run_game.sh
```

Controls:

- Player 1: `WASD` move, `Q/E` rotate, `Space` fire.
- Player 2: `IJKL` move, `U/O` rotate, right control or left control fire.
- `Enter` starts or advances missions.
- `Esc` exits.

## Mission flow

1. Operation White Dusk
2. Blackwater Lift
3. Glass Harbor
4. Zero Hour
5. Shatterline
6. Final Orders

## Save system

Progress is saved automatically after mission selection. The game resumes from the last completed mission index using a local JSON file in the user home directory.

## Windows artifact note

The Windows `.exe` files were generated in this Linux environment using Wine and Inno Setup. They are actual PE executables and are present in the repo:

- `dist/TheLastOrder.exe`
- `build/installer-output/TheLastOrder_Setup.exe`

## Repository layout

- `main.py` — the game loop and split-screen prototype
- `assets/` — icon and asset files
- `installer/` — Inno Setup source template
- `dist/` — generated Windows EXE payload
- `build/installer-output/` — generated Windows installer EXE
- `requirements.txt` — runtime dependencies
