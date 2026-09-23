import json
import os
import math
from playwright.sync_api import sync_playwright

project_dir = os.path.abspath(r'C:\Users\soyto.JOAQUIN2206\OneDrive\Desktop\Proyectos\perfumes-gestion')
pdf_dir = os.path.join(project_dir, 'PDFs')
indiv_dir = os.path.join(project_dir, 'paginas_individuales')

os.makedirs(pdf_dir, exist_ok=True)
os.makedirs(indiv_dir, exist_ok=True)

with open(os.path.join(project_dir, 'fem.json'), encoding='utf-8') as f:
    fem = json.load(f)
with open(os.path.join(project_dir, 'masc.json'), encoding='utf-8') as f:
    masc = json.load(f)
with open(os.path.join(project_dir, 'otros.json'), encoding='utf-8') as f:
    otros = json.load(f)

P_CLASSIC = "$22.000"
P_CLASSIC_PROMO = "2 x $40.000"
P_ARABIC = "$24.000"
P_AUTO = "$11.000"
P_AUTO_PROMO = "2 COMBOS x $20.000"

def render_col(items):
    lines = []
    for item in items:
        if isinstance(item, (list, tuple)):
            name = item[0]
            brand = item[1] if len(item) > 1 else ""
        elif isinstance(item, dict):
            name = item.get('name', '')
            brand = item.get('brand', '')
        else:
            name = str(item)
            brand = ""
        lines.append(f'<div class="item-row"><span class="item-name" title="{name}">{name}</span><span class="item-brand">{brand}</span></div>')
    return "".join(lines)

def render_2cols(items, max_left=None):
    if max_left is None:
        half = math.ceil(len(items) / 2)
    else:
        half = max_left
    left_items = items[:half]
    right_items = items[half:]
    return f'''
    <div class="fragrance-list-card-2col">
        <div class="col-list">
            {render_col(left_items)}
        </div>
        <div class="col-divider"></div>
        <div class="col-list">
            {render_col(right_items)}
        </div>
    </div>
    '''

CSS_COMMON = '''
@page {
    size: 860px 1216px;
    margin: 0;
}
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}
body {
    margin: 0;
    padding: 0;
    background: #000;
    color: #fff;
    font-family: 'Montserrat', sans-serif;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
}
.page {
    width: 860px;
    height: 1216px;
    page-break-after: always;
    page-break-inside: avoid;
    position: relative;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    padding: 36px 32px 32px 32px;
    overflow: hidden;
}
.title-container {
    text-align: center;
    margin-bottom: 12px;
}
.sub-script {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 28px;
    color: #ffd1dc;
    text-shadow: 0 0 10px rgba(255, 105, 180, 0.8), 2px 2px 5px rgba(0,0,0,0.9);
    margin-bottom: -6px;
}
.sub-script-masc {
    color: #cce4ff;
    text-shadow: 0 0 10px rgba(65, 105, 225, 0.8), 2px 2px 5px rgba(0,0,0,0.9);
}
.sub-script-gold {
    color: #ffe6a3;
    text-shadow: 0 0 10px rgba(223, 177, 91, 0.8), 2px 2px 5px rgba(0,0,0,0.9);
}
.main-title {
    font-family: 'Cinzel', serif;
    font-size: 38px;
    font-weight: 800;
    letter-spacing: 3px;
    color: #ffffff;
    text-transform: uppercase;
    text-shadow: 0 0 16px rgba(255, 255, 255, 0.7), 2px 3px 8px rgba(0,0,0,0.95);
}
.price-badge-pill {
    display: inline-block;
    background: rgba(10, 10, 15, 0.9);
    border: 1px solid #dfb15b;
    color: #ffe8b2;
    padding: 5px 18px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-top: 5px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.6);
}

/* ESTRUCTURA A 2 COLUMNAS POR PÁGINA */
.fragrance-list-card-2col {
    width: 100%;
    flex: 1;
    background: rgba(10, 8, 18, 0.85);
    backdrop-filter: blur(6px);
    border: 1.5px solid rgba(223, 177, 91, 0.4);
    border-radius: 16px;
    padding: 16px 20px;
    display: grid;
    grid-template-columns: 1fr 1px 1fr;
    gap: 18px;
    box-shadow: 0 10px 35px rgba(0,0,0,0.8);
    margin-bottom: 8px;
}
.col-divider {
    background: linear-gradient(180deg, transparent, rgba(223, 177, 91, 0.5) 20%, rgba(223, 177, 91, 0.5) 80%, transparent);
    width: 1px;
    height: 100%;
}
.col-list {
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
}
.item-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 3px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.07);
}
.item-row:last-child {
    border-bottom: none;
}
.item-name {
    font-family: 'Montserrat', sans-serif;
    font-weight: 700;
    font-size: 13.5px;
    color: #ffffff;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.9);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 235px;
}
.item-brand {
    font-family: 'Montserrat', sans-serif;
    font-weight: 600;
    font-size: 11.5px;
    color: #dfb15b;
    text-align: right;
    margin-left: 8px;
    white-space: nowrap;
}
.page-footer-num {
    position: absolute;
    bottom: 10px;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.5);
    letter-spacing: 1px;
}
.header-brand-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 6px;
}
.header-brand-logo img {
    width: 46px;
    height: 46px;
    border-radius: 50%;
    border: 1.5px solid #dfb15b;
    box-shadow: 0 0 12px rgba(192, 132, 252, 0.4);
}
.header-brand-name {
    font-family: 'Cinzel', serif;
    font-size: 18px;
    font-weight: 800;
    color: #dfb15b;
    letter-spacing: 3px;
}
'''

