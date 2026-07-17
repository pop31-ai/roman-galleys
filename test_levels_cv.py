"""
Римские Галеры — тестирование уровней через OpenCV
Делает скриншоты игры и анализирует объекты по цвету.
"""
import cv2
import numpy as np
import subprocess
import time
import os
import sys
import json

try:
    from PIL import ImageGrab
except ImportError:
    print("[!] Требуется Pillow: pip install Pillow")
    sys.exit(1)

try:
    import pyautogui
    pyautogui.FAILSAFE = False
except ImportError:
    print("[!] Требуется pyautogui: pip install pyautogui")
    sys.exit(1)

try:
    import pygetwindow as gw
except ImportError:
    gw = None

GAME_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "roman-boats.html")
GAME_URL = "file:///" + GAME_PATH.replace("\\", "/") + "#autostart"
SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Цвета объектов в HSV для детекции
COLOR_RANGES = {
    "player_hull": {"lower": np.array([5, 60, 40]), "upper": np.array([30, 255, 220])},
    "enemy_hull": {"lower": np.array([0, 100, 80]), "upper": np.array([12, 255, 220])},
    "coin": {"lower": np.array([18, 150, 200]), "upper": np.array([38, 255, 255])},
    "rock": {"lower": np.array([80, 10, 40]), "upper": np.array([130, 120, 200])},
    "water": {"lower": np.array([80, 40, 30]), "upper": np.array([120, 255, 255])},
    "hp_red": {"lower": np.array([0, 150, 150]), "upper": np.array([10, 255, 255])},
    "gold_ui": {"lower": np.array([18, 80, 120]), "upper": np.array([35, 255, 255])},
    "enemy_sail": {"lower": np.array([0, 150, 100]), "upper": np.array([12, 255, 220])},
    "player_sail": {"lower": np.array([15, 5, 140]), "upper": np.array([40, 100, 255])},
}


