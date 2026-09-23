# -*- coding: utf-8 -*-
"""
Actualiza sistema_ventas_y_ganancias.html con:
1. Pestañas '🔖 Reservas & Encargos' y '📚 Catálogo & Stock'
2. Autocompletado del catálogo de 556 fragancias de los PDFs en el formulario de ventas
3. Formulario y tabla de gestión de reservas (con convertir a venta)
4. Visor y buscador del catálogo completo con ajuste de stock en MySQL
"""

import os
import re

FILE_PATH = r"C:\Users\soyto.JOAQUIN2206\OneDrive\Desktop\Proyectos\perfumes-gestion\sistema_ventas_y_ganancias.html"
SCRATCH_PATH = r"C:\Users\soyto.JOAQUIN2206\.gemini\antigravity\scratch\perfumes-gestion\sistema_ventas_y_ganancias.html"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. AGREGAR ESTILOS CSS ADICIONALES ANTES DE </style>
css_extra = """
        /* AUTOCOMPLETE DROPDOWN */
        .autocomplete-dropdown {
            position: absolute;
            top: calc(100% + 4px);
            left: 0;
            right: 0;
            background: #1e293b;
            border: 1px solid var(--primary);
            border-radius: 8px;
            max-height: 260px;
            overflow-y: auto;
            z-index: 1000;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        }
        .autocomplete-item {
            padding: 9px 12px;
            cursor: pointer;
            border-bottom: 1px solid rgba(255,255,255,0.06);
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            transition: background 0.15s;
        }
        .autocomplete-item:hover {
            background: rgba(245, 158, 11, 0.2);
        }
        .autocomplete-item:last-child {
            border-bottom: none;
        }
        .auto-name {
            font-size: 0.88rem;
            font-weight: 700;
            color: #fff;
        }
        .auto-meta {
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-top: 2px;
        }
        .auto-tag {
            font-size: 0.7rem;
            padding: 2px 7px;
            border-radius: 6px;
            font-weight: 700;
            white-space: nowrap;
        }
        .tag-fem { background: rgba(236, 72, 153, 0.2); color: #f472b6; border: 1px solid rgba(236, 72, 153, 0.4); }
        .tag-masc { background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4); }
        .tag-arabe { background: rgba(234, 179, 8, 0.2); color: #facc15; border: 1px solid rgba(234, 179, 8, 0.4); }
        .tag-auto { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }
        .tag-unisex { background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.4); }

        /* BADGES FOR RESERVAS */
        .badge-op {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.72rem;
            font-weight: 700;
        }
        .badge-op-reserva { background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4); }
        .badge-op-confirmar { background: rgba(234, 179, 8, 0.2); color: #facc15; border: 1px solid rgba(234, 179, 8, 0.4); }
        .badge-op-encargo { background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.4); }
        .badge-op-entregado { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }

        /* STOCK CONTROLS */
        .stock-control {
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .btn-stock {
            width: 24px;
            height: 24px;
            border-radius: 4px;
            border: 1px solid var(--card-border);
            background: rgba(255,255,255,0.06);
            color: #fff;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: bold;
            transition: all 0.15s;
        }
        .btn-stock:hover {
            border-color: var(--primary);
            background: var(--primary);
            color: #000;
        }
        .btn-sm-action {
            padding: 5px 10px;
            font-size: 0.75rem;
            border-radius: 6px;
            font-weight: 700;
            cursor: pointer;
            border: 1px solid var(--card-border);
            background: rgba(255,255,255,0.05);
            color: #fff;
            transition: all 0.15s;
        }
        .btn-sm-action:hover {
            background: var(--primary);
            color: #000;
            border-color: var(--primary);
        }
        .btn-sm-success {
            background: rgba(16, 185, 129, 0.2);
            color: #34d399;
            border-color: rgba(16, 185, 129, 0.4);
        }
        .btn-sm-success:hover {
            background: var(--success);
            color: #fff;
        }
    </style>
"""

content = content.replace("    </style>", css_extra)