# =========================================================================
# 1. GENERACIÓN: CATÁLOGO FEMENINO (2 COLUMNAS)
# =========================================================================
fem_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>BJ BEAUTY - Catálogo Femenino</title>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Montserrat:wght@400;500;600;700&family=Playfair+Display:ital,wght@1,600;1,700&display=swap" rel="stylesheet">
<style>{CSS_COMMON}</style>
</head>
<body>
'''

# P1: PORTADA
fem_html += f'''
<div class="page" style="background-image: linear-gradient(180deg, rgba(8,6,14,0.35) 0%, rgba(8,6,14,0.85) 65%, #050408 100%), url('fondo_femeninas_rosas.jpg'); justify-content: center; align-items: center; text-align: center;">
    <div style="margin-top: 170px;">
        <img src="logo_bj_beauty.png" style="width: 215px; height: 215px; border-radius: 50%; box-shadow: 0 0 50px rgba(192, 132, 252, 0.6), 0 0 25px rgba(223, 177, 91, 0.5); border: 2px solid #dfb15b; margin-bottom: 25px;">
        <div style="font-family: 'Playfair Display', serif; font-style: italic; font-size: 34px; color: #ffd1dc; margin-bottom: 4px;">Colección Exclusiva</div>
        <div style="font-family: 'Cinzel', serif; font-size: 48px; font-weight: 900; letter-spacing: 5px; color: #ffffff; text-shadow: 0 0 25px rgba(255,255,255,0.7);">CATÁLOGO FEMENINO</div>
        <div style="font-size: 15px; letter-spacing: 4px; color: #c084fc; text-transform: uppercase; font-weight: 600; margin-top: 6px;">Alta Perfumería • Fragancias Árabes • Tendencias Virales</div>
        
        <div style="display: flex; justify-content: center; gap: 16px; margin-top: 35px;">
            <span style="background: rgba(15, 10, 25, 0.88); border: 1.5px solid #dfb15b; color: #ffe6a3; padding: 10px 22px; border-radius: 25px; font-weight: 700; font-size: 15px;">✨ 60ml: {P_CLASSIC} (Promo: {P_CLASSIC_PROMO})</span>
            <span style="background: rgba(15, 10, 25, 0.88); border: 1.5px solid #c084fc; color: #e9d5ff; padding: 10px 22px; border-radius: 25px; font-weight: 700; font-size: 15px;">👑 Árabes: {P_ARABIC}</span>
        </div>
    </div>
</div>
'''

# P2: NUEVOS INGRESOS FEM & TENDENCIAS (2 columnas)
nuevos_fem_list = otros.get('nuevos_fem', [])
# Completamos con destacados para armar 2 columnas equilibradas
nuevos_destacados_fem = nuevos_fem_list + [
    ("Delina", "Parfums de Marly"),
    ("Baccarat Rouge 540", "Maison Francis Kurkdjian"),
    ("Bianco Latte", "Giardini Di Toscana"),
    ("Yara Candy", "Lattafa"),
    ("Eclaire", "Lattafa"),
    ("Fakhar Rose", "Lattafa"),
    ("Mayar Cherry", "Lattafa")
]

fem_html += f'''
<div class="page" style="background-image: url('fondo_nuevos_ingresos_fem.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script">Tendencias 2026</div>
        <div class="main-title">NUEVOS INGRESOS & TENDENCIAS</div>
        <div class="price-badge-pill">ÚLTIMOS LANZAMIENTOS • {P_CLASSIC} / {P_ARABIC}</div>
    </div>
    {render_2cols(nuevos_destacados_fem)}
    <div class="page-footer-num">BJ BEAUTY • Colección Femenina</div>
</div>
'''

# P3: ÁRABES FEMENINAS (2 COLUMNAS: 10 y 10)
arabes_fem_full = list(otros['arabes_fem'])
if ('Victoria', 'Lattafa') not in arabes_fem_full:
    arabes_fem_full.append(('Victoria', 'Lattafa (Nuevo)'))

fem_html += f'''
<div class="page" style="background-image: url('fondo_arabes_dorado.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script sub-script-gold">Perfumería Oriental</div>
        <div class="main-title">ÁRABES FEMENINAS</div>
        <div class="price-badge-pill">PRECIO: {P_ARABIC} C/U • ALTA FIJACIÓN & ESTELA</div>
    </div>
    {render_2cols(arabes_fem_full)}
    <div class="page-footer-num">BJ BEAUTY • Colección Femenina</div>
