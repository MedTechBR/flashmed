#!/usr/bin/env python3
"""Ícones do FlashMed: raio claro sobre o âmbar queimado da marca (#C2410C).
   Quadrado CHEIO, sem canto transparente: o macOS põe moldura clara em ícone 'any' com transparência.
   Gera icons/icon-180.png, icon-192.png, icon-512.png e icon-maskable-512.png."""
from PIL import Image, ImageDraw

MARCA = (194, 65, 12, 255)
CLARO = (255, 247, 237, 255)
SOMBRA = (154, 52, 18, 255)

def raio(tam, escala):
    # polígono do raio no viewBox 24x24 (mesmo desenho do logo do cabeçalho)
    pts = [(13.5, 2.5), (5, 13.2), (11, 13.2), (9.8, 21.5), (19, 10.6), (12.9, 10.6)]
    c = tam / 2; k = tam / 24 * escala
    return [(c + (x - 12) * k, c + (y - 12) * k) for x, y in pts]

def icone(tam, maskable=False):
    im = Image.new("RGBA", (tam, tam), MARCA)
    d = ImageDraw.Draw(im)
    esc = 0.62 if maskable else 0.82
    sombra = [(x + tam * 0.012, y + tam * 0.018) for x, y in raio(tam, esc)]
    d.polygon(sombra, fill=SOMBRA)
    d.polygon(raio(tam, esc), fill=CLARO)
    return im

for tam in (180, 192, 512):
    icone(tam).save(f"icons/icon-{tam}.png")
icone(512, maskable=True).save("icons/icon-maskable-512.png")
print("ícones gerados")