# 2. ACTUALIZAR NAV-TABS CON LAS NUEVAS PESTAÑAS
nav_tabs_original = """        <div class="nav-tabs">
            <button class="tab-btn active" id="tab-btn-ventas" onclick="cambiarPestana('ventas')">
                🛍️ Ventas & Facturación
            </button>
            <button class="tab-btn" id="tab-btn-compras" onclick="cambiarPestana('compras')">
                📦 Costos & Mercadería
            </button>
        </div>"""

nav_tabs_nuevo = """        <div class="nav-tabs">
            <button class="tab-btn active" id="tab-btn-ventas" onclick="cambiarPestana('ventas')">
                🛍️ Ventas & Facturación
            </button>
            <button class="tab-btn" id="tab-btn-compras" onclick="cambiarPestana('compras')">
                📦 Costos & Mercadería
            </button>
            <button class="tab-btn" id="tab-btn-reservas" onclick="cambiarPestana('reservas')">
                🔖 Reservas & Encargos <span id="badge-count-reservas" style="background:var(--primary);color:#000;border-radius:10px;padding:2px 7px;font-size:0.75rem;margin-left:4px;font-weight:800;">4</span>
            </button>
            <button class="tab-btn" id="tab-btn-catalogo" onclick="cambiarPestana('catalogo')">
                📚 Catálogo & Stock <span style="background:rgba(255,255,255,0.1);color:#cbd5e1;border-radius:10px;padding:2px 7px;font-size:0.75rem;margin-left:4px;">556</span>
            </button>
        </div>"""

content = content.replace(nav_tabs_original, nav_tabs_nuevo)

# 3. AGREGAR AUTOCOMPLETADO Y PROMOS AL FORMULARIO DE VENTAS
form_fragancia_old = """                        <div class="form-group">
                            <label>Fragancia / Detalle</label>
                            <input type="text" id="fragancia" class="form-control" placeholder="Ej: Sauvage Dior / Yara Lattafa" required>
                        </div>"""

form_fragancia_new = """                        <!-- PRESETS DE PROMOS OFICIALES -->
                        <div style="margin-bottom: 11px;">
                            <label style="font-size: 0.74rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-bottom: 5px; display: block;">Promos Oficiales del Catálogo:</label>
                            <div style="display: flex; gap: 8px;">
                                <button type="button" class="btn-preset" onclick="aplicarPromoVenta('2x40')" title="Aplicar Promo Oficial 2 Perfumes Clásicos x $40.000">
                                    🔥 2 Perfumes x $40.000
                                </button>
                                <button type="button" class="btn-preset" onclick="aplicarPromoVenta('2x20auto')" title="Aplicar Promo Oficial 2 Combos Auto x $20.000">
                                    🚘 2 Combos Auto x $20.000
                                </button>
                            </div>
                        </div>

                        <div class="form-group" style="position: relative;">
                            <label>Fragancia / Detalle (Buscador del Catálogo)</label>
                            <div style="position: relative;">
                                <input type="text" id="fragancia" class="form-control" placeholder="🔍 Escribe para buscar (ej: My Way, Scandal, Sauvage...)" autocomplete="off" oninput="buscarEnCatalogo(this.value, 'venta')" onfocus="buscarEnCatalogo(this.value, 'venta')" required>
                                <div id="autocomplete-catalogo-venta" class="autocomplete-dropdown" style="display: none;"></div>
                            </div>
                        </div>"""

content = content.replace(form_fragancia_old, form_fragancia_new)

# 4. AGREGAR CAMPO DE NOTAS AL FORMULARIO DE VENTAS
form_pago_old = """                        <div class="form-group">
                            <label>Forma de Pago</label>
                            <select id="medio-pago" class="form-control">
                                <option value="Transferencia">Transferencia (MercadoPago/Banco)</option>
                                <option value="Efectivo">Efectivo</option>
                                <option value="Tarjeta / Cuotas">Tarjeta / Cuotas</option>
                            </select>
                        </div>"""

