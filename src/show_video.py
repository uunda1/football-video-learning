# src/show_video.py
import cv2
import time
from pathlib import Path

def main():
    video_path = Path("data/videos/partido.mp4")

    # 1) Comprobaciones defensivas
    if not video_path.exists():
        print(f"❌ No existe el archivo: {video_path.resolve()}")
        return

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print("❌ No se pudo abrir el vídeo.")
        return

    # 2) Propiedades del contenedor (informativas)
    fps_file   = cap.get(cv2.CAP_PROP_FPS)
    width      = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height     = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    framecount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print("🎥 Propiedades (del archivo):")
    print(f"- Resolución: {width} x {height}")
    print(f"- FPS (archivo): {fps_file}")
    print(f"- Frames totales (aprox): {framecount}")

    # 3) Variables para medir FPS "real" de procesamiento
    frames_shown = 0
    t0 = time.time()
    fps_real_suavizado = None         # para suavizar lecturas (EMA simple)
    alpha = 0.05                      # factor de suavizado (0..1)

    # 4) Bucle principal de reproducción
    while True:
        t_frame_start = time.time()

        ret, frame = cap.read()
        if not ret:
            print("🔚 Fin del vídeo o error de lectura.")
            break

        frames_shown += 1

        # 4.1) Calcular FPS real instantáneo (1 / tiempo_de_este_frame)
        dt = time.time() - t_frame_start
        fps_inst = (1.0 / dt) if dt > 0 else 0.0

        # 4.2) Suavizar el FPS (para evitar saltos grandes)
        if fps_real_suavizado is None:
            fps_real_suavizado = fps_inst
        else:
            fps_real_suavizado = (1 - alpha) * fps_real_suavizado + alpha * fps_inst

        # 4.3) Overlay de info en el frame (texto)
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (360, 90), (0, 0, 0), thickness=-1)  # caja semitransparente
        blended = cv2.addWeighted(overlay, 0.35, frame, 0.65, 0)

        cv2.putText(blended, f"FPS archivo: {fps_file:.2f}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2, cv2.LINE_AA)
        cv2.putText(blended, f"FPS real:    {fps_real_suavizado:6.2f}", (20, 75),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2, cv2.LINE_AA)

        # 4.4) Mostrar ventana
        cv2.imshow("Reproduccion - pulsa Q para salir", blended)

        # 4.5) Control de teclado: salir con 'q' (o 'Q')
        #    Espera 1 ms para permitir refresco; si quieres "intentar" reproducir al ritmo del archivo:
        #    puedes usar wait ms ~ 1000/fps_file (pero en análisis solemos no forzar).
        key = cv2.waitKey(1) & 0xFF
        if key in (ord('q'), ord('Q')):
            print("👋 Saliste manualmente con Q.")
            break

    # 5) Cierre ordenado
    cap.release()
    cv2.destroyAllWindows()

    # 6) Estadísticas finales
    dur = time.time() - t0
    fps_promedio = frames_shown / dur if dur > 0 else 0.0
    print(f"✅ Frames mostrados: {frames_shown}")
    print(f"⏱️  Duración reproducción: {dur:.2f}s")
    print(f"📈 FPS promedio real: {fps_promedio:.2f}")

if __name__ == "__main__":
    main()