</div>
'''

# P4 a P8: FEMENINAS CLÁSICAS (222 perfumes en 5 páginas de 44 items a 2 columnas de 22)
items_per_page = 44
fem_pages = [fem[i:i + items_per_page] for i in range(0, len(fem), items_per_page)]

for idx, page_items in enumerate(fem_pages):
    bg = 'fondo_femeninas_rosas.jpg' if idx % 2 == 0 else 'fondo_femeninas_orquideas.jpg'
    fem_html += f'''
    <div class="page" style="background-image: url('{bg}'); justify-content: space-between;">
        <div class="title-container">
            <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
            <div class="sub-script">Colección Clásica</div>
            <div class="main-title">FEMENINAS (Parte {idx+1})</div>
            <div class="price-badge-pill">60 ML • {P_CLASSIC} • PROMO: {P_CLASSIC_PROMO}</div>
        </div>
        {render_2cols(page_items, max_left=math.ceil(len(page_items)/2))}
        <div class="page-footer-num">BJ BEAUTY • Colección Femenina</div>
    </div>
    '''

# CONTRATAPA FEMENINA
fem_html += f'''
<div class="page" style="background-image: linear-gradient(rgba(8,6,14,0.9), rgba(8,6,14,0.95)), url('fondo_femeninas_rosas.jpg'); justify-content: center;">
    <div style="text-align: center; max-width: 680px; background: rgba(18, 14, 28, 0.88); border: 1.5px solid #dfb15b; border-radius: 20px; padding: 45px 35px; box-shadow: 0 12px 45px rgba(0,0,0,0.85);">
        <img src="logo_bj_beauty.png" style="width: 110px; height: 110px; border-radius: 50%; box-shadow: 0 0 25px rgba(192, 132, 252, 0.4); border: 1.5px solid #dfb15b; margin-bottom: 20px;">
        <div style="font-family: 'Cinzel', serif; font-size: 32px; color: #dfb15b; margin-bottom: 12px; font-weight: 800;">¿CÓMO REALIZAR TU PEDIDO?</div>
        <p style="color: #e2e8f0; font-size: 16px; margin-bottom: 25px; line-height: 1.6;">Elegí tus fragancias favoritas y coordiná tu pedido directamente por WhatsApp.</p>
        
        <div style="background: rgba(0,0,0,0.55); border: 1px solid rgba(223, 177, 91, 0.35); border-radius: 12px; padding: 20px; margin-bottom: 25px; text-align: left;">
            <div style="font-size: 15px; color: #ffd1dc; margin-bottom: 8px;">💳 <b>Medios de Pago:</b></div>
            <div style="color: #cbd5e1; font-size: 14px; margin-bottom: 14px;">• Efectivo / Transferencias (Mercado Pago, Cuenta DNI, Bancarias)</div>
            <div style="font-size: 15px; color: #ffe6a3; margin-bottom: 8px;">📦 <b>Entregas:</b></div>
            <div style="color: #cbd5e1; font-size: 14px;">• Puntos de encuentro y envíos a domicilio coordinados.</div>
        </div>

        <div style="font-family: 'Cinzel', serif; font-size: 22px; color: #fff; margin-bottom: 6px;">BJ BEAUTY • ALTA PERFUMERÍA</div>
        <div style="color: #c084fc; font-size: 14px; letter-spacing: 2px;">CALIDAD • PERSISTENCIA • ELEGANCIA</div>
    </div>
</div>
'''

fem_html += '</body></html>'
fem_file = os.path.join(project_dir, 'catalogo_femenino.html')
with open(fem_file, 'w', encoding='utf-8') as f:
    f.write(fem_html)
print('Generated catalogo_femenino.html with 2-column layout.')


# =========================================================================
# 2. GENERACIÓN: CATÁLOGO MASCULINO (2 COLUMNAS)
# =========================================================================
masc_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>BJ BEAUTY - Catálogo Masculino</title>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Montserrat:wght@400;500;600;700&family=Playfair+Display:ital,wght@1,600;1,700&display=swap" rel="stylesheet">
<style>{CSS_COMMON}</style>
</head>
<body>
'''

