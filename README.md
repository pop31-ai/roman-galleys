# Roman Galleys / Римские Галеры / Galeras Romanas

Arcade game where you pilot a Roman galley through rivers and seas of the ancient world. Dodge rocks, collect gold, and ram enemy ships!

Аркадная игра, где вы управляете римской галерой по рекам и морям древнего мира. Уклоняйтесь от камней, собирайте золото и тараните вражеские корабли!

Juego de arcade donde piloteas una galera romana por rios y mares del mundo antiguo. Esquiva rocas, recoge oro y embeste barcos enemigos!

## How to Play / Как играть / Como Jugar

- **A/D** or **arrows** / **стрелки** / **flechas** — movement
- **Space** / **Пробел** / **Espacio** — ram (cooldown ~1s)

## Уровни

| # | Название | Берега | Описание | Сложность |
|---|----------|--------|----------|-----------|
| 1 | Чистое море | Водоросли, кораллы | Бирюзовые воды Средиземноморья | ★☆☆☆☆ |
| 2 | Берега Тибра | Деревья, руины, кусты | Зелёные береги и руины храмов | ★★☆☆☆ |
| 3 | Гавань Остии | Бочки, ящики, сети | Торговые причалы и склады | ★★★☆☆ |
| 4 | Крепость Рима | Стены, башни, знамёна SPQR | Стены и башни легионеров | ★★★☆☆ |
| 5 | Пирамиды Египта | Пальмы, пирамиды, кактусы | Песчаные берега Нила | ★★★★☆ |
| 6 | Древняя Русь | Берёзы, избы, церкви | Деревянные крепости и заборы | ★★★★☆ |
| 7 | Финальная битва | Всё вместе | Последний бой за империю! | ★★★★★ |

## Береговые декорации

Каждый уровень имеет уникальные декорации на берегах реки:

- **Море** — водоросли, буи, кораллы
- **Тибр** — деревья, кусты, трава, античные руины
- **Гавань** — бочки, ящики, причальные столбы, сети
- **Крепость** — каменные стены с арками, башни, знамёна SPQR
- **Пирамиды** — египетские пирамиды, пальмы, кактусы, песчаные дюны
- **Русь** — берёзы, деревянные избы, заборы, церкви с куполами

## Римляне

При каждом событии появляется римлянин со стихом. Типы персонажей:

- **Сенатор** — с лавровым венком, одобряет золото
- **Центурион** — с шрамом на лице, руководит боем
- **Легионер** — основной боец, таранит от души
- **Торговец** — радуется каждому денарию
- **Гладиатор** — с золотыми серьгами, хвастается щитом
- **Раб** — удивляется всему подряд

## Запуск

Просто откройте `roman-boats.html` в браузере. Никаких серверов и зависимостей.

## Тестирование (CV)

Скрипт `test_levels_cv.py` автоматически проверяет уровни через компьютерное зрение (OpenCV):

```bash
pip install opencv-python Pillow pyautogui numpy
python test_levels_cv.py
```

Скрипт:
- Запускает локальный HTTP-сервер
- Открывает игру в браузере с автостартом
- Делает скриншоты на каждом уровне
- Детектит объекты по HSV-цветам (лодки, камни, монеты)
- Генерирует debug-изображения и JSON-отчёт

## Illustrated Book / Книга / Libro (9 PDFs, 3 languages)

The game comes with illustrated PDF books in 3 languages: Russian, English, Spanish.

### Russian / Русский

| Tome | File | Contents |
|------|------|----------|
| I | `Tome_1_Velichie_Imperii.pdf` | Introduction, controls, world, scoring, ram, obstacles, launch |
| II | `Tome_2_Zemli_Imperii.pdf` | All 7 levels + decoration catalog |
| III | `Tome_3_Kniga_Sudeb.pdf` | Characters, fates, glossary, Latin, strategies, achievements |

### English

| Tome | File | Contents |
|------|------|----------|
| I | `Tome_1_Glory_of_Empire.pdf` | Introduction, controls, world, scoring, ram, obstacles, launch |
| II | `Tome_2_Lands_of_Empire.pdf` | All 7 levels + decoration catalog |
| III | `Tome_3_Book_of_Fates.pdf` | Characters, fates, glossary, Latin, strategies, achievements |

### Spanish / Espanol

| Tome | File | Contents |
|------|------|----------|
| I | `Tome_1_Gloria_del_Imperio.pdf` | Introduccion, controles, mundo, puntuacion, ariete, obstaculos |
| II | `Tome_2_Tierras_del_Imperio.pdf` | Todos los 7 niveles + catalogo de decoraciones |
| III | `Tome_3_Libro_de_Destinos.pdf` | Personajes, destinos, glosario, latin, estrategias, logros |

Generation:

```bash
pip install reportlab
python generate_book.py
```

## Visual Game Guide / Визуальный гид (3 PDFs)

Detailed annotated illustrations of every game element, gameplay situations, and level previews:

| Language | File | Pages |
|----------|------|-------|
| RU | `Game_Art_RU.pdf` | Boat anatomy, HUD, obstacles, coins, characters, all 7 levels, ramming/dodging/collecting/damage |
| EN | `Game_Art_EN.pdf` | Same content in English |
| ES | `Game_Art_ES.pdf` | Same content in Spanish |

Each page includes:
- Game-accurate element drawings (exact colors from HTML5 Canvas code)
- Labeled callout annotations (hex colors, dimensions, frame counts)
- Full game scene mockups per level with water colors and decorations
- Gameplay situation diagrams (ramming, dodging, collecting, damage)
- All 6 character types with feature labels
- HUD element breakdown (health, ram cooldown, score, progress bar)

Generation:

```bash
python generate_game_art.py
```

## Стек

- HTML5 Canvas
- JavaScript (ES6)
- OpenCV + Python (тестирование)
- ReportLab (PDF-книга)
