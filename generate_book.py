from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os, math

W, H = A4
OUT = os.path.dirname(os.path.abspath(__file__))

FONT_DIR = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
pdfmetrics.registerFont(TTFont("Arial", os.path.join(FONT_DIR, "arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", os.path.join(FONT_DIR, "arialbd.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Oblique", os.path.join(FONT_DIR, "ariali.ttf")))
pdfmetrics.registerFont(TTFont("Arial-BoldOblique", os.path.join(FONT_DIR, "arialbi.ttf")))

GOLD = HexColor("#c9a84c")
DARK = HexColor("#1a1a2e")
BROWN = HexColor("#5D4037")
RED = HexColor("#c0392b")
BLUE = HexColor("#1a5276")
GREEN = HexColor("#1e8449")
SAND = HexColor("#d4a76a")
CREAM = HexColor("#f5f0e1")
GRAY = HexColor("#7f8c8d")
ORANGE = HexColor("#e67e22")
PURPLE = HexColor("#6c3483")
TEAL = HexColor("#1abc9c")
LIGHT_BLUE = HexColor("#5dade2")

# ============================================================
# DRAWING HELPERS
# ============================================================
def draw_border(c, color=GOLD, w=3):
    c.setStrokeColor(color)
    c.setLineWidth(w)
    c.rect(15*mm, 15*mm, W-30*mm, H-30*mm)
    c.setLineWidth(1.5)
    c.rect(18*mm, 18*mm, W-36*mm, H-36*mm)

def draw_corner_ornaments(c, color=GOLD):
    c.setFillColor(color)
    for x, y in [(22*mm, 22*mm), (W-22*mm, 22*mm), (22*mm, H-22*mm), (W-22*mm, H-22*mm)]:
        c.circle(x, y, 4*mm, fill=1)
        c.setFillColor(DARK)
        c.circle(x, y, 2*mm, fill=1)
        c.setFillColor(color)

def draw_divider(c, y, color=GOLD):
    c.setStrokeColor(color)
    c.setLineWidth(1)
    mid = W/2
    c.line(30*mm, y, mid-20*mm, y)
    c.line(mid+20*mm, y, W-30*mm, y)
    c.setFillColor(color)
    c.circle(mid, y, 3*mm, fill=1)
    c.setFillColor(DARK)
    c.circle(mid, y, 1.5*mm, fill=1)
    c.setFillColor(GOLD)

def draw_page_bg(c, color=CREAM):
    c.setFillColor(color)
    c.rect(0, 0, W, H, fill=1, stroke=0)

def draw_text_block(c, text, x, y, size=11, color=DARK, max_width=150*mm, leading=16):
    style = ParagraphStyle('body', fontName='Arial', fontSize=size, leading=leading, textColor=color)
    p = Paragraph(text, style)
    w2, h2 = p.wrap(max_width, 500*mm)
    p.drawOn(c, x, y - h2)
    return h2

def draw_chapter_title(c, num, title, subtitle=""):
    draw_page_bg(c, DARK)
    draw_border(c, GOLD, 4)
    draw_corner_ornaments(c, GOLD)
    c.setFillColor(GOLD)
    c.setFont("Arial-Bold", 60)
    c.drawCentredString(W/2, H-80*mm, str(num))
    c.setFont("Arial-Bold", 28)
    c.drawCentredString(W/2, H-100*mm, title)
    if subtitle:
        c.setFont("Arial", 14)
        c.setFillColor(CREAM)
        c.drawCentredString(W/2, H-115*mm, subtitle)
    draw_divider(c, H-125*mm, GOLD)

# ============================================================
# ILLUSTRATION DRAWING FUNCTIONS
# ============================================================
def draw_boat(c, x, y, w=40, h=16, color=BROWN):
    c.setFillColor(color)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    p = c.beginPath()
    p.moveTo(x-w/2, y-h/4)
    p.lineTo(x+w/2, y-h/4)
    p.lineTo(x+w/2-3, y+h/4)
    p.lineTo(x-w/2+3, y+h/4)
    p.close()
    c.drawPath(p, fill=1, stroke=1)
    c.setFillColor(HexColor("#8B7355"))
    c.rect(x-1, y-h/2-6, 2, h/2+4, fill=1, stroke=0)
    c.setFillColor(white)
    p2 = c.beginPath()
    p2.moveTo(x+1, y-h/2-4)
    p2.lineTo(x+14, y-h/4)
    p2.lineTo(x+1, y+h/6)
    p2.close()
    c.drawPath(p2, fill=1, stroke=0)

def draw_enemy_ship(c, x, y, w=35, h=14):
    c.setFillColor(RED)
    c.setStrokeColor(HexColor("#922b21"))
    c.setLineWidth(1)
    p = c.beginPath()
    p.moveTo(x-w/2, y-h/4)
    p.lineTo(x+w/2, y-h/4)
    p.lineTo(x+w/2-2, y+h/4)
    p.lineTo(x-w/2+2, y+h/4)
    p.close()
    c.drawPath(p, fill=1, stroke=1)
    c.setFillColor(BROWN)
    c.rect(x-1, y-h/2-5, 2, h/2+3, fill=1, stroke=0)
    c.setFillColor(HexColor("#922b21"))
    p2 = c.beginPath()
    p2.moveTo(x+1, y-h/2-3)
    p2.lineTo(x+12, y-h/4)
    p2.lineTo(x+1, y+h/6)
    p2.close()
    c.drawPath(p2, fill=1, stroke=0)

def draw_rock(c, x, y, size=15):
    c.setFillColor(HexColor("#7f8c8d"))
    p = c.beginPath()
    p.moveTo(x, y+size*0.6)
    p.lineTo(x-size*0.5, y-size*0.3)
    p.lineTo(x-size*0.2, y-size*0.5)
    p.lineTo(x+size*0.3, y-size*0.4)
    p.lineTo(x+size*0.5, y-size*0.1)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(HexColor("#95a5a6"))
    p2 = c.beginPath()
    p2.moveTo(x, y+size*0.6)
    p2.lineTo(x+size*0.1, y-size*0.2)
    p2.lineTo(x+size*0.5, y-size*0.1)
    p2.close()
    c.drawPath(p2, fill=1, stroke=0)

def draw_coin(c, x, y, r=8):
    c.setFillColor(GOLD)
    c.circle(x, y, r, fill=1, stroke=0)
    c.setFillColor(HexColor("#f0c040"))
    c.circle(x-1, y+1, r*0.7, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Arial-Bold", max(int(r*0.9), 6))
    c.drawCentredString(x-r*0.35, y-r*0.35, "X")

def draw_roman_face(c, x, y, size=20):
    s = size
    c.setFillColor(GRAY)
    c.circle(x, y+s*0.2, s*0.45, fill=1)
    c.setFillColor(HexColor("#e8c088"))
    c.circle(x, y+s*0.35, s*0.3, fill=1)
    c.setFillColor(white)
    c.circle(x-s*0.1, y+s*0.4, s*0.06, fill=1)
    c.circle(x+s*0.1, y+s*0.4, s*0.06, fill=1)
    c.setFillColor(black)
    c.circle(x-s*0.1, y+s*0.4, s*0.03, fill=1)
    c.circle(x+s*0.1, y+s*0.4, s*0.03, fill=1)
    c.setStrokeColor(HexColor("#cc0000"))
    c.setLineWidth(s*0.08)
    c.line(x, y+s*0.7, x, y+s*1.1)

def draw_pyramid(c, x, y, size=30):
    c.setFillColor(SAND)
    p = c.beginPath()
    p.moveTo(x, y+size)
    p.lineTo(x-size*0.8, y-size*0.3)
    p.lineTo(x+size*0.8, y-size*0.3)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(HexColor("#c49555"))
    p2 = c.beginPath()
    p2.moveTo(x, y+size)
    p2.lineTo(x, y-size*0.3)
    p2.lineTo(x+size*0.8, y-size*0.3)
    p2.close()
    c.drawPath(p2, fill=1, stroke=0)

def draw_birch(c, x, y, h=40):
    c.setFillColor(HexColor("#ecf0f1"))
    c.rect(x-2, y, 4, h, fill=1, stroke=0)
    c.setStrokeColor(HexColor("#2c3e50"))
    c.setLineWidth(0.5)
    for i in range(4):
        c.line(x-2, y+h*0.2+i*h*0.15, x+2, y+h*0.15+i*h*0.15)
    c.setFillColor(GREEN)
    c.circle(x, y+h+5, 10, fill=1, stroke=0)
    c.circle(x-6, y+h+2, 7, fill=1, stroke=0)
    c.circle(x+6, y+h+2, 7, fill=1, stroke=0)

def draw_fortress_wall(c, x, y, w=60, h=40):
    c.setFillColor(GRAY)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.setFillColor(HexColor("#95a5a6"))
    for r in range(3):
        for col in range(4):
            bx = x+3+col*14+(r%2)*7
            by = y+3+r*12
            c.rect(bx, by, 12, 10, fill=1, stroke=0)
    c.setFillColor(DARK)
    c.rect(x+w/2-6, y, 12, h*0.6, fill=1, stroke=0)

def draw_palm(c, x, y, h=35):
    c.setFillColor(BROWN)
    c.rect(x-2, y, 4, h, fill=1, stroke=0)
    c.setFillColor(GREEN)
    for angle in [-40, -15, 10, 35, 60]:
        rad = math.radians(angle)
        lx = x + math.cos(rad)*14
        ly = y + h + math.sin(rad)*8
        c.ellipse(x-2, ly-2, lx+2, ly+2, fill=1, stroke=0)

def draw_tree(c, x, y, h=40):
    c.setFillColor(HexColor("#6d4c2a"))
    c.rect(x-2, y, 4, h, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.circle(x, y+h+4, 12, fill=1, stroke=0)
    c.circle(x-7, y+h, 9, fill=1, stroke=0)
    c.circle(x+7, y+h, 9, fill=1, stroke=0)

def draw_barrel(c, x, y, s=10):
    c.setFillColor(HexColor("#8B6914"))
    c.ellipse(x-s, y-s*0.6, x+s, y+s*0.6, fill=1, stroke=0)
    c.setStrokeColor(HexColor("#5D4037"))
    c.setLineWidth(1)
    c.line(x-s, y-s*0.2, x+s, y-s*0.2)
    c.line(x-s, y+s*0.2, x+s, y+s*0.2)

def draw_flag(c, x, y, h=30, color=RED):
    c.setFillColor(HexColor("#6d4c2a"))
    c.rect(x-1, y, 2, h, fill=1, stroke=0)
    c.setFillColor(color)
    p = c.beginPath()
    p.moveTo(x+1, y+h)
    p.lineTo(x+18, y+h-5)
    p.lineTo(x+1, y+h-10)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Arial-Bold", 5)
    c.drawString(x+3, y+h-8, "SPQR")

def draw_waves(c, x, y, w=80):
    c.setStrokeColor(LIGHT_BLUE)
    c.setLineWidth(1.5)
    for i in range(3):
        yy = y - i*5
        pts = []
        for j in range(9):
            cx = x - w/2 + j*(w/8)
            cy = yy + (3 if j%2==0 else -3)
            pts.append((cx, cy))
        for k in range(len(pts)-1):
            c.line(pts[k][0], pts[k][1], pts[k+1][0], pts[k+1][1])

def _draw_label_small(c, text, x, y, size=7, color=DARK):
    c.setFillColor(color)
    c.setFont("Arial", size)
    c.drawString(x, y, text)

def draw_scene_sea(c, x, y):
    bx, by, bw, bh = x-70*mm, y-22*mm, 140*mm, 44*mm
    c.setFillColor(HexColor("#0e6655"))
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    c.setStrokeColor(Color(0.2, 0.6, 0.86, 0.25))
    c.setLineWidth(1.5)
    for row in range(int(bh/12)+1):
        yy = by + row*12
        for j in range(int(bw/8)):
            c.line(bx+j*8, yy+2*math.sin(j*0.7), bx+(j+1)*8, yy+2*math.sin((j+1)*0.7))
    draw_boat(c, x-20, y+2, 45, 18, GREEN)
    draw_rock(c, x+30, y-15, 12)
    draw_coin(c, x+50, y+12, 7)
    _draw_label_small(c, "Mare Nostrum", bx+3, by+bh-8, 7, CREAM)
    _draw_label_small(c, "Lv.1", bx+bw-18, by+bh-8, 7, GOLD)

def draw_scene_tiber(c, x, y):
    bx, by, bw, bh = x-70*mm, y-22*mm, 140*mm, 44*mm
    c.setFillColor(HexColor("#1a5276"))
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    c.setStrokeColor(Color(0.2, 0.6, 0.86, 0.25))
    c.setLineWidth(1.5)
    for row in range(int(bh/12)+1):
        yy = by + row*12
        for j in range(int(bw/8)):
            c.line(bx+j*8, yy+2*math.sin(j*0.7), bx+(j+1)*8, yy+2*math.sin((j+1)*0.7))
    draw_tree(c, bx+10, by+2, 25)
    draw_tree(c, bx+bw-25, by+2, 20)
    draw_boat(c, x, y+2, 45, 18, BROWN)
    _draw_label_small(c, "Tiberis", bx+3, by+bh-8, 7, CREAM)
    _draw_label_small(c, "Lv.2", bx+bw-18, by+bh-8, 7, GOLD)

def draw_scene_harbor(c, x, y):
    bx, by, bw, bh = x-70*mm, y-22*mm, 140*mm, 44*mm
    c.setFillColor(HexColor("#1b4f72"))
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    c.setStrokeColor(Color(0.2, 0.6, 0.86, 0.25))
    c.setLineWidth(1.5)
    for row in range(int(bh/12)+1):
        yy = by + row*12
        for j in range(int(bw/8)):
            c.line(bx+j*8, yy+2*math.sin(j*0.7), bx+(j+1)*8, yy+2*math.sin((j+1)*0.7))
    draw_barrel(c, bx+15, by+5, 7)
    draw_barrel(c, bx+30, by+5, 7)
    draw_barrel(c, bx+bw-20, by+5, 7)
    draw_boat(c, x+5, y+2, 45, 18, HexColor("#D2B48C"))
    _draw_label_small(c, "Portus Ostia", bx+3, by+bh-8, 7, CREAM)
    _draw_label_small(c, "Lv.3", bx+bw-18, by+bh-8, 7, GOLD)

def draw_scene_fortress(c, x, y):
    bx, by, bw, bh = x-70*mm, y-22*mm, 140*mm, 44*mm
    c.setFillColor(HexColor("#154360"))
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    c.setStrokeColor(Color(0.2, 0.6, 0.86, 0.25))
    c.setLineWidth(1.5)
    for row in range(int(bh/12)+1):
        yy = by + row*12
        for j in range(int(bw/8)):
            c.line(bx+j*8, yy+2*math.sin(j*0.7), bx+(j+1)*8, yy+2*math.sin((j+1)*0.7))
    draw_fortress_wall(c, bx+5, by+2, 45, 28)
    draw_flag(c, bx+bw-30, by+10, 20, RED)
    draw_boat(c, x, y+2, 45, 18, GREEN)
    _draw_label_small(c, "Castra Roma", bx+3, by+bh-8, 7, CREAM)
    _draw_label_small(c, "Lv.4", bx+bw-18, by+bh-8, 7, GOLD)

def draw_scene_egypt(c, x, y):
    bx, by, bw, bh = x-70*mm, y-22*mm, 140*mm, 44*mm
    c.setFillColor(HexColor("#1a5276"))
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    c.setStrokeColor(Color(0.2, 0.6, 0.86, 0.25))
    c.setLineWidth(1.5)
    for row in range(int(bh/12)+1):
        yy = by + row*12
        for j in range(int(bw/8)):
            c.line(bx+j*8, yy+2*math.sin(j*0.7), bx+(j+1)*8, yy+2*math.sin((j+1)*0.7))
    draw_pyramid(c, bx+15, by-2, 22)
    draw_pyramid(c, bx+50, by-5, 16)
    draw_boat(c, x-5, y+2, 45, 18, SAND)
    _draw_label_small(c, "Aegyptus", bx+3, by+bh-8, 7, CREAM)
    _draw_label_small(c, "Lv.5", bx+bw-18, by+bh-8, 7, GOLD)

def draw_scene_rus(c, x, y):
    bx, by, bw, bh = x-70*mm, y-22*mm, 140*mm, 44*mm
    c.setFillColor(HexColor("#1b4f72"))
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    c.setStrokeColor(Color(0.2, 0.6, 0.86, 0.25))
    c.setLineWidth(1.5)
    for row in range(int(bh/12)+1):
        yy = by + row*12
        for j in range(int(bw/8)):
            c.line(bx+j*8, yy+2*math.sin(j*0.7), bx+(j+1)*8, yy+2*math.sin((j+1)*0.7))
    draw_birch(c, bx+10, by+2, 25)
    draw_birch(c, bx+40, by+2, 20)
    draw_boat(c, x, y+2, 45, 18, BROWN)
    _draw_label_small(c, "Rus Antiqua", bx+3, by+bh-8, 7, CREAM)
    _draw_label_small(c, "Lv.6", bx+bw-18, by+bh-8, 7, GOLD)

def draw_scene_battle(c, x, y):
    bx, by, bw, bh = x-70*mm, y-22*mm, 140*mm, 44*mm
    c.setFillColor(HexColor("#154360"))
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    c.setStrokeColor(Color(0.2, 0.6, 0.86, 0.25))
    c.setLineWidth(1.5)
    for row in range(int(bh/12)+1):
        yy = by + row*12
        for j in range(int(bw/8)):
            c.line(bx+j*8, yy+2*math.sin(j*0.7), bx+(j+1)*8, yy+2*math.sin((j+1)*0.7))
    draw_boat(c, x-25, y+2, 40, 16, GREEN)
    draw_enemy_ship(c, x+25, y+2, 35, 14)
    draw_rock(c, x, y-12, 12)
    _draw_label_small(c, "FINALIS", bx+3, by+bh-8, 7, CREAM)
    _draw_label_small(c, "Lv.7", bx+bw-18, by+bh-8, 7, GOLD)

def draw_scene_controls(c, x, y):
    bx, by, bw, bh = x-70*mm, y-22*mm, 140*mm, 44*mm
    c.setFillColor(HexColor("#1a5276"))
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    c.setStrokeColor(Color(0.2, 0.6, 0.86, 0.25))
    c.setLineWidth(1.5)
    for row in range(int(bh/12)+1):
        yy = by + row*12
        for j in range(int(bw/8)):
            c.line(bx+j*8, yy+2*math.sin(j*0.7), bx+(j+1)*8, yy+2*math.sin((j+1)*0.7))
    draw_boat(c, x-25, y+2, 45, 18, BROWN)
    draw_rock(c, x+35, y-12, 10)
    draw_coin(c, x+15, y+15, 7)
    c.setFillColor(DARK)
    c.setFont("Arial-Bold", 7)
    c.drawString(x-55*mm, y+18, "[A/D]")
    c.drawString(x+38, y+18, "[SPACE]")
    _draw_label_small(c, "Controls", bx+3, by+bh-8, 7, CREAM)

def draw_scene_scoring(c, x, y):
    bx, by, bw, bh = x-70*mm, y-22*mm, 140*mm, 44*mm
    c.setFillColor(HexColor("#1b4f72"))
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    c.setStrokeColor(Color(0.2, 0.6, 0.86, 0.25))
    c.setLineWidth(1.5)
    for row in range(int(bh/12)+1):
        yy = by + row*12
        for j in range(int(bw/8)):
            c.line(bx+j*8, yy+2*math.sin(j*0.7), bx+(j+1)*8, yy+2*math.sin((j+1)*0.7))
    draw_coin(c, x-30, y+12, 9)
    draw_coin(c, x-5, y+18, 7)
    draw_coin(c, x+20, y+12, 9)
    draw_enemy_ship(c, x+40, y-5, 30, 12)
    draw_boat(c, x-40, y+2, 35, 14, GREEN)
    c.setFillColor(DARK)
    c.setFont("Arial-Bold", 8)
    c.drawString(x-50*mm, y-8, "+10")
    c.drawString(x+30, y-8, "+25")
    _draw_label_small(c, "Scoring", bx+3, by+bh-8, 7, CREAM)

def draw_scene_ram(c, x, y):
    bx, by, bw, bh = x-70*mm, y-22*mm, 140*mm, 44*mm
    c.setFillColor(HexColor("#154360"))
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    c.setStrokeColor(Color(0.2, 0.6, 0.86, 0.25))
    c.setLineWidth(1.5)
    for row in range(int(bh/12)+1):
        yy = by + row*12
        for j in range(int(bw/8)):
            c.line(bx+j*8, yy+2*math.sin(j*0.7), bx+(j+1)*8, yy+2*math.sin((j+1)*0.7))
    draw_boat(c, x-18, y+2, 40, 16, GREEN)
    draw_enemy_ship(c, x+22, y+2, 35, 14)
    c.setFillColor(Color(1, 0.4, 0, 0.35))
    c.circle(x+5, y+4, 16, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.setFont("Arial-Bold", 12)
    c.drawCentredString(x+5, y+18, "!")
    c.setFillColor(DARK)
    c.setFont("Arial-Bold", 7)
    c.drawString(x-55*mm, y+18, "[SPACE]")
    _draw_label_small(c, "Rostrum!", bx+3, by+bh-8, 7, CREAM)

def draw_scene_obstacles(c, x, y):
    bx, by, bw, bh = x-70*mm, y-22*mm, 140*mm, 44*mm
    c.setFillColor(HexColor("#0e6655"))
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    c.setStrokeColor(Color(0.2, 0.6, 0.86, 0.25))
    c.setLineWidth(1.5)
    for row in range(int(bh/12)+1):
        yy = by + row*12
        for j in range(int(bw/8)):
            c.line(bx+j*8, yy+2*math.sin(j*0.7), bx+(j+1)*8, yy+2*math.sin((j+1)*0.7))
    draw_rock(c, x-35, y-8, 14)
    draw_rock(c, x+25, y-12, 10)
    draw_enemy_ship(c, x+5, y+2, 30, 12)
    draw_coin(c, x-10, y+15, 7)
    draw_boat(c, x+45, y+2, 35, 14, GREEN)
    _draw_label_small(c, "Rocks | Enemies | Coins", bx+3, by+bh-8, 7, CREAM)

def draw_scene_launch(c, x, y):
    bx, by, bw, bh = x-70*mm, y-22*mm, 140*mm, 44*mm
    c.setFillColor(HexColor("#1a1a2e"))
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    draw_boat(c, x, y+2, 50, 20, GREEN)
    c.setFillColor(CREAM)
    c.setFont("Arial-Bold", 8)
    c.drawCentredString(x, y-12, "roman-boats.html")
    c.setFillColor(GOLD)
    c.setFont("Arial-Bold", 7)
    c.drawCentredString(x, y-20, "[ENTER]")
    _draw_label_small(c, "Open in browser", bx+3, by+bh-8, 7, CREAM)

def draw_scene_characters(c, x, y):
    bx, by, bw, bh = x-70*mm, y-22*mm, 140*mm, 44*mm
    c.setFillColor(HexColor("#1a1a2e"))
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.rect(bx, by, bw, bh, fill=0, stroke=1)
    names = ["Sen", "Cen", "Leg", "Mer", "Gla", "Sla"]
    for i, nm in enumerate(names):
        px = bx + 15 + i * 22
        py = y
        draw_roman_face(c, px, py, 14)
        c.setFillColor(CREAM)
        c.setFont("Arial", 6)
        c.drawCentredString(px, py-16, nm)
    _draw_label_small(c, "6 character types", bx+3, by+bh-8, 7, GOLD)

def draw_scene_fates(c, x, y):
    bx, by, bw, bh = x-70*mm, y-22*mm, 140*mm, 44*mm
    c.setFillColor(HexColor("#1a1a2e"))
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    draw_roman_face(c, x-30, y, 18)
    draw_roman_face(c, x, y+3, 22)
    draw_roman_face(c, x+30, y, 18)
    draw_coin(c, x-15, y+25, 5)
    draw_boat(c, x+20, y-15, 25, 10, GOLD)
    _draw_label_small(c, "Stories & Destinies", bx+3, by+bh-8, 7, GOLD)

def draw_scene_glossary(c, x, y):
    bx, by, bw, bh = x-70*mm, y-22*mm, 140*mm, 44*mm
    c.setFillColor(HexColor("#1a1a2e"))
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Arial-Bold", 9)
    c.drawCentredString(x-30, y+15, "SPQR")
    c.drawCentredString(x, y+15, "AVE")
    c.drawCentredString(x+30, y+15, "ROMA")
    draw_boat(c, x, y-5, 40, 14, BROWN)
    _draw_label_small(c, "Latin terms", bx+3, by+bh-8, 7, GOLD)

def draw_scene_latin(c, x, y):
    bx, by, bw, bh = x-70*mm, y-22*mm, 140*mm, 44*mm
    c.setFillColor(HexColor("#1a1a2e"))
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.setFont("Arial-Bold", 10)
    c.drawCentredString(x-35, y+12, "VENI")
    c.drawCentredString(x, y+12, "VIDI")
    c.drawCentredString(x+35, y+12, "VICI")
    draw_boat(c, x, y-8, 40, 14, RED)
    _draw_label_small(c, "Caesar's words", bx+3, by+bh-8, 7, GOLD)

def draw_scene_strategies(c, x, y):
    bx, by, bw, bh = x-70*mm, y-22*mm, 140*mm, 44*mm
    c.setFillColor(HexColor("#154360"))
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    c.setStrokeColor(Color(0.2, 0.6, 0.86, 0.25))
    c.setLineWidth(1.5)
    for row in range(int(bh/12)+1):
        yy = by + row*12
        for j in range(int(bw/8)):
            c.line(bx+j*8, yy+2*math.sin(j*0.7), bx+(j+1)*8, yy+2*math.sin((j+1)*0.7))
    draw_boat(c, x-20, y+5, 35, 14, GREEN)
    draw_enemy_ship(c, x+25, y+2, 28, 10)
    draw_rock(c, x, y-10, 10)
    _draw_label_small(c, "Dodge > Ram at high levels", bx+3, by+bh-8, 7, CREAM)

def draw_scene_achievements(c, x, y):
    bx, by, bw, bh = x-70*mm, y-22*mm, 140*mm, 44*mm
    c.setFillColor(HexColor("#1a1a2e"))
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    draw_coin(c, x-30, y+10, 10)
    draw_coin(c, x, y+15, 8)
    draw_coin(c, x+30, y+10, 10)
    c.setFillColor(GOLD)
    c.setFont("Arial-Bold", 8)
    c.drawCentredString(x, y-10, "FIRST RAM | 10 RAMS | UNDEFEATED")
    _draw_label_small(c, "Unlock achievements", bx+3, by+bh-8, 7, GOLD)

def draw_scene_conclusion(c, x, y):
    bx, by, bw, bh = x-70*mm, y-22*mm, 140*mm, 44*mm
    c.setFillColor(HexColor("#0e6655"))
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    c.setStrokeColor(Color(0.2, 0.6, 0.86, 0.25))
    c.setLineWidth(1.5)
    for row in range(int(bh/12)+1):
        yy = by + row*12
        for j in range(int(bw/8)):
            c.line(bx+j*8, yy+2*math.sin(j*0.7), bx+(j+1)*8, yy+2*math.sin((j+1)*0.7))
    draw_boat(c, x, y+2, 55, 22, GOLD)
    draw_flag(c, x+18, y+20, 22, RED)
    _draw_label_small(c, "Ave, Captain!", bx+3, by+bh-8, 7, GOLD)

def draw_scene_catalog(c, x, y):
    bx, by, bw, bh = x-70*mm, y-22*mm, 140*mm, 44*mm
    c.setFillColor(HexColor("#1a5276"))
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    c.setStrokeColor(Color(0.2, 0.6, 0.86, 0.25))
    c.setLineWidth(1.5)
    for row in range(int(bh/12)+1):
        yy = by + row*12
        for j in range(int(bw/8)):
            c.line(bx+j*8, yy+2*math.sin(j*0.7), bx+(j+1)*8, yy+2*math.sin((j+1)*0.7))
    draw_boat(c, bx+15, y+2, 28, 11, GREEN)
    draw_boat(c, bx+50, y+2, 28, 11, BROWN)
    draw_boat(c, bx+85, y+2, 28, 11, SAND)
    draw_rock(c, bx+30, y-12, 8)
    draw_coin(c, bx+70, y+14, 6)
    _draw_label_small(c, "All decorations x7 levels", bx+3, by+bh-8, 7, CREAM)

# ============================================================
# TEXT PAGE GENERATOR
# ============================================================
def text_page(c, chapter_num, chapter_title, subtitle, paragraphs, page_illustration=None):
    draw_chapter_title(c, chapter_num, chapter_title, subtitle)
    c.showPage()
    for i, (title, body) in enumerate(paragraphs):
        draw_page_bg(c, CREAM)
        draw_border(c, GOLD)
        draw_corner_ornaments(c, GOLD)
        c.setFillColor(DARK)
        c.setFont("Arial-Bold", 16)
        c.drawString(25*mm, H-30*mm, title)
        draw_divider(c, H-36*mm, GOLD)
        y = H - 45*mm
        for para in body:
            h = draw_text_block(c, para, 25*mm, y, size=11, max_width=W-50*mm, leading=15)
            y -= h + 4*mm
        if page_illustration:
            illust_y = y - 15*mm
            illust_h = 55*mm
            c.setStrokeColor(GOLD)
            c.setLineWidth(1.5)
            c.roundRect(20*mm, illust_y - illust_h, W-40*mm, illust_h, 4, fill=0, stroke=1)
            page_illustration(c, W/2, illust_y - illust_h/2)
        c.setFont("Arial-Oblique", 9)
        c.setFillColor(GRAY)
        c.drawCentredString(W/2, 22*mm, f"Roman Galleys - Tome {chapter_num} - Page {i+2}")
        c.showPage()

# ============================================================
# LANGUAGE CONTENT
# ============================================================
# Each tome: (title, subtitle, edition, toc_list, chapters_list)
# Each chapter: (title, subtitle, [(para_title, [body_lines])], illustration_func_or_None)
CONTENT = {
    "ru": {
        "book_title": "РИМСКИЕ ГАЛЕРЫ",
        "footer_prefix": "Римские Галеры",
    },
    "en": {
        "book_title": "ROMAN GALLEYS",
        "footer_prefix": "Roman Galleys",
    },
    "es": {
        "book_title": "GALERAS ROMANAS",
        "footer_prefix": "Galeras Romanas",
    },
}

TOME1 = {
    "ru": {
        "title1": "ВЕЛИЧИЕ", "title2": "ИМПЕРИИ",
        "subtitle": "Полное руководство по игре",
        "edition": "Издание первое, допущенное Сенатом Римской Республики",
        "toc": [
            ("I.", "Введение - Что такое Римские Галеры?"),
            ("II.", "Как играть - Основы управления"),
            ("III.", "Мир игры - Река Тибр и не только"),
            ("IV.", "Система очков и уровней"),
            ("V.", "Таран - Главное оружие"),
            ("VI.", "Препятствия - Камни, враги, монеты"),
            ("VII.", "Запуск игры"),
        ],
        "chapters": [
            ("ВВЕДЕНИЕ", "Что такое Римские Галеры?", [
                ("Добро пожаловать, воин!", [
                    "Римские Галеры - это аркадная игра, в которой вы становитесь капитаном римской галеры "
                    "и путешествуете по водам древнего мира. Ваша задача - уклоняться от камней, собирать "
                    "золото, таранить вражеские корабли и добраться до конца путешествия.",
                    "Игра вдохновлена реальной историей Римской империи, когда её флот господствовал "
                    "над Средиземным морем, а галеры были главным оружием легионов на воде.",
                ]),
                ("Историческая справка: Римский флот", [
                    "Римляне не всегда были морской державой. Первый настоящий военный флот был создан "
                    "во время Первой Пунической войны (264-241 до н.э.) против Карфагена. По преданию, "
                    "римляне захватили карфагенский корабль и по его образцу построили 120 квинкем!",
                    "Квинкема - пятибаночное гребное судно с тараном. Экипаж составлял до 300 человек, "
                    "из которых 200 были гребцами. Таран был главным оружием - им таранили борта "
                    "вражеских кораблей, чтобы уничтожить или обездвижить их.",
                    "В игре вы используете именно такой таран - нажмите ПРОБЕЛ, чтобы атаковать!",
                ]),
            ], draw_scene_sea),
            ("УПРАВЛЕНИЕ", "Основы управления галерой", [
                ("Управление", [
                    "Движение: A/D или стрелки влево/вправо",
                    "Таран: ПРОБЕЛ (перезарядка ~1 секунда)",
                    "Ваша галера автоматически плывёт вниз по реке - вам нужно уклоняться от препятствий.",
                ]),
                ("Интерфейс", [
                    "Внизу экрана отображается шкала здоровья (красные кружки), "
                    "индикатор перезарядки тарана и полоса прогресса текущего уровня.",
                    "В правом верхнем углу - текущий счёт и название уровня.",
                ]),
                ("Советы новичкам", [
                    "Не стойте на месте - река несёт вас вперёд!",
                    "Таран эффективен против врагов, но после удара нужно подождать перезарядки.",
                    "Золотые монеты дают очки - собирайте их, когда безопасно.",
                    "На каждом новом уровне скорость увеличивается - будьте бдительны!",
                ]),
            ], draw_scene_controls),
            ("МИР ИГРЫ", "Река Тибр и не только", [
                ("Средиземное море", [
                    "Первый уровень - спокойные бирюзовые воды. Здесь вы познакомитесь с управлением. "
                    "На берегах плещутся водоросли и кораллы - опасности минимальны.",
                    "Историческая справка: Средиземное море (Mare Nostrum - Наше море) было центром "
                    "Римской империи. Все крупные торговые и военные маршруты проходили через него.",
                ]),
                ("Берега Тибра", [
                    "Второй уровень переносит вас на реку Тибр, у самой столицы империи. "
                    "На зелёных берегах виднеются руины древних храмов и кустарники.",
                    "Историческая справка: Тибр (Tiberis) - главная река Рима, 405 км длиной. "
                    "По легенде, основатели Рима - Ромул и Рем - были брошены в Тибр, "
                    "но их вскормила волчица у берегов реки.",
                ]),
                ("Гавань Остии", [
                    "Третий уровень - торговая гавань. Причалы, бочки, ящики - здесь "
                    "много монет, но и враги становятся умнее.",
                    "Историческая справка: Остия - главный порт Рима, основанный в IV в. до н.э. "
                    "Через Остию в Рим поступали зерно, вино и товары со всего Средиземноморья.",
                ]),
            ], draw_scene_tiber),
            ("СИСТЕМА ОЧКОВ", "Прогресс и уровни", [
                ("Набор очков", [
                    "Монета = 10 очков",
                    "Уничтожение врага = 25 очков",
                    "Чем больше очков, тем быстрее игра!",
                ]),
                ("Система уровней", [
                    "Игра состоит из 7 уровней. Чтобы перейти на следующий, нужно набрать определённое "
                    "количество очков:",
                    "Ур.1: 80 очков - Ур.2: 200 - Ур.3: 350 - Ур.4: 520 - Ур.5: 700 - Ур.6: 900 - Финал",
                    "При переходе на новый уровень вы получаете кратковременную неуязвимость и "
                    "уникальную анимацию представления.",
                ]),
                ("Враги", [
                    "На каждом уровне враги становятся сильнее - у них больше здоровья. "
                    "На первом уровне врагу хватит одного удара тараном, а на последнем - трёх.",
                ]),
            ], draw_scene_scoring),
            ("ТАРАН", "Главное оружие галеры", [
                ("Как использовать", [
                    "Нажмите ПРОБЕЛ, чтобы активировать таран. Ваша галера на мгновение "
                    "ускоряется и наносит удар вражескому кораблю.",
                    "После удара нужна перезарядка - индикатор внизу экрана покажёт, когда "
                    "можно таранить снова.",
                ]),
                ("Историческая справка", [
                    "Таран (rostrum) крепился к носу корабля и представлял собой бронзовый "
                    "наконечник в форме клюва. Самые мощные тараны весили до 200 кг!",
                    "В битве при Экнаме (256 до н.э.) римский флот потопил 16 карфагенских "
                    "кораблей исключительно таранными ударами. Римляне стали первыми, кто "
                    "превратил морской бой в столкновение с тараном.",
                ]),
                ("Стратегия", [
                    "Не тараните каждый встречный корабль - подождите, пока враг подойдёт "
                    "достаточно близко. Таран может поразить только одного врага за раз!",
                    "Во время перезарядки уклоняйтесь от врагов - вы уязвимы.",
                ]),
            ], draw_scene_ram),
            ("ПРЕПЯТСТВИЯ", "Камни, враги, монеты", [
                ("Камни", [
                    "Серые камни - самые распространённые препятствия. Они наносят урон при "
                    "столкновении. Камни нельзя уничтожить - только уклоняться!",
                    "Размер камней варьируется от маленьких до крупных глыб.",
                ]),
                ("Вражеские корабли", [
                    "Красные корабли - вражеские лодки. Они движутся навстречу вам. "
                    "Чтобы уничтожить врага, используйте таран!",
                    "Враги появляются чаще на высоких уровнях и имеют больше здоровья.",
                ]),
                ("Золотые монеты", [
                    "Монеты светятся золотом и пульсируют. Собирайте их для очков! "
                    "Монеты не наносят урон - это безопасная добыча.",
                ]),
            ], draw_scene_obstacles),
            ("ЗАПУСК", "Как начать игру", [
                ("Простой запуск", [
                    "1. Откройте файл roman-boats.html в любом современном браузере.",
                    "2. На экране появится титульная заставка с кнопкой 'В БОЙ!'.",
                    "3. Нажмите на кнопку или клавишу ENTER.",
                    "4. Начнётся первый уровень - Чистое море!",
                ]),
                ("Системные требования", [
                    "Любой современный браузер (Chrome, Firefox, Edge, Safari).",
                    "Не требует установки, серверов или интернета.",
                    "Работает на Windows, macOS, Linux.",
                ]),
            ], draw_scene_launch),
        ],
    },
    "en": {
        "title1": "GLORY", "title2": "OF THE EMPIRE",
        "subtitle": "Complete Game Guide",
        "edition": "First Edition, Approved by the Senate of the Roman Republic",
        "toc": [
            ("I.", "Introduction - What Are Roman Galleys?"),
            ("II.", "How to Play - Controls"),
            ("III.", "World of the Game - The Tiber and Beyond"),
            ("IV.", "Scoring and Levels"),
            ("V.", "The Ram - Primary Weapon"),
            ("VI.", "Obstacles - Rocks, Enemies, Coins"),
            ("VII.", "Launching the Game"),
        ],
        "chapters": [
            ("INTRODUCTION", "What Are Roman Galleys?", [
                ("Welcome, Warrior!", [
                    "Roman Galleys is an arcade game where you become the captain of a Roman galley "
                    "and travel the waters of the ancient world. Your goal is to dodge rocks, collect "
                    "gold, ram enemy ships, and reach the end of your journey.",
                    "The game is inspired by the real history of the Roman Empire, when its fleet "
                    "dominated the Mediterranean Sea, and galleys were the primary weapon of the legions on water.",
                ]),
                ("Historical Note: The Roman Fleet", [
                    "The Romans were not always a naval power. The first real war fleet was created "
                    "during the First Punic War (264-241 BC) against Carthage. Legend has it that "
                    "the Romans captured a Carthaginian ship and built 120 quinqueremes from its design!",
                    "A quinquereme was a five-oared warship with a ram. The crew numbered up to 300, "
                    "of whom 200 were rowers. The ram was the primary weapon - it was used to pierce "
                    "the hulls of enemy ships to destroy or disable them.",
                    "In the game, you use exactly this kind of ram - press SPACE to attack!",
                ]),
            ], draw_scene_sea),
            ("CONTROLS", "Galley Control Basics", [
                ("Controls", [
                    "Movement: A/D or Left/Right arrows",
                    "Ram: SPACE (cooldown ~1 second)",
                    "Your galley automatically sails down the river - you must dodge obstacles.",
                ]),
                ("Interface", [
                    "At the bottom of the screen: health bar (red circles), "
                    "ram recharge indicator, and current level progress bar.",
                    "In the top right corner: current score and level name.",
                ]),
                ("Tips for Beginners", [
                    "Don't stand still - the river carries you forward!",
                    "The ram is effective against enemies, but you must wait for recharge after hitting.",
                    "Gold coins give points - collect them when it's safe.",
                    "On each new level the speed increases - stay alert!",
                ]),
            ], draw_scene_controls),
            ("WORLD", "The Tiber River and Beyond", [
                ("The Mediterranean Sea", [
                    "The first level - calm turquoise waters. Here you'll learn the controls. "
                    "Seaweed and coral line the shores - dangers are minimal.",
                    "Historical Note: The Mediterranean Sea (Mare Nostrum - Our Sea) was the center "
                    "of the Roman Empire. All major trade and military routes passed through it.",
                ]),
                ("The Banks of the Tiber", [
                    "The second level brings you to the Tiber River, near the capital of the empire. "
                    "Green banks show ruins of ancient temples and shrubbery.",
                    "Historical Note: The Tiber (Tiberis) is Rome's main river, 405 km long. "
                    "Legend says the founders of Rome - Romulus and Remus - were thrown into the Tiber, "
                    "but a she-wolf found and nursed them on the riverbanks.",
                ]),
                ("The Harbor of Ostia", [
                    "The third level - a trading harbor. Docks, barrels, crates - lots of coins here, "
                    "but enemies grow smarter too.",
                    "Historical Note: Ostia was Rome's main port, founded in the 4th century BC. "
                    "Grain, wine, and goods from across the Mediterranean flowed through Ostia to Rome.",
                ]),
            ], draw_scene_tiber),
            ("SCORING", "Progress and Levels", [
                ("Earning Points", [
                    "Coin = 10 points",
                    "Destroying an enemy = 25 points",
                    "The more points, the faster the game!",
                ]),
                ("Level System", [
                    "The game has 7 levels. To advance, you must earn a certain number of points:",
                    "Lv.1: 80 pts > Lv.2: 200 > Lv.3: 350 > Lv.4: 520 > Lv.5: 700 > Lv.6: 900 > Final",
                    "When advancing to a new level, you get temporary invincibility and "
                    "a unique level introduction animation.",
                ]),
                ("Enemies", [
                    "On each level enemies get stronger - they have more health. "
                    "On the first level one ram hit is enough, but on the last you need three.",
                ]),
            ], draw_scene_scoring),
            ("THE RAM", "The Galley's Primary Weapon", [
                ("How to Use", [
                    "Press SPACE to activate the ram. Your galley momentarily "
                    "accelerates and strikes the enemy ship.",
                    "After the hit you need to recharge - the indicator at the bottom shows "
                    "when you can ram again.",
                ]),
                ("Historical Note", [
                    "The ram (rostrum) was attached to the bow and was a bronze "
                    "tip shaped like a beak. The most powerful rams weighed up to 200 kg!",
                    "In the Battle of Ecnomus (256 BC), the Roman fleet sank 16 Carthaginian "
                    "ships using only ram attacks. The Romans were the first to turn naval "
                    "combat into ramming collisions.",
                ]),
                ("Strategy", [
                    "Don't ram every ship you see - wait for the enemy to get close enough. "
                    "The ram can only hit one enemy at a time!",
                    "During cooldown, dodge enemies - you're vulnerable.",
                ]),
            ], draw_scene_ram),
            ("OBSTACLES", "Rocks, Enemies, Coins", [
                ("Rocks", [
                    "Gray rocks are the most common obstacles. They deal damage on collision. "
                    "Rocks cannot be destroyed - only dodged!",
                    "Rock sizes vary from small pebbles to large boulders.",
                ]),
                ("Enemy Ships", [
                    "Red ships are enemy boats. They move towards you. "
                    "Use the ram to destroy them!",
                    "Enemies appear more frequently at higher levels and have more health.",
                ]),
                ("Gold Coins", [
                    "Coins glow gold and pulse. Collect them for points! "
                    "Coins deal no damage - they're safe loot.",
                ]),
            ], draw_scene_obstacles),
            ("LAUNCH", "Starting the Game", [
                ("Simple Launch", [
                    "1. Open the file roman-boats.html in any modern browser.",
                    "2. A title screen with a 'BATTLE!' button will appear.",
                    "3. Click the button or press ENTER.",
                    "4. The first level begins - The Clean Sea!",
                ]),
                ("System Requirements", [
                    "Any modern browser (Chrome, Firefox, Edge, Safari).",
                    "No installation, servers, or internet required.",
                    "Works on Windows, macOS, Linux.",
                ]),
            ], draw_scene_launch),
        ],
    },
    "es": {
        "title1": "GLORIA", "title2": "DEL IMPERIO",
        "subtitle": "Guia Completa del Juego",
        "edition": "Primera Edicion, Aprobada por el Senado de la Republica Romana",
        "toc": [
            ("I.", "Introduccion - Que son las Galeras Romanas?"),
            ("II.", "Como Jugar - Controles"),
            ("III.", "Mundo del Juego - El Tiber y Mas Alla"),
            ("IV.", "Puntuacion y Niveles"),
            ("V.", "El Ariete - Arma Principal"),
            ("VI.", "Obstaculos - Rocas, Enemigos, Monedas"),
            ("VII.", "Iniciar el Juego"),
        ],
        "chapters": [
            ("INTRODUCCION", "Que son las Galeras Romanas?", [
                ("Bienvenido, Guerrero!", [
                    "Las Galeras Romanas son un juego de arcade donde te conviertes en el capitan "
                    "de una galera romana y viajas por las aguas del mundo antiguo. Tu objetivo es "
                    "esquivar rocas, recoger oro, embestir barcos enemigos y llegar al final del viaje.",
                    "El juego esta inspirado en la historia real del Imperio Romano, cuando su flota "
                    "dominaba el Mediterraneo y las galeras eran el arma principal de las legiones en el agua.",
                ]),
                ("Nota Historica: La Flota Romana", [
                    "Los romanos no siempre fueron una potencia naval. La primera verdadera flota de guerra "
                    "fue creada durante la Primera Guerra Punica (264-241 a.C.) contra Cartago. "
                    "Segun la leyenda, los romanos capturaron un barco cartagines y construyeron "
                    "120 quinqueremes segun su diseno!",
                    "Una quinquereme era un barco de guerra con cinco remos por banco y un ariete. "
                    "La tripulacion llegaba a 300 personas, de las cuales 200 eran remeros. "
                    "El ariete era el arma principal - se usaba para perforar los cascos de los barcos enemigos.",
                    "En el juego usas exactamente este tipo de ariete - presiona ESPACIO para atacar!",
                ]),
            ], draw_scene_sea),
            ("CONTROLES", "Basics del Control de la Galera", [
                ("Controles", [
                    "Movimiento: A/D o flechas izquierda/derecha",
                    "Ariete: ESPACIO (recarga ~1 segundo)",
                    "Tu galera fluye automaticamente rio abajo - debes esquivar los obstaculos.",
                ]),
                ("Interfaz", [
                    "En la parte inferior: barra de salud (circulos rojos), "
                    "indicador de recarga del ariete y barra de progreso del nivel actual.",
                    "En la esquina superior derecha: puntuacion actual y nombre del nivel.",
                ]),
                ("Consejos para Principiantes", [
                    "No te quedes quieto - el rio te lleva hacia adelante!",
                    "El ariete es efectivo contra enemigos, pero despues del impacto debesperar la recarga.",
                    "Las monedas de oro dan puntos - recogelas cuando sea seguro.",
                    "En cada nivel nuevo la velocidad aumenta - mantente alerta!",
                ]),
            ], draw_scene_controls),
            ("MUNDO", "El Rio Tibre y Mas Alla", [
                ("El Mar Mediterraneo", [
                    "El primer nivel - aguas turquesas tranquilas. Aqui aprenderas los controles. "
                    "Algas y corales bordean las orillas - los peligros son minimos.",
                    "Nota Historica: El Mar Mediterraneo (Mare Nuestro Mar) era el centro "
                    "del Imperio Romano. Todas las rutas comerciales y militares importantes lo cruzaban.",
                ]),
                ("Las Orillas del Tibre", [
                    "El segundo nivel te lleva al Rio Tibre, cerca de la capital del imperio. "
                    "Bancas verdes muestran ruinas de templos antiguos y matorrales.",
                    "Nota Historica: El Tibre (Tiberis) es el rio principal de Roma, con 405 km. "
                    "La leyenda dice que los fundadores de Roma - Romulo y Remo - fueron arrojados al Tibre, "
                    "pero una loba los encontro y amamanto en las orillas del rio.",
                ]),
                ("El Puerto de Ostia", [
                    "El tercer nivel - un puerto comercial. Muelles, barriles, cajas - muchas monedas aqui, "
                    "pero los enemigos se vuelven mas inteligentes.",
                    "Nota Historica: Ostia fue el puerto principal de Roma, fundado en el siglo IV a.C. "
                    "Grano, vino y mercancias de todo el Mediterraneo fluian a Roma a traves de Ostia.",
                ]),
            ], draw_scene_tiber),
            ("PUNTUACION", "Progreso y Niveles", [
                ("Obtener Puntos", [
                    "Moneda = 10 puntos",
                    "Destruir un enemigo = 25 puntos",
                    "Cuantos mas puntos, mas rapido el juego!",
                ]),
                ("Sistema de Niveles", [
                    "El juego tiene 7 niveles. Para avanzar debes obtener cierta cantidad de puntos:",
                    "Nv.1: 80 pts > Nv.2: 200 > Nv.3: 350 > Nv.4: 520 > Nv.5: 700 > Nv.6: 900 > Final",
                    "Al avanzar de nivel obtienes invencibilidad temporal y "
                    "una animacion unica de presentacion del nivel.",
                ]),
                ("Enemigos", [
                    "En cada nivel los enemigos se hacen mas fuertes - tienen mas salud. "
                    "En el primer nivel un golpe de ariete basta, pero en el ultimo necesitas tres.",
                ]),
            ], draw_scene_scoring),
            ("EL ARIETE", "Arma Principal de la Galera", [
                ("Como Usarlo", [
                    "Presiona ESPACIO para activar el ariete. Tu galera se acelera momentaneamente "
                    "y golpea al barco enemigo.",
                    "Despues del golpe necesitas recargar - el indicador en la parte inferior muestra "
                    "cuando puedes embestir de nuevo.",
                ]),
                ("Nota Historica", [
                    "El ariete (rostrum) se unia a la proa y era una punta de bronce "
                    "en forma de pico. Los arietes mas poderosos pesaban hasta 200 kg!",
                    "En la Batalla de Ecnomo (256 a.C.), la flota romana hundio 16 barcos "
                    "cartagineses usando solo embestidas de ariete.",
                ]),
                ("Estrategia", [
                    "No embestas todos los barcos - espera a que el enemigo se acerque lo suficiente. "
                    "El ariete solo puede golpear a un enemigo a la vez!",
                    "Durante la recarga esquiva a los enemigos - estas vulnerable.",
                ]),
            ], draw_scene_ram),
            ("OBSTACULOS", "Rocas, Enemigos, Monedas", [
                ("Rocas", [
                    "Las rocas grises son los obstaculos mas comunes. Danan al colisionar. "
                    "Las rocas no se pueden destruir - solo esquivar!",
                    "Los tamanos varian de pequenos guijarros a grandes bloques.",
                ]),
                ("Barcos Enemigos", [
                    "Los barcos rojos son embarcaciones enemigas. Se mueven hacia ti. "
                    "Usa el ariete para destruirlos!",
                    "Los enemigos aparecen con mas frecuencia en niveles altos y tienen mas salud.",
                ]),
                ("Monedas de Oro", [
                    "Las monedas brillan dorado y pulsan. Recogelas para puntos! "
                    "Las monedas no danan - son botin seguro.",
                ]),
            ], draw_scene_obstacles),
            ("LANZAMIENTO", "Iniciar el Juego", [
                ("Lanzamiento Simple", [
                    "1. Abre el archivo roman-boats.html en cualquier navegador moderno.",
                    "2. Aparecera una pantalla de titulo con un boton 'A COMBATIR!'.",
                    "3. Haz clic en el boton o presiona ENTER.",
                    "4. Comienza el primer nivel - Mar Limpio!",
                ]),
                ("Requisitos del Sistema", [
                    "Cualquier navegador moderno (Chrome, Firefox, Edge, Safari).",
                    "No requiere instalacion, servidores ni internet.",
                    "Funciona en Windows, macOS, Linux.",
                ]),
            ], draw_scene_launch),
        ],
    },
}

TOME2 = {
    "ru": {
        "title1": "ЗЕМЛИ", "title2": "ИМПЕРИИ",
        "subtitle": "Гид по уровням и берегам",
        "edition": "Издание второе, дополненное",
        "toc": [
            ("I.", "Чистое море - Воды Средиземноморья"),
            ("II.", "Берега Тибра - Сердце Рима"),
            ("III.", "Гавань Остии - Торговый путь"),
            ("IV.", "Крепость Рима - Стены легионов"),
            ("V.", "Пирамиды Египта - Тайны Нила"),
            ("VI.", "Древняя Русь - Леса и реки"),
            ("VII.", "Финальная битва - Последнее испытание"),
            ("VIII.", "Береговые декорации - Полный каталог"),
        ],
        "chapters": [
            ("ЧИСТОЕ МОРЕ", "Воды Средиземноморья - Уровень 1", [
                ("Описание уровня", [
                    "Бирюзовые воды, спокойствие и первые шаги. На берегах - водоросли, "
                    "кораллы и плавучие буи. Идеальное место для обучения.",
                    "Сложность: 1/5 | Скорость: 1.5-3 | Враги: HP 1 | Набор: 80 очков",
                ]),
                ("Историческая справка", [
                    "Средиземное море (Mare Nostrum) - 2,5 млн км2. Для римлян оно было "
                    "центром мира. Торговые пути связывали Рим с Египтом, Грецией, "
                    "Иберией и Карфагеном.",
                    "Водоросли и кораллы, которые вы видите на берегах - не просто украшение. "
                    "В древности рифы были серьёзной опасностью для кораблей.",
                ]),
                ("Декорации берегов", [
                    "Водоросли - зелёные стебли, покачивающиеся волной",
                    "Буи - красные плавучие маркеры",
                    "Кораллы - красные рифные образования",
                ]),
            ], draw_scene_sea),
            ("БЕРЕГА ТИБРА", "Сердце Рима - Уровень 2", [
                ("Описание уровня", [
                    "Зелёные береги реки Тибр. Видны деревья, кусты и руины древних храмов.",
                    "Сложность: 2/5 | Скорость: 2-4 | Враги: HP 1 | Набор: 200 очков",
                ]),
                ("Историческая справка", [
                    "Тибр (405 км) - четвёртая по длине река Италии. Город Рим вырос "
                    "на семи холмах у его берегов.",
                    "Легенда о Ромуле и Реме: младенцев бросили в Тибр, но волчица Лупа "
                    "нашла их и вскормила. Так родился Рим!",
                ]),
                ("Декорации берегов", [
                    "Деревья - пышные зелёные кроны на коричневых стволах",
                    "Кусты - заросли у самой воды",
                    "Руины - каменные колонны и стены античных построек",
                    "Трава - отдельные стебли травы на берегу",
                ]),
            ], draw_scene_tiber),
            ("ГАВАНЬ ОСТИИ", "Торговый путь - Уровень 3", [
                ("Описание уровня", [
                    "Торговая гавань с причалами, бочками и сетями. Больше монет, "
                    "но и враги хитрее.",
                    "Сложность: 3/5 | Скорость: 2.2-4.5 | Враги: HP 2 | Набор: 350 очков",
                ]),
                ("Историческая справка", [
                    "Остия - порт Рима, основанный в IV в. до н.э. Название происходит "
                    "от латинского 'ostium' - устье (реки).",
                    "Бочки на берегах - стандартная тара для вина и оливкового масла. "
                    "Римляне называли их 'dolia' (большие) и 'amphorae' (глиняные).",
                ]),
                ("Декорации берегов", [
                    "Бочки - деревянные бочки с металлическими обручами",
                    "Ящики - деревянные грузовые тюки",
                    "Причальные столбы - деревянные сваи с каменными головками",
                    "Сети - рыболовные сети на столбах",
                ]),
            ], draw_scene_harbor),
            ("КРЕПОСТЬ РИМА", "Стены легионов - Уровень 4", [
                ("Описание уровня", [
                    "Каменные стены крепости с арками, башни стражи, знамёна SPQR.",
                    "Сложность: 3/5 | Скорость: 2.5-5 | Враги: HP 2 | Набор: 520 очков",
                ]),
                ("Историческая справка", [
                    "SPQR - Senatus Populusque Romanus (Сенат и Народ Римский). "
                    "Этот девиз украшал все государственные здания Рима.",
                    "Римские крепости (castra) строились по стандартному плану: "
                    "прямоугольная форма с четырьмя воротами и ровом вокруг стен.",
                ]),
                ("Декорации берегов", [
                    "Стены - каменная кладка с арками и воротами",
                    "Башни - сторожевые башни с зубцами",
                    "Знамёна SPQR - красные стяги Римской Республики",
                ]),
            ], draw_scene_fortress),
            ("ПИРАМИДЫ ЕГИПТА", "Тайны Нила - Уровень 5", [
                ("Описание уровня", [
                    "Песчаные берега Нила, великие пирамиды, пальмы и кактусы.",
                    "Сложность: 4/5 | Скорость: 2.8-5.5 | Враги: HP 2 | Набор: 700 очков",
                ]),
                ("Историческая справка", [
                    "Великая Пирамида Гизы - единственное из Семи чудес древнего мира, "
                    "сохранившееся до наших дней. Высота - 146 м, построена около 2560 г. до н.э.",
                    "Римляне завоевали Египет в 30 г. до н.э., когда Октавиан победил "
                    "Клеопатру и Марка Антония.",
                ]),
                ("Декорации берегов", [
                    "Пирамиды - треугольные каменные конструкции с теневой гранью",
                    "Пальмы - коричневые стволы с зелёными кронами-веерами",
                    "Кактусы - зелёные колючие растения с ветвями",
                    "Песчаные дюны - светлые песчаные отмели",
                ]),
            ], draw_scene_egypt),
            ("ДРЕВНЯЯ РУСЬ", "Леса и реки - Уровень 6", [
                ("Описание уровня", [
                    "Белые берёзы, деревянные избы, заборы и церкви с золотыми куполами.",
                    "Сложность: 4/5 | Скорость: 3-5.5 | Враги: HP 3 | Набор: 900 очков",
                ]),
                ("Историческая справка", [
                    "Древняя Русь (IX-XIII вв.) - восточнославянское государство. "
                    "Столица - Киев, 'мать городов русских'.",
                    "Берёза - символ Руси. Белая кора использовалась для изготовления "
                    "посуды, туфель (лапти), и даже лодок (берестяные лодки).",
                    "Деревянное зодчество - русские мастера строили храмы без единого гвоздя.",
                ]),
                ("Декорации берегов", [
                    "Берёзы - белые стволы с чёрными полосами, зелёные кроны",
                    "Избы - деревянные дома с треугольными крышами и печными трубами",
                    "Заборы - деревянные частоколы из вертикальных жердей",
                    "Церкви - белые стены, тёмные крыши, золотые купола-кресты",
                ]),
            ], draw_scene_rus),
            ("ФИНАЛЬНАЯ БИТВА", "Последнее испытание - Уровень 7", [
                ("Описание уровня", [
                    "Все берега смешиваются: деревья, пирамиды, берёзы, крепости.",
                    "Сложность: 5/5 | Скорость: 3.5-6 | Враги: HP 3 | Набор: бесконечность",
                ]),
                ("Стратегия выживания", [
                    "На финальном уровне максимальная скорость. Враги появляются "
                    "очень часто и имеют 3 HP. Это проверка на мастерство!",
                    "Используйте таран только когда уверены в попадании.",
                    "Собирайте монеты - они появляются реже, но каждый очко важен.",
                ]),
                ("Поздравляем!", [
                    "Если вы дошли до финального уровня - вы настоящий воин Рима!",
                    "Империя гордится вами, капитан!",
                ]),
            ], draw_scene_battle),
            ("КАТАЛОГ ДЕКОРАЦИЙ", "Полный список береговых элементов", [
                ("Морские декорации (Ур.1)", [
                    "Водоросли - зелёные полосы, покачивающиеся в течении",
                    "Буи - красные плавучие маркеры на белых столбах",
                    "Кораллы - красные рифные образования, растущие со дна",
                ]),
                ("Речные декорации (Ур.2)", [
                    "Деревья - пышные кроны на коричневых стволах",
                    "Кусты - зелёные заросли у самой воды",
                    "Руины - каменные колонны и фрагменты стен храмов",
                ]),
                ("Портовые декорации (Ур.3)", [
                    "Бочки - деревянные бочки с металлическими обручами",
                    "Ящики - деревянные грузовые тюки с крестовиной",
                    "Столбы - деревянные причальные сваи",
                    "Сети - рыболовные сети на столбах",
                ]),
                ("Крепостные декорации (Ур.4)", [
                    "Стены - каменная кладка с арками и воротами",
                    "Башни - сторожевые башни с зубцами",
                    "Знамёна SPQR - красные стяги Римской Республики",
                ]),
            ], draw_scene_catalog),
        ],
    },
    "en": {
        "title1": "LANDS", "title2": "OF THE EMPIRE",
        "subtitle": "Guide to Levels and Shores",
        "edition": "Second Edition, Expanded",
        "toc": [
            ("I.", "The Clean Sea - Mediterranean Waters"),
            ("II.", "Banks of the Tiber - Heart of Rome"),
            ("III.", "Harbor of Ostia - Trade Route"),
            ("IV.", "Fortress of Rome - Legion Walls"),
            ("V.", "Pyramids of Egypt - Secrets of the Nile"),
            ("VI.", "Ancient Rus - Forests and Rivers"),
            ("VII.", "Final Battle - The Last Trial"),
            ("VIII.", "Shore Decorations - Full Catalog"),
        ],
        "chapters": [
            ("THE CLEAN SEA", "Mediterranean Waters - Level 1", [
                ("Level Description", [
                    "Turquoise waters, tranquility, and first steps. Shores lined with seaweed, "
                    "coral, and floating buoys. The perfect place to learn.",
                    "Difficulty: 1/5 | Speed: 1.5-3 | Enemies: HP 1 | Set: 80 points",
                ]),
                ("Historical Note", [
                    "The Mediterranean Sea (Mare Nostrum) - 2.5 million km2. For the Romans, "
                    "it was the center of the world. Trade routes connected Rome with Egypt, "
                    "Greece, Iberia, and Carthage.",
                    "Seaweed and coral on the shores aren't just decoration. In ancient times, "
                    "reefs were a serious danger for ships.",
                ]),
                ("Shore Decorations", [
                    "Seaweed - green stalks swaying in the waves",
                    "Buoys - red floating markers",
                    "Coral - red reef formations",
                ]),
            ], draw_scene_sea),
            ("BANKS OF THE TIBER", "Heart of Rome - Level 2", [
                ("Level Description", [
                    "Green banks of the Tiber River. Trees, bushes, and ruins of ancient temples visible.",
                    "Difficulty: 2/5 | Speed: 2-4 | Enemies: HP 1 | Set: 200 points",
                ]),
                ("Historical Note", [
                    "The Tiber (405 km) is Italy's fourth longest river. Rome grew on seven hills "
                    "along its banks.",
                    "Legend of Romulus and Remus: infants were thrown into the Tiber, but a she-wolf "
                    "found and nursed them. Thus Rome was born!",
                ]),
                ("Shore Decorations", [
                    "Trees - lush green crowns on brown trunks",
                    "Bushes - thickets right at the water's edge",
                    "Ruins - stone columns and walls of ancient buildings",
                    "Grass - individual grass stems on the shore",
                ]),
            ], draw_scene_tiber),
            ("HARBOR OF OSTIA", "Trade Route - Level 3", [
                ("Level Description", [
                    "A trading harbor with docks, barrels, and nets. More coins, but enemies are cleverer.",
                    "Difficulty: 3/5 | Speed: 2.2-4.5 | Enemies: HP 2 | Set: 350 points",
                ]),
                ("Historical Note", [
                    "Ostia was Rome's port, founded in the 4th century BC. The name comes from "
                    "the Latin 'ostium' - mouth (of the river).",
                    "Barrels on the shores are standard containers for wine and olive oil. "
                    "Romans called them 'dolia' (large) and 'amphorae' (clay).",
                ]),
                ("Shore Decorations", [
                    "Barrels - wooden barrels with metal hoops",
                    "Crates - wooden cargo bundles",
                    "Dock posts - wooden pilings with stone caps",
                    "Nets - fishing nets on posts",
                ]),
            ], draw_scene_harbor),
            ("FORTRESS OF ROME", "Legion Walls - Level 4", [
                ("Level Description", [
                    "Stone fortress walls with arches, guard towers, SPQR banners.",
                    "Difficulty: 3/5 | Speed: 2.5-5 | Enemies: HP 2 | Set: 520 points",
                ]),
                ("Historical Note", [
                    "SPQR - Senatus Populusque Romanus (Senate and People of Rome). "
                    "This motto adorned all state buildings of Rome.",
                    "Roman fortresses (castra) were built to a standard plan: "
                    "rectangular shape with four gates and a moat around the walls.",
                ]),
                ("Shore Decorations", [
                    "Walls - stone masonry with arches and gates",
                    "Towers - watchtowers with battlements",
                    "SPQR Banners - red flags of the Roman Republic",
                ]),
            ], draw_scene_fortress),
            ("PYRAMIDS OF EGYPT", "Secrets of the Nile - Level 5", [
                ("Level Description", [
                    "Sandy shores of the Nile, great pyramids, palms, and cacti.",
                    "Difficulty: 4/5 | Speed: 2.8-5.5 | Enemies: HP 2 | Set: 700 points",
                ]),
                ("Historical Note", [
                    "The Great Pyramid of Giza is the only surviving Wonder of the Ancient World. "
                    "Height: 146 m, built around 2560 BC.",
                    "The Romans conquered Egypt in 30 BC when Octavian defeated Cleopatra "
                    "and Mark Antony.",
                ]),
                ("Shore Decorations", [
                    "Pyramids - triangular stone structures with shaded faces",
                    "Palms - brown trunks with green fan crowns",
                    "Cacti - green thorny plants with branches",
                    "Sand dunes - light sandy shallows",
                ]),
            ], draw_scene_egypt),
            ("ANCIENT RUS", "Forests and Rivers - Level 6", [
                ("Level Description", [
                    "White birches, wooden izbas, fences, and churches with golden domes.",
                    "Difficulty: 4/5 | Speed: 3-5.5 | Enemies: HP 3 | Set: 900 points",
                ]),
                ("Historical Note", [
                    "Ancient Rus (9th-13th centuries) - an East Slavic state. "
                    "Capital: Kiev, 'mother of Russian cities'.",
                    "The birch is the symbol of Rus. White bark was used for making "
                    "dishes, shoes (lapti), and even boats (bark boats).",
                    "Wooden architecture - Russian masters built temples without a single nail.",
                ]),
                ("Shore Decorations", [
                    "Birches - white trunks with black stripes, green crowns",
                    "Izbas - wooden houses with triangular roofs and chimneys",
                    "Fences - wooden palisades from vertical stakes",
                    "Churches - white walls, dark roofs, golden dome-crosses",
                ]),
            ], draw_scene_rus),
            ("FINAL BATTLE", "The Last Trial - Level 7", [
                ("Level Description", [
                    "All shores mix together: trees, pyramids, birches, fortresses.",
                    "Difficulty: 5/5 | Speed: 3.5-6 | Enemies: HP 3 | Set: infinity",
                ]),
                ("Survival Strategy", [
                    "Maximum speed on the final level. Enemies appear very frequently with 3 HP.",
                    "Use the ram only when you're sure of a hit.",
                    "Collect coins - they appear less often, but every point matters.",
                ]),
                ("Congratulations!", [
                    "If you've reached the final level - you're a true warrior of Rome!",
                    "The Empire is proud of you, Captain!",
                ]),
            ], draw_scene_battle),
            ("DECORATION CATALOG", "Complete List of Shore Elements", [
                ("Sea Decorations (Lv.1)", [
                    "Seaweed - green strips swaying in the current",
                    "Buoys - red floating markers on white posts",
                    "Coral - red reef formations growing from the seabed",
                ]),
                ("River Decorations (Lv.2)", [
                    "Trees - lush crowns on brown trunks",
                    "Bushes - green thickets at the water's edge",
                    "Ruins - stone columns and fragments of temple walls",
                ]),
                ("Port Decorations (Lv.3)", [
                    "Barrels - wooden barrels with metal hoops",
                    "Crates - wooden cargo bundles with cross markings",
                    "Posts - wooden dock pilings",
                    "Nets - fishing nets on posts",
                ]),
                ("Fortress Decorations (Lv.4)", [
                    "Walls - stone masonry with arches and gates",
                    "Towers - watchtowers with battlements",
                    "SPQR Banners - red flags of the Roman Republic",
                ]),
            ], draw_scene_catalog),
        ],
    },
    "es": {
        "title1": "TIERRAS", "title2": "DEL IMPERIO",
        "subtitle": "Guia de Niveles y Orillas",
        "edition": "Segunda Edicion, Ampliada",
        "toc": [
            ("I.", "Mar Limpio - Aguas del Mediterraneo"),
            ("II.", "Orillas del Tibre - Corazon de Roma"),
            ("III.", "Puerto de Ostia - Ruta Comercial"),
            ("IV.", "Fortaleza de Roma - Muros de las Legiones"),
            ("V.", "Piramides de Egipto - Secretos del Nilo"),
            ("VI.", "Rus Antigua - Bosques y Rios"),
            ("VII.", "Batalla Final - La Ultima Prueba"),
            ("VIII.", "Decoraciones de Orilla - Catalogo Completo"),
        ],
        "chapters": [
            ("MAR LIMPIO", "Aguas del Mediterraneo - Nivel 1", [
                ("Descripcion del nivel", [
                    "Aguas turquesas, tranquilidad y primeros pasos. Orillas con algas, "
                    "corales y boyas flotantes. Lugar perfecto para aprender.",
                    "Dificultad: 1/5 | Velocidad: 1.5-3 | Enemigos: HP 1 | Meta: 80 puntos",
                ]),
                ("Nota Historica", [
                    "El Mediterraneo (Mare Nuestro Mar) - 2,5 millones de km2. Para los romanos "
                    "era el centro del mundo.",
                    "Las algas y corales en las orillas no son solo decoracion. En la antiguedad, "
                    "los arrecifes eran un peligro serio para los barcos.",
                ]),
                ("Decoraciones de Orilla", [
                    "Algas - tallos verdes meciendose con las olas",
                    "Boyas - marcadores rojos flotantes",
                    "Corales - formaciones rojas de arrecife",
                ]),
            ], draw_scene_sea),
            ("ORILLAS DEL TIBRE", "Corazon de Roma - Nivel 2", [
                ("Descripcion del nivel", [
                    "Orillas verdes del Rio Tibre. Arboles, arbustos y ruinas de templos antiguos.",
                    "Dificultad: 2/5 | Velocidad: 2-4 | Enemigos: HP 1 | Meta: 200 puntos",
                ]),
                ("Nota Historica", [
                    "El Tibre (405 km) es el cuarto rio mas largo de Italia. Roma crecio "
                    "en siete colinas a sus orillas.",
                    "Leyenda de Romulo y Remo: los infantes fueron arrojados al Tibre, pero una loba "
                    "los encontro y amamanto. Asi nacio Roma!",
                ]),
                ("Decoraciones de Orilla", [
                    "Arboles - coronas verdes exuberantes en troncos marrones",
                    "Arbustos - matorrales al borde del agua",
                    "Ruinas - columnas de piedra y muros de edificios antiguos",
                ]),
            ], draw_scene_tiber),
            ("PUERTO DE OSTIA", "Ruta Comercial - Nivel 3", [
                ("Descripcion del nivel", [
                    "Puerto comercial con muelles, barriles y redes. Mas monedas, "
                    "pero los enemigos son mas astutos.",
                    "Dificultad: 3/5 | Velocidad: 2.2-4.5 | Enemigos: HP 2 | Meta: 350 puntos",
                ]),
                ("Nota Historica", [
                    "Ostia fue el puerto de Roma, fundado en el siglo IV a.C.",
                    "Los barriles en las orillas son contenedores estandar para vino y aceite de oliva.",
                ]),
                ("Decoraciones de Orilla", [
                    "Barriles - barriles de madera con aros metalicos",
                    "Cajas - fardos de carga de madera",
                    "Postes - pilotes de madera con capitales de piedra",
                    "Redes - redes de pesca en postes",
                ]),
            ], draw_scene_harbor),
            ("FORTALEZA DE ROMA", "Muros de las Legiones - Nivel 4", [
                ("Descripcion del nivel", [
                    "Muros de piedra de la fortaleza con arcos, torres de vigilancia, banderas SPQR.",
                    "Dificultad: 3/5 | Velocidad: 2.5-5 | Enemigos: HP 2 | Meta: 520 puntos",
                ]),
                ("Nota Historica", [
                    "SPQR - Senatus Populusque Romanus (Senado y Pueblo de Roma). "
                    "Este lema adornaba todos los edificios estatales de Roma.",
                ]),
                ("Decoraciones de Orilla", [
                    "Muros - mamposteria de piedra con arcos y puertas",
                    "Torres - torres de vigilancia con almenas",
                    "Estandartes SPQR - banderas rojas de la Republica Romana",
                ]),
            ], draw_scene_fortress),
            ("PIRAMIDES DE EGIPTO", "Secretos del Nilo - Nivel 5", [
                ("Descripcion del nivel", [
                    "Orillas arenosas del Nilo, grandes piramides, palmeras y cactus.",
                    "Dificultad: 4/5 | Velocidad: 2.8-5.5 | Enemigos: HP 2 | Meta: 700 puntos",
                ]),
                ("Nota Historica", [
                    "La Gran Piramide de Giza es la unica Maravilla del Mundo Antiguo que sobrevive. "
                    "Altura: 146 m, construida alrededor del 2560 a.C.",
                ]),
                ("Decoraciones de Orilla", [
                    "Piramides - estructuras de piedra triangulares con cara sombreada",
                    "Palmeras - troncos marrones con coronas de abanico verdes",
                    "Cactus - plantas espinosas verdes con ramas",
                ]),
            ], draw_scene_egypt),
            ("RUS ANTIGUA", "Bosques y Rios - Nivel 6", [
                ("Descripcion del nivel", [
                    "Abedules blancos, izbas de madera, cercas e iglesias con cumbres doradas.",
                    "Dificultad: 4/5 | Velocidad: 3-5.5 | Enemigos: HP 3 | Meta: 900 puntos",
                ]),
                ("Nota Historica", [
                    "Rus Antigua (siglos IX-XIII) - estado eslavico oriental. "
                    "Capital: Kiev, 'madre de las ciudades rusas'.",
                    "El abedul es el simbolo de Rus. La corteza blanca se usaba para hacer "
                    "platos, zapatos (lapti) y hasta barcos.",
                ]),
                ("Decoraciones de Orilla", [
                    "Abedules - troncos blancos con rayas negras, coronas verdes",
                    "Izbas - casas de madera con techos triangulares y chimeneas",
                    "Cercas - empalizadas de madera de postes verticales",
                ]),
            ], draw_scene_rus),
            ("BATALLA FINAL", "La Ultima Prueba - Nivel 7", [
                ("Descripcion del nivel", [
                    "Todas las orillas se mezclan: arboles, piramides, abedules, fortalezas.",
                    "Dificultad: 5/5 | Velocidad: 3.5-6 | Enemigos: HP 3 | Meta: infinito",
                ]),
                ("Estrategia de Supervivencia", [
                    "Velocidad maxima en el nivel final. Los enemigos aparecen muy seguido con 3 HP.",
                    "Usa el ariete solo cuando estes seguro del impacto.",
                ]),
                ("Felicidades!", [
                    "Si llegaste al nivel final - eres un verdadero guerrero de Roma!",
                    "El Imperio esta orgulloso de ti, Capitan!",
                ]),
            ], draw_scene_battle),
            ("CATALOGO DE DECORACIONES", "Lista Completa de Elementos de Orilla", [
                ("Decoraciones Marinas (Nv.1)", [
                    "Algas - tiras verdes meciendose en la corriente",
                    "Boyas - marcadores rojos flotantes en postes blancos",
                    "Corales - formaciones rojas de arrecife",
                ]),
                ("Decoraciones Fluviales (Nv.2)", [
                    "Arboles - coronas exuberantes en troncos marrones",
                    "Arbustos - matorrales al borde del agua",
                    "Ruinas - columnas de piedra y fragmentos de muros de templos",
                ]),
                ("Decoraciones Portuarias (Nv.3)", [
                    "Barriles - barriles de madera con aros metalicos",
                    "Cajas - fardos de carga de madera con marca de cruz",
                    "Postes - pilotes de madera del muelle",
                ]),
                ("Decoraciones de Fortaleza (Nv.4)", [
                    "Muros - mamposteria de piedra con arcos y puertas",
                    "Torres - torres de vigilancia con almenas",
                    "Estandartes SPQR - banderas rojas de la Republica Romana",
                ]),
            ], draw_scene_catalog),
        ],
    },
}

TOME3 = {
    "ru": {
        "title1": "КНИГА", "title2": "СУДЕБ",
        "subtitle": "Персонажи, глоссарий и мудрости",
        "edition": "Издание третье, окончательное",
        "toc": [
            ("I.", "Персонажи - Римляне, которые сопровождают вас"),
            ("II.", "Судьбы - Истории каждого персонажа"),
            ("III.", "Глоссарий - Слова и термины игры"),
            ("IV.", "Латынь в игре - Язык Рима"),
            ("V.", "Стратегии и секреты"),
            ("VI.", "Достижения - Что можно открыть"),
            ("VII.", "Заключение - Аве, капитан!"),
        ],
        "chapters": [
            ("ПЕРСОНАЖИ", "Римляне, которые сопровождают вас", [
                ("Сенатор", [
                    "Узнаваем по лавровому венку на голове. Говорит о золоте и политике. "
                    "Его стихи пропитаны мудростью Сената и жадностью к денариям.",
                    "Появляется при сборе монет и при достижении milestone-очков.",
                ]),
                ("Центурион", [
                    "Узнаваем по шраму на лице. Строгий, дисциплинированный. "
                    "Говорит короткими рублеными фразами. Его стихи - приказы.",
                    "Появляется при таране и при получении урона.",
                ]),
                ("Легионер", [
                    "Основной боец. Без особых украшений, но с сильным духом. "
                    "Его стихи - боевые кличи.",
                    "Появляется при старте игры, при таране и при milestone.",
                ]),
                ("Торговец", [
                    "Всегда радуется деньгам. Его стихи - о выгоде и прибыли. "
                    "Представитель класса 'всадников' - богатых купцов.",
                    "Появляется при сборе монет и при столкновении с врагом.",
                ]),
                ("Гладиатор", [
                    "С золотыми серьгами, бывший раб, ставший бойцом. "
                    "Его стихи - о силе и победе.",
                    "Появляется при milestone и при таране.",
                ]),
                ("Раб", [
                    "Самый скромный персонаж. Удивляется всему. "
                    "Его стихи - детские восклицания боли и удивления.",
                    "Появляется при сборе монет, при уроне и при старте.",
                ]),
            ], draw_scene_characters),
            ("СУДЬБЫ", "Истории каждого персонажа", [
                ("Судьба Сенатора: Гай Юлий Аурелий", [
                    "Гай Юлий Аурелий - потомок древнего рода. Он сидит в Сенате "
                    "уже 30 лет и считает, что знает, как управлять империей.",
                    "Аурелий никогда не был на корабле, но считает себя экспертом "
                    "по морскому делу. Он написал три трактата, ни один из которых не был прочитан.",
                ]),
                ("Судьба Центуриона: Марк Петроний Железный", [
                    "Петроний получил прозвище 'Железный' после того, как "
                    "в битве при Каннах (216 до н.э.) его шлем был сбит мечом, "
                    "но он продолжал сражаться без шлема.",
                    "На его лице - три шрама. Петроний считает их декоративными и гордится каждым.",
                ]),
                ("Судьба Легионера: Луций из Тибура", [
                    "Луций - обычный солдат из небольшого города Тибур (совр. Тиволи). "
                    "Он мечтает вернуться домой и открыть виноградник.",
                    "Пока он таранит вражеские корабли, его виноградник "
                    "зарастает сорняками. Но Луций верит - однажды он вернётся.",
                ]),
                ("Судьба Торговца: Аврелия Морская", [
                    "Аврелия - одна из немногих женщин-торговцев Рима. "
                    "Она управляет флотом из 12 торговых кораблей.",
                    "Аврелия спонсирует гладиаторские бои, потому что считает "
                    "их 'хорошей инвестицией в PR'.",
                ]),
                ("Судьба Гладиатора: Спартак Младший", [
                    "Внук одного из сподвижников великого Спартака (или так он утверждает). "
                    "На самом деле он родился в Риме и никогда не был рабом.",
                    "Но его история продаёт билеты на арену в два раза лучше.",
                ]),
                ("Судьба Раба: Бедный Феликс", [
                    "Феликс - раб-писец, который записывает речи сенаторов. "
                    "Единственный грамотный человек в экипаже.",
                    "Феликс мечтает о свободе. Его хозяин пообещал освободить его, "
                    "когда он запишет 1000 речей. Сейчас он на 847-й.",
                ]),
            ], draw_scene_fates),
            ("ГЛОССАРИЙ", "Слова и термины игры", [
                ("Игровые термины", [
                    "Галера (triremis/galera) - гребной боевой корабль с тараном",
                    "Таран (rostrum) - бронзовый наконечник на носу корабля",
                    "Денарий (denarius) - основная серебряная монета Рима",
                    "Квинкема (quinquereme) - пятибаночное судно (5 рядов гребцов)",
                    "Легион (legio) - основное тактическое соединение римской армии",
                    "Центурион (centurio) - командир центурии (80 солдат)",
                ]),
                ("Слова из стихов", [
                    "Аве! - Привет! Здравствуй! (лат.ave)",
                    "SPQR - Senatus Populusque Romanus - Сенат и Народ Римский",
                    "Империя (imperium) - власть, государство",
                    "Марс - бог войны, покровитель Рима",
                    "Юпитер - верховный бог, повелитель молний",
                ]),
                ("Географические термины", [
                    "Тибр (Tiberis) - река, на которой стоит Рим (405 км)",
                    "Остия (Ostia) - порт Рима в устье Тибра",
                    "Маре Нострум (Mare Nostrum) - Наше море (Средиземное море)",
                    "Карфаген - вражеский город в Северной Африке",
                ]),
            ], draw_scene_glossary),
            ("ЛАТЫНЬ В ИГРЕ", "Язык Рима звучит в каждом стихе", [
                ("Ключевые фразы", [
                    "Ave Caesar! - Здравствуй, Цезарь!",
                    "Alea iacta est - Жребий брошен (Юлий Цезарь, 49 до н.э.)",
                    "Veni, vidi, vici - Пришёл, увидел, победил (Цезарь, 47 до н.э.)",
                    "Senatus Populusque Romanus - Сенат и Народ Римский",
                    "Carthago delenda est - Карфаген должен быть разрушен (Катон Старший)",
                    "Et tu, Brute? - И ты, Брут? (Цезарь перед смертью)",
                ]),
                ("Числа по-латыни", [
                    "I = 1, II = 2, III = 3, IV = 4, V = 5",
                    "VI = 6, VII = 7, VIII = 8, IX = 9, X = 10",
                    "L = 50, C = 100, D = 500, M = 1000",
                    "Римляне не знали нуля! Zero пришёл из Индии через арабов.",
                ]),
            ], draw_scene_latin),
            ("СТРАТЕГИИ", "Секреты опытного капитана", [
                ("Начинающий капитан", [
                    "1. Не паникуйте - камни движутся медленно на первых уровнях.",
                    "2. Держитесь центра - так проще уклоняться в обе стороны.",
                    "3. Не тараните каждый встречный - подождите, пока враг будет на линии.",
                    "4. Собирайте монеты - они безопасны и дают очки.",
                ]),
                ("Опытный воин", [
                    "1. Используйте таран проактивно - уничтожайте врагов раньше.",
                    "2. Следите за перезарядкой - во время cooldown'а вы уязвимы.",
                    "3. На высоких уровнях приоритет - уклонение, не уничтожение.",
                ]),
                ("Легендарный стратег", [
                    "1. На финальном уровне - минимум таранов, максимум уклонений.",
                    "2. Монеты собирайте только в 'окнах безопасности'.",
                    "3. Помните: скорость растёт с очками. Чем лучше играете, тем сложнее!",
                ]),
            ], draw_scene_strategies),
            ("ДОСТИЖЕНИЯ", "Что можно открыть", [
                ("Боевые достижения", [
                    "Первый таран - Уничтожить первого врага",
                    "10 таранов - Уничтожить 10 врагов за игру",
                    "Таранный мастер - Уничтожить врага на максимальной скорости",
                    "Непобедимый - Пройти уровень без потерь",
                ]),
                ("Сокровища", [
                    "Золотой путь - Собрать 100 монет за игру",
                    "Сокровище Цезаря - Набрать 500 очков",
                    "Богатство Империи - Набрать 1000 очков",
                ]),
                ("Путешественник", [
                    "Моряк - Добраться до Гавани Остии",
                    "Легионер - Добраться до Крепости Рима",
                    "Путешественник - Добраться до Пирамид",
                    "Славянин - Добраться до Древней Руси",
                    "Победитель - Добраться до Финальной битвы",
                ]),
            ], draw_scene_achievements),
            ("ЗАКЛЮЧЕНИЕ", "Аве, капитан!", [
                ("Последнее слово", [
                    "Эта книга - ваш путеводитель по миру Римских Галер. "
                    "Вы познали историю римского флота, узнали о берегах Тибра "
                    "и пирамидах Египта, прочитали судьбы шести римлян.",
                    "Каждый раз, когда вы нажимаете 'В БОЙ!', вы становитесь "
                    "частью великой истории.",
                ]),
                ("Мудрость Рима", [
                    "Dum spiro, spero - Пока дышу, надеюсь",
                    "Fortuna audaces iuvat - Фортуна помогает смелым",
                    "Dulce et decorum est pro patria mori - "
                    "Сладко и достойно умирать за отечество (Гораций)",
                    "Все дороги ведут в Рим - и все реки ведут к победе!",
                ]),
                ("Аве, капитан!", [
                    "Империя ждёт новых побед. Тибр течёт. Галера готова.",
                    "Ave, imperator! Morituri te salutant!",
                    "(Здравствуй, император! Идущие на смерть приветствуют тебя!)",
                ]),
            ], draw_scene_conclusion),
        ],
    },
    "en": {
        "title1": "BOOK", "title2": "OF FATES",
        "subtitle": "Characters, Glossary and Wisdom",
        "edition": "Third Edition, Final",
        "toc": [
            ("I.", "Characters - Romans Who Accompany You"),
            ("II.", "Fates - Stories of Each Character"),
            ("III.", "Glossary - Words and Terms"),
            ("IV.", "Latin in the Game - The Language of Rome"),
            ("V.", "Strategies and Secrets"),
            ("VI.", "Achievements - What You Can Unlock"),
            ("VII.", "Conclusion - Ave, Captain!"),
        ],
        "chapters": [
            ("CHARACTERS", "Romans Who Accompany You", [
                ("The Senator", [
                    "Recognized by his laurel wreath. Speaks of gold and politics. "
                    "His poems are steeped in the wisdom of the Senate and greed for denarii.",
                    "Appears when collecting coins and reaching milestone points.",
                ]),
                ("The Centurion", [
                    "Recognized by his facial scar. Strict, disciplined. "
                    "Speaks in short, clipped phrases. His poems are orders.",
                    "Appears when ramming and taking damage.",
                ]),
                ("The Legionary", [
                    "The main fighter. No special ornaments, but strong in spirit. "
                    "His poems are battle cries.",
                    "Appears at game start, when ramming, and at milestones.",
                ]),
                ("The Merchant", [
                    "Always happy about money. His poems are about profit and gain. "
                    "A member of the equestrian class - wealthy traders.",
                    "Appears when collecting coins and colliding with enemies.",
                ]),
                ("The Gladiator", [
                    "With golden earrings, a former slave turned fighter. "
                    "His poems are about strength and victory.",
                    "Appears at milestones and when ramming.",
                ]),
                ("The Slave", [
                    "The most humble character. Amazed by everything. "
                    "His poems are childlike exclamations of pain and surprise.",
                    "Appears when collecting coins, taking damage, and at game start.",
                ]),
            ], draw_scene_characters),
            ("FATES", "Stories of Each Character", [
                ("Fate of the Senator: Gaius Julius Aurelius", [
                    "Gaius Julius Aurelius is a descendant of an ancient lineage. "
                    "He has sat in the Senate for 30 years and believes he knows how to run the empire.",
                    "Aurelius has never been on a ship but considers himself an expert "
                    "on naval affairs. He wrote three treatises, none of which were ever read.",
                ]),
                ("Fate of the Centurion: Marcus Petronius the Iron", [
                    "Petronius earned the nickname 'The Iron' after the Battle of Cannae (216 BC) "
                    "when his helmet was knocked off by a sword, but he continued fighting without it.",
                    "Three scars adorn his face. Petronius considers them decorative and is proud of each.",
                ]),
                ("Fate of the Legionary: Lucius of Tibur", [
                    "Lucius is an ordinary soldier from the small city of Tibur (modern Tivoli). "
                    "He dreams of returning home to open a vineyard.",
                    "While he rams enemy ships, his vineyard overgrows with weeds. "
                    "But Lucius believes - one day he will return.",
                ]),
                ("Fate of the Merchant: Aurelia the Sea Trader", [
                    "Aurelia is one of the few women merchants of Rome. "
                    "She manages a fleet of 12 trading ships.",
                    "Aurelia sponsors gladiatorial games because she considers them "
                    "a 'good investment in PR'.",
                ]),
                ("Fate of the Gladiator: Spartacus Junior", [
                    "Grandson of a follower of the great Spartacus (or so he claims). "
                    "In reality, he was born in Rome and was never a slave.",
                    "But his story sells arena tickets twice as well.",
                ]),
                ("Fate of the Slave: Poor Felix", [
                    "Felix is a slave-scribe who records senators' speeches. "
                    "The only literate person in the crew.",
                    "Felix dreams of freedom. His master promised to free him "
                    "when he records 1000 speeches. He's currently on number 847.",
                ]),
            ], draw_scene_fates),
            ("GLOSSARY", "Words and Terms of the Game", [
                ("Game Terms", [
                    "Galley (triremis/galera) - a rowed warship with a ram",
                    "Ram (rostrum) - bronze tip on the bow of the ship",
                    "Denarius (denarius) - the main silver coin of Rome",
                    "Quinquereme (quinquereme) - five-oared ship (5 rows of rowers)",
                    "Legion (legio) - the main tactical unit of the Roman army",
                    "Centurion (centurio) - commander of a century (80 soldiers)",
                ]),
                ("Words from Poems", [
                    "Ave! - Hello! Greetings! (Latin: ave)",
                    "SPQR - Senatus Populusque Romanus - Senate and People of Rome",
                    "Empire (imperium) - power, state",
                    "Mars - god of war, protector of Rome",
                    "Jupiter - supreme god, ruler of lightning",
                ]),
                ("Geographic Terms", [
                    "Tiber (Tiberis) - the river on which Rome stands (405 km)",
                    "Ostia (Ostia) - Rome's port at the mouth of the Tiber",
                    "Mare Nostrum (Mare Nostrum) - Our Sea (the Mediterranean)",
                    "Carthage - enemy city in North Africa",
                ]),
            ], draw_scene_glossary),
            ("LATIN IN THE GAME", "The Language of Rome in Every Verse", [
                ("Key Phrases", [
                    "Ave Caesar! - Hail, Caesar!",
                    "Alea iacta est - The die is cast (Julius Caesar, 49 BC)",
                    "Veni, vidi, vici - I came, I saw, I conquered (Caesar, 47 BC)",
                    "Senatus Populusque Romanus - Senate and People of Rome",
                    "Carthago delenda est - Carthage must be destroyed (Cato the Elder)",
                    "Et tu, Brute? - And you, Brutus? (Caesar before death)",
                ]),
                ("Numbers in Latin", [
                    "I = 1, II = 2, III = 3, IV = 4, V = 5",
                    "VI = 6, VII = 7, VIII = 8, IX = 9, X = 10",
                    "L = 50, C = 100, D = 500, M = 1000",
                    "The Romans didn't know zero! Zero came from India through the Arabs.",
                ]),
            ], draw_scene_latin),
            ("STRATEGIES", "Secrets of an Experienced Captain", [
                ("Beginner Captain", [
                    "1. Don't panic - rocks move slowly on early levels.",
                    "2. Stay in the center - it's easier to dodge both ways.",
                    "3. Don't ram every ship - wait for the enemy to be on line.",
                    "4. Collect coins - they're safe and give points.",
                ]),
                ("Veteran Warrior", [
                    "1. Use the ram proactively - destroy enemies before they approach.",
                    "2. Watch the cooldown - you're vulnerable during recharge.",
                    "3. At higher levels, dodging takes priority over destroying.",
                ]),
                ("Legendary Strategist", [
                    "1. On the final level - minimum rams, maximum dodging.",
                    "2. Collect coins only in 'safe windows'.",
                    "3. Remember: speed grows with points. The better you play, the harder it gets!",
                ]),
            ], draw_scene_strategies),
            ("ACHIEVEMENTS", "What You Can Unlock", [
                ("Combat Achievements", [
                    "First Ram - Destroy the first enemy",
                    "10 Rams - Destroy 10 enemies in a game",
                    "Ram Master - Destroy an enemy at maximum speed",
                    "Undefeated - Complete a level without taking damage",
                ]),
                ("Treasures", [
                    "Golden Path - Collect 100 coins in a game",
                    "Caesar's Treasure - Score 500 points",
                    "Wealth of the Empire - Score 1000 points",
                ]),
                ("Traveler", [
                    "Sailor - Reach the Harbor of Ostia",
                    "Legionary - Reach the Fortress of Rome",
                    "Traveler - Reach the Pyramids",
                    "Slav - Reach Ancient Rus",
                    "Champion - Reach the Final Battle",
                ]),
            ], draw_scene_achievements),
            ("CONCLUSION", "Ave, Captain!", [
                ("Final Words", [
                    "This book is your guide to the world of Roman Galleys. "
                    "You've learned the history of the Roman fleet, explored the banks of the Tiber "
                    "and the pyramids of Egypt, and read the fates of six Romans.",
                    "Every time you click 'BATTLE!', you become part of a great story.",
                ]),
                ("Wisdom of Rome", [
                    "Dum spiro, spero - While I breathe, I hope",
                    "Fortuna audaces iuvat - Fortune favors the bold",
                    "Dulce et decorum est pro patria mori - "
                    "It is sweet and fitting to die for one's country (Horace)",
                    "All roads lead to Rome - and all rivers lead to victory!",
                ]),
                ("Ave, Captain!", [
                    "The Empire awaits new victories. The Tiber flows. The galley is ready.",
                    "Ave, imperator! Morituri te salutant!",
                    "(Hail, emperor! Those about to die salute you!)",
                ]),
            ], draw_scene_conclusion),
        ],
    },
    "es": {
        "title1": "LIBRO", "title2": "DE LOS DESTINOS",
        "subtitle": "Personajes, Glosario y Sabiduria",
        "edition": "Tercera Edicion, Final",
        "toc": [
            ("I.", "Personajes - Romanos que Te Acompanan"),
            ("II.", "Destinos - Historias de Cada Personaje"),
            ("III.", "Glosario - Palabras y Terminos"),
            ("IV.", "Latin en el Juego - El Idioma de Roma"),
            ("V.", "Estrategias y Secretos"),
            ("VI.", "Logros - Que Puedes Desbloquear"),
            ("VII.", "Conclusion - Ave, Capitan!"),
        ],
        "chapters": [
            ("PERSONAJES", "Romanos que Te Acompanan", [
                ("El Senador", [
                    "Reconocible por su corona de laurel. Habla de oro y politica. "
                    "Sus poemas estan impregnados de sabiduria del Senado y avaricia por denarios.",
                    "Aparece al recoger monedas y al alcanzar puntos de hito.",
                ]),
                ("El Centurion", [
                    "Reconocible por su cicatriz en la cara. Estricto, disciplinado. "
                    "Habla en frases cortas y secas. Sus poemas son ordenes.",
                    "Aparece al embestir y al recibir dano.",
                ]),
                ("El Legionario", [
                    "El luchador principal. Sin ornamentas especiales, pero con espiritu fuerte. "
                    "Sus poemas son gritos de batalla.",
                    "Aparece al iniciar el juego, al embestir y en hitos.",
                ]),
                ("El Mercader", [
                    "Siempre feliz por el dinero. Sus poemas son sobre ganancia y beneficio. "
                    "Miembro de la clase ecuestre - comerciantes ricos.",
                    "Aparece al recoger monedas y al colisionar con enemigos.",
                ]),
                ("El Gladiador", [
                    "Con aretes de oro, un ex esclavo convertido en luchador. "
                    "Sus poemas son sobre fuerza y victoria.",
                    "Aparece en hitos y al embestir.",
                ]),
                ("El Esclavo", [
                    "El personaje mas humilde. Se asombra de todo. "
                    "Sus poemas son exclamaciones infantiles de dolor y sorpresa.",
                    "Aparece al recoger monedas, recibir dano y al iniciar.",
                ]),
            ], draw_scene_characters),
            ("DESTINOS", "Historias de Cada Personaje", [
                ("Destino del Senador: Cayo Julio Aurelio", [
                    "Cayo Julio Aurelio es descendiente de un linaje antiguo. "
                    "Ha estado en el Senado 30 anos y cree saber como gobernar el imperio.",
                    "Aurelio nunca ha estado en un barco pero se considera experto en asuntos navales.",
                ]),
                ("Destino del Centurion: Marco Petronio el Hierro", [
                    "Petronio gano el apodo de 'El Hierro' despues de la Batalla de Canas (216 a.C.) "
                    "cuando su casco fue derribado por una espada, pero继续luchando sin el.",
                    "Tres cicatrices adornan su cara. Petronio las considera decorativas.",
                ]),
                ("Destino del Legionario: Lucio de Tibur", [
                    "Lucio es un soldado comun de la pequena ciudad de Tibur (actual Tivoli). "
                    "Sona con volver a casa para abrir una vid.",
                    "Mientras embeste barcos enemigos, su vid crece maleza. "
                    "Pero Lucio cree - un dia regresara.",
                ]),
                ("Destino del Mercader: Aurelia la Comerciante Maritima", [
                    "Aurelia es una de las pocas mujeres comerciantes de Roma. "
                    "Administra una flota de 12 barcos comerciales.",
                    "Aurelia patrocina juegos de gladiadores porque los considera "
                    "una 'buena inversion en relaciones publicas'.",
                ]),
                ("Destino del Gladiador: Espartaco el Joven", [
                    "Nieto de un companero del gran Espartaco (o asi el lo afirma). "
                    "En realidad nacio en Roma y nunca fue esclavo.",
                    "Pero su historia vende entradas a la arena al doble.",
                ]),
                ("Destino del Esclavo: Pobre Felix", [
                    "Felix es un esclavo escriba que registra los discursos de los senadores. "
                    "La unica persona alfabetizada en la tripulacion.",
                    "Felix sonia con la libertad. Su dueno prometio liberarlo "
                    "cuando registre 1000 discursos. Va por el numero 847.",
                ]),
            ], draw_scene_fates),
            ("GLOSARIO", "Palabras y Terminos del Juego", [
                ("Terminos del Juego", [
                    "Galera (triremis/galera) - barco de guerra a remos con ariete",
                    "Ariete (rostrum) - punta de bronce en la proa del barco",
                    "Denario (denarius) - moneda de plata principal de Roma",
                    "Quinquerreme (quinquereme) - barco de cinco remos por banco",
                    "Legion (legio) - unidad tactica principal del ejercito romano",
                    "Centurion (centurio) - comandante de una centuria (80 soldados)",
                ]),
                ("Palabras de los Poemas", [
                    "Ave! - Hola! Saludos! (lat. ave)",
                    "SPQR - Senatus Populusque Romanus - Senado y Pueblo de Roma",
                    "Imperio (imperium) - poder, estado",
                    "Marte - dios de la guerra, protector de Roma",
                    "Jupiter - dios supremo, senor del rayo",
                ]),
                ("Terminos Geograficos", [
                    "Tiber (Tiberis) - rio donde esta Roma (405 km)",
                    "Ostia (Ostia) - puerto de Roma en la desembocadura del Tibre",
                    "Mare Nostrum (Mare Nuestro Mar) - Mar Mediterraneo",
                    "Cartago - ciudad enemiga en el norte de Africa",
                ]),
            ], draw_scene_glossary),
            ("LATIN EN EL JUEGO", "El Idioma de Roma en Cada Verso", [
                ("Frases Clave", [
                    "Ave Caesar! - Salve, Cesar!",
                    "Alea iacta est - La suerte esta echada (Julio Cesar, 49 a.C.)",
                    "Veni, vidi, vici - Vine, vi, venci (Cesar, 47 a.C.)",
                    "Senatus Populusque Romanus - Senado y Pueblo de Roma",
                    "Carthago delenda est - Cartago debe ser destruida (Caton el Viejo)",
                ]),
                ("Numeros en Latin", [
                    "I = 1, II = 2, III = 3, IV = 4, V = 5",
                    "VI = 6, VII = 7, VIII = 8, IX = 9, X = 10",
                    "L = 50, C = 100, D = 500, M = 1000",
                    "Los romanos no conocian el cero! El cero vino de la India a traves de los arabes.",
                ]),
            ], draw_scene_latin),
            ("ESTRATEGIAS", "Secretos de un Capitan Experimentado", [
                ("Capitan Principiante", [
                    "1. No entres en panico - las rocas se mueven lento en los primeros niveles.",
                    "2. Mantente en el centro - es mas facil esquivar a ambos lados.",
                    "3. No embestas todos los barcos - espera a que el enemigo este en linea.",
                    "4. Recoge monedas - son seguras y dan puntos.",
                ]),
                ("Guerrero Veterano", [
                    "1. Usa el ariete proactivamente - destruye enemigos antes de que se acerquen.",
                    "2. Vigila la recarga - estas vulnerable durante el enfriamiento.",
                    "3. En niveles altos, esquivar tiene prioridad sobre destruir.",
                ]),
                ("Estratega Legendario", [
                    "1. En el nivel final - minimo de embestidas, maximo de esquivas.",
                    "2. Recoge monedas solo en 'ventanas seguras'.",
                    "3. Recuerda: la velocidad crece con los puntos. Cuanto mejor juegues, mas dificil sera!",
                ]),
            ], draw_scene_strategies),
            ("LOGROS", "Que Puedes Desbloquear", [
                ("Logros de Combate", [
                    "Primer Ariete - Destruir al primer enemigo",
                    "10 Arietes - Destruir 10 enemigos en una partida",
                    "Maestro del Ariete - Destruir un enemigo a velocidad maxima",
                    "Invicto - Completar un nivel sin recibir dano",
                ]),
                ("Tesoros", [
                    "Camino Dorado - Recoger 100 monedas en una partida",
                    "Tesoro de Cesar - Alcanzar 500 puntos",
                    "Riqueza del Imperio - Alcanzar 1000 puntos",
                ]),
                ("Viajero", [
                    "Marinero - Llegar al Puerto de Ostia",
                    "Legionario - Llegar a la Fortaleza de Roma",
                    "Viajero - Llegar a las Piramides",
                    "Eslavo - Llegar a la Rus Antigua",
                    "Campeon - Llegar a la Batalla Final",
                ]),
            ], draw_scene_achievements),
            ("CONCLUSION", "Ave, Capitan!", [
                ("Palabras Finales", [
                    "Este libro es tu guia por el mundo de las Galeras Romanas. "
                    "Has aprendido la historia de la flota romana, explorado las orillas del Tibre "
                    "y las piramides de Egipto, y leido los destinos de seis romanos.",
                    "Cada vez que haces clic en 'A COMBATIR!', te conviertes parte de una gran historia.",
                ]),
                ("Sabiduria de Roma", [
                    "Dum spiro, spero - Mientras respiro, espero",
                    "Fortuna audaces iuvat - La fortuna favorece a los audaces",
                    "Dulce et decorum est pro patria mori - "
                    "Es dulce y digno morir por la patria (Horacio)",
                    "Todos los caminos llevan a Roma - y todos los rios llevan a la victoria!",
                ]),
                ("Ave, Capitan!", [
                    "El Imperio espera nuevas victorias. El Tibre fluye. La galera esta lista.",
                    "Ave, imperator! Morituri te salutant!",
                    "(Salve, emperador! Los que van a morir te saludan!)",
                ]),
            ], draw_scene_conclusion),
        ],
    },
}

# ============================================================
# GENERATION FUNCTIONS
# ============================================================
ILLUSTRATIONS_MAP = {
    "scene_sea": draw_scene_sea,
    "scene_tiber": draw_scene_tiber,
    "scene_harbor": draw_scene_harbor,
    "scene_fortress": draw_scene_fortress,
    "scene_egypt": draw_scene_egypt,
    "scene_rus": draw_scene_rus,
    "scene_battle": draw_scene_battle,
    "scene_controls": draw_scene_controls,
    "scene_scoring": draw_scene_scoring,
    "scene_ram": draw_scene_ram,
    "scene_obstacles": draw_scene_obstacles,
    "scene_launch": draw_scene_launch,
    "scene_characters": draw_scene_characters,
    "scene_fates": draw_scene_fates,
    "scene_glossary": draw_scene_glossary,
    "scene_latin": draw_scene_latin,
    "scene_strategies": draw_scene_strategies,
    "scene_achievements": draw_scene_achievements,
    "scene_conclusion": draw_scene_conclusion,
    "scene_catalog": draw_scene_catalog,
}

LANG_NAMES = {"ru": "Русский", "en": "English", "es": "Espanol"}
TOME_NAMES = {
    "ru": {1: "Величие Империи", 2: "Земли Империи", 3: "Книга Судеб"},
    "en": {1: "Glory of the Empire", 2: "Lands of the Empire", 3: "Book of Fates"},
    "es": {1: "Gloria del Imperio", 2: "Tierras del Imperio", 3: "Libro de los Destinos"},
}
TOME_FILENAMES = {
    "ru": {1: "Tome_1_Velichie_Imperii", 2: "Tome_2_Zemli_Imperii", 3: "Tome_3_Kniga_Sudeb"},
    "en": {1: "Tome_1_Glory_of_Empire", 2: "Tome_2_Lands_of_Empire", 3: "Tome_3_Book_of_Fates"},
    "es": {1: "Tome_1_Gloria_del_Imperio", 2: "Tome_2_Tierras_del_Imperio", 3: "Tome_3_Libro_de_Destinos"},
}

def get_tome_data(tome_num, lang):
    if tome_num == 1: return TOME1[lang]
    if tome_num == 2: return TOME2[lang]
    return TOME3[lang]

def generate_tome(tome_num, lang):
    data = get_tome_data(tome_num, lang)
    cn = CONTENT[lang]
    fname = TOME_FILENAMES[lang][tome_num]
    c = canvas.Canvas(os.path.join(OUT, f"{fname}.pdf"), pagesize=A4)

    # === TITLE PAGE ===
    draw_page_bg(c, DARK)
    draw_border(c, GOLD, 5)
    draw_corner_ornaments(c, GOLD)
    c.setFillColor(GOLD)
    c.setFont("Arial-Bold", 14)
    tlabel = {1: "I", 2: "II", 3: "III"}[tome_num]
    c.drawCentredString(W/2, H-40*mm, f"TOME {tlabel}")
    c.setFont("Arial-Bold", 36)
    c.drawCentredString(W/2, H-65*mm, data["title1"])
    c.drawCentredString(W/2, H-82*mm, data["title2"])
    draw_divider(c, H-95*mm, GOLD)
    c.setFont("Arial", 14)
    c.setFillColor(CREAM)
    c.drawCentredString(W/2, H-108*mm, data["subtitle"])
    c.setFont("Arial", 12)
    c.drawCentredString(W/2, H-120*mm, cn["book_title"])

    if tome_num == 1:
        draw_boat(c, W/2, H-145*mm, 80, 30)
    elif tome_num == 2:
        draw_pyramid(c, W/2-40, H-145*mm, 25)
        draw_birch(c, W/2+40, H-145*mm, 30)
        draw_fortress_wall(c, W/2-30, H-165*mm, 60, 30)
    else:
        draw_roman_face(c, W/2, H-145*mm, 25)

    c.setFont("Arial-Oblique", 10)
    c.setFillColor(GRAY)
    c.drawCentredString(W/2, 40*mm, data["edition"])
    c.drawCentredString(W/2, 33*mm, "Anno Domini MMXXVI")
    c.showPage()

    # === TABLE OF CONTENTS ===
    draw_page_bg(c, CREAM)
    draw_border(c, GOLD)
    draw_corner_ornaments(c, GOLD)
    c.setFillColor(DARK)
    c.setFont("Arial-Bold", 24)
    toc_title = {"ru": "СОДЕРЖАНИЕ", "en": "TABLE OF CONTENTS", "es": "CONTENIDO"}[lang]
    c.drawCentredString(W/2, H-35*mm, toc_title)
    draw_divider(c, H-42*mm, GOLD)
    y = H - 55*mm
    for num, title in data["toc"]:
        c.setFillColor(BROWN)
        c.setFont("Arial-Bold", 12)
        c.drawString(30*mm, y, num)
        c.setFillColor(DARK)
        c.setFont("Arial", 12)
        c.drawString(45*mm, y, title)
        y -= 9*mm
    c.showPage()

    # === CHAPTERS ===
    for ch_i, (ch_title, ch_subtitle, paragraphs, illustration_fn) in enumerate(data["chapters"]):
        text_page(c, ch_i+1, ch_title, ch_subtitle, paragraphs, illustration_fn)

    # === FOOTER ON LAST PAGE ===
    page_label = {"ru": "Стр.", "en": "Page", "es": "Pag."}[lang]
    c.setFont("Arial-Oblique", 9)
    c.setFillColor(GRAY)
    c.drawCentredString(W/2, 15*mm, f"{cn['footer_prefix']} - Tome {tome_num} - {page_label} END")

    c.save()
    print(f"[+] Tome {tome_num} ({LANG_NAMES[lang]}): {fname}.pdf")

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("  GENERATING 3 TOMES x 3 LANGUAGES = 9 PDFs")
    print("=" * 50)
    for lang in ["ru", "en", "es"]:
        for tome in [1, 2, 3]:
            generate_tome(tome, lang)
    print("\n[+] All 9 PDFs generated!")