# P1: PORTADA MASCULINA
masc_html += f'''
<div class="page" style="background-image: linear-gradient(180deg, rgba(6,8,16,0.35) 0%, rgba(6,8,16,0.85) 65%, #04060c 100%), url('fondo_masculinas_seda_azul.jpg'); justify-content: center; align-items: center; text-align: center;">
    <div style="margin-top: 170px;">
        <img src="logo_bj_beauty.png" style="width: 215px; height: 215px; border-radius: 50%; box-shadow: 0 0 50px rgba(56, 189, 248, 0.5), 0 0 25px rgba(223, 177, 91, 0.5); border: 2px solid #dfb15b; margin-bottom: 25px;">
        <div style="font-family: 'Playfair Display', serif; font-style: italic; font-size: 34px; color: #cce4ff; margin-bottom: 4px;">Colección Exclusiva</div>
        <div style="font-family: 'Cinzel', serif; font-size: 48px; font-weight: 900; letter-spacing: 5px; color: #ffffff; text-shadow: 0 0 25px rgba(255,255,255,0.7);">CATÁLOGO MASCULINO</div>
        <div style="font-size: 15px; letter-spacing: 4px; color: #38bdf8; text-transform: uppercase; font-weight: 600; margin-top: 6px;">Alta Perfumería • Perfumería Árabe • Distinción & Carácter</div>
        
        <div style="display: flex; justify-content: center; gap: 16px; margin-top: 35px;">
            <span style="background: rgba(10, 15, 28, 0.88); border: 1.5px solid #dfb15b; color: #ffe6a3; padding: 10px 22px; border-radius: 25px; font-weight: 700; font-size: 15px;">✨ 60ml: {P_CLASSIC} (Promo: {P_CLASSIC_PROMO})</span>
            <span style="background: rgba(10, 15, 28, 0.88); border: 1.5px solid #38bdf8; color: #bae6fd; padding: 10px 22px; border-radius: 25px; font-weight: 700; font-size: 15px;">👑 Árabes: {P_ARABIC}</span>
        </div>
    </div>
</div>
'''

# P2: NUEVOS INGRESOS MASC & TENDENCIAS (2 COLUMNAS)
nuevos_masc_list = otros.get('nuevos_masc', [])
masc_html += f'''
<div class="page" style="background-image: url('fondo_nuevos_ingresos_masc.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script sub-script-masc">Tendencias 2026</div>
        <div class="main-title">NUEVOS INGRESOS</div>
        <div class="price-badge-pill">ÚLTIMOS LANZAMIENTOS • {P_CLASSIC} / {P_ARABIC}</div>
    </div>
    {render_2cols(nuevos_masc_list)}
    <div class="page-footer-num">BJ BEAUTY • Colección Masculina</div>
</div>
'''

# P3: ÁRABES MASCULINAS (2 COLUMNAS)
arabes_masc_total = list(otros['arabes_masc'])
nuevos_masc_arabes = [
    ('Altair', 'Parfums de Marly'),
    ('Amber Oud Aqua Dubai', 'Al Haramain'),
    ('Asad Zanzibar', 'Lattafa'),
    ('Khamrah Waha', 'Lattafa'),
    ('Liquid Brun', 'French Avenue')
]
for item in nuevos_masc_arabes:
    if item not in arabes_masc_total:
        arabes_masc_total.append(item)

half_am = math.ceil(len(arabes_masc_total) / 2)
arabes_masc_p1 = arabes_masc_total[:half_am]
arabes_masc_p2 = arabes_masc_total[half_am:]

masc_html += f'''
<div class="page" style="background-image: url('fondo_arabes_noche.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script sub-script-gold">Perfumería Oriental</div>
        <div class="main-title">ÁRABES MASCULINAS (I)</div>
        <div class="price-badge-pill">PRECIO: {P_ARABIC} C/U • BEST SELLERS GLOBALES</div>
    </div>
    {render_2cols(arabes_masc_p1)}
    <div class="page-footer-num">BJ BEAUTY • Colección Masculina</div>
</div>
'''

masc_html += f'''
<div class="page" style="background-image: url('fondo_arabes_vortice.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script sub-script-gold">Perfumería Oriental</div>
        <div class="main-title">ÁRABES MASCULINAS (II)</div>
        <div class="price-badge-pill">PRECIO: {P_ARABIC} C/U • NOTAS DE OUD & CUERO</div>
    </div>
    {render_2cols(arabes_masc_p2)}
    <div class="page-footer-num">BJ BEAUTY • Colección Masculina</div>
</div>
'''

# P5 a P9: MASCULINAS CLÁSICAS (210 perfumes en 5 páginas de 42 items a 2 columnas de 21)
masc_items_per_page = 42
masc_pages = [masc[i:i + masc_items_per_page] for i in range(0, len(masc), masc_items_per_page)]

for idx, page_items in enumerate(masc_pages):
    bg = 'fondo_masculinas_seda_azul.jpg' if idx % 2 == 0 else 'fondo_masculinas_estrellas.jpg'
    masc_html += f'''
    <div class="page" style="background-image: url('{bg}'); justify-content: space-between;">
        <div class="title-container">
            <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
            <div class="sub-script sub-script-masc">Colección Clásica</div>
            <div class="main-title">MASCULINAS (Parte {idx+1})</div>
            <div class="price-badge-pill">60 ML • {P_CLASSIC} • PROMO: {P_CLASSIC_PROMO}</div>
        </div>
        {render_2cols(page_items, max_left=math.ceil(len(page_items)/2))}
        <div class="page-footer-num">BJ BEAUTY • Colección Masculina</div>
    </div>
    '''

