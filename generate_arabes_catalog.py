import json
import os
from playwright.sync_api import sync_playwright

output_dir = os.path.abspath(r'C:\Users\soyto.JOAQUIN2206\OneDrive\Desktop\Proyectos\perfumes-gestion')

with open(os.path.join(output_dir, 'otros.json'), encoding='utf-8') as f:
    otros = json.load(f)

P_ARABIC = "$24.000"

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

CSS = '''
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
    padding: 40px 36px 36px 36px;
    overflow: hidden;
}
.title-container {
    text-align: center;
    margin-bottom: 14px;
}
.sub-script-gold {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 32px;
    color: #ffe6a3;
    text-shadow: 0 0 12px rgba(223, 177, 91, 0.8), 2px 2px 5px rgba(0,0,0,0.95);
    margin-bottom: -6px;
}
.main-title {
    font-family: 'Cinzel', serif;
    font-size: 42px;
    font-weight: 800;
    letter-spacing: 3px;
    color: #ffffff;
    text-transform: uppercase;
    text-shadow: 0 0 18px rgba(255, 255, 255, 0.7), 2px 3px 8px rgba(0,0,0,0.95);
}
.price-badge-pill {
    display: inline-block;
    background: rgba(10, 8, 16, 0.92);
    border: 1.5px solid #dfb15b;
    color: #ffe8b2;
    padding: 6px 20px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-top: 6px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.7);
}
.fragrance-list-card {
    width: 100%;
    flex: 1;
    background: rgba(10, 8, 18, 0.82);
    backdrop-filter: blur(6px);
    border: 1px solid rgba(223, 177, 91, 0.4);
    border-radius: 16px;
    padding: 18px 26px;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    box-shadow: 0 10px 35px rgba(0,0,0,0.75);
}
.item-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 4px 0;
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
    font-size: 14px;
    color: #dfb15b;
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
    box-shadow: 0 0 14px rgba(223, 177, 91, 0.5);
}
.header-brand-name {
    font-family: 'Cinzel', serif;
    font-size: 20px;
    font-weight: 800;
    color: #dfb15b;
    letter-spacing: 3px;
}
'''

html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>BJ BEAUTY - Catálogo Exclusivo de Fragancias Árabes 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Montserrat:wght@400;500;600;700&family=Playfair+Display:ital,wght@1,600;1,700&display=swap" rel="stylesheet">
<style>
{CSS}
</style>
</head>
<body>
'''

p_num = 1

# PÁGINA 1: PORTADA ÁRABE
html += f'''
<div class="page" style="background-image: linear-gradient(180deg, rgba(8,6,14,0.3) 0%, rgba(8,6,14,0.85) 60%, #050408 100%), url('fondo_arabes_dorado.jpg'); justify-content: center; align-items: center; text-align: center;">
    <div style="margin-top: 170px;">
        <img src="logo_bj_beauty.png" style="width: 215px; height: 215px; border-radius: 50%; box-shadow: 0 0 50px rgba(223, 177, 91, 0.65), 0 0 25px rgba(192, 132, 252, 0.5); border: 2px solid #dfb15b; margin-bottom: 25px;">
        <div style="font-family: 'Playfair Display', serif; font-style: italic; font-size: 34px; color: #ffe6a3; margin-bottom: 4px;">Edición de Lujo Oriental</div>
        <div style="font-family: 'Cinzel', serif; font-size: 46px; font-weight: 900; letter-spacing: 5px; color: #ffffff; text-shadow: 0 0 25px rgba(255,255,255,0.7);">PERFUMERÍA ÁRABE</div>
        <div style="font-size: 15px; letter-spacing: 4px; color: #dfb15b; text-transform: uppercase; font-weight: 600; margin-top: 6px;">Oud • Ámbar • Vainilla • Especias • Tendencias Virales</div>
        
        <div style="display: flex; justify-content: center; gap: 16px; margin-top: 35px;">
            <span style="background: rgba(15, 10, 25, 0.88); border: 1.5px solid #dfb15b; color: #ffe6a3; padding: 12px 26px; border-radius: 25px; font-weight: 800; font-size: 16px; box-shadow: 0 6px 20px rgba(0,0,0,0.7);">👑 PRECIO OFICIAL: {P_ARABIC} C/U</span>
            <span style="background: rgba(15, 10, 25, 0.88); border: 1.5px solid #c084fc; color: #e9d5ff; padding: 12px 26px; border-radius: 25px; font-weight: 700; font-size: 16px; box-shadow: 0 6px 20px rgba(0,0,0,0.7);">✨ Máxima Concentración & Estela</span>
        </div>
    </div>
