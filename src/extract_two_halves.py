# src/extract_two_halves.py
from pathlib import Path
from extract_clip import extract_clip  # Importa la función del otro script

if __name__ == "__main__":
    src = Path("data/videos/partido.mp4")

    # Ajusta los tiempos a tu caso
    info1 = extract_clip(
        src_path=src,
        dst_path=Path("data/clips/first_half.mp4"),
        t_start="30:00",
        t_end="01:17:00",      # p.ej. "45:30" si hubo añadido
        fallback_fps=25.0   # usa 30.0 si tu vídeo es 30 fps
    )
    print("\n✅ Primera parte extraída:")
    for k, v in info1.items():
        print(f"- {k}: {v}")

    info2 = extract_clip(
        src_path=src,
        dst_path=Path("data/clips/second_half.mp4"),
        t_start="01:31:00",    # ajusta si hubo añadido
        t_end="02:20:00",
        fallback_fps=25.0
    )
    print("\n✅ Segunda parte extraída:")
    for k, v in info2.items():
        print(f"- {k}: {v}")