# CONTRATAPA MASCULINA
masc_html += f'''
<div class="page" style="background-image: linear-gradient(rgba(6,8,16,0.9), rgba(6,8,16,0.95)), url('fondo_masculinas_estrellas.jpg'); justify-content: center;">
    <div style="text-align: center; max-width: 680px; background: rgba(14, 18, 30, 0.88); border: 1.5px solid #dfb15b; border-radius: 20px; padding: 45px 35px; box-shadow: 0 12px 45px rgba(0,0,0,0.85);">
        <img src="logo_bj_beauty.png" style="width: 110px; height: 110px; border-radius: 50%; box-shadow: 0 0 25px rgba(56, 189, 248, 0.4); border: 1.5px solid #dfb15b; margin-bottom: 20px;">
        <div style="font-family: 'Cinzel', serif; font-size: 32px; color: #dfb15b; margin-bottom: 12px; font-weight: 800;">¿CÓMO REALIZAR TU PEDIDO?</div>
        <p style="color: #e2e8f0; font-size: 16px; margin-bottom: 25px; line-height: 1.6;">Elegí tus fragancias favoritas y coordiná tu pedido directamente por WhatsApp.</p>
        
        <div style="background: rgba(0,0,0,0.55); border: 1px solid rgba(223, 177, 91, 0.35); border-radius: 12px; padding: 20px; margin-bottom: 25px; text-align: left;">
            <div style="font-size: 15px; color: #bae6fd; margin-bottom: 8px;">💳 <b>Medios de Pago:</b></div>
            <div style="color: #cbd5e1; font-size: 14px; margin-bottom: 14px;">• Efectivo / Transferencias (Mercado Pago, Cuenta DNI, Bancarias)</div>
            <div style="font-size: 15px; color: #ffe6a3; margin-bottom: 8px;">📦 <b>Entregas:</b></div>
            <div style="color: #cbd5e1; font-size: 14px;">• Puntos de encuentro y envíos a domicilio coordinados.</div>
        </div>

        <div style="font-family: 'Cinzel', serif; font-size: 22px; color: #fff; margin-bottom: 6px;">BJ BEAUTY • ALTA PERFUMERÍA</div>
        <div style="color: #38bdf8; font-size: 14px; letter-spacing: 2px;">INTENSIDAD • FIJACIÓN • DISTINCIÓN</div>
    </div>
</div>
'''

masc_html += '</body></html>'
masc_file = os.path.join(project_dir, 'catalogo_masculino.html')
with open(masc_file, 'w', encoding='utf-8') as f:
    f.write(masc_html)
print('Generated catalogo_masculino.html with 2-column layout.')


# =========================================================================
# 3. GENERACIÓN: CATÁLOGO ÁRABES (2 COLUMNAS)
# =========================================================================
arabes_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>BJ BEAUTY - Catálogo Perfumería Árabe</title>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Montserrat:wght@400;500;600;700&family=Playfair+Display:ital,wght@1,600;1,700&display=swap" rel="stylesheet">
<style>{CSS_COMMON}</style>
</head>
<body>
'''

# P1: PORTADA ÁRABES
arabes_html += f'''
<div class="page" style="background-image: linear-gradient(180deg, rgba(8,6,14,0.3) 0%, rgba(8,6,14,0.85) 60%, #050408 100%), url('fondo_arabes_dorado.jpg'); justify-content: center; align-items: center; text-align: center;">
    <div style="margin-top: 170px;">
        <img src="logo_bj_beauty.png" style="width: 215px; height: 215px; border-radius: 50%; box-shadow: 0 0 50px rgba(223, 177, 91, 0.65), 0 0 25px rgba(192, 132, 252, 0.5); border: 2px solid #dfb15b; margin-bottom: 25px;">
        <div style="font-family: 'Playfair Display', serif; font-style: italic; font-size: 34px; color: #ffe6a3; margin-bottom: 4px;">Edición de Lujo Oriental</div>
        <div style="font-family: 'Cinzel', serif; font-size: 46px; font-weight: 900; letter-spacing: 5px; color: #ffffff; text-shadow: 0 0 25px rgba(255,255,255,0.7);">PERFUMERÍA ÁRABE</div>
        <div style="font-size: 15px; letter-spacing: 4px; color: #dfb15b; text-transform: uppercase; font-weight: 600; margin-top: 6px;">Oud • Ámbar • Vainilla • Especias • Tendencias Virales</div>
        
        <div style="display: flex; justify-content: center; gap: 16px; margin-top: 35px;">
            <span style="background: rgba(15, 10, 25, 0.88); border: 1.5px solid #dfb15b; color: #ffe6a3; padding: 12px 26px; border-radius: 25px; font-weight: 800; font-size: 16px;">👑 PRECIO: {P_ARABIC} C/U</span>
            <span style="background: rgba(15, 10, 25, 0.88); border: 1.5px solid #c084fc; color: #e9d5ff; padding: 12px 26px; border-radius: 25px; font-weight: 700; font-size: 16px;">✨ Máxima Concentración & Estela</span>
        </div>
    </div>