</div>
'''
p_num += 1

# PÁGINA 2: ÁRABES FEMENINAS
# Agregamos Victoria de nuevos_fem si no está
arabes_fem_full = list(otros['arabes_fem'])
if ('Victoria', 'Lattafa') not in arabes_fem_full:
    arabes_fem_full.append(('Victoria', 'Lattafa (Nuevo)'))

html += f'''
<div class="page" style="background-image: url('fondo_arabes_dorado.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script-gold">Sensualidad & Opulencia</div>
        <div class="main-title">ÁRABES FEMENINAS</div>
        <div class="price-badge-pill">PRECIO: {P_ARABIC} • FRUTALES GOURMAND, DULCES & FLORALES</div>
    </div>
    <div class="fragrance-list-card">
        {render_list(arabes_fem_full)}
    </div>
    <div class="page-footer-num">Página {p_num}</div>
</div>
'''
p_num += 1

# PÁGINA 3: ÁRABES MASCULINAS (I)
arabes_masc_total = list(otros['arabes_masc'])
# Agregamos los nuevos masculinos árabes de otros['nuevos_masc'] que no estén
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

half = (len(arabes_masc_total) + 1) // 2
arabes_masc_p1 = arabes_masc_total[:half]
arabes_masc_p2 = arabes_masc_total[half:]

html += f'''
<div class="page" style="background-image: url('fondo_arabes_noche.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script-gold">Poder & Misterio</div>
        <div class="main-title">ÁRABES MASCULINAS (I)</div>
        <div class="price-badge-pill">PRECIO: {P_ARABIC} • BEST SELLERS GLOBALES & TENDENCIAS</div>
    </div>
    <div class="fragrance-list-card">
        {render_list(arabes_masc_p1)}
    </div>
    <div class="page-footer-num">Página {p_num}</div>
</div>
'''
p_num += 1

# PÁGINA 4: ÁRABES MASCULINAS (II)
html += f'''
<div class="page" style="background-image: url('fondo_arabes_vortice.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script-gold">Intensidad Oriental</div>
        <div class="main-title">ÁRABES MASCULINAS (II)</div>
        <div class="price-badge-pill">PRECIO: {P_ARABIC} • NOTAS DE OUD, CUERO & MADERAS NOBLES</div>
    </div>
    <div class="fragrance-list-card">
        {render_list(arabes_masc_p2)}
    </div>
    <div class="page-footer-num">Página {p_num}</div>
</div>
'''
p_num += 1

# PÁGINA 5: ÁRABES UNISEX
html += f'''
<div class="page" style="background-image: url('fondo_arabes_cielo.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="header-brand-logo"><img src="logo_bj_beauty.png"><span class="header-brand-name">BJ BEAUTY</span></div>
        <div class="sub-script-gold">Equilibrio & Alta Gama</div>
        <div class="main-title">ÁRABES UNISEX</div>
        <div class="price-badge-pill">PRECIO: {P_ARABIC} • ARMONÍAS COMPARTIDAS SIN GÉNERO</div>
    </div>
    <div class="fragrance-list-card" style="max-height: 720px; margin-top: 160px;">
        {render_list(otros['arabes_unisex'])}
    </div>
    <div class="page-footer-num">Página {p_num}</div>
</div>
'''
p_num += 1

# PÁGINA 6: CONTRATAPA ÁRABE
html += f'''
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
    <div class="page-footer-num">Página {p_num}</div>
</div>
'''

html += '</body></html>'

html_file = os.path.join(output_dir, 'catalogo_arabes.html')
pdf_file = os.path.join(output_dir, 'Catalogo_BJ_Beauty_Arabes.pdf')
preview_file = os.path.join(output_dir, 'preview_catalogo_arabes.jpg')

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Created catalogo_arabes.html ({p_num} pages)')

print('Rendering Catalogo_BJ_Beauty_Arabes.pdf with Playwright...')
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 860, "height": 1216})
    page.goto('file:///' + html_file.replace('\\\\', '/'), wait_until='networkidle')
    page.screenshot(path=preview_file, clip={"x": 0, "y": 0, "width": 860, "height": 1216})
    page.pdf(
        path=pdf_file,
        width='860px',
        height='1216px',
        print_background=True,
        margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
    )
    browser.close()

print(f'Successfully created {pdf_file}!')
