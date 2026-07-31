

class Chip8:
    def __init__(self):
        # 4 kb memory
        self.memory = [0] * 4096
        # Regs
        self.V = [0] * 16
        self.I = 0
        self.pc = 0x200
        self.stack = []
        self.key = [0] * 16
        self.video = [0] * (64 * 32)
        self.delay_timer = 0
        self.sound_timer = 0

    def init_fontset(self):
        # Standart font
        fontset = [
            0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
            0x20, 0x60, 0x20, 0x20, 0x70,  # 1
            0xF0, 0x01, 0xF0, 0x10, 0xF0,  # 2
            0xF0, 0x01, 0xF0, 0x01, 0xF0,  # 3
            0x90, 0x90, 0xF0, 0x01, 0x01,  # 4
            0xF0, 0x10, 0xF0, 0x01, 0xF0,  # 5
            0xF0, 0x10, 0xF0, 0x90, 0xF0,  # 6
            0xF0, 0x01, 0x02, 0x04, 0x04,  # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
            0xF0, 0x90, 0xF0, 0x01, 0xF0,  # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
            0xF0, 0x10, 0x10, 0x10, 0xF0,  # C
            0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
            0xF0, 0x10, 0xF0, 0x10, 0xF0,  # E
            0xF0, 0x10, 0xF0, 0x10, 0x10  # F
        ]
        for i in range(80):
            self.memory[i] = fontset[i]

    def load_rom(self, rom_path):
        # Read binary
        with open(rom_path, "rb") as f:
            rom_data = f.read()

        # Write game bytes
        for i in range(len(rom_data)):
            self.memory[0x200 + i] = rom_data[i]
        print(f"[Chip8]: Loaded {len(rom_data)} bytes from {rom_path}")

    def cycle(self):

        opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
        self.pc += 2

        match (opcode & 0xF000):
            # JP addr
            case 0x1000:
                addr = opcode & 0x0FFF
                self.pc = addr

            # LD Vx, byte
            case 0x6000:
                x = (opcode & 0x0F00) >> 8
                kk = opcode & 0x00FF
                self.V[x] = kk
            # ADD Vx, byte
            case 0x7000:
                x = (opcode & 0x0F00) >> 8
                kk = opcode & 0x00FF
                self.V[x] = (self.V[x] + kk) & 0xFF
            # Math commands
            case 0x8000:
                x = (opcode & 0x0F00) >> 8
                y = (opcode & 0x00F0) >> 4
                sub_op = opcode & 0x000F
                # COPY
                if sub_op == 0: self.V[x] = self.V[y]
                # OR
                elif sub_op == 1: self.V[x] |= self.V[y]
                # AND
                elif sub_op == 2: self.V[x] &= self.V[y]
                # XOR
                elif sub_op == 3: self.V[x] ^= self.V[y]
                # ADD
                elif sub_op == 4:
                    val_sum = self.V[x] + self.V[y]
                    flag = 1 if val_sum > 255 else 0
                    self.V[x] = val_sum & 0xFF
                    self.V[15] = flag
                # SUB
                elif sub_op == 5:
                    flag = 1 if self.V[x] >= self.V[y] else 0
                    self.V[x] = (self.V[x] - self.V[y]) & 0xFF
                    self.V[15] = flag
                # SHR
                elif sub_op == 6:
                    flag = self.V[x] & 0x01
                    self.V[x] >>= 1
                    self.V[15] = flag
                # SUBN
                elif sub_op == 7:
                    flag = 1 if self.V[y] >= self.V[x] else 0
                    self.V[x] = (self.V[y] - self.V[x]) & 0xFF
                    self.V[15] = flag
                # SHL
                elif sub_op == 0xE:
                    flag = (self.V[x] & 0x80) >> 7  # Забираем крайний левый бит
                    self.V[x] = (self.V[x] << 1) & 0xFF
                    self.V[15] = flag
            # SE
            case 0x3000:
                x = (opcode & 0x0F00) >> 8
                kk = opcode & 0x00FF
                if self.V[x] == kk:
                    self.pc += 2
            # SNE
            case 0x4000:
                x = (opcode & 0x0F00) >> 8
                kk = opcode & 0x00FF
                if self.V[x] != kk:
                    self.pc += 2
            # SE Vx, Vy
            case 0x5000:
                if (opcode & 0x000F) == 0:
                    x = (opcode & 0x0F00) >> 8
                    y = (opcode & 0x00F0) >> 4
                    if self.V[x] == self.V[y]:
                        self.pc += 2
            # SNE Vx, Vy
            case 0x9000:
                if (opcode & 0x000F) == 0:
                    x = (opcode & 0x0F00) >> 8
                    y = (opcode & 0x00F0) >> 4
                    if self.V[x] != self.V[y]:
                        self.pc += 2
            # LD I, addr
            case 0xA000:
                addr = opcode & 0x0FFF
                self.I = addr
            # JP v0, addr
            case 0xB000:
                addr = opcode & 0x0FFF
                self.pc = addr + self.V[0]
            # RND
            case 0xC000:
                import random
                x = (opcode & 0x0F00) >> 8
                kk = opcode & 0x00FF
                self.V[x] = random.randint(0, 255) & kk
            # DRW
            case 0xD000:
                x = (opcode & 0x0F00) >> 8
                y = (opcode & 0x00F0) >> 4
                height = opcode & 0x000F

                start_x = self.V[x]
                start_y = self.V[y]
                self.V[15] = 0

                # loop for image
                for row in range(height):
                    sprite_byte = self.memory[self.I + row]

                    for col in range(8):
                        # check if current bit is 1
                        if (sprite_byte & (0x80 >> col)) != 0:
                            screen_x = (start_x + col) % 64
                            screen_y = (start_y + row) % 32
                            index = screen_x + (screen_y * 64)

                            # if pixel is 1 - collision
                            if self.video[index] == 1:
                                self.V[15] = 1
                                self.video[index] = 0 # turn off
                            else:
                                self.video[index] = 1 # turn on
            # Keyboard
            case 0xE000:
                x = (opcode & 0x0F00) >> 8
                key_index = self.V[x]
                sub_op = opcode & 0x00FF

                if sub_op == 0x009E: # SKP Vx
                    if self.key[key_index] == 1:
                        self.pc += 2
                elif sub_op == 0x00A1: # SKNP Vx
                    if self.key[key_index] == 0:
                        self.pc += 2
            # SYS commands
            case 0xF000:
                x = (opcode & 0x0F00) >> 8
                sub_op = opcode & 0x00FF

                # 1. Work with timers
                if sub_op == 0x0007:   # LD Vx, DT
                    self.V[x] = self.delay_timer
                elif sub_op == 0x0015: # LD DT, Vx
                    self.delay_timer = self.V[x]
                elif sub_op == 0x0018: # LD ST, Vx
                    self.sound_timer = self.V[x]

                # 2. Math with I reg
                elif sub_op == 0x001E: # ADD I, Vx
                    self.I = (self.I + self.V[x]) & 0xFFF

                # 3. BCD
                elif sub_op == 0x0029: # LD F, Vx
                    self.I = self.V[x] * 5
                elif sub_op == 0x0033: # LD B, Vx
                    self.memory[self.I] = self.V[x] // 100
                    self.memory[self.I + 1] = (self.V[x] // 10) % 10
                    self.memory[self.I + 2] = self.V[x] % 10

                elif sub_op == 0x0055: # LD [I], Vx
                    for i in range(x + 1):
                        self.memory[self.I + i] = self.V[i]
                elif sub_op == 0x0065: # LD Vx, [I]
                    for i in range(x + 1):
                        self.V[i] = self.memory[self.I + i]

                # 5. Wait for keys
                elif sub_op == 0x000A: # LD Vx, K
                    key_pressed = False
                    for i in range(16):
                        if self.key[i] == 1:
                            self.V[x] = i
                            key_pressed = True
                            break
                    if not key_pressed:
                        self.pc -= 2 # if not pressed










