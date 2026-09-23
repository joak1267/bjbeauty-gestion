# Generador de Catalogo
import json, os

output_path = r'C:\Users\soyto.JOAQUIN2206\OneDrive\Desktop\Proyectos\perfumes-gestion'

fusion = [
    ('Fusión N°1: Midnight Crown', 'Cápsula Fusión (Masc)'),
    ('Fusión N°2: Rosé Infinity', 'Cápsula Fusión (Fem)'),
    ('Fusión N°3: Forbidden Nights', 'Cápsula Fusión (Masc)'),
    ('Fusión N°4: Sky Kiss', 'Cápsula Fusión (Fem)'),
    ('Fusión N°5: Imperium', 'Cápsula Fusión (Masc)'),
    ('Fusión N°6: Velour Rouge', 'Cápsula Fusión (Fem)')
]

auto = [
    ('1. Jazmín', 'Floral y elegante'), ('2. Frutos Rojos', 'Dulce y envolvente'),
    ('3. Naranja Pimienta', 'Cítrico y vibrante'), ('4. Limón', 'Fresco y energizante'),
    ('5. Sandía Pepino', 'Refrescante y liviano'), ('6. Erba Pura', 'Exótico y adictivo'),
    ('7. Grosellas & Nectarina', 'Frutal y jugoso'), ('8. Uva', 'Intenso y dulce'),
    ('9. Chicle', 'Divertido y único'), ('10. Cherry', 'Dulce y seductor'),
    ('11. Coco & Vainilla', 'Cálido y envolvente'), ('12. Naranja Canela', 'Especiado y reconfortante'),
    ('13. La Vie Est Belle', 'Dulce, floral y sofisticado')
]

nuevos_fem = [
    ('Power of You', 'Giorgio Armani'), ('Valentino Born in Roma Extradose', 'Valentino'), ('Victoria', 'Lattafa')
]

nuevos_masc = [
    ('Altair', 'Parfums de Marly'), ('Amber Oud Aqua Dubai', 'Al Haramain'), ('Asad Zanzibar', 'Lattafa'),
    ('Imagination', 'Louis Vuitton'), ('Khamrah Waha', 'Lattafa'), ('Liquid Brun', 'French Avenue'),
    ('Messi', 'Messi'), ('MYSLF L\'Absolu', 'Yves Saint Laurent'), ('Noir de Noir', 'Tom Ford'),
    ('Nouveau Monde', 'Louis Vuitton'), ('Nuit de Feu', 'Louis Vuitton')
]
