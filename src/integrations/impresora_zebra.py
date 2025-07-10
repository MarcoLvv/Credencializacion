import os
import tempfile
import time
from pathlib import Path

from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

from src.utils.rutas import get_temp_credencial_dir

# import win32api
# import win32print
# import subprocess
#
# # === CONFIGURACIÓN ===
# NOMBRE_IMPRESORA_ZEBRA = "Zebra ZC300 USB Card Printer"
TEMP_DIR = get_temp_credencial_dir()
# Path(TEMP_DIR).mkdir(exist_ok=True)
#
CR80_SIZE = (85.6 * mm, 53.98 * mm)  # Tamaño tarjeta CR80 en puntos
#
#
# def verificar_estado_impresora():
#   """Verifica si la impresora está disponible y en línea"""
#   try:
#     # Obtener lista de impresoras
#     impresoras = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
#
#     for impresora in impresoras:
#       if NOMBRE_IMPRESORA_ZEBRA in impresora[2]:
#         # Abrir impresora para verificar estado
#         handle = win32print.OpenPrinter(impresora[2])
#         try:
#           # Obtener atributos de la impresora
#           atributos = win32print.GetPrinter(handle, 2)
#           estado = atributos['Status']
#
#           print(f"[INFO] Estado de la impresora: {estado}")
#
#           # Verificar si está en línea
#           if estado == 0:  # 0 = impresora lista
#             print("[INFO] Impresora está en línea y lista")
#             return True
#           else:
#             print(f"[WARNING] Impresora tiene problemas. Estado: {estado}")
#             return False
#
#         finally:
#           win32print.ClosePrinter(handle)
#
#     print(f"[ERROR] No se encontró la impresora '{NOMBRE_IMPRESORA_ZEBRA}'")
#     return False
#
#   except Exception as e:
#     print(f"[ERROR] Error verificando estado de impresora: {e}")
#     return False
#
#
def generar_pdf_doble_cara(frente_path, reverso_path):
    """Genera PDF de 2 páginas con fondo blanco y contenido completo"""
    from reportlab.lib.units import mm

    os.makedirs(TEMP_DIR, exist_ok=True)
    pdf_path = os.path.join(TEMP_DIR, "credencial_doble_cara.pdf")

    # Aplicar bordes redondeados a ambas imágenes
    frente_path_rounded = frente_path
    reverso_path_rounded = reverso_path

    c = canvas.Canvas(pdf_path, pagesize=CR80_SIZE)

    # Página 1: Frontal
    c.setFillColorRGB(1, 1, 1)  # Fondo blanco
    c.rect(0, 0, CR80_SIZE[0], CR80_SIZE[1], stroke=0, fill=1)
    c.drawImage(frente_path_rounded, 0, 0, width=CR80_SIZE[0], height=CR80_SIZE[1])
    c.showPage()

    # Página 2: Reverso
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, CR80_SIZE[0], CR80_SIZE[1], stroke=0, fill=1)
    c.drawImage(reverso_path_rounded, 0, 0, width=CR80_SIZE[0], height=CR80_SIZE[1])
    c.showPage()

    c.save()

    print(f"[OK] PDF generado correctamente en: {pdf_path}")
    return pdf_path

