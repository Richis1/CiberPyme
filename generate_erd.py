import sys
from PIL import Image, ImageDraw, ImageFont

# Define schema directly based on models to ensure we have the relations right
tables = {
    "auth_user": {
        "color": "#6366f1",  # Indigo (User management)
        "cols": [
            ("id", "INTEGER", "PK"),
            ("username", "varchar(150)", ""),
            ("password", "varchar(128)", ""),
            ("email", "varchar(254)", ""),
            ("first_name", "varchar(150)", ""),
            ("last_name", "varchar(150)", ""),
            ("is_active", "bool", ""),
            ("is_staff", "bool", ""),
            ("is_superuser", "bool", ""),
            ("date_joined", "datetime", ""),
            ("last_login", "datetime", ""),
        ],
        "pos": (50, 100)
    },
    "principal_perfil": {
        "color": "#818cf8",  # Lighter Indigo
        "cols": [
            ("id", "INTEGER", "PK"),
            ("usuario_id", "INTEGER", "FK -> auth_user.id"),
            ("empresa_id", "INTEGER", "FK -> auth_user.id"),
            ("nombre_empresa", "varchar(200)", ""),
            ("rfc", "varchar(13)", ""),
            ("curp", "varchar(18)", ""),
            ("telefono", "varchar(20)", ""),
            ("notas", "TEXT", ""),
        ],
        "pos": (50, 600)
    },
    "principal_alertaseguridad": {
        "color": "#ef4444",  # Red (Alerts)
        "cols": [
            ("id", "INTEGER", "PK"),
            ("titulo", "varchar(200)", ""),
            ("descripcion", "TEXT", ""),
            ("nivel", "varchar(10)", ""),
            ("fecha", "datetime", ""),
        ],
        "pos": (50, 1000)
    },
    "principal_progresocurso": {
        "color": "#0ea5e9",  # Sky Blue (Course Progress)
        "cols": [
            ("id", "INTEGER", "PK"),
            ("usuario_id", "INTEGER", "FK -> auth_user.id"),
            ("curso_id", "bigint", "FK -> principal_curso.id"),
            ("estado", "varchar(20)", ""),
            ("porcentaje", "INTEGER", ""),
            ("ultima_pagina", "INTEGER", ""),
            ("fecha_completado", "datetime", ""),
        ],
        "pos": (550, 100)
    },
    "principal_progresosimulacion": {
        "color": "#f59e0b",  # Amber (Simulation Progress)
        "cols": [
            ("id", "INTEGER", "PK"),
            ("usuario_id", "INTEGER", "FK -> auth_user.id"),
            ("simulacion_id", "bigint", "FK -> principal_simulacion.id"),
            ("completado", "bool", ""),
            ("puntaje", "INTEGER", ""),
            ("fecha", "datetime", ""),
        ],
        "pos": (550, 500)
    },
    "principal_materialcurso": {
        "color": "#3b82f6",  # Blue (Course Material)
        "cols": [
            ("id", "INTEGER", "PK"),
            ("curso_id", "bigint", "FK -> principal_curso.id"),
            ("nombre", "varchar(200)", ""),
            ("archivo", "varchar(100)", ""),
        ],
        "pos": (550, 850)
    },
    "principal_curso": {
        "color": "#3b82f6",  # Blue (Courses Core)
        "cols": [
            ("id", "INTEGER", "PK"),
            ("titulo", "varchar(200)", ""),
            ("descripcion", "TEXT", ""),
            ("orden", "INTEGER", ""),
            ("puntos", "INTEGER", ""),
            ("icono", "varchar(50)", ""),
            ("video", "varchar(100)", ""),
        ],
        "pos": (1050, 100)
    },
    "principal_simulacion": {
        "color": "#f59e0b",  # Amber (Simulations Core)
        "cols": [
            ("id", "INTEGER", "PK"),
            ("titulo", "varchar(200)", ""),
            ("descripcion", "TEXT", ""),
            ("icono", "varchar(50)", ""),
            ("puntos", "INTEGER", ""),
        ],
        "pos": (1050, 600)
    },
    "principal_contenidocurso": {
        "color": "#2563eb",  # Darker Blue (Course Details)
        "cols": [
            ("id", "INTEGER", "PK"),
            ("curso_id", "bigint", "FK -> principal_curso.id"),
            ("titulo", "varchar(200)", ""),
            ("texto", "TEXT", ""),
            ("imagen", "varchar(100)", ""),
            ("orden", "INTEGER", ""),
        ],
        "pos": (1550, 100)
    },
    "principal_pregunta": {
        "color": "#10b981",  # Emerald Green (Quizzes)
        "cols": [
            ("id", "INTEGER", "PK"),
            ("curso_id", "bigint", "FK -> principal_curso.id"),
            ("texto", "TEXT", ""),
            ("orden", "INTEGER", ""),
        ],
        "pos": (1550, 480)
    },
    "principal_desafiosimulacion": {
        "color": "#d97706",  # Darker Amber (Simulation Details)
        "cols": [
            ("id", "INTEGER", "PK"),
            ("simulacion_id", "bigint", "FK -> principal_simulacion.id"),
            ("imagen", "varchar(100)", ""),
            ("texto_complementario", "TEXT", ""),
            ("es_peligro", "bool", ""),
            ("explicacion", "TEXT", ""),
        ],
        "pos": (1550, 850)
    },
    "principal_opcion": {
        "color": "#059669",  # Darker Emerald Green (Quiz Options)
        "cols": [
            ("id", "INTEGER", "PK"),
            ("pregunta_id", "bigint", "FK -> principal_pregunta.id"),
            ("texto", "varchar(255)", ""),
            ("es_correcta", "bool", ""),
        ],
        "pos": (2050, 480)
    }
}