form_pago_new = """                        <div class="form-group">
                            <label>Forma de Pago</label>
                            <select id="medio-pago" class="form-control">
                                <option value="Transferencia">Transferencia (MercadoPago/Banco)</option>
                                <option value="Efectivo">Efectivo</option>
                                <option value="Tarjeta / Cuotas">Tarjeta / Cuotas</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Notas / Observaciones (opcional)</label>
                            <input type="text" id="venta-notas" class="form-control" placeholder="Ej: Silvia a confirmar aromatizante / Enviar con moño">
                        </div>"""

content = content.replace(form_pago_old, form_pago_new)

# 5. AGREGAR SECCIONES HTML DE RESERVAS Y CATÁLOGO ANTES DE </div> DEL CONTAINER (LÍNEA 980)
secciones_extra = """
        <!-- ============================================== -->
        <!-- SECCIÓN 3: RESERVAS & ENCARGOS                 -->
        <!-- ============================================== -->
        <div id="seccion-reservas" style="display: none;">
            <div class="main-layout">
                <!-- FORMULARIO DE NUEVA RESERVA -->
                <div class="form-card">
                    <h2>🔖 Nueva Reserva / Encargo</h2>
                    <form id="reserva-form" onsubmit="guardarReservaForm(event)">
                        <div class="form-group">
                            <label>Cliente o Destino</label>
                            <input type="text" id="reserva-cliente" class="form-control" placeholder="Ej: Silvia Ferbola / Maria Laura" required>
                        </div>

                        <div class="form-group">
                            <label>Tipo de Operación</label>
                            <select id="reserva-tipo-op" class="form-control" onchange="autoAjustarTipoOperacion()">
                                <option value="Reserva Cliente">👤 Reserva de Cliente</option>
                                <option value="A Confirmar">⏳ A Confirmar por Cliente</option>
                                <option value="Encargo Proveedor">📦 Encargo / Reposición Proveedor</option>
                            </select>
                        </div>

                        <div class="form-group" style="position: relative;">
                            <label>Fragancia / Producto (Catálogo)</label>
                            <div style="position: relative;">
                                <input type="text" id="reserva-fragancia" class="form-control" placeholder="🔍 Escribe aroma (ej: La Bomba, Erba Pura...)" autocomplete="off" oninput="buscarEnCatalogo(this.value, 'reserva')" onfocus="buscarEnCatalogo(this.value, 'reserva')" required>
                                <div id="autocomplete-catalogo-reserva" class="autocomplete-dropdown" style="display: none;"></div>
                            </div>
                        </div>

                        <div class="form-row">
                            <div class="form-group">
                                <label>Cantidad</label>
                                <input type="number" id="reserva-cantidad" class="form-control" value="1" min="1" required>
                            </div>
                            <div class="form-group">
                                <label>Precio / Costo Estimado ($)</label>
                                <input type="number" id="reserva-precio" class="form-control" value="22000" required>
                            </div>
                        </div>

                        <div class="form-group">
                            <label>Estado Inicial</label>
                            <select id="reserva-estado" class="form-control">
                                <option value="Reservado">Reservado</option>
                                <option value="Pendiente de Confirmación">Pendiente de Confirmación</option>
                                <option value="Por Encargar">Por Encargar</option>
                                <option value="Confirmado">Confirmado</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label>Notas / Detalles</label>
                            <textarea id="reserva-notas" class="form-control" rows="2" placeholder="Ej: Reservar para el fin de semana / Confirmar fragancia"></textarea>
                        </div>

                        <input type="hidden" id="reserva-tipo-prod" value="perfume">

                        <button type="submit" class="btn btn-primary" style="width: 100%; justify-content: center; padding: 12px;">
                            💾 Guardar en Reservas
                        </button>
                    </form>
                </div>

                <!-- TABLA DE RESERVAS REGISTRADAS -->
                <div class="table-card">
                    <div class="table-header">
                        <h2>📋 Lista de Reservas, Confirmaciones & Encargos</h2>
                        <input type="text" id="filtro-reservas" class="search-box" placeholder="🔍 Buscar cliente, perfume o encargo..." oninput="filtrarReservas()">
                    </div>

                    <div class="table-responsive">
                        <table>
                            <thead>
                                <tr>
                                    <th class="col-nowrap" style="width: 85px;">Fecha</th>
                                    <th>Cliente / Destino</th>
                                    <th>Tipo</th>
                                    <th>Fragancia / Producto</th>
                                    <th class="col-cant" style="width: 45px;">Cant.</th>
                                    <th class="col-nowrap" style="width: 85px;">Importe</th>
                                    <th class="col-estado" style="width: 130px;">Estado</th>
                                    <th>Notas</th>
                                    <th style="width: 110px; text-align: right;">Acciones</th>
                                </tr>
                            </thead>
                            <tbody id="tabla-reservas-cuerpo">
                                <!-- Inserción dinámica -->
                            </tbody>
                        </table>
                    </div>
                    <div id="sin-reservas" class="empty-state">No hay reservas ni pedidos pendientes.</div>
                </div>
            </div>
        </div>

        <!-- ============================================== -->
        <!-- SECCIÓN 4: CATÁLOGO & STOCK DE PRODUCTOS       -->
        <!-- ============================================== -->
        <div id="seccion-catalogo" style="display: none;">
            <div class="table-card">
                <div class="table-header" style="flex-direction: column; align-items: stretch; gap: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                        <div>
                            <h2 style="margin: 0; color: var(--primary);">📚 Catálogo Oficial BJ BEAUTY & Control de Stock</h2>
                            <p style="color: var(--text-muted); font-size: 0.85rem; margin-top: 2px;">
                                Fragancias extraídas de los catálogos en PDF: Femeninos, Masculinos, Árabes, Unisex y Automotor
                            </p>
                        </div>
                        <input type="text" id="filtro-catalogo-input" class="search-box" style="width: 280px;" placeholder="🔍 Buscar perfume o marca..." oninput="filtrarCatalogo()">
                    </div>

                    <!-- CHIPS DE FILTRO POR CATEGORÍA -->
                    <div class="chips-container" id="chips-catalogo">
                        <button class="filter-chip active" onclick="filtrarCatalogoCat('todas', this)">✨ Todas (556)</button>
                        <button class="filter-chip" onclick="filtrarCatalogoCat('Femenina', this)">🌸 Femeninos</button>
                        <button class="filter-chip" onclick="filtrarCatalogoCat('Masculina', this)">👔 Masculinos</button>
                        <button class="filter-chip" onclick="filtrarCatalogoCat('Árabe', this)">🕌 Perfumería Árabe</button>
                        <button class="filter-chip" onclick="filtrarCatalogoCat('Unisex', this)">✨ Unisex & Nicho</button>
                        <button class="filter-chip" onclick="filtrarCatalogoCat('Cápsula', this)">💎 Cápsula Fusión</button>
                        <button class="filter-chip" onclick="filtrarCatalogoCat('Automotor', this)">🚗 Automotor & Textil</button>
                    </div>
                </div>

                <div class="table-responsive" style="max-height: 550px;">
                    <table>
                        <thead>
                            <tr>
                                <th>Fragancia / Aroma</th>
                                <th>Marca / Casa</th>
                                <th>Categoría Oficial</th>
                                <th class="col-nowrap" style="width: 90px;">Precio Venta</th>
                                <th class="col-nowrap" style="width: 80px;">Costo Reposición</th>
                                <th class="col-nowrap" style="width: 105px; text-align: center;">Stock Físico</th>
                                <th style="width: 130px; text-align: right;">Acciones</th>
                            </tr>
                        </thead>
                        <tbody id="tabla-catalogo-cuerpo">
                            <!-- Inserción dinámica -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
"""

content = content.replace("    </div>\n\n    <!-- ============================================== -->\n    <!-- MODAL: RESUMEN MENSUAL DE GESTIÓN              -->", secciones_extra + "\n    </div>\n\n    <!-- ============================================== -->\n    <!-- MODAL: RESUMEN MENSUAL DE GESTIÓN              -->")

with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(content)

with open(SCRATCH_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("HTML base actualizado con éxito.")
