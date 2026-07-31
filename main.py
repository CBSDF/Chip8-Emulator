import pygame
import sys
from chip8 import Chip8


def main():
    # 1. Init our cpu
    cpu = Chip8()
    cpu.init_fontset()

    # Path to your rom
    rom_file = ""
    cpu.load_rom(rom_file)

    # 2. Init pygame
    pygame.init()
    # Оriginal screen is small so we make it bigger
    SCALE = 10
    screen = pygame.display.set_mode((64 * SCALE, 32 * SCALE))
    pygame.display.set_caption("Python CHIP-8 Emulator")

    clock = pygame.time.Clock()
    is_running = True

    # Main game loop
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            # 1 - pressed 2 - not pressed
            elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                state = 1 if event.type == pygame.KEYDOWN else 0

                # Standart Layout of keyboard
                match event.key:
                    case pygame.K_1:
                        cpu.key[0x1] = state
                    case pygame.K_2:
                        cpu.key[0x2] = state
                    case pygame.K_3:
                        cpu.key[0x3] = state
                    case pygame.K_4:
                        cpu.key[0xC] = state
                    case pygame.K_q:
                        cpu.key[0x4] = state
                    case pygame.K_w:
                        cpu.key[0x5] = state
                    case pygame.K_e:
                        cpu.key[0x6] = state
                    case pygame.K_r:
                        cpu.key[0xD] = state
                    case pygame.K_a:
                        cpu.key[0x7] = state
                    case pygame.K_s:
                        cpu.key[0x8] = state
                    case pygame.K_d:
                        cpu.key[0x9] = state
                    case pygame.K_f:
                        cpu.key[0xE] = state
                    case pygame.K_z:
                        cpu.key[0xA] = state
                    case pygame.K_x:
                        cpu.key[0x0] = state
                    case pygame.K_c:
                        cpu.key[0xB] = state
                    case pygame.K_v:
                        cpu.key[0xF] = state

        for _ in range(10):
            cpu.cycle()
        if cpu.delay_timer > 0: cpu.delay_timer -= 1
        if cpu.sound_timer > 0: cpu.sound_timer -= 1

        screen.fill((0, 0, 0))  # Clear screen by black color

        for y in range(32):
            for x in range(64):
                index = x + (y * 64)
                # if 1 we fill pixel white color
                if cpu.video[index] == 1:
                    pygame.draw.rect(
                        screen,
                        (255, 255, 255),  # White color
                        (x * SCALE, y * SCALE, SCALE, SCALE)
                    )

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
