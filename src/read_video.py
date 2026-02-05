# src/read_video.py
import cv2
from pathlib import Path

def main():
    # 1) Define la ruta del vídeo (relativa a la raíz del repo)
    video_path = Path("data/videos/partido.mp4")

    # 2) Comprobación defensiva: ¿existe el archivo?
    if not video_path.exists():
        print(f"❌ No se encontró el vídeo en: {video_path.resolve()}")
        print("Coloca el archivo MP4 en data/videos/partido.mp4 o ajusta la ruta.")
        return

    # 3) Crea el capturador de vídeo
    cap = cv2.VideoCapture(str(video_path))

    # 4) Comprueba que se abrió correctamente
    if not cap.isOpened():
        print("❌ Error abriendo el vídeo. ¿Está corrupto o sin permisos?")
        return

    # 5) Lee propiedades del vídeo
    fps    = cap.get(cv2.CAP_PROP_FPS)             # frames por segundo
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # ancho en píxeles
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # alto en píxeles
    count  = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # nº total de frames (aprox.)

    # 6) Muestra la información básica
    print("🎥 Propiedades del vídeo")
    print(f"- Ruta      : {video_path}")
    print(f"- Resolución: {width} x {height} (ancho x alto)")
    print(f"- FPS       : {fps}")
    print(f"- Frames    : {count}")

    # 7) Lee algunos frames para verificar acceso (sin abrir ventanas aún)
    frames_to_read = 30
    read_ok = 0
    for _ in range(frames_to_read):
        ret, frame = cap.read()
        if not ret:
            break
        read_ok += 1

    print(f"✅ Frames leídos correctamente: {read_ok}/{frames_to_read}")

    # 8) Libera recursos
    cap.release()

if __name__ == "__main__":
    main()