#
#
# def aplicar_mascara_redondeada(imagen_path, radio=40):
#   img = Image.open(imagen_path).convert("RGBA")
#   w, h = img.size
#
#   # Crear máscara con esquinas redondeadas
#   mask = Image.new("L", (w, h), 0)
#   draw = ImageDraw.Draw(mask)
#   draw.rounded_rectangle((0, 0, w, h), radius=radio, fill=255)
#
#   # Aplicar máscara a la imagen original
#   img.putalpha(mask)
#
#   # Fondo blanco detrás para eliminar transparencia (si usas reportlab)
#   fondo_blanco = Image.new("RGB", (w, h), (255, 255, 255))
#   fondo_blanco.paste(img, mask=img.split()[3])  # Usar canal alfa como máscara
#
#   # Guardar temporal
#   temp_path = imagen_path.replace(".png", "_rounded.jpg")
#   fondo_blanco.save(temp_path, format="JPEG", quality=100)
#   return temp_path
#
#
# def imprimir_con_win32print(pdf_path):
#   """Método alternativo usando win32print directamente"""
#   try:
#     # Abrir impresora
#     handle = win32print.OpenPrinter(NOMBRE_IMPRESORA_ZEBRA)
#
#     try:
#       # Iniciar trabajo de impresión
#       job_id = win32print.StartDocPrinter(handle, 1, ("Credencial", None, "RAW"))
#
#       # Leer archivo PDF
#       with open(pdf_path, 'rb') as f:
#         pdf_data = f.read()
#
#       # Enviar datos
#       win32print.StartPagePrinter(handle)
#       win32print.WritePrinter(handle, pdf_data)
#       win32print.EndPagePrinter(handle)
#       win32print.EndDocPrinter(handle)
#
#       print("[OK] Impresión enviada usando win32print")
#       return True
#
#     finally:
#       win32print.ClosePrinter(handle)
#
#   except Exception as e:
#     print(f"[ERROR] Falló impresión con win32print: {e}")
#     return False
#
#
# def imprimir_con_subprocess(pdf_path):
#   """Método alternativo usando subprocess y Adobe Reader/Acrobat"""
#   try:
#     # Buscar Adobe Reader o Acrobat
#     adobe_paths = [
#       r"C:\Program Files\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
#       r"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
#       r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe",
#       r"C:\Program Files (x86)\Adobe\Acrobat DC\Acrobat\Acrobat.exe"
#     ]
#
#     adobe_exe = None
#     for path in adobe_paths:
#       if os.path.exists(path):
#         adobe_exe = path
#         break
#
#     if adobe_exe:
#       # Usar Adobe Reader para imprimir
#       cmd = [adobe_exe, "/t", pdf_path, NOMBRE_IMPRESORA_ZEBRA]
#       subprocess.run(cmd, check=True)
#       print("[OK] Impresión enviada usando Adobe Reader")
#       return True
#     else:
#       # Usar comando de Windows
#       cmd = ["print", f"/D:{NOMBRE_IMPRESORA_ZEBRA}", pdf_path]
#       subprocess.run(cmd, shell=True, check=True)
#       print("[OK] Impresión enviada usando comando print de Windows")
#       return True
#
#   except Exception as e:
#     print(f"[ERROR] Falló impresión con subprocess: {e}")
#     return False
#
#
# def reiniciar_cola_impresion():
#   """Reinicia la cola de impresión de la impresora"""
#   try:
#     # Pausar cola
#     subprocess.run(["net", "stop", "spooler"], capture_output=True)
#     time.sleep(2)
#
#     # Reiniciar cola
#     subprocess.run(["net", "start", "spooler"], capture_output=True)
#     time.sleep(3)
#
#     print("[INFO] Cola de impresión reiniciada")
#     return True
#
#   except Exception as e:
#     print(f"[ERROR] No se pudo reiniciar cola de impresión: {e}")
#     return False
#
#
# def imprimir_credencial_zebra_pdf(frente_path, reverso_path):
#   """Función principal mejorada para imprimir credenciales"""
#   try:
#     # Verificar que las imágenes existen
#     if not os.path.exists(frente_path):
#       raise FileNotFoundError(f"No se encontró la imagen frontal: {frente_path}")
#
#     if not os.path.exists(reverso_path):
#       raise FileNotFoundError(f"No se encontró la imagen trasera: {reverso_path}")
#
#     # Generar PDF
#     pdf_path = generar_pdf_doble_cara(frente_path, reverso_path)
#     print(f"[INFO] PDF generado en: {pdf_path}")
#
#     # Verificar estado de la impresora
#     if not verificar_estado_impresora():
#       print("[WARNING] Problemas detectados con la impresora, intentando reiniciar cola...")
#       reiniciar_cola_impresion()
#       time.sleep(5)  # Esperar a que se reinicie
#
#     # Intentar varios métodos de impresión
#     print("[INFO] Intentando método 1: ShellExecute...")
#     try:
#       result = win32api.ShellExecute(
#         0,
#         "printto",
#         pdf_path,
#         f'"{NOMBRE_IMPRESORA_ZEBRA}"',
#         ".",
#         0
#       )
#
#       if result > 32:
#         print("[OK] Método 1 exitoso: PDF enviado usando ShellExecute")
#         return True
#       else:
#         print(f"[ERROR] ShellExecute falló con código: {result}")
#
#     except Exception as e:
#       print(f"[ERROR] ShellExecute falló: {e}")
#
#     print("[INFO] Intentando método 2: win32print...")
#     if imprimir_con_win32print(pdf_path):
#       return True
#
#     print("[INFO] Intentando método 3: subprocess...")
#     if imprimir_con_subprocess(pdf_path):
#       return True
#
#     # Si todos los métodos fallan
#     print("[ERROR] Todos los métodos de impresión fallaron")
#     print("[SUGERENCIA] Verifica:")
#     print("1. Que la impresora esté encendida y conectada")
#     print("2. Que tenga tarjetas de PVC disponibles")
#     print("3. Que los drivers estén actualizados")
#     print("4. Que no haya trabajos de impresión bloqueados en la cola")
#
#     return False
#
#   except Exception as e:
#     print(f"[ERROR] Error general en impresión: {e}")
#     return False
#
#
# # === FUNCIONES DE DIAGNÓSTICO ===
#
# def diagnosticar_impresora():
#   """Función de diagnóstico completa"""
#   print("=== DIAGNÓSTICO DE IMPRESORA ZEBRA ===")
#
#   # 1. Verificar si está en la lista de impresoras
#   try:
#     impresoras = [p[2] for p in
#                   win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)]
#     print(f"Impresoras disponibles: {impresoras}")
#
#     if NOMBRE_IMPRESORA_ZEBRA in impresoras:
#       print(f"✓ Impresora '{NOMBRE_IMPRESORA_ZEBRA}' encontrada")
#     else:
#       print(f"✗ Impresora '{NOMBRE_IMPRESORA_ZEBRA}' NO encontrada")
#       return False
#
#   except Exception as e:
#     print(f"✗ Error listando impresoras: {e}")
#     return False
#
#   # 2. Verificar estado detallado
#   verificar_estado_impresora()
#
#   # 3. Verificar cola de impresión
#   try:
#     handle = win32print.OpenPrinter(NOMBRE_IMPRESORA_ZEBRA)
#     try:
#       jobs = win32print.EnumJobs(handle, 0, -1, 1)
#       print(f"Trabajos en cola: {len(jobs)}")
#       for job in jobs:
#         print(f"  - Trabajo: {job['pDocument']}, Estado: {job['Status']}")
#     finally:
#       win32print.ClosePrinter(handle)
#   except Exception as e:
#     print(f"Error verificando cola: {e}")
#
#   return True

#
# # === EJEMPLO DE USO ===
# if __name__ == "__main__":
# 	# Ejecutar diagnóstico
# 	diagnosticar_impresora()
#
# 	# Ejemplo de impresión (descomenta para usar)
# 	# frente = "ruta/a/imagen_frente.png"
# 	# reverso = "ruta/a/imagen_reverso.png"
# 	# imprimir_credencial_zebra_pdf(frente, reverso)