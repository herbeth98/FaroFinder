"""Gera o ícone do FaroFinder.exe (launcher/icone.ico e icone.png) a partir de logo/FaroFinder-icone-1024.png.

O desenho vem da identidade visual (vetores em web/marca). Depois de rodar, compile com launcher\\compilar.bat.
Uso: .venv\\Scripts\\python.exe launcher\\make_icon.py
"""
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
LAUNCHER = RAIZ / "launcher"
TAMANHOS = [16, 20, 24, 32, 40, 48, 64, 96, 128, 256]


def main():
    base = Image.open(RAIZ / "logo" / "FaroFinder-icone-1024.png").convert("RGBA")
    base.resize((256, 256), Image.LANCZOS).save(LAUNCHER / "icone.png")
    base.save(LAUNCHER / "icone.ico", sizes=[(s, s) for s in TAMANHOS])
    (RAIZ / "logo" / "FaroFinder.ico").write_bytes((LAUNCHER / "icone.ico").read_bytes())
    print("ícones gravados em launcher/ e logo/")


if __name__ == "__main__":
    main()
