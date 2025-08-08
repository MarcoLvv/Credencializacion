# Ajustar a aspecto 3:4 (ancho:alto) sin recortar
import cv2
import numpy as np
import logging

from src.utils.rutas import get_data_dir, heearcascade_face_path

logging.basicConfig(
    filename="camera_controller.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
def haarcascade_faces():
    haar_dir = heearcascade_face_path()
    archivos = [archivo.name for archivo in haar_dir.iterdir() if archivo.is_file() and archivo.suffix == ".xml"]
    print(f"Haarcascades encontrados: {archivos}")
    return [str(haar_dir / archivo) for archivo in archivos]


def detectar_rostro(imagen):
    # Solo convertir a gris si es una imagen en color
    if len(imagen.shape) == 3 and imagen.shape[2] == 3:
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    else:
        gray = imagen  # Ya es gris

    for cascade_path in haarcascade_faces():
        face_cascade = cv2.CascadeClassifier(cascade_path)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        if len(faces) > 0:
            print(f"✅ Rostro detectado con: {cascade_path}")
            return faces
    print("❌ No se detectó rostro con ningún Haarcascade.")
    return None

def process_frame_with_face(frame: np.ndarray, label=None, already_rgb=False) -> np.ndarray:
    logging.debug("Procesando fotograma...")

    if frame is None:
        logging.error("El fotograma recibido es None.")
        return None

    try:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) if not already_rgb else frame
    except Exception as e:
        logging.error(f"Error al convertir a RGB: {e}")
        return None

    cropped = detect_and_expand_face(frame_rgb, zoomout_factor=2.0)

    if cropped is None:
        logging.warning("No se detectó rostro, se usá la imagen completa recortada.")
        print("No se detectó rostro, se usá la imagen completa recortada.")

        cropped = crop_to_4_5(frame_rgb)
        if cropped is None:
            logging.error("Error al recortar imagen a 4:5.")
            return None

    enhanced = enhance_image(cropped)

    transparent = remove_background_mask(enhanced)
    if transparent is None:
        logging.warning("Falló eliminación de fondo, se retorna imagen mejorada.")
        return enhanced

    return transparent


def detect_and_expand_face(image: np.ndarray, zoomout_factor=2.0) -> np.ndarray | None:
    logging.debug("Entrando a detect_and_expand_face()")

    if image is None:
        logging.error("Imagen de entrada es None.")
        return None

    try:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    except Exception as e:
        logging.error(f"Error al convertir a escala de grises: {e}")
        return None

    faces = detectar_rostro(gray)

    if len(faces) == 0:
        logging.warning("No se detectó ningún rostro.")
        return None

    x, y, w, h = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)[0]
    cx, cy = x + w // 2, y + h // 2

    expanded_w = int(w * zoomout_factor)
    expanded_h = int(h * zoomout_factor)

    x1 = max(0, cx - expanded_w // 2)
    y1 = max(0, cy - expanded_h // 2)
    x2 = min(image.shape[1], cx + expanded_w // 2)
    y2 = min(image.shape[0], cy + expanded_h // 2)

    crop = image[y1:y2, x1:x2]
    return crop_to_aspect(crop, aspect_ratio=3 / 4)


def crop_to_aspect(image: np.ndarray, aspect_ratio=3/4) -> np.ndarray:
    if image is None:
        logging.error("Imagen recibida es None en crop_to_aspect().")
        return None

    h, w = image.shape[:2]
    current_aspect = w / h

    if current_aspect > aspect_ratio:
        new_w = int(h * aspect_ratio)
        x1 = (w - new_w) // 2
        return image[:, x1:x1 + new_w]
    elif current_aspect < aspect_ratio:
        new_h = int(w / aspect_ratio)
        y1 = (h - new_h) // 2
        return image[y1:y1 + new_h, :]
    else:
        return image


def crop_to_4_5(image: np.ndarray) -> np.ndarray:
    return crop_to_aspect(image, aspect_ratio=4 / 5)


def enhance_image(image: np.ndarray) -> np.ndarray:
    logging.debug("Entrando a enhance_image()")

    if image is None:
        logging.error("Imagen es None en enhance_image().")
        return None

    try:
        image = cv2.convertScaleAbs(image, alpha=1.2, beta=15)
        kernel = np.array([[0, -1, 0], [-1, 5.2, -1], [0, -1, 0]])
        return cv2.filter2D(image, -1, kernel)
    except Exception as e:
        logging.error(f"Error al mejorar imagen: {e}")
        return image


def remove_background_mask(frame: np.ndarray) -> np.ndarray:
    logging.debug("Entrando a remove_background_mask()")

    if frame is None or not isinstance(frame, np.ndarray):
        logging.error("Frame inválido en remove_background_mask().")
        return None

    h, w = frame.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)

    center_x, center_y = w // 2, int(h * 0.45)
    axes_length = (int(w * 0.45), int(h * 0.6))

    cv2.ellipse(mask, (center_x, center_y), axes_length, 0, 0, 360, 255, -1)

    if frame.shape[2] == 3:
        frame_rgba = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)
    else:
        frame_rgba = frame.copy()

    frame_rgba[:, :, 3] = mask
    return frame_rgba

#def crop_to_4_5(image, output_size=(800, 1000)):

def crop_to_4_5(image, output_size=(800, 1000)):
    logging.debug("Entrando a crop_to_4_5()")
    h, w = image.shape[:2]
    target_ratio = 4 / 5

    if w / h > target_ratio:
        new_w = int(h * target_ratio)
        new_h = h
    else:
        new_w = w
        new_h = int(w / target_ratio)

    x1 = (w - new_w) // 2
    y1 = (h - new_h) // 2
    cropped = image[y1:y1 + new_h, x1:x1 + new_w]

    if output_size:
        return cv2.resize(cropped, output_size, interpolation=cv2.INTER_AREA)
    return cropped

def draw_guide_cross(frame):
    h, w = frame.shape[:2]
    color = (255, 0, 0)  # Azul en RGB
    thickness = 1

    # Línea horizontal
    cv2.line(frame, (0, h // 2), (w, h // 2), color, thickness)

    # Línea vertical
    cv2.line(frame, (w // 2, 0), (w // 2, h), color, thickness)

    return frame

def detect_available_cameras(max_camaras=3):
    cameras = []
    for i in range(max_camaras):
        cam = cv2.VideoCapture(i)
        if cam.isOpened():
            ret, frame = cam.read()
            if ret:
                cameras.append(i)
            cam.release()
    return cameras