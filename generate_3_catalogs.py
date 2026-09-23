import json
import os
import math
from playwright.sync_api import sync_playwright

output_dir = os.path.abspath(r'C:\Users\soyto.JOAQUIN2206\OneDrive\Desktop\Proyectos\perfumes-gestion')

with open(os.path.join(output_dir, 'fem.json'), encoding='utf-8') as f:
    fem = json.load(f)
with open(os.path.join(output_dir, 'masc.json'), encoding='utf-8') as f:
    masc = json.load(f)
with open(os.path.join(output_dir, 'otros.json'), encoding='utf-8') as f:
    otros = json.load(f)

P_CLASSIC = "$22.000"
P_CLASSIC_PROMO = "2 x $40.000"
P_ARABIC = "$24.000"
P_AUTO = "$11.000"
P_AUTO_PROMO = "2 COMBOS x $20.000"

def render_list(items):
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
        lines.append(f'<div class="item-row"><span class="item-name">{name}</span><span class="item-brand">{brand}</span></div>')
    return "".join(lines)

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
    padding: 38px 36px 36px 36px;
    overflow: hidden;
}
.title-container {
    text-align: center;
    margin-bottom: 12px;
}
.sub-script {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 30px;
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
    font-size: 42px;
    font-weight: 800;
    letter-spacing: 3px;
    color: #ffffff;
    text-transform: uppercase;
    text-shadow: 0 0 16px rgba(255, 255, 255, 0.7), 2px 3px 8px rgba(0,0,0,0.95);
}
.price-badge-pill {
    display: inline-block;
    background: rgba(10, 10, 15, 0.88);
    border: 1px solid #dfb15b;
    color: #ffe8b2;
    padding: 5px 18px;
    border-radius: 20px;
    font-size: 13.5px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-top: 6px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.6);
}
.fragrance-list-card {
    width: 100%;
    flex: 1;
    background: rgba(10, 12, 18, 0.82);
    backdrop-filter: blur(5px);
    border: 1px solid rgba(223, 177, 91, 0.35);
    border-radius: 14px;
    padding: 16px 24px;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    box-shadow: 0 8px 30px rgba(0,0,0,0.7);
}
.item-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 3.5px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.item-row:last-child {
    border-bottom: none;
}
.item-name {
    font-family: 'Montserrat', sans-serif;
    font-weight: 700;
    font-size: 16.5px;
    color: #ffffff;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.9);
}
.item-brand {
    font-family: 'Montserrat', sans-serif;
    font-weight: 500;
    font-size: 13.5px;
    color: #e5b966;
    text-align: right;
    margin-left: 12px;
}
.page-footer-num {
    position: absolute;
    bottom: 12px;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.5);
    letter-spacing: 1px;
}
.header-brand-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
}
.header-brand-logo img {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    border: 1.5px solid #dfb15b;
    box-shadow: 0 0 12px rgba(192, 132, 252, 0.4);
}
.header-brand-name {
    font-family: 'Cinzel', serif;
    font-size: 20px;
    font-weight: 800;
    color: #dfb15b;
    letter-spacing: 3px;
}
'''

# =========================================================================
# 1. CATÁLOGO FEMENINO
# =========================================================================
fem_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>BJ BEAUTY - Catálogo Femenino 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Montserrat:wght@400;500;600;700&family=Playfair+Display:ital,wght@1,600;1,700&display=swap" rel="stylesheet">
<style>
{CSS_COMMON}
</style>
</head>
<body>
'''

p_fem = 1

