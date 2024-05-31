import pygame as pg
import random as rnd
pg.init()

width, columns, rows = 400, 16, 20
khoangCach = width // columns
height = khoangCach * rows
grid = [0] * columns * rows

BackGround_img=pg.image.load('bg.jpg')
BACKGROUND=pg.transform.scale(BackGround_img,(width,height))
amThanh=pg.mixer.Sound('Whoosh.mp3')
tocDo, diem, level, temp = 1000, 0, 1, 0

picture = [] 
for n in range(8):
    picture.append(pg.transform.scale(pg.image.load(f'T_{n}.jpg'), (khoangCach, khoangCach)))

WIN = pg.display.set_mode([width, height])
pg.display.set_caption('Tetris Game')

suKientetro = pg.USEREVENT + 1
pg.time.set_timer(suKientetro, tocDo)
pg.key.set_repeat(1, 100)

tetrorominos = [[0, 1, 1, 0,
                 0, 1, 1, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0],  # O
                 [0, 0, 0, 0,
                 2, 2, 2, 2,
                 0, 0, 0, 0,
                 0, 0, 0, 0],  # I
                [0, 0, 0, 0,
                 3, 3, 3, 0,
                 0, 0, 3, 0,
                 0, 0, 0, 0],  # J
                [0, 0, 4, 0,
                 4, 4, 4, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0],  # L
                [0, 5, 5, 0,
                 5, 5, 0, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0],  # S
                [6, 6, 0, 0,
                 0, 6, 6, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0],  # Z
                [0, 0, 0, 0,
                 7, 7, 7, 0,
                 0, 7, 0, 0,
                 0, 0, 0, 0]]  # T

class Tetromino:
    def __init__(self, tetro, row=0, column=5):
        self.tetro = tetro
        self.row = row
        self.column = column
#Tetromino lên màn hình.
    def show(self):
        for index, value in enumerate(self.tetro):
            if value > 0:
                x = (self.column + index % 4) * khoangCach
                y = (self.row + index // 4) * khoangCach
                WIN.blit(picture[value], (x, y))
#Kiểm soát biên giới
    def check(self, r, c):
        for index, value in enumerate(self.tetro):
            if value > 0:
                rs = r + index // 4
                cs = c + index % 4
                if rs >= rows or cs < 0 or cs >= columns or grid[rs * columns + cs] > 0:
                    return False
        return True

    def update(self, r, c):
        if self.check(self.row + r, self.column + c):
            self.row += r
            self.column += c
            return True
        return False

    def xoayHinh(self):
        savetetro = self.tetro.copy()
        for index, value in enumerate(savetetro):
            self.tetro[(2 - (index % 4)) * 4 + (index // 4)] = value
        if not self.check(self.row, self.column):
            self.tetro = savetetro.copy()

def nhanVaoLuoi():
    for index, value in enumerate(character.tetro):
        if value > 0:
            rs = character.row + index // 4
            cs = character.column + index % 4
            grid[rs * columns + cs] = value

def xoaDong():
  fullrows = 0
  for row in range(rows):
    for column in range(columns):
      if grid[row*columns+column] == 0: 
        break
    else:
      del grid[row*columns:row*columns+columns] 
      grid[0:0] = [0]*columns  
      fullrows += 1
  return fullrows**2*100


def draw_window(character, grid, diem, level):
    WIN.blit(BACKGROUND, (0, 0))
    character.show()

    for index, value in enumerate(grid):
        if value > 0:
            x, y = index % columns * khoangCach, index // columns * khoangCach
            WIN.blit(picture[value], (x, y))

    vanBan = pg.font.SysFont('consolas', 30).render(f'{diem:,}', True, (255, 255, 255))
    WIN.blit(vanBan, (10,10))

    vanBan = pg.font.SysFont('consolas', 20).render(f'Level: {level}', True, (255, 255, 255))
    WIN.blit(vanBan, (10,50))

    if any(grid[1 * columns:3 * columns]):
        ketThuc = pg.font.SysFont('consolas', 50).render("KẾT THÚC!", True, (255, 255, 255))
        WIN.blit(ketThuc, (80, 200))
        pg.display.flip(), pg.time.delay(3000), pg.quit(), exit()

    pg.display.flip()


def main():
    global character, tocDo, diem, level, temp

    while True:
        pg.time.delay(100)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == suKientetro:
                if not character.update(1, 0):
                    nhanVaoLuoi()
                    diem += xoaDong()
                    if diem > 0 and diem // 500 >= level and temp != diem:
                        tocDo = int(tocDo * 0.8)
                        pg.time.set_timer(suKientetro, tocDo)
                        level = diem // 500 + 1
                        temp = diem
                    character = Tetromino(rnd.choice(tetrorominos))
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    character.update(0, -1)
                if event.key == pg.K_RIGHT:
                    character.update(0, 1)
                if event.key == pg.K_DOWN:
                    character.update(1, 0)
                if event.key == pg.K_SPACE:
                    character.xoayHinh()
                    amThanh.play()

        draw_window(character, grid, diem, level)

if __name__=="__main__":
    character = Tetromino(rnd.choice(tetrorominos))
    main()
