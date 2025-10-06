import pygame as robots

# --- размер экран ---
W, H = 800, 600
robots.init()  # запуск завода
screen = robots.display.set_mode((W, H)) # построим цех для тестирования роботов
clock = robots.time.Clock() # установим скорость всех роботов

# ================== РЕКТЫ (прямоугольники) ==================
# 1) оранжевый вправо (после выхода за границу возвращается в старт)
orange_Zagotovka = robots.Rect(20, 120, 60, 40)
orange = orange_Zagotovka.copy()
dvigenie_X = 3

# 2) зелёный и фиолетовый влево (с возвратом на старт)
green_Zagotovka   = robots.Rect(700, 60, 60, 40)
green  = green_Zagotovka.copy()
green_edet_po_X = -2

violet_Zagotovka  = robots.Rect(700, 200, 60, 40)
violet = violet_Zagotovka.copy()
violet_edet_po_X = -4

# ================== РОМБЫ (сверху вниз, разные скорости) ==================
# равномерно по ширине: 1/4, 2/4, 3/4
def diamond_points(cx, cy, w, h):
    # ромб из 4 точек: верх, право, низ, лево
    return [(cx, cy - h//2), (cx + w//2, cy), (cx, cy + h//2), (cx - w//2, cy)]

diamond_width, diamond_height = 50, 70
rhomb_starts = [
    {"cx": int(W*0.25), "cy": -40, "color": (255, 160, 160), "vy": 2},  # светло-красный
    {"cx": int(W*0.50), "cy": -120, "color": (128, 0, 32),   "vy": 3},  # бордовый
    {"cx": int(W*0.75), "cy": -200, "color": (139, 69, 19),  "vy": 5},  # коричневый
]
rhombs = [dict(d) for d in rhomb_starts]  # текущие позиции (cx, cy) меняются

# ================== ЖЁЛТЫЙ КРУГ (управляется стрелками) ==================
KRUG_pos = [40, H - 40]   # левый нижний угол
KRUG_base_r = 24
KRUG_r = KRUG_base_r
KRUG_color_normal = "yellow"
KRUG_color_small  = (255, 255, 224)  # светло-жёлтый
KRUG_color = KRUG_color_normal
KRUG_speed = 2.5

# ================== ЧЁРНЫЙ ТРЕУГОЛЬНИК (в левом верхнем углу, растёт) ==================
tri_anchor = (60, 60)  # «центр» фигуры
tri_base = [(0, -20), (-18, 16), (18, 16)]  # базовые точки относительно anchor
tri_scale = 1.0
tri_growth = 0.03  # скорость роста за кадр
tri_color = "black"

# --- Кремово-розовый овал (в правом верхнем углу) ---
oval_color = (255, 224, 230)   # кремово-розовый
oval_margin = 20               # отступ от правого и верхнего края
oval_base_w, oval_base_h = 140, 84
oval_scale = 1.0               # текущий масштаб
oval_shrink = 0.998            # скорость уменьшения (0.995 = медленно)
oval_min_scale = 0.05          # минимальный масштаб, затем ресет



def tri_points(anchor, scale):
    ax, ay = anchor
    pts = []
    for (x, y) in tri_base:
        pts.append((ax + int(x*scale), ay + int(y*scale)))
    return pts

# ================== ЦИКЛ ==================
running = True
while running:
    for e in robots.event.get():
        if e.type == robots.QUIT:
            running = False
        elif e.type == robots.KEYDOWN:
            if e.key == robots.K_SPACE:
                # пробел: покрасить в светло-жёлтый и уменьшить в 2 раза
                KRUG_color = KRUG_color_small
                KRUG_r = max(4, KRUG_base_r // 2)
                KRUG_speed = 1.5
            if e.key in (robots.K_LSHIFT, robots.K_RSHIFT):
                # shift: вернуть нормальный цвет и размер
                KRUG_color = KRUG_color_normal
                KRUG_r = KRUG_base_r
                KRUG_speed = 2.5

    # --- управление кругом (стрелки) ---
    keys = robots.key.get_pressed()
    if keys[robots.K_LEFT]:  KRUG_pos[0] -= KRUG_speed
    if keys[robots.K_RIGHT]: KRUG_pos[0] += KRUG_speed
    if keys[robots.K_UP]:    KRUG_pos[1] -= KRUG_speed
    if keys[robots.K_DOWN]:  KRUG_pos[1] += KRUG_speed
    # по желанию можно ограничить экраном:
    KRUG_pos[0] = max(KRUG_r, min(W - KRUG_r, KRUG_pos[0]))
    KRUG_pos[1] = max(KRUG_r, min(H - KRUG_r, KRUG_pos[1]))

    # --- движение прямоугольников ---
    orange.x += dvigenie_X
    if orange.left > W:  # вышел справа — вернуть на старт
        orange = orange_Zagotovka.copy()

    green.x  += green_edet_po_X
    violet.x += violet_edet_po_X
    if green.right < 0:
        green = green_Zagotovka.copy()
    if violet.right < 0:
        violet = violet_Zagotovka.copy()

    # --- движение ромбов сверху вниз (со сбросом на старт) ---
    for i, rh in enumerate(rhombs):
        rh["cy"] += rh["vy"]
        if rh["cy"] - diamond_height//2 > H:
            # вернуть на старт (горизонталь фиксированная, вертикаль стартовая)
            rh["cx"] = rhomb_starts[i]["cx"]
            rh["cy"] = rhomb_starts[i]["cy"]

    # --- рост треугольника ---
    tri_scale += tri_growth
    # (опционально лимитируй)
    if tri_scale > 36.0:
        tri_scale = 1.0  # по кругу: заново рост
    
    # --- обновление овала ---
    oval_scale *= oval_shrink
    if oval_scale < oval_min_scale:
        oval_scale = 1.0

    cur_w = int(oval_base_w * oval_scale)
    cur_h = int(oval_base_h * oval_scale)
    # фиксируем верхний правый угол: правый край = W - oval_margin, верх = oval_margin
    oval_rect = robots.Rect(W - oval_margin - cur_w, oval_margin, cur_w, cur_h)

    
    
    # --- РЕНДЕР ---
    screen.fill("white")
    
    # треугольник (растёт)
    robots.draw.polygon(screen, tri_color, tri_points(tri_anchor, tri_scale))
    robots.draw.ellipse(screen, oval_color, oval_rect)

    # прямоугольники
    robots.draw.rect(screen, (255, 140, 0), orange)       # оранжевый
    robots.draw.rect(screen, "green", green)               # зелёный
    robots.draw.rect(screen, (138, 43, 226), violet)       # фиолетовый (blueviolet)

    # ромбы
    for rh in rhombs:
        pts = diamond_points(rh["cx"], rh["cy"], diamond_width, diamond_height)
        robots.draw.polygon(screen, rh["color"], pts)

    # круг (управление)
    robots.draw.circle(screen, KRUG_color, (int(KRUG_pos[0]), int(KRUG_pos[1])), KRUG_r)

    robots.display.flip()
    clock.tick(60)


robots.quit()