</div>
'''

# P2: ÁRABES FEMENINAS (2 COLUMNAS)
arabes_html += f'''
<div class="page" style="background-image: url('fondo_arabes_dorado.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script-gold">Sensualidad & Opulencia</div>
        <div class="main-title">ÁRABES FEMENINAS</div>
        <div class="price-badge-pill">PRECIO: {P_ARABIC} • FRUTALES GOURMAND, DULCES & FLORALES</div>
    </div>
    {render_2cols(arabes_fem_full)}
    <div class="page-footer-num">BJ BEAUTY • Colección Árabe</div>
</div>
'''

# P3: ÁRABES MASCULINAS (I) (2 COLUMNAS)
arabes_html += f'''
<div class="page" style="background-image: url('fondo_arabes_noche.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script-gold">Poder & Misterio</div>
        <div class="main-title">ÁRABES MASCULINAS (I)</div>
        <div class="price-badge-pill">PRECIO: {P_ARABIC} • BEST SELLERS GLOBALES & VIRALES</div>
    </div>
    {render_2cols(arabes_masc_p1)}
    <div class="page-footer-num">BJ BEAUTY • Colección Árabe</div>
</div>
'''

# P4: ÁRABES MASCULINAS (II) (2 COLUMNAS)
arabes_html += f'''
<div class="page" style="background-image: url('fondo_arabes_vortice.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script-gold">Intensidad Oriental</div>
        <div class="main-title">ÁRABES MASCULINAS (II)</div>
        <div class="price-badge-pill">PRECIO: {P_ARABIC} • NOTAS DE OUD, CUERO & MADERAS</div>
    </div>
    {render_2cols(arabes_masc_p2)}
    <div class="page-footer-num">BJ BEAUTY • Colección Árabe</div>
</div>
'''

# P5: ÁRABES UNISEX (2 COLUMNAS)
arabes_html += f'''
<div class="page" style="background-image: url('fondo_arabes_cielo.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script-gold">Equilibrio & Alta Gama</div>
        <div class="main-title">ÁRABES UNISEX</div>
        <div class="price-badge-pill">PRECIO: {P_ARABIC} • ARMONÍAS COMPARTIDAS SIN GÉNERO</div>
    </div>
    {render_2cols(otros['arabes_unisex'])}
    <div class="page-footer-num">BJ BEAUTY • Colección Árabe</div>
</div>
'''

# CONTRATAPA ÁRABES
arabes_html += f'''
<div class="page" style="background-image: linear-gradient(rgba(8,6,14,0.9), rgba(8,6,14,0.95)), url('fondo_arabes_noche.jpg'); justify-content: center;">
    <div style="text-align: center; max-width: 680px; background: rgba(18, 14, 28, 0.88); border: 1.5px solid #dfb15b; border-radius: 20px; padding: 45px 35px; box-shadow: 0 12px 45px rgba(0,0,0,0.85);">
        <img src="logo_bj_beauty.png" style="width: 110px; height: 110px; border-radius: 50%; box-shadow: 0 0 25px rgba(223, 177, 91, 0.5); border: 1.5px solid #dfb15b; margin-bottom: 20px;">
        <div style="font-family: 'Cinzel', serif; font-size: 32px; color: #dfb15b; margin-bottom: 12px; font-weight: 800;">¿CÓMO PEDIR TUS ÁRABES?</div>
        <p style="color: #e2e8f0; font-size: 16px; margin-bottom: 25px; line-height: 1.6;">Elegí tus fragancias árabes favoritas y coordiná tu entrega directamente por WhatsApp.</p>
        
        <div style="background: rgba(0,0,0,0.55); border: 1px solid rgba(223, 177, 91, 0.35); border-radius: 12px; padding: 20px; margin-bottom: 25px; text-align: left;">
            <div style="font-size: 15px; color: #ffe6a3; margin-bottom: 8px;">💳 <b>Medios de Pago:</b></div>
            <div style="color: #cbd5e1; font-size: 14px; margin-bottom: 14px;">• Efectivo / Transferencias (Mercado Pago, Cuenta DNI, Bancarias)</div>
            <div style="font-size: 15px; color: #ffd1dc; margin-bottom: 8px;">📦 <b>Entregas:</b></div>
            <div style="color: #cbd5e1; font-size: 14px;">• Puntos de encuentro y envíos coordinados a todo el país.</div>
        </div>

        <div style="font-family: 'Cinzel', serif; font-size: 22px; color: #fff; margin-bottom: 6px;">BJ BEAUTY • COLECCIÓN ÁRABE DUBÁI</div>
        <div style="color: #dfb15b; font-size: 14px; letter-spacing: 2px;">OPULENCIA • ESTELA • MÁXIMA PERSISTENCIA</div>
    </div>