# PORTADA FEMENINA
fem_html += f'''
<div class="page" style="background-image: linear-gradient(180deg, rgba(8,6,14,0.4) 0%, rgba(8,6,14,0.85) 65%, #050408 100%), url('fondo_femeninas_rosas.jpg'); justify-content: center; align-items: center; text-align: center;">
    <div style="margin-top: 180px;">
        <img src="logo_bj_beauty.png" style="width: 210px; height: 210px; border-radius: 50%; box-shadow: 0 0 45px rgba(192, 132, 252, 0.55), 0 0 25px rgba(223, 177, 91, 0.5); border: 2px solid #dfb15b; margin-bottom: 25px;">
        <div style="font-family: 'Playfair Display', serif; font-style: italic; font-size: 32px; color: #ffd1dc; margin-bottom: 4px;">Colección Exclusiva</div>
        <div style="font-family: 'Cinzel', serif; font-size: 48px; font-weight: 900; letter-spacing: 5px; color: #ffffff; text-shadow: 0 0 25px rgba(255,255,255,0.7);">CATÁLOGO FEMENINO</div>
        <div style="font-size: 15px; letter-spacing: 4px; color: #c084fc; text-transform: uppercase; font-weight: 600; margin-top: 6px;">Alta Perfumería • Fragancias Árabes • Tendencias Virales</div>
        
        <div style="display: flex; justify-content: center; gap: 16px; margin-top: 35px;">
            <span style="background: rgba(15, 10, 25, 0.85); border: 1.5px solid #dfb15b; color: #ffe6a3; padding: 10px 22px; border-radius: 25px; font-weight: 700; font-size: 15px; box-shadow: 0 6px 20px rgba(0,0,0,0.6);">✨ 60ml: {P_CLASSIC} (Promo: {P_CLASSIC_PROMO})</span>
            <span style="background: rgba(15, 10, 25, 0.85); border: 1.5px solid #c084fc; color: #e9d5ff; padding: 10px 22px; border-radius: 25px; font-weight: 700; font-size: 15px; box-shadow: 0 6px 20px rgba(0,0,0,0.6);">👑 Árabes de Lujo: {P_ARABIC}</span>
        </div>
    </div>
</div>
'''
p_fem += 1

# NUEVOS INGRESOS FEM
fem_html += f'''
<div class="page" style="background-image: url('fondo_nuevos_ingresos_fem.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script">Tendencias 2026</div>
        <div class="main-title">NUEVOS INGRESOS</div>
        <div class="price-badge-pill">ÚLTIMOS LANZAMIENTOS • {P_CLASSIC} / {P_ARABIC}</div>
    </div>
    <div class="fragrance-list-card" style="max-height: 480px; margin-top: 250px;">
        {render_list(otros.get('nuevos_fem', []))}
    </div>
    <div class="page-footer-num">Página {p_fem}</div>
</div>
'''
p_fem += 1

# ÁRABES FEMENINAS
fem_html += f'''
<div class="page" style="background-image: url('fondo_arabes_dorado.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script sub-script-gold">Perfumería Oriental</div>
        <div class="main-title">ÁRABES FEMENINAS</div>
        <div class="price-badge-pill">PRECIO: {P_ARABIC} C/U • ALTA FIJACIÓN & ESTELA</div>
    </div>
    <div class="fragrance-list-card">
        {render_list(otros['arabes_fem'])}
    </div>
    <div class="page-footer-num">Página {p_fem}</div>
</div>
'''
p_fem += 1

# FEMENINAS CLASICAS (10 páginas)
fem_per_page = math.ceil(len(fem) / 10)
fem_chunks = [fem[i:i + fem_per_page] for i in range(0, len(fem), fem_per_page)]

for idx, chunk in enumerate(fem_chunks):
    bg = 'fondo_femeninas_rosas.jpg' if idx % 2 == 0 else 'fondo_femeninas_orquideas.jpg'
    fem_html += f'''
    <div class="page" style="background-image: url('{bg}'); justify-content: space-between;">
        <div class="title-container">
            <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
            <div class="sub-script">Colección Clásica</div>
            <div class="main-title">FEMENINAS (Parte {idx+1})</div>
            <div class="price-badge-pill">60 ML • {P_CLASSIC} • PROMO: {P_CLASSIC_PROMO}</div>
        </div>
        <div class="fragrance-list-card">
            {render_list(chunk)}
        </div>
        <div class="page-footer-num">Página {p_fem}</div>
    </div>
    '''
    p_fem += 1

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
    <div class="page-footer-num">Página {p_fem}</div>
</div>
'''

fem_html += '</body></html>'
with open(os.path.join(output_dir, 'catalogo_femenino.html'), 'w', encoding='utf-8') as f:
    f.write(fem_html)
print(f'Created catalogo_femenino.html ({p_fem} pages)')


# =========================================================================
# 2. CATÁLOGO MASCULINO
# =========================================================================
masc_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>BJ BEAUTY - Catálogo Masculino 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Montserrat:wght@400;500;600;700&family=Playfair+Display:ital,wght@1,600;1,700&display=swap" rel="stylesheet">
<style>
{CSS_COMMON}
</style>
</head>
<body>
'''

