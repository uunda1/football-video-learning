# src/extract_clip.py
import cv2
from pathlib import Path
import math

def parse_time_to_seconds(t: str) -> float:
    """
    Convierte 'mm:ss' o 'hh:mm:ss' o 'segundos' a float(segundos).
    """
    t = t.strip()
    if ":" not in t:
        return float(t)
    parts = [float(p) for p in t.split(":")]
    if len(parts) == 2:  # mm:ss
        mm, ss = parts
        return mm * 60 + ss
    elif len(parts) == 3:  # hh:mm:ss
        hh, mm, ss = parts
        return hh * 3600 + mm * 60 + ss
    else:
        raise ValueError("Formato de tiempo no reconocido. Usa ss, mm:ss o hh:mm:ss")

def extract_clip(
    src_path: Path,
    dst_path: Path,
    t_start: str,
    t_end: str,
    fallback_fps: float = 25.0,
    fourcc_str: str = "mp4v"
):
    """
    Extrae un clip del vídeo entre t_start y t_end (formatos 'ss', 'mm:ss' o 'hh:mm:ss')
    y lo guarda en dst_path (MP4).
    """
    if not src_path.exists():
        raise FileNotFoundError(f"No existe el archivo fuente: {src_path}")

    cap = cv2.VideoCapture(str(src_path))
    if not cap.isOpened():
        raise RuntimeError("No se pudo abrir el vídeo")

    fps_file   = cap.get(cv2.CAP_PROP_FPS)
    width      = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height     = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    framecount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # En algunos contenedores FPS reportado puede ser 0 o extraño (directos, VFR)
    fps = fps_file if (fps_file is not None and fps_file > 1e-3) else fallback_fps

    # Tiempos a segundos
    start_sec = parse_time_to_seconds(t_start)
    end_sec   = parse_time_to_seconds(t_end)
    if end_sec <= start_sec:
        cap.release()
        raise ValueError("t_end debe ser mayor que t_start")

    # Aproximación tiempo → índice de frame
    start_frame = int(math.floor(start_sec * fps))
    end_frame   = int(math.ceil(end_sec * fps))

    # Posicionamos el puntero lo más cerca del frame inicial
    cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, start_frame))

    # Preparar escritor
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*fourcc_str)  # 'mp4v' suele “just work” para .mp4
    writer = cv2.VideoWriter(str(dst_path), fourcc, fps, (width, height))

    current_frame_idx = start_frame
    written = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            # Fin de archivo o error de lectura
            break

        if current_frame_idx < start_frame:
            current_frame_idx += 1
            continue

        if current_frame_idx > end_frame:
            break

        writer.write(frame)
        written += 1
        current_frame_idx += 1

    cap.release()
    writer.release()

    return {
        "src": str(src_path),
        "dst": str(dst_path),
        "fps_file": fps_file,
        "fps_used": fps,
        "width": width,
        "height": height,
        "framecount_file": framecount,
        "start_sec": start_sec,
        "end_sec": end_sec,
        "frames_written": written,
        "approx_duration_out_s": (written / fps) if fps > 0 else None
    }

if __name__ == "__main__":
    # ⚙️ Ajusta aquí las ventanas de tiempo que quieres cortar
    src = Path("data/videos/partido.mp4")
    dst = Path("data/clips/clip_20_00_25_00.mp4")

    info = extract_clip(src, dst, t_start="20:00", t_end="25:00")
    print("✅ Clip extraído:")
    for k, v in info.items():
        print(f"- {k}: {v}")