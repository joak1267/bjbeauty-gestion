import json
import os
import math

with open('fem.json', encoding='utf-8') as f:
    fem = json.load(f)
with open('masc.json', encoding='utf-8') as f:
    masc = json.load(f)
with open('otros.json', encoding='utf-8') as f:
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

html = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Catalogo Oficial de Fragancias 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Montserrat:wght@400;500;600;700&family=Playfair+Display:ital,wght@1,600&display=swap" rel="stylesheet">
<style>
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
    padding: 42px 36px 36px 36px;
    overflow: hidden;
}
.title-container {
    text-align: center;
    margin-bottom: 12px;
}
.sub-script {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 32px;
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
    font-size: 44px;
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
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-top: 6px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.6);
}
.fragrance-list-card {
    width: 100%;
    flex: 1;
    background: rgba(10, 12, 18, 0.78);
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
    padding: 4px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.item-row:last-child {
    border-bottom: none;
}
.item-name {
    font-family: 'Montserrat', sans-serif;
    font-weight: 700;
    font-size: 17px;
    color: #ffffff;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.9);
}
.item-brand {
    font-family: 'Montserrat', sans-serif;
    font-weight: 500;
    font-size: 14px;
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
</style>
</head>
<body>
'''

page_num = 1

# P1: PORTADA
html += f'''
<div class="page" style="background-image: url('portada_catalogo_oficial.jpg'); padding: 0; justify-content: flex-end;">
    <div style="width: 100%; background: linear-gradient(transparent, rgba(0,0,0,0.95) 40%, #000); padding: 50px 40px 35px 40px; text-align: center;">
        <div style="font-family: 'Cinzel', serif; font-size: 26px; color: #dfb15b; letter-spacing: 2px; margin-bottom: 8px;">LISTADO DE FRAGANCIAS EXCLUSIVAS 2026</div>
        <div style="font-size: 16px; color: #e2e8f0; margin-bottom: 14px;">Extractos de Perfume 60ml • Cápsula Fusión • Perfumería Árabe • Línea Automóvil</div>
        <div style="display: flex; justify-content: center; gap: 15px;">
            <span style="background: rgba(223, 177, 91, 0.2); border: 1px solid #dfb15b; color: #ffe6a3; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 13px;">✨ 60ml: {P_CLASSIC} (Promo: {P_CLASSIC_PROMO})</span>
            <span style="background: rgba(223, 177, 91, 0.2); border: 1px solid #dfb15b; color: #ffe6a3; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 13px;">🕌 Árabes & Fusión: {P_ARABIC}</span>
            <span style="background: rgba(223, 177, 91, 0.2); border: 1px solid #dfb15b; color: #ffe6a3; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 13px;">🚗 Combo Auto: {P_AUTO}</span>
        </div>
    </div>
</div>
'''
page_num += 1

# P2: PRECIOS Y PRODUCTOS
html += f'''
<div class="page" style="background-image: linear-gradient(rgba(8,9,14,0.85), rgba(8,9,14,0.9)), url('fondo_masculinas_estrellas.jpg'); justify-content: space-between;">
    <div class="title-container" style="margin-top: 10px;">
        <div class="sub-script sub-script-gold">Lista Oficial</div>
        <div class="main-title">PRECIOS Y PROMOCIONES</div>
        <div class="price-badge-pill">TODOS LOS PRODUCTOS EN STOCK DISPONIBLE</div>
    </div>

    <div style="width: 100%; display: flex; flex-direction: column; gap: 20px;">
        <div style="display: flex; gap: 20px; align-items: center; background: rgba(18, 20, 30, 0.85); border: 1px solid rgba(223, 177, 91, 0.4); border-radius: 14px; padding: 18px 24px;">
            <img src="promo_2_fragancias.png" style="width: 140px; height: 160px; object-fit: cover; border-radius: 10px; border: 1px solid #dfb15b;">
            <div style="flex: 1;">
                <div style="font-family: 'Cinzel', serif; font-size: 24px; color: #fff; margin-bottom: 4px;">Perfumes 60ml (Clásicos)</div>
                <div style="color: #dfb15b; font-size: 32px; font-weight: 800; margin-bottom: 4px;">{P_CLASSIC}</div>
                <div style="background: rgba(255, 105, 180, 0.2); border: 1px solid #ff7597; color: #ffb3c6; padding: 4px 12px; border-radius: 6px; font-size: 14px; font-weight: 700; display: inline-block; margin-bottom: 8px;">🔥 SÚPER PROMO: {P_CLASSIC_PROMO}</div>
                <p style="color: #cbd5e1; font-size: 14px;">Envases de vidrio de 60ml con spray plateado micro-fino. Extracto concentrado de máxima fijación (8 a 12 horas de duración).</p>
            </div>
        </div>

        <div style="display: flex; gap: 20px; align-items: center; background: rgba(18, 20, 30, 0.85); border: 1px solid rgba(223, 177, 91, 0.5); border-radius: 14px; padding: 18px 24px;">
            <img src="frasco_arabe_lujo.jpg" style="width: 140px; height: 160px; object-fit: cover; border-radius: 10px; border: 1px solid #dfb15b;">
            <div style="flex: 1;">
                <div style="font-family: 'Cinzel', serif; font-size: 24px; color: #dfb15b; margin-bottom: 4px;">Línea Árabe & Cápsula Fusión</div>
                <div style="color: #fff; font-size: 32px; font-weight: 800; margin-bottom: 4px;">{P_ARABIC}</div>
                <div style="background: rgba(223, 177, 91, 0.2); border: 1px solid #dfb15b; color: #ffe6a3; padding: 4px 12px; border-radius: 6px; font-size: 14px; font-weight: 700; display: inline-block; margin-bottom: 8px;">✨ EDICIÓN DE LUJO Y TENDENCIA</div>
                <p style="color: #cbd5e1; font-size: 14px;">Mismo frasco de 60ml oficial con formulaciones complejas de Oriente: notas de Oud, Ámbar, Vainilla oriental y especias hipnóticas.</p>
            </div>
        </div>

        <div style="display: flex; gap: 20px; align-items: center; background: rgba(18, 20, 30, 0.85); border: 1px solid rgba(223, 177, 91, 0.4); border-radius: 14px; padding: 18px 24px;">
            <img src="combo_auto_interior.png" style="width: 140px; height: 160px; object-fit: cover; border-radius: 10px; border: 1px solid #dfb15b;">
            <div style="flex: 1;">
                <div style="font-family: 'Cinzel', serif; font-size: 24px; color: #fff; margin-bottom: 4px;">Combo Auto & Fragancia Textil</div>
                <div style="color: #dfb15b; font-size: 32px; font-weight: 800; margin-bottom: 4px;">{P_AUTO}</div>
                <div style="background: rgba(56, 189, 248, 0.2); border: 1px solid #38bdf8; color: #bae6fd; padding: 4px 12px; border-radius: 6px; font-size: 14px; font-weight: 700; display: inline-block; margin-bottom: 8px;">🚗 PROMO AUTO: {P_AUTO_PROMO}</div>
                <p style="color: #cbd5e1; font-size: 14px;">Incluye difusor colgante de madera 8ml + spray textil 30ml para tapizados y alfombras en bolsita con etiqueta kraft y moño.</p>
            </div>
        </div>
    </div>
    <div class="page-footer-num">Página {page_num}</div>
</div>
'''
page_num += 1

# P3: CAPSULA FUSION
html += f'''
<div class="page" style="background-image: linear-gradient(rgba(10,12,18,0.55), rgba(10,12,18,0.8)), url('banner_capsula_fusion.jpg'); justify-content: space-between;">
    <div class="title-container" style="margin-top: 10px;">
        <div class="sub-script sub-script-gold">Edición Exclusiva</div>
        <div class="main-title">CÁPSULA FUSIÓN</div>
        <div class="price-badge-pill">PRECIO: {P_ARABIC} C/U • DOS ESENCIAS, UN NUEVO LEGADO</div>
    </div>

    <div class="fragrance-list-card" style="max-height: 460px; margin-top: 300px;">
        {render_list(otros['fusion'])}
    </div>
    <div class="page-footer-num">Página {page_num}</div>
</div>
'''
page_num += 1

# P4: LINEA AUTO
html += f'''
<div class="page" style="background-image: url('tabla_aromas_auto_completa.jpg'); padding: 0; justify-content: flex-end;">
    <div style="width: 100%; background: linear-gradient(transparent, rgba(0,0,0,0.95) 35%, #000); padding: 30px 40px 25px 40px; text-align: center;">
        <div style="display: flex; justify-content: center; gap: 20px;">
            <span style="background: rgba(223, 177, 91, 0.25); border: 1px solid #dfb15b; color: #ffe6a3; padding: 8px 18px; border-radius: 20px; font-weight: 700; font-size: 16px;">🚗 COMBO: {P_AUTO}</span>
            <span style="background: rgba(223, 177, 91, 0.25); border: 1px solid #dfb15b; color: #ffe6a3; padding: 8px 18px; border-radius: 20px; font-weight: 700; font-size: 16px;">🔥 PROMO: {P_AUTO_PROMO}</span>
        </div>
    </div>
</div>
'''
page_num += 1

# P5: NUEVOS INGRESOS
nuevos_total = otros.get('nuevos_fem', []) + otros.get('nuevos_masc', [])
html += f'''
<div class="page" style="background-image: url('fondo_nuevos_ingresos_masc.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="sub-script sub-script-gold">Tendencias 2026</div>
        <div class="main-title">NUEVOS INGRESOS</div>
        <div class="price-badge-pill">ÚLTIMOS LANZAMIENTOS • {P_CLASSIC} / {P_ARABIC} SEGÚN LÍNEA</div>
    </div>

    <div class="fragrance-list-card" style="max-height: 720px;">
        {render_list(nuevos_total)}
    </div>
    <div class="page-footer-num">Página {page_num}</div>
</div>
'''
page_num += 1

# P6: ARABES FEM
html += f'''
<div class="page" style="background-image: url('fondo_arabes_dorado.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="sub-script sub-script-gold">Perfumería Oriental</div>
        <div class="main-title">ÁRABES FEMENINAS</div>
        <div class="price-badge-pill">PRECIO: {P_ARABIC} C/U • ALTA FIJACIÓN & ESTELA</div>
    </div>

    <div class="fragrance-list-card">
        {render_list(otros['arabes_fem'])}
    </div>
    <div class="page-footer-num">Página {page_num}</div>
</div>
'''
page_num += 1

# P7 & P8: ARABES MASC
arabes_masc_p1 = otros['arabes_masc'][:19]
arabes_masc_p2 = otros['arabes_masc'][19:]

html += f'''
<div class="page" style="background-image: url('fondo_arabes_noche.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="sub-script sub-script-gold">Perfumería Oriental</div>
        <div class="main-title">ÁRABES MASCULINAS (I)</div>
        <div class="price-badge-pill">PRECIO: {P_ARABIC} C/U • NOTAS DE OUD, ÁMBAR Y CUERO</div>
    </div>

    <div class="fragrance-list-card">
        {render_list(arabes_masc_p1)}
    </div>
    <div class="page-footer-num">Página {page_num}</div>
</div>
'''
page_num += 1

html += f'''
<div class="page" style="background-image: url('fondo_arabes_vortice.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="sub-script sub-script-gold">Perfumería Oriental</div>
        <div class="main-title">ÁRABES MASCULINAS (II)</div>
        <div class="price-badge-pill">PRECIO: {P_ARABIC} C/U • MÁXIMA INTENSIDAD</div>
    </div>

    <div class="fragrance-list-card">
        {render_list(arabes_masc_p2)}
    </div>
    <div class="page-footer-num">Página {page_num}</div>
</div>
'''
page_num += 1

# P9: ARABES UNISEX
html += f'''
<div class="page" style="background-image: url('fondo_arabes_cielo.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="sub-script sub-script-gold">Perfumería Oriental</div>
        <div class="main-title">ÁRABES UNISEX</div>
        <div class="price-badge-pill">PRECIO: {P_ARABIC} C/U • ARMONÍAS COMPARTIDAS</div>
    </div>

    <div class="fragrance-list-card" style="max-height: 650px;">
        {render_list(otros['arabes_unisex'])}
    </div>
    <div class="page-footer-num">Página {page_num}</div>
</div>
'''
page_num += 1

# P10 to P19: FEMENINAS CLASICAS (222 / 10 = ~22-23)
fem_per_page = math.ceil(len(fem) / 10)
fem_chunks = [fem[i:i + fem_per_page] for i in range(0, len(fem), fem_per_page)]

for idx, chunk in enumerate(fem_chunks):
    bg = 'fondo_femeninas_rosas.jpg' if idx % 2 == 0 else 'fondo_femeninas_orquideas.jpg'
    html += f'''
    <div class="page" style="background-image: url('{bg}'); justify-content: space-between;">
        <div class="title-container">
            <div class="sub-script">Colección Clásica</div>
            <div class="main-title">FEMENINAS (Parte {idx+1})</div>
            <div class="price-badge-pill">60 ML • {P_CLASSIC} • PROMO: {P_CLASSIC_PROMO}</div>
        </div>

        <div class="fragrance-list-card">
            {render_list(chunk)}
        </div>
        <div class="page-footer-num">Página {page_num}</div>
    </div>
    '''
    page_num += 1

# P20 to P28: MASCULINAS CLASICAS (210 / 9 = ~23-24)
masc_per_page = math.ceil(len(masc) / 9)
masc_chunks = [masc[i:i + masc_per_page] for i in range(0, len(masc), masc_per_page)]

for idx, chunk in enumerate(masc_chunks):
    bg = 'fondo_masculinas_seda_azul.jpg' if idx % 2 == 0 else 'fondo_masculinas_estrellas.jpg'
    html += f'''
    <div class="page" style="background-image: url('{bg}'); justify-content: space-between;">
        <div class="title-container">
            <div class="sub-script sub-script-masc">Colección Clásica</div>
            <div class="main-title">MASCULINAS (Parte {idx+1})</div>
            <div class="price-badge-pill">60 ML • {P_CLASSIC} • PROMO: {P_CLASSIC_PROMO}</div>
        </div>

        <div class="fragrance-list-card">
            {render_list(chunk)}
        </div>
        <div class="page-footer-num">Página {page_num}</div>
    </div>
    '''
    page_num += 1

# P29: UNISEX & NICHO
html += f'''
<div class="page" style="background-image: url('fondo_unisex_atardecer.jpg'); justify-content: space-between;">
    <div class="title-container">
        <div class="sub-script sub-script-gold">Línea Exclusiva</div>
        <div class="main-title">UNISEX & NICHO</div>
        <div class="price-badge-pill">60 ML • {P_CLASSIC} / {P_ARABIC} • NOTAS DE AUTOR</div>
    </div>

    <div class="fragrance-list-card">
        {render_list(otros['unisex'])}
    </div>
    <div class="page-footer-num">Página {page_num}</div>
</div>
'''
page_num += 1

# P30: CONTRATAPA / CONTACTO
html += f'''
<div class="page" style="background-image: linear-gradient(rgba(8,9,14,0.9), rgba(8,9,14,0.95)), url('fondo_masculinas_seda_azul.jpg'); justify-content: center;">
    <div style="text-align: center; max-width: 680px; background: rgba(18, 20, 30, 0.85); border: 1px solid rgba(223, 177, 91, 0.4); border-radius: 16px; padding: 40px 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.8);">
        <div style="font-family: 'Cinzel', serif; font-size: 34px; color: #dfb15b; margin-bottom: 15px;">¿CÓMO REALIZAR TU PEDIDO?</div>
        <p style="color: #e2e8f0; font-size: 17px; margin-bottom: 25px; line-height: 1.6;">Elegí tus fragancias favoritas del catálogo y contactanos directamente por WhatsApp para coordinar tu entrega o envío.</p>

        <div style="background: rgba(0,0,0,0.5); border: 1px solid rgba(223, 177, 91, 0.3); border-radius: 12px; padding: 20px; margin-bottom: 25px; text-align: left;">
            <div style="font-size: 16px; color: #ffd1dc; margin-bottom: 8px;">💳 <b>Medios de Pago:</b></div>
            <div style="color: #cbd5e1; font-size: 15px; margin-bottom: 12px;">• Efectivo / Transferencias (Mercado Pago, Cuenta DNI, Bancos)</div>
            <div style="font-size: 16px; color: #ffe6a3; margin-bottom: 8px;">📦 <b>Entregas:</b></div>
            <div style="color: #cbd5e1; font-size: 15px;">• Puntos de encuentro y envíos a domicilio coordinados.</div>
        </div>

        <div style="font-family: 'Cinzel', serif; font-size: 20px; color: #fff; margin-bottom: 8px;">¡GRACIAS POR ELEGIRNOS!</div>
        <div style="color: #dfb15b; font-size: 15px; letter-spacing: 1px;">CALIDAD • PERSISTENCIA • ALTA GAMA</div>
    </div>
    <div class="page-footer-num">Página {page_num}</div>
</div>
'''

html += '''
</body>
</html>
'''

with open('catalogo_30_paginas.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('SUCCESS! Created catalogo_30_paginas.html with pages:', page_num - 1)
