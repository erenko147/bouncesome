# BounceSome

A simple C program that displays bouncing text with changing colors using SDL2.

## Prerequisites

- CMake (version 3.10 or higher)
- C compiler (supporting C11)
- SDL2 development libraries
- SDL2_ttf development libraries

## Installation

### Windows

1. Install SDL2 and SDL2_ttf development libraries:
   - Download SDL2 development libraries from https://github.com/libsdl-org/SDL/releases
   - Download SDL2_ttf development libraries from https://github.com/libsdl-org/SDL_ttf/releases
   - Extract both to a location on your system
   - Set SDL2_DIR and SDL2_TTF_DIR environment variables to point to these locations

2. Build the project:
```bash
mkdir build
cd build
cmake ..
cmake --build .
```

### Linux

1. Install dependencies:
```bash
# Ubuntu/Debian
sudo apt-get install libsdl2-dev libsdl2-ttf-dev

# Fedora
sudo dnf install SDL2-devel SDL2_ttf-devel

# Arch Linux
sudo pacman -S sdl2 sdl2_ttf
```

2. Build the project:
```bash
mkdir build
cd build
cmake ..
make
```

## Running

After building, run the executable:
```bash
./bouncesome
```

## Features

- Bouncing text that moves around the window
- Rainbow color cycling effect
- Smooth animation at 60 FPS
- Clean window closing with proper resource cleanup