p_masc = 1

# PORTADA MASCULINA
masc_html += f'''
<div class="page" style="background-image: linear-gradient(180deg, rgba(6,8,16,0.35) 0%, rgba(6,8,16,0.85) 65%, #04060c 100%), url('fondo_masculinas_seda_azul.jpg'); justify-content: center; align-items: center; text-align: center;">
    <div style="margin-top: 180px;">
        <img src="logo_bj_beauty.png" style="width: 210px; height: 210px; border-radius: 50%; box-shadow: 0 0 45px rgba(56, 189, 248, 0.45), 0 0 25px rgba(223, 177, 91, 0.5); border: 2px solid #dfb15b; margin-bottom: 25px;">
        <div style="font-family: 'Playfair Display', serif; font-style: italic; font-size: 32px; color: #cce4ff; margin-bottom: 4px;">Colección Exclusiva</div>
        <div style="font-family: 'Cinzel', serif; font-size: 48px; font-weight: 900; letter-spacing: 5px; color: #ffffff; text-shadow: 0 0 25px rgba(255,255,255,0.7);">CATÁLOGO MASCULINO</div>
        <div style="font-size: 15px; letter-spacing: 4px; color: #38bdf8; text-transform: uppercase; font-weight: 600; margin-top: 6px;">Alta Perfumería • Perfumería Árabe • Distinción & Carácter</div>
        
        <div style="display: flex; justify-content: center; gap: 16px; margin-top: 35px;">
            <span style="background: rgba(10, 15, 28, 0.85); border: 1.5px solid #dfb15b; color: #ffe6a3; padding: 10px 22px; border-radius: 25px; font-weight: 700; font-size: 15px; box-shadow: 0 6px 20px rgba(0,0,0,0.6);">✨ 60ml: {P_CLASSIC} (Promo: {P_CLASSIC_PROMO})</span>
            <span style="background: rgba(10, 15, 28, 0.85); border: 1.5px solid #38bdf8; color: #bae6fd; padding: 10px 22px; border-radius: 25px; font-weight: 700; font-size: 15px; box-shadow: 0 6px 20px rgba(0,0,0,0.6);">👑 Árabes de Lujo: {P_ARABIC}</span>
        </div>
    </div>
</div>
'''
p_masc += 1

# NUEVOS INGRESOS MASC
masc_html += f'''
<div class="page" style="background-image: url('fondo_nuevos_ingresos_masc.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script sub-script-masc">Tendencias 2026</div>
        <div class="main-title">NUEVOS INGRESOS</div>
        <div class="price-badge-pill">ÚLTIMOS LANZAMIENTOS • {P_CLASSIC} / {P_ARABIC}</div>
    </div>
    <div class="fragrance-list-card" style="max-height: 520px; margin-top: 220px;">
        {render_list(otros.get('nuevos_masc', []))}
    </div>
    <div class="page-footer-num">Página {p_masc}</div>
</div>
'''
p_masc += 1

# ÁRABES MASCULINAS (Parte I y II)
arabes_masc_p1 = otros['arabes_masc'][:19]
arabes_masc_p2 = otros['arabes_masc'][19:]

masc_html += f'''
<div class="page" style="background-image: url('fondo_arabes_noche.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script sub-script-gold">Perfumería Oriental</div>
        <div class="main-title">ÁRABES MASCULINAS (I)</div>
        <div class="price-badge-pill">PRECIO: {P_ARABIC} C/U • NOTAS DE OUD, ÁMBAR Y CUERO</div>
    </div>
    <div class="fragrance-list-card">
        {render_list(arabes_masc_p1)}
    </div>
    <div class="page-footer-num">Página {p_masc}</div>
</div>
'''
p_masc += 1

masc_html += f'''
<div class="page" style="background-image: url('fondo_arabes_vortice.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script sub-script-gold">Perfumería Oriental</div>
        <div class="main-title">ÁRABES MASCULINAS (II)</div>
        <div class="price-badge-pill">PRECIO: {P_ARABIC} C/U • MÁXIMA INTENSIDAD</div>
    </div>
    <div class="fragrance-list-card">
        {render_list(arabes_masc_p2)}
    </div>
    <div class="page-footer-num">Página {p_masc}</div>
</div>
'''
p_masc += 1

