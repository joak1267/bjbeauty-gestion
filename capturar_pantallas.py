# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import os

artifact_dir = r"C:\Users\soyto.JOAQUIN2206\.gemini\antigravity\brain\bbcb62b7-8969-4f76-8758-1ff2052fbf54"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1400, "height": 900})
    page.goto("http://localhost:5000")
    page.wait_for_timeout(2000)

    # 1. Captura pestaña Ventas
    shot1 = os.path.join(artifact_dir, "panel_ventas_silvia.png")
    page.screenshot(path=shot1)
    print("Captura 1 guardada:", shot1)

    # 2. Captura pestaña Reservas & Encargos
    page.click("#tab-btn-reservas")
    page.wait_for_timeout(1000)
    shot2 = os.path.join(artifact_dir, "panel_reservas_pedidos.png")
    page.screenshot(path=shot2)
    print("Captura 2 guardada:", shot2)

    # 3. Captura pestaña Catálogo & Stock
    page.click("#tab-btn-catalogo")
    page.wait_for_timeout(1000)
    shot3 = os.path.join(artifact_dir, "panel_catalogo_stock.png")
    page.screenshot(path=shot3)
    print("Captura 3 guardada:", shot3)

    browser.close()
