from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os, math

W, H = A4
OUT = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
pdfmetrics.registerFont(TTFont("Arial", os.path.join(FONT_DIR, "arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", os.path.join(FONT_DIR, "arialbd.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Oblique", os.path.join(FONT_DIR, "ariali.ttf")))

# Game-accurate colors
GOLD = HexColor("#c9a84c")
DARK = HexColor("#1a1a2e")
CREAM = HexColor("#f5f0e1")
GRAY = HexColor("#7f8c8d")
BROWN = HexColor("#5D4037")
RED = HexColor("#c0392b")
GREEN = HexColor("#27ae60")
SAND = HexColor("#d4a76a")

# Game-accurate element colors
WATER_SEA = HexColor("#0e6655")
WATER_TIBER = HexColor("#1a5276")
WATER_HARBOR = HexColor("#1b4f72")
WATER_FORTRESS = HexColor("#154360")
BOAT_HULL = HexColor("#654321")
BOAT_DECK = HexColor("#daa520")
BOAT_MAST = HexColor("#8B7355")
BOAT_SAIL = HexColor("#f5f5dc")
BOAT_RAM = HexColor("#888888")
ENEMY_HULL = HexColor("#8b0000")
ENEMY_SAIL = HexColor("#cc0000")
ROCK_FILL = HexColor("#5d6d7e")
ROCK_STROKE = HexColor("#7f8c8d")
COIN_GOLD = HexColor("#ffd700")
COIN_DARK = HexColor("#b8860b")
HEALTH_RED = HexColor("#e74c3c")
ORANGE = HexColor("#ff6600")
PANEL_BG = Color(0, 0, 0, 0.75)

def draw_bg(c, color=DARK):
    c.setFillColor(color)
    c.rect(0, 0, W, H, fill=1, stroke=0)

def draw_page_frame(c):
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.rect(10*mm, 10*mm, W-20*mm, H-20*mm)

def draw_label(c, text, x, y, size=9, color=GOLD, bold=False):
    fn = "Arial-Bold" if bold else "Arial"
    c.setFillColor(color)
    c.setFont(fn, size)
    c.drawString(x, y, text)

def draw_arrow_line(c, x1, y1, x2, y2, color=GOLD, lw=1):
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    c.line(x1, y1, x2, y2)
    angle = math.atan2(y2-y1, x2-x1)
    al = 6
    c.line(x2, y2, x2 - al*math.cos(angle-0.4), y2 - al*math.sin(angle-0.4))
    c.line(x2, y2, x2 - al*math.cos(angle+0.4), y2 - al*math.sin(angle+0.4))

def draw_callout(c, text, px, py, tx, ty, size=8):
    draw_arrow_line(c, px, py, tx, ty, GOLD, 0.8)
    c.setFillColor(PANEL_BG)
    tw = len(text) * size * 0.55 + 6
    c.roundRect(px - 2, py - 3, tw, size + 6, 3, fill=1, stroke=0)
    draw_label(c, text, px, py, size, CREAM)

# ============================================================
# GAME-ACCURATE ELEMENT DRAWING (matches HTML5 Canvas code)
# ============================================================
def draw_game_boat(c, x, y, w=60, h=28, is_enemy=False):
    hull_c = ENEMY_HULL if is_enemy else BOAT_HULL
    stroke_c = HexColor("#ff4444") if is_enemy else GOLD
    deck_c = HexColor("#ff6666") if is_enemy else BOAT_DECK
    sail_c = ENEMY_SAIL if is_enemy else BOAT_SAIL
    sail_stroke = HexColor("#ff0000") if is_enemy else GOLD

    c.setFillColor(hull_c)
    c.setStrokeColor(stroke_c)
    c.setLineWidth(2)
    p = c.beginPath()
    p.moveTo(x - w/2, y - h/4)
    p.lineTo(x + w/2, y - h/4)
    p.lineTo(x + w/2 - 5, y + h/4)
    p.lineTo(x - w/2 + 5, y + h/4)
    p.close()
    c.drawPath(p, fill=1, stroke=1)

    c.setStrokeColor(deck_c)
    c.setLineWidth(1)
    c.line(x - w/3, y, x + w/3, y)

    c.setFillColor(BOAT_MAST)
    c.rect(x - 2, y - h/2 - 10, 4, h/2 + 5, fill=1, stroke=0)

    c.setFillColor(sail_c)
    c.setStrokeColor(sail_stroke)
    c.setLineWidth(1)
    p2 = c.beginPath()
    p2.moveTo(x + 2, y - h/2 - 8)
    p2.lineTo(x + 22, y - h/4)
    p2.lineTo(x + 2, y + h/8)
    p2.close()
    c.drawPath(p2, fill=1, stroke=1)

    c.setFillColor(BOAT_RAM)
    p3 = c.beginPath()
    p3.moveTo(x - w/2 - 8, y)
    p3.lineTo(x - w/2, y - 4)
    p3.lineTo(x - w/2, y + 4)
    p3.close()
    c.drawPath(p3, fill=1, stroke=0)

def draw_game_rock(c, x, y, w=40, h=32):
    c.setFillColor(ROCK_FILL)
    c.setStrokeColor(ROCK_STROKE)
    c.setLineWidth(1)
    p = c.beginPath()
    p.moveTo(x, y)
    p.lineTo(x + w, y + 2)
    p.lineTo(x + w - 3, y + h)
    p.lineTo(x + 3, y + h - 2)
    p.close()
    c.drawPath(p, fill=1, stroke=1)
    c.setFillColor(HexColor("#85929e"))
    c.circle(x + w/2 - 3, y + h/3, 3, fill=1, stroke=0)

def draw_game_coin(c, x, y, r=10):
    c.setFillColor(COIN_GOLD)
    c.setStrokeColor(COIN_DARK)
    c.setLineWidth(2)
    c.circle(x, y, r, fill=1, stroke=1)
    c.setFillColor(COIN_DARK)
    c.setFont("Arial-Bold", 12)
    c.drawCentredString(x, y - 4, "$")

def draw_game_water(c, x, y, w, h, water_color):
    c.setFillColor(water_color)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.setStrokeColor(Color(0.2, 0.6, 0.86, 0.3))
    c.setLineWidth(2)
    for row in range(int(h/40) + 1):
        yy = y + row * 40
        pts = []
        for j in range(int(w/5) + 1):
            cx = x + j * 5
            cy = yy + 4 * math.sin(j * 0.5)
            pts.append((cx, cy))
        for k in range(len(pts)-1):
            c.line(pts[k][0], pts[k][1], pts[k+1][0], pts[k+1][1])

def draw_game_hud(c, x, y):
    c.setFillColor(PANEL_BG)
    c.roundRect(x, y, 200, 50, 5, fill=1, stroke=0)
    for i in range(3):
        hx = x + 15 + i * 28
        hy = y + 25
        c.setFillColor(HEALTH_RED)
        c.setStrokeColor(GOLD)
        c.setLineWidth(2)
        c.circle(hx, hy, 10, fill=1, stroke=1)
    c.setFillColor(HEALTH_RED)
    c.rect(x + 100, y + 20, 80, 12, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.rect(x + 100, y + 20, 80, 12, fill=0, stroke=1)
    draw_label(c, "RAM", x + 102, y + 22, 8, GOLD)

def draw_game_progress(c, x, y, progress=0.6):
    c.setFillColor(PANEL_BG)
    c.roundRect(x, y, 180, 18, 3, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(x + 2, y + 2, 176 * progress, 14, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.rect(x + 2, y + 2, 176, 14, fill=0, stroke=1)
    draw_label(c, f"{int(progress*350)}/350", x + 150, y + 4, 9, CREAM)

# ============================================================
# BANK DECORATION DRAWING (game-accurate)
# ============================================================
def draw_deco_seaweed(c, x, y):
    c.setStrokeColor(HexColor("#2ecc71"))
    c.setLineWidth(3)
    p1 = c.beginPath()
    p1.moveTo(x+25, y+60)
    # quadratic: ctrl(x+15,y+30) -> end(x+25+sin,y+5)
    ex1 = x+25+math.sin(y*0.05)*8
    ey1 = y+5
    p1.curveTo(x+15, y+30, x+15, y+30, ex1, ey1)
    c.drawPath(p1, fill=0, stroke=1)
    c.setStrokeColor(HexColor("#27ae60"))
    c.setLineWidth(2)
    p2 = c.beginPath()
    p2.moveTo(x+35, y+60)
    ex2 = x+35+math.cos(y*0.04)*6
    ey2 = y+10
    p2.curveTo(x+45, y+35, x+45, y+35, ex2, ey2)
    c.drawPath(p2, fill=0, stroke=1)

def draw_deco_buoy(c, x, y):
    c.setFillColor(HexColor("#e74c3c"))
    c.circle(x+30, y+35, 8, fill=1, stroke=0)
    c.setFillColor(HexColor("#f5f5dc"))
    c.rect(x+28, y+10, 4, 20, fill=1, stroke=0)

def draw_deco_coral(c, x, y):
    c.setFillColor(HexColor("#e74c3c"))
    c.circle(x+25, y+45, 10, fill=1, stroke=0)
    c.circle(x+35, y+38, 8, fill=1, stroke=0)
    c.circle(x+30, y+30, 7, fill=1, stroke=0)

def draw_deco_tree(c, x, y):
    c.setFillColor(BROWN)
    c.rect(x+26, y+35, 8, 25, fill=1, stroke=0)
    c.setFillColor(HexColor("#228B22"))
    c.circle(x+30, y+25, 18, fill=1, stroke=0)
    c.setFillColor(HexColor("#2ecc71"))
    c.circle(x+24, y+22, 12, fill=1, stroke=0)

def draw_deco_bush(c, x, y):
    c.setFillColor(HexColor("#27ae60"))
    c.circle(x+30, y+45, 15, fill=1, stroke=0)
    c.circle(x+18, y+42, 10, fill=1, stroke=0)
    c.circle(x+42, y+42, 10, fill=1, stroke=0)

def draw_deco_ruin(c, x, y):
    c.setFillColor(HexColor("#bdc3c7"))
    c.rect(x+15, y+20, 8, 40, fill=1, stroke=0)
    c.rect(x+35, y+30, 8, 30, fill=1, stroke=0)
    c.rect(x+15, y+18, 28, 6, fill=1, stroke=0)
    c.setFillColor(HexColor("#95a5a6"))
    c.rect(x+25, y+25, 6, 35, fill=1, stroke=0)

def draw_deco_grass(c, x, y):
    c.setStrokeColor(HexColor("#27ae60"))
    c.setLineWidth(2)
    for i in range(5):
        c.line(x+10+i*10, y+60, x+10+i*10+math.sin(i)*5, y+35)

def draw_deco_barrel(c, x, y):
    c.setFillColor(HexColor("#8B4513"))
    c.ellipse(x+18, y+22, x+42, y+58, fill=1, stroke=0)
    c.setStrokeColor(BROWN)
    c.setLineWidth(2)
    c.ellipse(x+18, y+29, x+42, y+35, fill=0, stroke=1)
    c.ellipse(x+18, y+45, x+42, y+51, fill=0, stroke=1)

def draw_deco_crate(c, x, y):
    c.setFillColor(HexColor("#D2B48C"))
    c.rect(x+15, y+30, 30, 25, fill=1, stroke=0)
    c.setStrokeColor(HexColor("#8B4513"))
    c.setLineWidth(2)
    c.rect(x+15, y+30, 30, 25, fill=0, stroke=1)
    c.line(x+15, y+42, x+45, y+42)
    c.line(x+30, y+30, x+30, y+55)

def draw_deco_post(c, x, y):
    c.setFillColor(BROWN)
    c.rect(x+27, y+15, 6, 45, fill=1, stroke=0)
    c.setFillColor(HexColor("#bdc3c7"))
    c.circle(x+30, y+15, 5, fill=1, stroke=0)

def draw_deco_net(c, x, y):
    c.setStrokeColor(HexColor("#f5f5dc"))
    c.setLineWidth(1)
    for i in range(4):
        c.line(x+15, y+20+i*10, x+45, y+20+i*10)
        c.line(x+15+i*10, y+20, x+15+i*10, y+50)

def draw_deco_wall(c, x, y):
    c.setFillColor(GRAY)
    c.rect(x+5, y+10, 50, 50, fill=1, stroke=0)
    c.setFillColor(HexColor("#95a5a6"))
    for r in range(4):
        for col in range(3):
            c.rect(x+8+col*16+(r%2)*8, y+13+r*12, 14, 10, fill=1, stroke=0)
    c.setFillColor(BROWN)
    c.rect(x+22, y+35, 16, 25, fill=1, stroke=0)

def draw_deco_tower(c, x, y):
    c.setFillColor(GRAY)
    c.rect(x+12, y+5, 36, 55, fill=1, stroke=0)
    c.setFillColor(HexColor("#95a5a6"))
    for i in range(4):
        c.rect(x+12+i*9, y+2, 8, 8, fill=1, stroke=0)
    c.setFillColor(BROWN)
    c.rect(x+24, y+35, 12, 25, fill=1, stroke=0)
    c.setFillColor(DARK)
    c.rect(x+18, y+15, 6, 8, fill=1, stroke=0)
    c.rect(x+36, y+15, 6, 8, fill=1, stroke=0)

def draw_deco_banner(c, x, y):
    c.setFillColor(BROWN)
    c.rect(x+28, y+5, 4, 55, fill=1, stroke=0)
    c.setFillColor(RED)
    p = c.beginPath()
    p.moveTo(x+32, y+10)
    p.lineTo(x+50, y+18)
    p.lineTo(x+32, y+30)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Arial-Bold", 8)
    c.drawString(x+33, y+24, "SPQR")

def draw_deco_palm(c, x, y):
    c.setFillColor(HexColor("#8B4513"))
    c.rect(x+27, y+30, 6, 30, fill=1, stroke=0)
    c.setStrokeColor(HexColor("#228B22"))
    c.setLineWidth(3)
    for angle_deg in [0, 72, 144, 216, 288]:
        rad = math.radians(angle_deg)
        ex = x + 30 + math.cos(rad) * 20
        ey = y + 25 + math.sin(rad) * 15
        cx1 = x+30+math.cos(rad)*10
        cy1 = y+25+math.sin(rad)*8
        p = c.beginPath()
        p.moveTo(x+30, y+25)
        p.curveTo(cx1, cy1, cx1, cy1, ex, ey)
        c.drawPath(p, fill=0, stroke=1)

def draw_deco_pyramid(c, x, y):
    c.setFillColor(SAND)
    p = c.beginPath()
    p.moveTo(x+30, y+10)
    p.lineTo(x+5, y+60)
    p.lineTo(x+55, y+60)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(HexColor("#c49555"))
    p2 = c.beginPath()
    p2.moveTo(x+30, y+10)
    p2.lineTo(x+30, y+60)
    p2.lineTo(x+55, y+60)
    p2.close()
    c.drawPath(p2, fill=1, stroke=0)
    c.setStrokeColor(COIN_DARK)
    c.setLineWidth(1)
    p3 = c.beginPath()
    p3.moveTo(x+30, y+10)
    p3.lineTo(x+5, y+60)
    p3.lineTo(x+55, y+60)
    p3.close()
    c.drawPath(p3, fill=0, stroke=1)

def draw_deco_sand(c, x, y):
    c.setFillColor(HexColor("#f0d9a0"))
    c.ellipse(x, y+38, x+60, y+62, fill=1, stroke=0)

def draw_deco_cactus(c, x, y):
    c.setFillColor(HexColor("#27ae60"))
    c.rect(x+26, y+20, 8, 40, fill=1, stroke=0)
    c.rect(x+14, y+28, 14, 8, fill=1, stroke=0)
    c.rect(x+14, y+22, 8, 14, fill=1, stroke=0)
    c.rect(x+36, y+32, 14, 8, fill=1, stroke=0)
    c.rect(x+42, y+26, 8, 14, fill=1, stroke=0)

def draw_deco_birch(c, x, y):
    c.setFillColor(HexColor("#ecf0f1"))
    c.rect(x+27, y+20, 6, 40, fill=1, stroke=0)
    c.setStrokeColor(DARK)
    c.setLineWidth(1)
    for i in range(4):
        c.line(x+27, y+25+i*8, x+33, y+23+i*8)
    c.setFillColor(HexColor("#2ecc71"))
    c.circle(x+30, y+18, 14, fill=1, stroke=0)

def draw_deco_izba(c, x, y):
    c.setFillColor(HexColor("#8B4513"))
    c.rect(x+10, y+30, 40, 30, fill=1, stroke=0)
    c.setFillColor(HexColor("#D2691E"))
    p = c.beginPath()
    p.moveTo(x+5, y+30)
    p.lineTo(x+30, y+12)
    p.lineTo(x+55, y+30)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(BROWN)
    c.rect(x+24, y+40, 12, 20, fill=1, stroke=0)
    c.setFillColor(HexColor("#f39c12"))
    c.rect(x+15, y+36, 8, 8, fill=1, stroke=0)

def draw_deco_fence(c, x, y):
    c.setFillColor(HexColor("#8B4513"))
    for i in range(5):
        c.rect(x+8+i*10, y+25, 4, 35, fill=1, stroke=0)
    c.rect(x+8, y+32, 44, 4, fill=1, stroke=0)
    c.rect(x+8, y+48, 44, 4, fill=1, stroke=0)

def draw_deco_church(c, x, y):
    c.setFillColor(HexColor("#ecf0f1"))
    c.rect(x+15, y+25, 30, 35, fill=1, stroke=0)
    c.setFillColor(DARK)
    p = c.beginPath()
    p.moveTo(x+12, y+25)
    p.lineTo(x+30, y+8)
    p.lineTo(x+48, y+25)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.circle(x+30, y+10, 4, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(x+30, y+6, x+30, y+14)
    c.line(x+26, y+10, x+34, y+10)
    c.setFillColor(BROWN)
    c.rect(x+25, y+40, 10, 20, fill=1, stroke=0)

# ============================================================
# ROMAN CHARACTER DRAWING (game-accurate with size=50)
# ============================================================
def draw_roman(c, x, y, rtype="legionary", size=40):
    s = size
    # Helmet dome (semicircle)
    c.setFillColor(HexColor("#888888"))
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    r = s * 0.45
    p_helm = c.beginPath()
    for deg in range(0, 181, 5):
        rad = math.radians(deg)
        px = x + r * math.cos(rad)
        py = y - s*0.2 + r * math.sin(rad)
        if deg == 0:
            p_helm.moveTo(px, py)
        else:
            p_helm.lineTo(px, py)
    p_helm.close()
    c.drawPath(p_helm, fill=1, stroke=1)
    c.setFillColor(HexColor("#888888"))
    c.rect(x - s*0.35, y - s*0.4, s*0.7, s*0.55, fill=1, stroke=0)

    # Crest/plume (quadratic beziers converted to cubic)
    c.setFillColor(RED)
    p = c.beginPath()
    p.moveTo(x, y - s*0.55)
    # Q1: (x, y-s*0.55) -> ctrl(x+s*0.15, y-s*0.45) -> (x+s*0.15, y-s*0.35)
    c1x = x + (x + s*0.15 - x) * 2/3
    c1y = (y - s*0.55) + ((y - s*0.45) - (y - s*0.55)) * 2/3
    c2x = (x + s*0.15) + ((x + s*0.15) - (x + s*0.15)) * 2/3
    c2y = (y - s*0.35) + ((y - s*0.45) - (y - s*0.35)) * 2/3
    p.curveTo(c1x, c1y, c2x, c2y, x + s*0.15, y - s*0.35)
    # Q2: -> ctrl(x+s*0.15, y-s*0.25) -> (x, y-s*0.15)
    c1x2 = x + s*0.15
    c1y2 = y - s*0.35 + 2/3 * ((y - s*0.25) - (y - s*0.35))
    c2x2 = x + 2/3 * ((x + s*0.15) - x)
    c2y2 = (y - s*0.15) + 2/3 * ((y - s*0.25) - (y - s*0.15))
    p.curveTo(c1x2, c1y2, c2x2, c2y2, x, y - s*0.15)
    # Q3: -> ctrl(x-s*0.15, y-s*0.25) -> (x-s*0.15, y-s*0.35)
    c1x3 = x
    c1y3 = (y - s*0.15) + 2/3 * ((y - s*0.25) - (y - s*0.15))
    c2x3 = (x - s*0.15) + 2/3 * ((x - s*0.15) - (x - s*0.15))
    c2y3 = (y - s*0.35) + 2/3 * ((y - s*0.25) - (y - s*0.35))
    p.curveTo(c1x3, c1y3, c2x3, c2y3, x - s*0.15, y - s*0.35)
    # Q4: -> ctrl(x-s*0.15, y-s*0.45) -> (x, y-s*0.55)
    c1x4 = x - s*0.15
    c1y4 = (y - s*0.35) + 2/3 * ((y - s*0.45) - (y - s*0.35))
    c2x4 = x + 2/3 * ((x - s*0.15) - x)
    c2y4 = (y - s*0.55) + 2/3 * ((y - s*0.45) - (y - s*0.55))
    p.curveTo(c1x4, c1y4, c2x4, c2y4, x, y - s*0.55)
    c.drawPath(p, fill=1, stroke=0)

    # Face
    face_c = HexColor("#d4a574") if rtype == "slave" else HexColor("#e8c088")
    c.setFillColor(face_c)
    c.circle(x, y + s*0.05, s*0.3, fill=1, stroke=0)

    # Eyes
    c.setFillColor(HexColor("#222222"))
    c.circle(x - s*0.12, y - s*0.02, s*0.04, fill=1, stroke=0)
    c.circle(x + s*0.12, y - s*0.02, s*0.04, fill=1, stroke=0)

    # Mouth (arc approximated with lines)
    c.setStrokeColor(HexColor("#6b3a1f"))
    c.setLineWidth(2)
    p_mouth = c.beginPath()
    for deg in range(0, 181, 10):
        rad = math.radians(deg)
        mx = x + s*0.1 * math.cos(rad)
        my = y + s*0.12 + s*0.08 * math.sin(rad)
        if deg == 0:
            p_mouth.moveTo(mx, my)
        else:
            p_mouth.lineTo(mx, my)
    c.drawPath(p_mouth, fill=0, stroke=1)

    # Type-specific features
    if rtype == "senator":
        c.setStrokeColor(HexColor("#228B22"))
        c.setLineWidth(3)
        p_wreath = c.beginPath()
        for deg in range(320, 381, 5):
            rad = math.radians(deg)
            wx = x + s*0.35 * math.cos(rad)
            wy = y - s*0.25 + s*0.35 * math.sin(rad)
            if deg == 320:
                p_wreath.moveTo(wx, wy)
            else:
                p_wreath.lineTo(wx, wy)
        c.drawPath(p_wreath, fill=0, stroke=1)
    elif rtype == "centurion":
        c.setStrokeColor(HexColor("#a0522d"))
        c.setLineWidth(2)
        c.line(x + s*0.15, y - s*0.1, x + s*0.25, y + s*0.15)
    elif rtype == "gladiator":
        c.setFillColor(GOLD)
        c.circle(x - s*0.12, y - s*0.09, s*0.025, fill=1, stroke=0)
        c.circle(x + s*0.12, y - s*0.09, s*0.025, fill=1, stroke=0)

# ============================================================
# FULL GAME SCENE RENDERING
# ============================================================
def draw_full_scene(c, x, y, w, h, water_color, bank_theme=None):
    draw_game_water(c, x, y, w, h, water_color)
    if bank_theme:
        if bank_theme == "sea":
            draw_deco_seaweed(c, x+5, y+5)
            draw_deco_coral(c, x+w-65, y+5)
            draw_deco_buoy(c, x+5, y+h-65)
        elif bank_theme == "tiber":
            draw_deco_tree(c, x+5, y+10)
            draw_deco_bush(c, x+w-65, y+20)
            draw_deco_ruin(c, x+5, y+h-70)
        elif bank_theme == "harbor":
            draw_deco_barrel(c, x+5, y+10)
            draw_deco_crate(c, x+w-65, y+15)
            draw_deco_post(c, x+25, y+h-65)
            draw_deco_net(c, x+w-65, y+h-60)
        elif bank_theme == "fortress":
            draw_deco_wall(c, x+5, y+5)
            draw_deco_tower(c, x+w-65, y+5)
            draw_deco_banner(c, x+20, y+h-65)
        elif bank_theme == "pyramid":
            draw_deco_pyramid(c, x+5, y+10)
            draw_deco_palm(c, x+w-65, y+10)
            draw_deco_cactus(c, x+5, y+h-65)
            draw_deco_sand(c, x+w-65, y+h-50)
        elif bank_theme == "rus":
            draw_deco_birch(c, x+5, y+10)
            draw_deco_izba(c, x+w-65, y+10)
            draw_deco_fence(c, x+20, y+h-65)
            draw_deco_church(c, x+w-70, y+h-70)

# ============================================================
# ILLUSTRATION PAGES
# ============================================================
def page_title(c):
    draw_bg(c, DARK)
    c.setStrokeColor(GOLD)
    c.setLineWidth(3)
    c.rect(12*mm, 12*mm, W-24*mm, H-24*mm)
    c.setFillColor(GOLD)
    c.setFont("Arial-Bold", 10)
    c.drawCentredString(W/2, H-25*mm, "TOME I - ILLUSTRATED GUIDE")
    c.setFont("Arial-Bold", 32)
    c.drawCentredString(W/2, H-55*mm, "GAME VISUAL GUIDE")
    c.setFont("Arial-Bold", 18)
    c.setFillColor(CREAM)
    c.drawCentredString(W/2, H-75*mm, "Every Element Annotated")
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(60*mm, H-82*mm, W-60*mm, H-82*mm)

    bx, by, bw, bh = 30*mm, H-160*mm, W-60*mm, 65*mm
    draw_game_water(c, bx, by, bw, bh, WATER_SEA)
    draw_game_boat(c, bx+bw/2-40, by+bh/2, 50, 24, False)
    draw_game_boat(c, bx+bw/2+50, by+bh/2+10, 45, 20, True)
    draw_game_rock(c, bx+bw/2+10, by+10, 30, 25)
    draw_game_coin(c, bx+bw/2-20, by+bh-15, 8)

    c.setFillColor(GOLD)
    c.setFont("Arial-Oblique", 10)
    c.drawCentredString(W/2, 25*mm, "Generated from actual game data - roman-boats.html")
    c.showPage()

def page_boat_anatomy(c):
    draw_bg(c, DARK)
    draw_page_frame(c)
    draw_label(c, "PLAYER BOAT - ANATOMY", 25*mm, H-25*mm, 16, GOLD, True)

    bx, by = W/2, H-130*mm
    draw_game_boat(c, bx, by, 120, 56, False)

    draw_callout(c, "Hull #654321", bx-95, by+45, bx-70, by+10)
    draw_callout(c, "Gold trim #c9a84c", bx+30, by+45, bx+35, by+8)
    draw_callout(c, "Mast #8B7355", bx+15, by+55, bx+5, by+35)
    draw_callout(c, "Sail (ivory)", bx+55, by+40, bx+50, by+15)
    draw_callout(c, "Ram #888888", bx-110, by+20, bx-75, by)
    draw_callout(c, "Deck line #daa520", bx+30, by-15, bx+35, by-5)

    draw_label(c, "The ram (rostrum) is at the FRONT - press SPACE to activate!", 25*mm, H-175*mm, 11, CREAM)
    draw_label(c, "Ram hit deals damage to enemies. Cooldown: 60 frames (~1 second)", 25*mm, H-185*mm, 10, HexColor("#aaaaaa"))

    draw_label(c, "Enemy boat uses same structure but with red colors:", 25*mm, H-200*mm, 11, CREAM, True)
    draw_game_boat(c, W/2, H-220*mm, 110, 50, True)
    draw_label(c, "Hull: #8b0000  Sail: #cc0000  Stroke: #ff4444", 25*mm, H-240*mm, 10, HexColor("#ff6666"))

    c.showPage()

def page_obstacles_coins(c):
    draw_bg(c, DARK)
    draw_page_frame(c)
    draw_label(c, "OBSTACLES & COLLECTIBLES", 25*mm, H-25*mm, 16, GOLD, True)

    # ROCK
    draw_label(c, "ROCK", 25*mm, H-42*mm, 13, RED, True)
    draw_game_rock(c, 60*mm, H-90*mm, 60, 48)
    draw_callout(c, "Fill: #5d6d7e", 25*mm, H-105*mm, 55*mm, H-90*mm)
    draw_callout(c, "Highlight: #85929e", 100*mm, H-115*mm, 85*mm, H-85*mm)
    draw_callout(c, "Stroke: #7f8c8d", 110*mm, H-100*mm, 100*mm, H-65*mm)
    draw_label(c, "Size: 30-50 x 25-40 px (random)", 25*mm, H-120*mm, 9, HexColor("#aaaaaa"))
    draw_label(c, "Cannot be destroyed - only dodged!", 25*mm, H-130*mm, 10, RED)

    # COIN
    draw_label(c, "GOLD COIN", 25*mm, H-145*mm, 13, GOLD, True)
    draw_game_coin(c, 70*mm, H-185*mm, 16)
    draw_game_coin(c, 95*mm, H-185*mm, 10)
    draw_game_coin(c, 115*mm, H-185*mm, 13)
    draw_callout(c, "Fill: #ffd700", 25*mm, H-195*mm, 60*mm, H-185*mm)
    draw_callout(c, "Stroke: #b8860b", 100*mm, H-200*mm, 100*mm, H-185*mm)
    draw_callout(c, "Symbol: $ (Georgia Bold 12px)", 130*mm, H-190*mm, 120*mm, H-180*mm)
    draw_label(c, "Radius: 10px + sin(pulse)*2 animation", 25*mm, H-210*mm, 9, HexColor("#aaaaaa"))
    draw_label(c, "Value: 10 points. Safe to collect!", 25*mm, H-220*mm, 10, GREEN)

    # PARTICLES
    draw_label(c, "PARTICLE EFFECTS", 25*mm, H-238*mm, 13, GOLD, True)
    effects = [("Rock hit", GRAY, 8), ("Coin", COIN_GOLD, 12), ("Ram", RED, 10), ("Kill", ORANGE, 20), ("Damage", HEALTH_RED, 10)]
    ex = 30*mm
    for name, color, count in effects:
        for j in range(min(count, 8)):
            px = ex + (j % 4) * 8
            py = H - 255*mm + (j // 4) * 10
            c.setFillColor(color)
            c.circle(px, py, 2 + (j%3), fill=1, stroke=0)
        draw_label(c, name, ex - 3, H - 268*mm, 7, color)
        ex += 30*mm

    c.showPage()

def page_hud(c):
    draw_bg(c, DARK)
    draw_page_frame(c)
    draw_label(c, "HUD - HEADS-UP DISPLAY", 25*mm, H-25*mm, 16, GOLD, True)

    # Full HUD mockup
    hud_x, hud_y = 30*mm, H-100*mm
    draw_game_hud(c, hud_x, hud_y)
    draw_callout(c, "Health: 3 red circles", hud_x - 5, hud_y + 60, hud_x + 50, hud_y + 35)
    draw_callout(c, "Ram cooldown bar", hud_x + 100, hud_y + 60, hud_x + 130, hud_y + 32)

    # Progress bar
    draw_game_progress(c, hud_x, hud_y - 30, 0.6)
    draw_callout(c, "Level progress", hud_x - 5, hud_y - 45, hud_x + 70, hud_y - 22)
    draw_label(c, "score/next_level_threshold", hud_x + 100, hud_y - 45, 8, HexColor("#aaaaaa"))

    # Score display
    draw_label(c, "Score display (HTML above canvas):", 25*mm, H-155*mm, 11, CREAM, True)
    c.setFillColor(PANEL_BG)
    c.roundRect(25*mm, H-185*mm, 160*mm, 18*mm, 5, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Arial-Bold", 20)
    c.drawString(30*mm, H-178*mm, "Score: 150 | Tiber Banks")
    draw_label(c, "Font: Georgia Bold 28px, color: #c9a84c", 25*mm, H-195*mm, 8, HexColor("#aaaaaa"))

    # Level transition banner
    draw_label(c, "Level Transition Banner:", 25*mm, H-210*mm, 11, CREAM, True)
    c.setFillColor(PANEL_BG)
    c.roundRect(25*mm, H-250*mm, W-50*mm, 25*mm, 5, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Arial-Bold", 18)
    c.drawCentredString(W/2, H-240*mm, "LEVEL 2: TIBER BANKS")
    c.setFillColor(CREAM)
    c.setFont("Arial", 10)
    c.drawCentredString(W/2, H-248*mm, "Heart of Rome")
    draw_label(c, "Duration: 150 frames. Fade in/out animation.", 25*mm, H-260*mm, 8, HexColor("#aaaaaa"))

    # Roman popup
    draw_label(c, "Roman Character Popup:", 25*mm, H-275*mm, 11, CREAM, True)
    c.setFillColor(PANEL_BG)
    c.roundRect(25*mm, H-370*mm, 45*mm, 37*mm, 8, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.roundRect(25*mm, H-370*mm, 45*mm, 37*mm, 8, fill=0, stroke=1)
    draw_roman(c, 47*mm, H-330*mm, "centurion", 30)
    c.setFillColor(CREAM)
    c.setFont("Arial", 7)
    c.drawCentredString(47*mm, H-350*mm, "RAM THEM!")
    c.drawCentredString(47*mm, H-357*mm, "We don't retreat!")
    draw_label(c, "Size: 170x140px at (15,80)", 75*mm, H-340*mm, 8, HexColor("#aaaaaa"))
    draw_label(c, "Duration: 180 frames", 75*mm, H-350*mm, 8, HexColor("#aaaaaa"))
    draw_label(c, "Fade in: 20f, Fade out: 30f", 75*mm, H-360*mm, 8, HexColor("#aaaaaa"))

    c.showPage()

def page_characters(c):
    draw_bg(c, DARK)
    draw_page_frame(c)
    draw_label(c, "ROMAN CHARACTERS - ALL 6 TYPES", 25*mm, H-25*mm, 16, GOLD, True)

    chars = [
        ("SENATOR", "senator", "Laurel wreath #228B22"),
        ("CENTURION", "centurion", "Scar #a0522d"),
        ("LEGIONARY", "legionary", "Standard fighter"),
        ("MERCHANT", "legionary", "Gold trader"),
        ("GLADIATOR", "gladiator", "Gold eyebrow rings"),
        ("SLAVE", "slave", "Darker skin #d4a574"),
    ]
    cx = 35*mm
    for i, (name, rtype, feature) in enumerate(chars):
        col = i % 3
        row = i // 3
        px = 35*mm + col * 55*mm
        py = H - 70*mm - row * 80*mm
        draw_roman(c, px, py, rtype, 35)
        draw_label(c, name, px - 15, py - 50, 10, GOLD, True)
        draw_label(c, feature, px - 15, py - 62, 7, HexColor("#aaaaaa"))

    draw_label(c, "Appear on events: coin collect, ram, damage, milestone, level start", 25*mm, H-245*mm, 10, CREAM)
    draw_label(c, "Popup box: 170x140px, rounded corners, gold border, 75% black bg", 25*mm, H-257*mm, 9, HexColor("#aaaaaa"))

    c.showPage()

def page_level_preview(c, level_num, level_name, water_color, theme, difficulty, speed, enemies_hp, score_needed, deco_names):
    draw_bg(c, DARK)
    draw_page_frame(c)
    draw_label(c, f"LEVEL {level_num}: {level_name}", 25*mm, H-25*mm, 16, GOLD, True)

    # Game scene
    sx, sy, sw, sh = 20*mm, H-140*mm, W-40*mm, 80*mm
    draw_full_scene(c, sx, sy, sw, sh, water_color, theme)
    draw_game_boat(c, sx + sw/2, sy + sh/2, 50, 24, False)
    draw_game_rock(c, sx + sw/2 + 60, sy + sh/3, 35, 28)
    draw_game_coin(c, sx + sw/2 - 40, sy + sh/2 + 20, 9)

    # Stats
    draw_label(c, f"Difficulty: {'*' * difficulty}{'.' * (5-difficulty)} ({difficulty}/5)", 25*mm, H-155*mm, 11, CREAM)
    draw_label(c, f"Speed: {speed[0]} -> {speed[1]} | Enemies: HP {enemies_hp} | Set: {score_needed} pts", 25*mm, H-167*mm, 10, HexColor("#aaaaaa"))

    # Decorations list
    draw_label(c, "Bank Decorations:", 25*mm, H-183*mm, 12, GOLD, True)
    dy = H - 196*mm
    for dn in deco_names:
        draw_label(c, f"  - {dn}", 30*mm, dy, 9, CREAM)
        dy -= 11

    # Water color swatch
    c.setFillColor(water_color)
    c.rect(W-60*mm, H-175*mm, 30*mm, 15*mm, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.rect(W-60*mm, H-175*mm, 30*mm, 15*mm, fill=0, stroke=1)
    draw_label(c, f"Water: {water_color.hexval()}", W-60*mm, H-183*mm, 7, HexColor("#aaaaaa"))

    c.showPage()

def page_gameplay_situation(c, title, description, setup_fn):
    draw_bg(c, DARK)
    draw_page_frame(c)
    draw_label(c, title, 25*mm, H-25*mm, 16, GOLD, True)

    sx, sy, sw, sh = 20*mm, H-150*mm, W-40*mm, 90*mm
    setup_fn(c, sx, sy, sw, sh)

    draw_label(c, description, 25*mm, H-168*mm, 10, CREAM)
    c.showPage()

def situation_ramming(c, x, y, w, h):
    draw_game_water(c, x, y, w, h, WATER_FORTRESS)
    draw_game_boat(c, x+w/2-20, y+h/2, 50, 24, False)
    draw_game_boat(c, x+w/2+35, y+h/2, 45, 20, True)
    # Ram glow
    c.setFillColor(Color(1, 0.4, 0, 0.3))
    c.circle(x+w/2+10, y+h/2+12, 18, fill=1, stroke=0)
    draw_label(c, "RAM!", x+w/2+5, y+h/2+25, 14, HexColor("#ff6600"), True)
    draw_label(c, "<-- SPACE", x+w/2-20, y+h/2+35, 9, GOLD)
    draw_label(c, "Player ram hits enemy -> +25 pts", 25*mm, y-15, 10, CREAM)
    draw_label(c, "Enemy flashes white (alpha=0.5) for 10 frames", 25*mm, y-27, 9, HexColor("#aaaaaa"))
    draw_label(c, "15 red particles burst outward", 25*mm, y-39, 9, HexColor("#aaaaaa"))
    # particles
    for i in range(12):
        px = x+w/2+10 + (i%4)*12 - 20
        py = y+h/2+12 + (i//4)*10 - 5
        c.setFillColor(RED)
        c.circle(px, py, 2, fill=1, stroke=0)

def situation_dodging(c, x, y, w, h):
    draw_game_water(c, x, y, w, h, WATER_SEA)
    draw_game_boat(c, x+w/2+30, y+h/2+15, 50, 24, False)
    draw_game_rock(c, x+w/2-30, y+h/2-10, 40, 32)
    draw_game_rock(c, x+w/2-10, y+h/2+25, 35, 28)
    draw_label(c, "Use A/D to dodge!", x+w/2+50, y+h/2+35, 10, GOLD)
    draw_label(c, "Rocks cannot be destroyed", 25*mm, y-15, 10, RED)
    draw_label(c, "Move left/right to avoid collision. Stay near center for max options.", 25*mm, y-27, 9, HexColor("#aaaaaa"))

def situation_collecting(c, x, y, w, h):
    draw_game_water(c, x, y, w, h, WATER_HARBOR)
    draw_game_boat(c, x+w/2, y+h/2, 50, 24, False)
    draw_game_coin(c, x+w/2-40, y+h/2+25, 12)
    draw_game_coin(c, x+w/2+35, y+h/2+30, 10)
    draw_game_coin(c, x+w/2-10, y+h/2+40, 8)
    draw_game_coin(c, x+w/2+50, y+h/2+15, 11)
    # particles
    for i in range(8):
        px = x+w/2-40 + (i%4)*8
        py = y+h/2+25 + (i//4)*6
        c.setFillColor(COIN_GOLD)
        c.circle(px, py, 2+(i%2), fill=1, stroke=0)
    draw_label(c, "Coins pulse with sin(r) animation", 25*mm, y-15, 10, GOLD)
    draw_label(c, "12 gold particles burst on collect. Value: 10 pts each.", 25*mm, y-27, 9, HexColor("#aaaaaa"))

def situation_damage(c, x, y, w, h):
    draw_game_water(c, x, y, w, h, WATER_TIBER)
    draw_game_boat(c, x+w/2, y+h/2, 50, 24, False)
    draw_game_rock(c, x+w/2-5, y+h/2-20, 35, 28)
    draw_game_enemy_ship(c, x+w/2+40, y+h/2+5, 40, 18)
    # damage flash
    c.setFillColor(Color(1, 0, 0, 0.15))
    c.rect(x, y, w, h, fill=1, stroke=0)
    draw_label(c, "DAMAGE!", x+w/2-20, y+h/2+35, 14, RED, True)
    # hp lost
    for i in range(3):
        hx = x + 20 + i*18
        hy = y + h - 15
        if i < 2:
            c.setFillColor(HEALTH_RED)
        else:
            c.setFillColor(HexColor("#555555"))
        c.setStrokeColor(GOLD)
        c.setLineWidth(1.5)
        c.circle(hx, hy, 7, fill=1, stroke=1)
    draw_label(c, "8 gray particles + screen flash on hit", 25*mm, y-15, 10, RED)
    draw_label(c, "Lose 1 HP (3 max). Invincibility frames after hit.", 25*mm, y-27, 9, HexColor("#aaaaaa"))

def draw_game_enemy_ship(c, x, y, w=35, h=14):
    c.setFillColor(ENEMY_HULL)
    c.setStrokeColor(HexColor("#ff4444"))
    c.setLineWidth(1)
    p = c.beginPath()
    p.moveTo(x-w/2, y-h/4)
    p.lineTo(x+w/2, y-h/4)
    p.lineTo(x+w/2-2, y+h/4)
    p.lineTo(x-w/2+2, y+h/4)
    p.close()
    c.drawPath(p, fill=1, stroke=1)
    c.setFillColor(BOAT_MAST)
    c.rect(x-1, y-h/2-5, 2, h/2+3, fill=1, stroke=0)
    c.setFillColor(ENEMY_SAIL)
    p2 = c.beginPath()
    p2.moveTo(x+1, y-h/2-3)
    p2.lineTo(x+12, y-h/4)
    p2.lineTo(x+1, y+h/6)
    p2.close()
    c.drawPath(p2, fill=1, stroke=0)

def page_decorations_catalog(c):
    draw_bg(c, DARK)
    draw_page_frame(c)
    draw_label(c, "ALL BANK DECORATIONS - CATALOG", 25*mm, H-25*mm, 16, GOLD, True)

    themes = [
        ("SEA", WATER_SEA, [draw_deco_seaweed, draw_deco_buoy, draw_deco_coral]),
        ("TIBER", WATER_TIBER, [draw_deco_tree, draw_deco_bush, draw_deco_ruin, draw_deco_grass]),
        ("HARBOR", WATER_HARBOR, [draw_deco_barrel, draw_deco_crate, draw_deco_post, draw_deco_net]),
        ("FORTRESS", WATER_FORTRESS, [draw_deco_wall, draw_deco_tower, draw_deco_banner]),
    ]

    ty = H - 40*mm
    for tname, wcolor, decos in themes:
        draw_label(c, tname, 25*mm, ty, 11, GOLD, True)
        dx = 55*mm
        for deco_fn in decos:
            draw_game_water(c, dx, ty - 12, 18*mm, 18*mm, wcolor)
            deco_fn(c, dx + 2*mm, ty - 12*mm)
            dx += 22*mm
        ty -= 28*mm

    themes2 = [
        ("PYRAMID", WATER_TIBER, [draw_deco_pyramid, draw_deco_palm, draw_deco_cactus, draw_deco_sand]),
        ("RUS", WATER_HARBOR, [draw_deco_birch, draw_deco_izba, draw_deco_fence, draw_deco_church]),
    ]
    for tname, wcolor, decos in themes2:
        draw_label(c, tname, 25*mm, ty, 11, GOLD, True)
        dx = 55*mm
        for deco_fn in decos:
            draw_game_water(c, dx, ty - 12, 18*mm, 18*mm, wcolor)
            deco_fn(c, dx + 2*mm, ty - 12*mm)
            dx += 22*mm
        ty -= 28*mm

    c.showPage()

def page_water_colors(c):
    draw_bg(c, DARK)
    draw_page_frame(c)
    draw_label(c, "WATER COLORS BY LEVEL", 25*mm, H-25*mm, 16, GOLD, True)

    levels = [
        ("Lv.1 Clean Sea", WATER_SEA, "sea"),
        ("Lv.2 Tiber Banks", WATER_TIBER, "tiber"),
        ("Lv.3 Harbor of Ostia", WATER_HARBOR, "harbor"),
        ("Lv.4 Fortress of Rome", WATER_FORTRESS, "fortress"),
        ("Lv.5 Pyramids of Egypt", WATER_TIBER, "pyramid"),
        ("Lv.6 Ancient Rus", WATER_HARBOR, "rus"),
        ("Lv.7 Final Battle", WATER_FORTRESS, "final"),
    ]

    ty = H - 45*mm
    for name, color, theme in levels:
        c.setFillColor(color)
        c.rect(25*mm, ty - 5, 80*mm, 18*mm, fill=1, stroke=0)
        c.setStrokeColor(GOLD)
        c.setLineWidth(1)
        c.rect(25*mm, ty - 5, 80*mm, 18*mm, fill=0, stroke=1)
        draw_label(c, name, 28*mm, ty, 10, CREAM)
        draw_label(c, color.hexval(), 108*mm, ty, 8, HexColor("#aaaaaa"))

        # Mini scene
        draw_game_water(c, 130*mm, ty - 5, 45*mm, 18*mm, color)
        if theme == "sea":
            draw_deco_seaweed(c, 131*mm, ty - 4)
        elif theme == "tiber":
            draw_deco_tree(c, 131*mm, ty - 3)
        elif theme == "harbor":
            draw_deco_barrel(c, 131*mm, ty - 3)
        elif theme == "fortress":
            draw_deco_tower(c, 131*mm, ty - 3)
        draw_game_boat(c, 150*mm, ty + 4, 20, 9, False)

        ty -= 25*mm

    c.showPage()

# ============================================================
# MAIN - Generate Game Art for all 3 languages
# ============================================================
LEVELS_DATA = [
    (1, "CLEAN SEA", WATER_SEA, "sea", 1, (1.5, 3), 1, 80, ["Seaweed", "Buoy", "Coral"]),
    (2, "TIBER BANKS", WATER_TIBER, "tiber", 2, (2, 4), 1, 200, ["Tree", "Bush", "Ruin", "Grass"]),
    (3, "HARBOR OF OSTIA", WATER_HARBOR, "harbor", 3, (2.2, 4.5), 2, 350, ["Barrel", "Crate", "Post", "Net"]),
    (4, "FORTRESS OF ROME", WATER_FORTRESS, "fortress", 3, (2.5, 5), 2, 520, ["Wall", "Tower", "Banner SPQR"]),
    (5, "PYRAMIDS OF EGYPT", WATER_TIBER, "pyramid", 4, (2.8, 5.5), 2, 700, ["Pyramid", "Palm", "Cactus", "Sand"]),
    (6, "ANCIENT RUS", WATER_HARBOR, "rus", 4, (3, 5.5), 3, 900, ["Birch", "Izba", "Fence", "Church"]),
    (7, "FINAL BATTLE", WATER_FORTRESS, "final", 5, (3.5, 6), 3, 9999, ["All mixed"]),
]

LANG_NAMES = {"ru": "Russian", "en": "English", "es": "Spanish"}
LANG_PREFIXES = {"ru": "RU", "en": "EN", "es": "ES"}

def generate_game_art(lang):
    prefix = LANG_PREFIXES[lang]
    fname = f"Game_Art_{prefix}.pdf"
    c = canvas.Canvas(os.path.join(OUT, fname), pagesize=A4)

    page_title(c)
    page_boat_anatomy(c)
    page_obstacles_coins(c)
    page_hud(c)
    page_characters(c)
    page_water_colors(c)
    page_decorations_catalog(c)

    for lv in LEVELS_DATA:
        page_level_preview(c, *lv)

    page_gameplay_situation(c, "RAMMING - USE THE BOW", "Press SPACE to ram enemy ships. Deal damage + collect points.", situation_ramming)
    page_gameplay_situation(c, "DODGING - AVOID ROCKS", "Use A/D keys to move left/right. Rocks are indestructible!", situation_dodging)
    page_gameplay_situation(c, "COLLECTING COINS", "Gold coins give +10 points each. Safe to collect - no damage!", situation_collecting)
    page_gameplay_situation(c, "TAKING DAMAGE", "Collisions cost 1 HP. You have 3 HP max. Invincibility after hit.", situation_damage)

    c.save()
    print(f"[+] Game Art ({LANG_NAMES[lang]}): {fname}")

if __name__ == "__main__":
    print("=" * 50)
    print("  GENERATING GAME ART ILLUSTRATIONS")
    print("=" * 50)
    for lang in ["ru", "en", "es"]:
        generate_game_art(lang)
    print("\n[+] All 3 Game Art PDFs generated!")