# MASCULINAS CLASICAS (9 páginas)
masc_per_page = math.ceil(len(masc) / 9)
masc_chunks = [masc[i:i + masc_per_page] for i in range(0, len(masc), masc_per_page)]

for idx, chunk in enumerate(masc_chunks):
    bg = 'fondo_masculinas_seda_azul.jpg' if idx % 2 == 0 else 'fondo_masculinas_estrellas.jpg'
    masc_html += f'''
    <div class="page" style="background-image: url('{bg}'); justify-content: space-between;">
        <div class="title-container">
            <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
            <div class="sub-script sub-script-masc">Colección Clásica</div>
            <div class="main-title">MASCULINAS (Parte {idx+1})</div>
            <div class="price-badge-pill">60 ML • {P_CLASSIC} • PROMO: {P_CLASSIC_PROMO}</div>
        </div>
        <div class="fragrance-list-card">
            {render_list(chunk)}
        </div>
        <div class="page-footer-num">Página {p_masc}</div>
    </div>
    '''
    p_masc += 1

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
    <div class="page-footer-num">Página {p_masc}</div>
</div>
'''

masc_html += '</body></html>'
with open(os.path.join(output_dir, 'catalogo_masculino.html'), 'w', encoding='utf-8') as f:
    f.write(masc_html)
print(f'Created catalogo_masculino.html ({p_masc} pages)')


# =========================================================================
# 3. CATÁLOGO UNISEX, NICHO & AUTOMOTOR
# =========================================================================
esp_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>BJ BEAUTY - Líneas Especiales, Unisex & Automotor 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Montserrat:wght@400;500;600;700&family=Playfair+Display:ital,wght@1,600;1,700&display=swap" rel="stylesheet">
<style>
{CSS_COMMON}
</style>
</head>
<body>
'''

p_esp = 1

# PORTADA LÍNEAS ESPECIALES
esp_html += f'''
<div class="page" style="background-image: linear-gradient(180deg, rgba(8,6,14,0.3) 0%, rgba(8,6,14,0.85) 65%, #050408 100%), url('banner_capsula_fusion.jpg'); justify-content: center; align-items: center; text-align: center;">
    <div style="margin-top: 180px;">
        <img src="logo_bj_beauty.png" style="width: 210px; height: 210px; border-radius: 50%; box-shadow: 0 0 45px rgba(223, 177, 91, 0.6), 0 0 25px rgba(192, 132, 252, 0.5); border: 2px solid #dfb15b; margin-bottom: 25px;">
        <div style="font-family: 'Playfair Display', serif; font-style: italic; font-size: 32px; color: #ffe6a3; margin-bottom: 4px;">Ediciones de Autor</div>
        <div style="font-family: 'Cinzel', serif; font-size: 44px; font-weight: 900; letter-spacing: 4px; color: #ffffff; text-shadow: 0 0 25px rgba(255,255,255,0.7);">UNISEX, NICHO & AUTOMÓVIL</div>
        <div style="font-size: 15px; letter-spacing: 4px; color: #dfb15b; text-transform: uppercase; font-weight: 600; margin-top: 6px;">Cápsula Fusión • Alta Gama Nicho • Aromas Textiles y Auto</div>
        
        <div style="display: flex; justify-content: center; gap: 16px; margin-top: 35px;">
            <span style="background: rgba(15, 10, 25, 0.85); border: 1.5px solid #dfb15b; color: #ffe6a3; padding: 10px 22px; border-radius: 25px; font-weight: 700; font-size: 15px; box-shadow: 0 6px 20px rgba(0,0,0,0.6);">💎 Fusión & Nicho: {P_ARABIC}</span>
            <span style="background: rgba(15, 10, 25, 0.85); border: 1.5px solid #c084fc; color: #e9d5ff; padding: 10px 22px; border-radius: 25px; font-weight: 700; font-size: 15px; box-shadow: 0 6px 20px rgba(0,0,0,0.6);">🚗 Combo Auto: {P_AUTO} (Promo: {P_AUTO_PROMO})</span>
        </div>
    </div>
</div>
'''
p_esp += 1