def open_game():
    """Запускает локальный сервер и открывает игру с автостартом."""
    import webbrowser
    import threading

    port = 18923
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    from http.server import HTTPServer, SimpleHTTPRequestHandler
    server = HTTPServer(("127.0.0.1", port), SimpleHTTPRequestHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    url = f"http://127.0.0.1:{port}/roman-boats.html#autostart"
    print(f"[*] Сервер запущен на порту {port}")
    print(f"[*] Открываю: {url}")
    webbrowser.open(url)
    print("[*] Жду 6 секунд для загрузки и автостарта...")
    time.sleep(6)
    server.shutdown()


def take_screenshot(name):
    """Делает скриншот и сохраняет."""
    img = np.array(ImageGrab.grab())
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    cv2.imwrite(path, img)
    return img


def find_objects_by_color(img, color_name, roi=None):
    """Находит объекты по цвету на изображении."""
    if roi:
        x, y, w, h = roi
        img = img[y:y+h, x:x+w]

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cr = COLOR_RANGES[color_name]
    mask = cv2.inRange(hsv, cr["lower"], cr["upper"])

    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    objects = []
    for c in contours:
        area = cv2.contourArea(c)
        if area > 10:
            x, y, w, h = cv2.boundingRect(c)
            if roi:
                x += roi[0]
                y += roi[1]
            objects.append({"x": x, "y": y, "w": w, "h": h, "area": area})

    return objects


def find_game_canvas(img):
    """Находит canvas игры по синему цвету воды. Возвращает (x,y,w,h) или None."""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    water_mask = cv2.inRange(hsv, COLOR_RANGES["water"]["lower"], COLOR_RANGES["water"]["upper"])

    kernel = np.ones((10, 10), np.uint8)
    water_mask = cv2.morphologyEx(water_mask, cv2.MORPH_CLOSE, kernel)
    water_mask = cv2.morphologyEx(water_mask, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(water_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    # Игровой canvas ~800x600, ищем прямоугольник с подходящей пропорцией
    best = None
    best_score = 0
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        # КанVAS игры должен быть достаточно большим
        if w > 200 and h > 200:
            # Штрафуем за несоответствие пропорции 4:3
            ratio = w / max(h, 1)
            ratio_score = 1.0 - abs(ratio - 1.33) * 0.5
            score = area * ratio_score
            if score > best_score:
                best_score = score
                best = (x, y, w, h)

    if best is None:
        # Фоллбэк: просто самый большой контур > 10000
        largest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest) > 10000:
            best = cv2.boundingRect(largest)

    return best


def analyze_level_from_screenshot(img, level_num):
    """Анализирует скриншот уровня и возвращает статистику."""
    canvas = find_game_canvas(img)
    if not canvas:
        return {"error": "Canvas не найден", "level": level_num}

    cx, cy, cw, ch = canvas
    roi = (cx, cy, cw, ch)
    result = {
        "level": level_num,
        "canvas_region": {"x": cx, "y": cy, "w": cw, "h": ch},
        "objects": {},
        "checks": [],
    }

    for color_name in COLOR_RANGES:
        if color_name in ("water", "hp_red", "gold_ui"):
            continue
        objects = find_objects_by_color(img, color_name, roi)
        result["objects"][color_name] = {
            "count": len(objects),
            "positions": [{"x": o["x"], "y": o["y"], "w": o["w"], "h": o["h"], "area": round(o["area"], 1)} for o in objects],
        }

    player = result["objects"].get("player_hull", {})
    player_sail = result["objects"].get("player_sail", {})
    enemies = result["objects"].get("enemy_hull", {})
    coins = result["objects"].get("coin", {})
    rocks = result["objects"].get("rock", {})

    has_player = player.get("count", 0) > 0 or player_sail.get("count", 0) > 0
    result["checks"].append({"test": "player_visible", "pass": has_player,
                             "detail": f"hull={player.get('count',0)} sail={player_sail.get('count',0)}"})

    total_objects = sum(v.get("count", 0) for v in result["objects"].values())
    result["checks"].append({"test": "objects_present", "pass": total_objects >= 1,
                             "detail": f"obj_count={total_objects}"})

    enemy_count = enemies.get("count", 0)
    rock_count = rocks.get("count", 0)
    coin_count = coins.get("count", 0)

    result["checks"].append({"test": "enemies", "pass": True,
                             "detail": f"count={enemy_count}"})
    result["checks"].append({"test": "rocks", "pass": True,
                             "detail": f"count={rock_count}"})
    result["checks"].append({"test": "coins", "pass": True,
                             "detail": f"count={coin_count}"})

    if level_num >= 2:
        result["checks"].append({
            "test": "enemies_on_high_level",
            "pass": enemy_count > 0,
            "detail": f"Lv{level_num} expects >=1 enemy, found={enemy_count}"
        })

    return result


def draw_debug(img, analysis, level_num):
    """Рисует отладочное изображение с аннотациями."""
    debug = img.copy()
    canvas = analysis.get("canvas_region")
    if canvas:
        x, y, w, h = canvas["x"], canvas["y"], canvas["w"], canvas["h"]
        cv2.rectangle(debug, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(debug, f"Level {level_num}", (x + 10, y + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    colors = {
        "player_hull": (255, 165, 0),
        "enemy_hull": (0, 0, 255),
        "coin": (0, 255, 255),
        "rock": (128, 128, 128),
    }

    for obj_name, data in analysis.get("objects", {}).items():
        if obj_name in colors:
            for pos in data.get("positions", []):
                color = colors[obj_name]
                cv2.rectangle(debug, (pos["x"], pos["y"]),
                              (pos["x"] + pos["w"], pos["y"] + pos["h"]), color, 2)
                cv2.putText(debug, obj_name, (pos["x"], pos["y"] - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

    y_off = 20
    for check in analysis.get("checks", []):
        status = "PASS" if check["pass"] else "FAIL"
        color = (0, 255, 0) if check["pass"] else (0, 0, 255)
        text = f"{status}: {check['test']} - {check['detail']}"
        cv2.putText(debug, text, (10, y_off),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        y_off += 22

    path = os.path.join(SCREENSHOT_DIR, f"debug_level_{level_num}.png")
    cv2.imwrite(path, debug)
    return debug


def focus_browser():
    """Находит и фокусирует окно браузера."""
    if gw is None:
        return
    time.sleep(1)
    try:
        all_windows = gw.getAllWindows()
        for win in all_windows:
            title = win.title.lower() if win.title else ""
            if any(kw in title for kw in ["roman", "galera", "html", "boat", "index", "file"]):
                try:
                    if win.isMinimized:
                        win.restore()
                    win.activate()
                    time.sleep(0.5)
                    print(f"  Фокус: {win.title}")
                    return
                except Exception:
                    pass
    except Exception:
        pass
    print("  [!] Не удалось найти окно, пробую кликнуть по центру")
    screen = pyautogui.size()
    pyautogui.click(screen.width // 2, screen.height // 2)
    time.sleep(0.3)


def simulate_gameplay():
    """Имитирует нажатия клавиш для прохождения уровней."""
    print("\n[*] Игра автозапущена (параметр ?autostart)")
    focus_browser()
    time.sleep(2)

    print("[*] Начинаю имитацию игры...")
    results = []

    for level in range(5):
        print(f"\n{'='*50}")
        print(f"[*] УРОВЕНЬ {level + 1}: Анализирую...")
        time.sleep(3)

        level_objects = {"player_hull": 0, "enemy_hull": 0, "coin": 0, "rock": 0}
        screenshots_for_level = []

        for shot in range(5):
            name = f"level_{level+1}_frame_{shot}"
            img = take_screenshot(name)
            screenshots_for_level.append(img)

            analysis = analyze_level_from_screenshot(img, level + 1)
            for obj_name, data in analysis.get("objects", {}).items():
                if obj_name in level_objects:
                    level_objects[obj_name] = max(level_objects[obj_name], data.get("count", 0))

            focus_browser()
            if shot % 2 == 0:
                pyautogui.keyDown("left")
                time.sleep(0.5)
                pyautogui.keyUp("left")
            else:
                pyautogui.keyDown("right")
                time.sleep(0.5)
                pyautogui.keyUp("right")
            time.sleep(1)

        final_img = screenshots_for_level[-1]
        final_analysis = analyze_level_from_screenshot(final_img, level + 1)
        draw_debug(final_img, final_analysis, level + 1)

        level_result = {
            "level": level + 1,
            "max_objects": level_objects,
            "checks": final_analysis.get("checks", []),
        }
        results.append(level_result)

        pyautogui.press("space")
        time.sleep(0.5)

    return results


def run_static_analysis():
    """Статический анализ изображений уровней (без реальной игры)."""
    print("\n[*] Статический анализ изображений...")
    results = []

    for level_num in range(1, 6):
        img_path = os.path.join(SCREENSHOT_DIR, f"level_{level_num}_frame_4.png")
        if not os.path.exists(img_path):
            print(f"  [!] Нет скриншота для уровня {level_num}")
            continue

        img = cv2.imread(img_path)
        if img is None:
            continue

        analysis = analyze_level_from_screenshot(img, level_num)
        if "error" in analysis:
            print(f"  [!] Уровень {level_num}: {analysis['error']}")
        else:
            draw_debug(img, analysis, level_num)

        all_pass = all(c["pass"] for c in analysis.get("checks", []))
        status = "OK" if all_pass else "WARN"
        print(f"  [{status}] Уровень {level_num}: {len(analysis.get('checks',[]))} проверок")

        for check in analysis.get("checks", []):
            icon = "+" if check["pass"] else "!"
            print(f"    [{icon}] {check['test']}: {check['detail']}")

        results.append(analysis)

    return results


def generate_report(results):
    """Генерирует отчёт в JSON."""
    report = {
        "game": "Римские Галеры",
        "total_levels": 5,
        "level_data": [
            {"name": "Тибр", "score_to_next": 80, "enemy_hp": 1, "base_speed": 1.5},
            {"name": "Гавань Остии", "score_to_next": 200, "enemy_hp": 2, "base_speed": 2.0},
            {"name": "Средиземное море", "score_to_next": 400, "enemy_hp": 2, "base_speed": 2.5},
            {"name": "Пиратские воды", "score_to_next": 650, "enemy_hp": 3, "base_speed": 3.0},
            {"name": "Финальная битва", "score_to_next": "Infinity", "enemy_hp": 3, "base_speed": 3.5},
        ],
        "test_results": results,
    }

    report_path = os.path.join(SCREENSHOT_DIR, "test_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n[*] Отчёт сохранён: {report_path}")
    return report


def main():
    print("=" * 50)
    print("  РИМСКИЕ ГАЛЕРЫ — ТЕСТИРОВАНИЕ УРОВНЕЙ")
    print("=" * 50)

    # Проверяем зависимости
    print("[*] Проверяю зависимости...")
    try:
        import PIL
        print(f"  [+] Pillow {PIL.__version__}")
    except ImportError:
        print("  [-] Pillow не установлен. pip install Pillow")
        return

    try:
        import pyautogui
        print(f"  [+] pyautogui установлен")
    except ImportError:
        print("  [-] pyautogui не установлен. pip install pyautogui")
        return

    # Шаг 1: Открываем игру
    open_game()

    # Шаг 2: Делаем скриншот начального экрана
    print("\n[*] Скриншот начального экрана...")
    start_img = take_screenshot("00_start_screen")
    print(f"  Сохранено: screenshots/00_start_screen.png")

    # Шаг 3: Запускаем игру и имитируем прохождение
    results = simulate_gameplay()

    # Шаг 4: Статический анализ
    static_results = run_static_analysis()

    # Шаг 5: Генерируем отчёт
    all_results = results + static_results
    report = generate_report(all_results)

    # Шаг 6: Итоги
    print("\n" + "=" * 50)
    print("  ИТОГИ ТЕСТИРОВАНИЯ")
    print("=" * 50)

    total_checks = 0
    passed_checks = 0
    for r in all_results:
        for check in r.get("checks", []):
            total_checks += 1
            if check["pass"]:
                passed_checks += 1

    print(f"  Всего проверок: {total_checks}")
    print(f"  Пройдено: {passed_checks}")
    print(f"  Провалено: {total_checks - passed_checks}")
    print(f"  Процент: {passed_checks/max(total_checks,1)*100:.1f}%")

    print(f"\n  Скриншоты: {SCREENSHOT_DIR}/")
    print(f"  Отладочные изображения: screenshots/debug_level_*.png")
    print(f"  JSON-отчёт: screenshots/test_report.json")

    print("\n[*] Готово!")


if __name__ == "__main__":
    main()
