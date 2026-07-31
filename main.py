import pygame
import sys
from chip8 import Chip8


def main():
    # 1. Initialize CPU
    cpu = Chip8()
    cpu.init_fontset()
    rom_file = ""
    cpu.load_rom(rom_file)

    # 2. Initialize Pygame
    pygame.init()
    SCALE = 10
    WIDTH, HEIGHT = 64 * SCALE, 32 * SCALE

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Python CHIP-8 Emulator")

    small_buffer = pygame.Surface((64, 32))
    big_buffer = pygame.Surface((WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    running = True

    key_map = {
        pygame.K_1: 0x1, pygame.K_2: 0x2, pygame.K_3: 0x3, pygame.K_4: 0xC,
        pygame.K_q: 0x4, pygame.K_w: 0x5, pygame.K_e: 0x6, pygame.K_r: 0xD,
        pygame.K_a: 0x7, pygame.K_s: 0x8, pygame.K_d: 0x9, pygame.K_f: 0xE,
        pygame.K_z: 0xA, pygame.K_x: 0x0, pygame.K_c: 0xB, pygame.K_v: 0xF
    }

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                state = 1 if event.type == pygame.KEYDOWN else 0
                if event.key in key_map:
                    cpu.key[key_map[event.key]] = state

        # CPU execution
        for _ in range(10):
            cpu.cycle()
        if cpu.delay_timer > 0:
            cpu.delay_timer -= 1
        if cpu.sound_timer > 0:
            cpu.sound_timer -= 1

        small_buffer.fill((0, 0, 0))

        # 2. Draw only white pixels (black is already the background)
        for y in range(32):
            for x in range(64):
                if cpu.video[y * 64 + x]:
                    small_buffer.set_at((x, y), (255, 255, 255))

        pygame.transform.scale(small_buffer, (WIDTH, HEIGHT), big_buffer)

        screen.blit(big_buffer, (0, 0))
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