# Image dimensions
W, H = 2500, 1350
bg_color = "#0f172a"  # Slate 900
panel_bg = "#1e293b"  # Slate 800
text_color = "#f8fafc"  # Slate 50
text_muted = "#94a3b8"  # Slate 400
border_color = "#334155"  # Slate 700

img = Image.new("RGB", (W, H), bg_color)
draw = ImageDraw.Draw(img)

# Try to load a nice font, otherwise use default
try:
    font_title = ImageFont.truetype("arialbd.ttf", 16)
    font_bold = ImageFont.truetype("arialbd.ttf", 12)
    font_regular = ImageFont.truetype("arial.ttf", 12)
    font_header = ImageFont.truetype("arialbd.ttf", 24)
except IOError:
    font_title = ImageFont.load_default()
    font_bold = ImageFont.load_default()
    font_regular = ImageFont.load_default()
    font_header = ImageFont.load_default()

# Draw title
draw.text((50, 30), "DIAGRAMA DE BASE DE DATOS (PYMES)", font=font_header, fill="#38bdf8")
draw.text((50, 65), "Esquema actual de la base de datos de Django (db.sqlite3)", font=font_regular, fill=text_muted)

# Table sizes and layout constants
col_width = 400
row_height = 24
header_height = 36

# Draw tables
table_bounds = {}
for tname, info in tables.items():
    x, y = info["pos"]
    num_cols = len(info["cols"])
    h = header_height + num_cols * row_height + 10
    
    # Save bounds for drawing relation lines
    table_bounds[tname] = (x, y, x + col_width, y + h)
    
    # Outer container rounded rectangle (represented as rect with borders)
    # Background
    draw.rectangle([x, y, x + col_width, y + h], fill=panel_bg, outline=border_color, width=1)
    
    # Color bar header
    draw.rectangle([x, y, x + col_width, y + header_height], fill=info["color"])
    
    # Title
    draw.text((x + 12, y + 8), tname, font=font_title, fill="#ffffff")
    
    # Columns
    curr_y = y + header_height + 5
    for cname, ctype, ckey in info["cols"]:
        # Key mark
        key_color = "#f59e0b" if "PK" in ckey else ("#10b981" if "FK" in ckey else text_muted)
        key_txt = "🔑 " if "PK" in ckey else ("🔗 " if "FK" in ckey else "   ")
        
        # Name
        name_font = font_bold if ckey else font_regular
        name_color = text_color if not ckey else "#ffffff"
        
        draw.text((x + 10, curr_y), f"{key_txt}{cname}", font=name_font, fill=name_color)
        
        # Type & constraint details
        type_txt = f"{ctype}"
        if ckey:
            type_txt += f" ({ckey})"
        
        # Draw type right-aligned
        type_w = draw.textlength(type_txt, font=font_regular) if hasattr(draw, "textlength") else len(type_txt) * 6
        draw.text((x + col_width - type_w - 10, curr_y), type_txt, font=font_regular, fill=text_muted)
        
        curr_y += row_height