# CÁPSULA FUSIÓN
esp_html += f'''
<div class="page" style="background-image: linear-gradient(rgba(10,12,18,0.55), rgba(10,12,18,0.8)), url('banner_capsula_fusion.jpg'); justify-content: space-between;">
    <div class="title-container" style="margin-top: 10px;">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script sub-script-gold">Edición Exclusiva</div>
        <div class="main-title">CÁPSULA FUSIÓN</div>
        <div class="price-badge-pill">PRECIO: {P_ARABIC} C/U • DOS ESENCIAS, UN NUEVO LEGADO</div>
    </div>
    <div class="fragrance-list-card" style="max-height: 460px; margin-top: 250px;">
        {render_list(otros['fusion'])}
    </div>
    <div class="page-footer-num">Página {p_esp}</div>
</div>
'''
p_esp += 1

# ÁRABES UNISEX
esp_html += f'''
<div class="page" style="background-image: url('fondo_arabes_cielo.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script sub-script-gold">Perfumería Oriental</div>
        <div class="main-title">ÁRABES UNISEX</div>
        <div class="price-badge-pill">PRECIO: {P_ARABIC} C/U • ARMONÍAS COMPARTIDAS</div>
    </div>
    <div class="fragrance-list-card" style="max-height: 650px;">
        {render_list(otros['arabes_unisex'])}
    </div>
    <div class="page-footer-num">Página {p_esp}</div>
</div>
'''
p_esp += 1

# UNISEX & NICHO
esp_html += f'''
<div class="page" style="background-image: url('fondo_unisex_atardecer.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script sub-script-gold">Línea Exclusiva</div>
        <div class="main-title">UNISEX & NICHO</div>
        <div class="price-badge-pill">60 ML • {P_CLASSIC} / {P_ARABIC} • NOTAS DE AUTOR</div>
    </div>
    <div class="fragrance-list-card">
        {render_list(otros['unisex'])}
    </div>
    <div class="page-footer-num">Página {p_esp}</div>
</div>
'''
p_esp += 1

# LÍNEA AUTOMÓVIL OFICIAL (IMAGEN NUEVA COMPOSICION CON LOGO BJ BEAUTY Y PRECIOS)
esp_html += f'''
<div class="page" style="padding: 0; justify-content: center; background: #000;">
    <img src="linea_auto_bj_beauty.jpg" style="width: 100%; height: 100%; object-fit: contain;">
    <div class="page-footer-num">Página {p_esp}</div>
</div>
'''
p_esp += 1

# CONTRATAPA LÍNEAS ESPECIALES
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
    <div class="page-footer-num">Página {p_esp}</div>
</div>
'''

esp_html += '</body></html>'
with open(os.path.join(output_dir, 'catalogo_unisex_y_automotor.html'), 'w', encoding='utf-8') as f:
    f.write(esp_html)
print(f'Created catalogo_unisex_y_automotor.html ({p_esp} pages)')

# =========================================================================
# COMPILACIÓN DE LOS 3 PDFS CON PLAYWRIGHT
# =========================================================================
catalogs = [
    ('catalogo_femenino.html', 'Catalogo_BJ_Beauty_Femenino.pdf', 'preview_catalogo_femenino.jpg'),
    ('catalogo_masculino.html', 'Catalogo_BJ_Beauty_Masculino.pdf', 'preview_catalogo_masculino.jpg'),
    ('catalogo_unisex_y_automotor.html', 'Catalogo_BJ_Beauty_Unisex_y_Automotor.pdf', 'preview_catalogo_unisex_auto.jpg')
]

print('\nStarting Playwright PDF generation...')
with sync_playwright() as p:
    browser = p.chromium.launch()
    for html_file, pdf_file, preview_img in catalogs:
        print(f'Rendering {pdf_file}...')
        page = browser.new_page(viewport={"width": 860, "height": 1216})
        file_path = os.path.join(output_dir, html_file)
        page.goto('file:///' + file_path.replace('\\\\', '/'), wait_until='networkidle')
        
        # Guardar preview de la portada
        page.screenshot(path=os.path.join(output_dir, preview_img), clip={"x": 0, "y": 0, "width": 860, "height": 1216})
        
        # Generar PDF completo
        page.pdf(
            path=os.path.join(output_dir, pdf_file),
            width='860px',
            height='1216px',
            print_background=True,
            margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
        )
        print(f'Successfully generated: {pdf_file}')
    browser.close()

print('\nALL 3 CATALOGS HAVE BEEN COMPILED SUCCESSFULLY!')