</div>
'''

arabes_html += '</body></html>'
arabes_file = os.path.join(project_dir, 'catalogo_arabes.html')
with open(arabes_file, 'w', encoding='utf-8') as f:
    f.write(arabes_html)
print('Generated catalogo_arabes.html with 2-column layout.')


# =========================================================================
# 4. GENERACIÓN: CATÁLOGO UNISEX & AUTOMOTOR (2 COLUMNAS)
# =========================================================================
esp_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>BJ BEAUTY - Unisex, Nicho & Automotor</title>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Montserrat:wght@400;500;600;700&family=Playfair+Display:ital,wght@1,600;1,700&display=swap" rel="stylesheet">
<style>{CSS_COMMON}</style>
</head>
<body>
'''

# P1: PORTADA
esp_html += f'''
<div class="page" style="background-image: linear-gradient(180deg, rgba(8,6,14,0.3) 0%, rgba(8,6,14,0.85) 65%, #050408 100%), url('banner_capsula_fusion.jpg'); justify-content: center; align-items: center; text-align: center;">
    <div style="margin-top: 170px;">
        <img src="logo_bj_beauty.png" style="width: 215px; height: 215px; border-radius: 50%; box-shadow: 0 0 50px rgba(223, 177, 91, 0.6), 0 0 25px rgba(192, 132, 252, 0.5); border: 2px solid #dfb15b; margin-bottom: 25px;">
        <div style="font-family: 'Playfair Display', serif; font-style: italic; font-size: 34px; color: #ffe6a3; margin-bottom: 4px;">Ediciones de Autor</div>
        <div style="font-family: 'Cinzel', serif; font-size: 42px; font-weight: 900; letter-spacing: 4px; color: #ffffff; text-shadow: 0 0 25px rgba(255,255,255,0.7);">UNISEX, NICHO & AUTOMÓVIL</div>
        <div style="font-size: 15px; letter-spacing: 4px; color: #dfb15b; text-transform: uppercase; font-weight: 600; margin-top: 6px;">Cápsula Fusión • Alta Gama Nicho • Aromas Textiles y Auto</div>
        
        <div style="display: flex; justify-content: center; gap: 16px; margin-top: 35px;">
            <span style="background: rgba(15, 10, 25, 0.88); border: 1.5px solid #dfb15b; color: #ffe6a3; padding: 10px 22px; border-radius: 25px; font-weight: 700; font-size: 15px;">💎 Fusión & Nicho: {P_ARABIC}</span>
            <span style="background: rgba(15, 10, 25, 0.88); border: 1.5px solid #c084fc; color: #e9d5ff; padding: 10px 22px; border-radius: 25px; font-weight: 700; font-size: 15px;">🚗 Combo Auto: {P_AUTO} (Promo: {P_AUTO_PROMO})</span>
        </div>
    </div>
</div>
'''

# P2: CÁPSULA FUSIÓN (2 COLUMNAS)
esp_html += f'''
<div class="page" style="background-image: linear-gradient(rgba(10,12,18,0.55), rgba(10,12,18,0.8)), url('banner_capsula_fusion.jpg'); justify-content: space-between;">
    <div class="title-container" style="margin-top: 10px;">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script sub-script-gold">Edición Exclusiva</div>
        <div class="main-title">CÁPSULA FUSIÓN</div>
        <div class="price-badge-pill">PRECIO: {P_ARABIC} C/U • DOS ESENCIAS, UN NUEVO LEGADO</div>
    </div>
    {render_2cols(otros['fusion'])}
    <div class="page-footer-num">BJ BEAUTY • Líneas Especiales</div>
</div>
'''

# P3: UNISEX & NICHO (2 COLUMNAS)
esp_html += f'''
<div class="page" style="background-image: url('fondo_unisex_atardecer.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script sub-script-gold">Línea Exclusiva</div>
        <div class="main-title">UNISEX & NICHO</div>
        <div class="price-badge-pill">60 ML • {P_CLASSIC} / {P_ARABIC} • NOTAS DE AUTOR</div>
    </div>
    {render_2cols(otros['unisex'])}
    <div class="page-footer-num">BJ BEAUTY • Líneas Especiales</div>
</div>
'''

# P4: LÍNEA AUTOMÓVIL (FICHA OFICIAL DE DIFUSORES CON LOGO Y PRECIO DE COMBO)
esp_html += f'''
<div class="page" style="padding: 0; justify-content: center; background: #000;">
    <img src="linea_auto_bj_beauty.jpg" style="width: 100%; height: 100%; object-fit: contain;">
    <div class="page-footer-num">BJ BEAUTY • Línea Automotor</div>
</div>
'''