# Draw relations (lines connecting tables)
relations = [
    # (From Table, To Table, From Field Index, To Field Index, color)
    ("principal_perfil", "auth_user", 1, 0, "#818cf8"), # usuario_id
    ("principal_perfil", "auth_user", 2, 0, "#818cf8"), # empresa_id
    ("principal_progresocurso", "auth_user", 1, 0, "#6366f1"), # usuario_id
    ("principal_progresocurso", "principal_curso", 2, 0, "#0ea5e9"), # curso_id
    ("principal_progresosimulacion", "auth_user", 1, 0, "#6366f1"), # usuario_id
    ("principal_progresosimulacion", "principal_simulacion", 2, 0, "#f59e0b"), # simulacion_id
    ("principal_materialcurso", "principal_curso", 1, 0, "#3b82f6"), # curso_id
    ("principal_contenidocurso", "principal_curso", 1, 0, "#3b82f6"), # curso_id
    ("principal_pregunta", "principal_curso", 1, 0, "#10b981"), # curso_id
    ("principal_opcion", "principal_pregunta", 1, 0, "#10b981"), # pregunta_id
    ("principal_desafiosimulacion", "principal_simulacion", 1, 0, "#f59e0b"), # simulacion_id
]

for from_t, to_t, from_idx, to_idx, rcolor in relations:
    if from_t in table_bounds and to_t in table_bounds:
        fx1, fy1, fx2, fy2 = table_bounds[from_t]
        tx1, ty1, tx2, ty2 = table_bounds[to_t]
        
        # Calculate approximate connector coordinates
        # We connect right edge of source to left edge of target, or vice versa
        # based on horizontal positions
        
        # Source point: center of the specific row
        from_y = fy1 + header_height + 5 + (from_idx * row_height) + (row_height // 2)
        # Target point: center of the specific row (often PK id at index 0)
        to_y = ty1 + header_height + 5 + (to_idx * row_height) + (row_height // 2)
        
        if fx1 == tx1:
            # Same column, route line outside to the left
            start_pt = (fx1, from_y)
            end_pt = (tx1, to_y)
            offset_x = fx1 - 25
            draw.line([start_pt, (offset_x, start_pt[1]), (offset_x, end_pt[1]), end_pt], fill=rcolor, width=2)
            draw.ellipse([end_pt[0] - 3, end_pt[1] - 3, end_pt[0] + 3, end_pt[1] + 3], fill=rcolor)
        elif fx1 > tx2:
            # Source is to the right of Target
            start_pt = (fx1, from_y)
            end_pt = (tx2, to_y)
            # Draw line with elbow
            mid_x = (start_pt[0] + end_pt[0]) // 2
            draw.line([start_pt, (mid_x, start_pt[1]), (mid_x, end_pt[1]), end_pt], fill=rcolor, width=2)
            # Arrow/dot at target
            draw.ellipse([end_pt[0] - 3, end_pt[1] - 3, end_pt[0] + 3, end_pt[1] + 3], fill=rcolor)
        else:
            # Source is to the left of Target
            start_pt = (fx2, from_y)
            end_pt = (tx1, to_y)
            # Draw line with elbow
            mid_x = (start_pt[0] + end_pt[0]) // 2
            draw.line([start_pt, (mid_x, start_pt[1]), (mid_x, end_pt[1]), end_pt], fill=rcolor, width=2)
            # Arrow/dot at target
            draw.ellipse([end_pt[0] - 3, end_pt[1] - 3, end_pt[0] + 3, end_pt[1] + 3], fill=rcolor)

# Save image
img.save("diagrama.png")
print("New ER diagram saved as diagrama.png successfully!")
