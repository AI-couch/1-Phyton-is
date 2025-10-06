import pygame as pg

pg.init()
screen = pg.display.set_mode((800, 600))
clock = pg.time.Clock()

# Два типа объектов: просто прямоугольники
bot1 = pg.Rect(20, 120, 40, 40)
bot2 = pg.Rect(300, 60, 40, 40)

vx1 = 2
vx2 = -1

running = True
while running:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False

    bot1.x += vx1
    bot2.x += vx2

    screen.fill("white")
    pg.draw.rect(screen, "gold", bot1)  # методы модуля draw
    pg.draw.rect(screen, "skyblue", bot2)
    pg.display.flip()
    clock.tick(60)

pg.quit()