# P5: CONTRATAPA UNISEX & AUTOMOTOR
esp_html += f'''
<div class="page" style="background-image: linear-gradient(rgba(8,6,14,0.9), rgba(8,6,14,0.95)), url('fondo_unisex_atardecer.jpg'); justify-content: center;">
    <div style="text-align: center; max-width: 680px; background: rgba(18, 14, 28, 0.88); border: 1.5px solid #dfb15b; border-radius: 20px; padding: 45px 35px; box-shadow: 0 12px 45px rgba(0,0,0,0.85);">
        <img src="logo_bj_beauty.png" style="width: 110px; height: 110px; border-radius: 50%; box-shadow: 0 0 25px rgba(223, 177, 91, 0.4); border: 1.5px solid #dfb15b; margin-bottom: 20px;">
        <div style="font-family: 'Cinzel', serif; font-size: 32px; color: #dfb15b; margin-bottom: 12px; font-weight: 800;">¿CÓMO REALIZAR TU PEDIDO?</div>
        <p style="color: #e2e8f0; font-size: 16px; margin-bottom: 25px; line-height: 1.6;">Elegí tus fragancias o combos de auto favoritos y contactanos por WhatsApp.</p>
        
        <div style="background: rgba(0,0,0,0.55); border: 1px solid rgba(223, 177, 91, 0.35); border-radius: 12px; padding: 20px; margin-bottom: 25px; text-align: left;">
            <div style="font-size: 15px; color: #ffd1dc; margin-bottom: 8px;">💳 <b>Medios de Pago:</b></div>
            <div style="color: #cbd5e1; font-size: 14px; margin-bottom: 14px;">• Efectivo / Transferencias (Mercado Pago, Cuenta DNI, Bancarias)</div>
            <div style="font-size: 15px; color: #ffe6a3; margin-bottom: 8px;">📦 <b>Entregas:</b></div>
            <div style="color: #cbd5e1; font-size: 14px;">• Puntos de encuentro y envíos a domicilio coordinados.</div>
        </div>

        <div style="font-family: 'Cinzel', serif; font-size: 22px; color: #fff; margin-bottom: 6px;">BJ BEAUTY • AROMAS & EXCLUSIVIDAD</div>
        <div style="color: #dfb15b; font-size: 14px; letter-spacing: 2px;">CÁPSULA FUSIÓN • NICHO • AUTOMOTOR</div>
    </div>
</div>
'''

esp_html += '</body></html>'
esp_file = os.path.join(project_dir, 'catalogo_unisex_y_automotor.html')
with open(esp_file, 'w', encoding='utf-8') as f:
    f.write(esp_html)
print('Generated catalogo_unisex_y_automotor.html with 2-column layout.')


# =========================================================================
# COMPILACIÓN: PDFS EN CARPETA EXCLUSIVA /PDFs/ Y PÁGINAS INDIVIDUALES
# =========================================================================
catalog_jobs = [
    ('catalogo_femenino.html', 'Catalogo_BJ_Beauty_Femenino.pdf', 'Femenino', 'preview_catalogo_femenino.jpg'),
    ('catalogo_masculino.html', 'Catalogo_BJ_Beauty_Masculino.pdf', 'Masculino', 'preview_catalogo_masculino.jpg'),
    ('catalogo_arabes.html', 'Catalogo_BJ_Beauty_Arabes.pdf', 'Arabes', 'preview_catalogo_arabes.jpg'),
    ('catalogo_unisex_y_automotor.html', 'Catalogo_BJ_Beauty_Unisex_y_Automotor.pdf', 'Unisex_Auto', 'preview_catalogo_unisex_auto.jpg')
]

print('\nStarting Playwright compilation of 4 PDFs and individual pages...')
with sync_playwright() as p:
    browser = p.chromium.launch()
    for html_name, pdf_name, prefix, preview_name in catalog_jobs:
        html_path = os.path.join(project_dir, html_name)
        pdf_path = os.path.join(pdf_dir, pdf_name)
        
        page = browser.new_page(viewport={"width": 860, "height": 1216})
        page.goto('file:///' + html_path.replace('\\\\', '/'), wait_until='networkidle')
        
        # 1. Guardar preview de la portada en project_dir
        page.screenshot(path=os.path.join(project_dir, preview_name), clip={"x": 0, "y": 0, "width": 860, "height": 1216})
        
        # 2. Generar PDF completo en la carpeta exclusiva /PDFs/
        page.pdf(
            path=pdf_path,
            width='860px',
            height='1216px',
            print_background=True,
            margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
        )
        print(f'-> Saved PDF in /PDFs/{pdf_name}')
        
        # 3. Exportar cada página como imagen individual en /paginas_individuales/
        pages = page.query_selector_all('.page')
        print(f'   Exporting {len(pages)} individual pages for {prefix}...')
        for p_idx, p_elem in enumerate(pages):
            out_img = os.path.join(indiv_dir, f'{prefix}_Pagina_{p_idx+1:02d}.jpg')
            p_elem.screenshot(path=out_img, quality=92, type='jpeg')
        
        browser.close()
        browser = p.chromium.launch()

    browser.close()

print('\nALL 4 PDFS AND INDIVIDUAL PAGES GENERATED SUCCESSFULLY!')
