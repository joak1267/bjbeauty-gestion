import os
from playwright.sync_api import sync_playwright

html_content = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;800;900&family=Montserrat:wght@600;700;800;900&family=Playfair+Display:ital,wght@1,700&display=swap" rel="stylesheet">
<style>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}
body {
    width: 664px;
    height: 1024px;
    position: relative;
    overflow: hidden;
    background: #000;
}
.bg-image {
    width: 664px;
    height: 1024px;
    position: absolute;
    top: 0;
    left: 0;
    z-index: 1;
}

/* LOGO BJ BEAUTY EN CABECERA */
.logo-badge {
    position: absolute;
    top: 12px;
    left: 15px;
    z-index: 10;
    width: 82px;
    height: 82px;
    border-radius: 50%;
    box-shadow: 0 0 25px rgba(192, 132, 252, 0.5), 0 4px 12px rgba(0,0,0,0.9);
    background: #000;
    border: 1.5px solid #dfb15b;
}

/* BARRA SUPERIOR BRANDING BJ BEAUTY */
.brand-strip {
    position: absolute;
    top: 18px;
    left: 106px;
    z-index: 10;
}
.brand-strip .main-txt {
    font-family: 'Cinzel', serif;
    font-size: 18px;
    font-weight: 900;
    letter-spacing: 3px;
    color: #dfb15b;
    text-shadow: 0 0 12px rgba(0,0,0,0.95);
}
.brand-strip .sub-txt {
    font-family: 'Montserrat', sans-serif;
    font-size: 8.5px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #c084fc;
    text-transform: uppercase;
    text-shadow: 0 0 8px rgba(0,0,0,0.9);
}

/* PRECIO PRINCIPAL DEL COMBO (NO SE VENDEN SEPARADOS) */
.combo-price-tag {
    position: absolute;
    top: 270px;
    left: 305px;
    z-index: 10;
    background: linear-gradient(135deg, rgba(22, 14, 35, 0.96), rgba(8, 6, 14, 0.98));
    border: 2px solid #dfb15b;
    border-radius: 14px;
    padding: 8px 16px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(0,0,0,0.9), 0 0 20px rgba(223, 177, 91, 0.4);
}
.combo-price-header {
    font-family: 'Montserrat', sans-serif;
    font-size: 9px;
    font-weight: 800;
    color: #ffd1dc;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 2px;
}
.combo-price-val {
    font-family: 'Cinzel', serif;
    font-size: 30px;
    font-weight: 900;
    color: #ffffff;
    text-shadow: 0 0 12px rgba(255,255,255,0.5);
    line-height: 1;
}
.combo-price-promo {
    font-family: 'Montserrat', sans-serif;
    font-size: 11px;
    font-weight: 800;
    color: #dfb15b;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-top: 4px;
    background: rgba(223, 177, 91, 0.18);
    padding: 3px 8px;
    border-radius: 6px;
    border: 1px solid rgba(223, 177, 91, 0.35);
}
.combo-includes {
    font-family: 'Montserrat', sans-serif;
    font-size: 8px;
    font-weight: 600;
    color: #e9d5ff;
    margin-top: 4px;
    letter-spacing: 0.5px;
}
</style>
</head>
<body>
    <img src="linea_auto_original.jpg" class="bg-image">
    
    <!-- LOGO BJ BEAUTY OFICIAL -->
    <img src="logo_bj_beauty.png" class="logo-badge">
    <div class="brand-strip">
        <div class="main-txt">BJ BEAUTY</div>
        <div class="sub-txt">LÍNEA AUTOMOTOR & TEXTIL • EXCLUSIVA</div>
    </div>

    <!-- PRECIO COMBO ÚNICO (SE VENDE COMPLETO) -->
    <div class="combo-price-tag">
        <div class="combo-price-header">✨ COMBO TEXTIL + DIFUSOR ✨</div>
        <div class="combo-price-val">$11.000</div>
        <div class="combo-price-promo">🚗 PROMO: 2 X $20.000</div>
        <div class="combo-includes">Incluye Textil 30ml + Difusor 8ml</div>
    </div>
</body>
</html>
'''

with open('temp_auto_render.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 664, "height": 1024}, device_scale_factor=2)
    file_url = 'file:///' + os.path.abspath('temp_auto_render.html').replace('\\\\', '/')
    page.goto(file_url, wait_until='networkidle')
    page.screenshot(path='linea_auto_bj_beauty.jpg', quality=95, type='jpeg')
    browser.close()

print('Rendered linea_auto_bj_beauty.jpg (only combo price, no separate sales) successfully!')
