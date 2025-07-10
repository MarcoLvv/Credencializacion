# import os
# import tempfile
# from reportlab.lib.units import mm
# from reportlab.pdfgen import canvas
#
# CR80_SIZE = (85.6 * mm, 53.98 * mm)  # tamaño tarjeta CR80
#
# def generar_pdf_doble_cara(frente_path, reverso_path):
#     pdf_path = os.path.join(tempfile.gettempdir(), "credencial_doble_cara.pdf")
#     c = canvas.Canvas(pdf_path, pagesize=CR80_SIZE)
#
#     c.drawImage(frente_path, 0, 0, width=CR80_SIZE[0], height=CR80_SIZE[1])
#     c.showPage()
#     c.drawImage(reverso_path, 0, 0, width=CR80_SIZE[0], height=CR80_SIZE[1])
#     c.save()
#     print(f"[INFO] PDF generado en: {pdf_path}")
#     return pdf_path
