import os
from io import BytesIO
from django.http import FileResponse
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor, black
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import Image

def gerar_pdf(resultado):
    """Gera um PDF com layout aprimorado e título reposicionado."""
    # Registrar fontes Roboto
    font_path = os.path.join(settings.STATIC_ROOT, 'core', 'fonts')
    pdfmetrics.registerFont(TTFont('Roboto', os.path.join(font_path, 'Roboto-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('Roboto-Bold', os.path.join(font_path, 'Roboto-Bold.ttf')))
    pdfmetrics.registerFont(TTFont('Roboto-Italic', os.path.join(font_path, 'Roboto-Italic.ttf')))

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    page_width, page_height = A4

    # Caminho para os recursos
    logo_path = os.path.join(settings.STATIC_ROOT, 'core', 'imagens', 'logo.png')

    if not os.path.exists(logo_path):
        raise FileNotFoundError(f"Logo não encontrado em: {logo_path}")

    # Cabeçalho com fundo cinza claro
    header_height = 150
    c.setFillColor(HexColor("#f7f7f7"))
    c.rect(0, page_height - header_height, page_width, header_height, fill=1, stroke=0)

    # Adicionar o logo centralizado no cabeçalho, mantendo a proporção
    logo = ImageReader(logo_path)
    original_width, original_height = logo.getSize()
    max_width = 240  # Limite de largura
    max_height = 160  # Limite de altura

    # Calcula proporção para manter o aspecto
    aspect_ratio = original_width / original_height
    if original_width > max_width:
        final_width = max_width
        final_height = max_width / aspect_ratio
    if final_height > max_height:
        final_height = max_height
        final_width = max_height * aspect_ratio

    logo_x = (page_width - final_width) / 2  # Centraliza horizontalmente
    logo_y = page_height - header_height + (header_height - final_height) / 2  # Centraliza verticalmente
    c.drawImage(logo, logo_x, logo_y, width=final_width, height=final_height, mask='auto')

    # Título centralizado no cabeçalho abaixo do logo
    c.setFont("Roboto-Bold", 18)
    c.setFillColor(black)
    c.drawCentredString(page_width / 2, page_height - header_height - 20, "Relatório de Resultado")

    # Informações do resultado
    c.setFont("Roboto-Bold", 12)
    text_y = page_height - header_height - 80
    c.drawString(50, text_y, "QR Code:")
    c.setFont("Roboto", 12)
    c.drawString(150, text_y, resultado.qr_value)

    text_y -= 20
   
    c.drawString(50, text_y, "ID Entrada:")
    c.setFont("Roboto", 12)
    c.drawString(150, text_y, resultado.id_entrada)

    text_y -= 20
    c.setFont("Roboto-Bold", 12)
    c.drawString(50, text_y, "Data e Hora:")
    c.setFont("Roboto", 12)
    c.drawString(150, text_y, resultado.data_hora.strftime('%d/%m/%Y %H:%M'))

    text_y -= 20
    c.setFont("Roboto-Bold", 12)
    c.drawString(50, text_y, "Informação:")
    c.setFont("Roboto", 12)
    c.drawString(150, text_y, resultado.informacao)

    text_y -= 20
    c.setFont("Roboto-Bold", 12)
    c.drawString(50, text_y, "Máximo de Padrões:")
    c.setFont("Roboto", 12)
    c.drawString(200, text_y, str(resultado.max_padroes))

    # Adicionar imagem do resultado (se disponível)
    if resultado.imagem:
        img = Image.open(BytesIO(resultado.imagem))
        img_width, img_height = img.size
        max_width = 400
        max_height = 300
        aspect_ratio = img_width / img_height
        if img_width > max_width:
            img_width = max_width
            img_height = max_width / aspect_ratio
        if img_height > max_height:
            img_height = max_height
            img_width = max_height * aspect_ratio

        img_byte_stream = BytesIO()
        img.save(img_byte_stream, format="JPEG")
        img_byte_stream.seek(0)
        c.drawImage(
            ImageReader(img_byte_stream),
            (page_width - img_width) / 2,
            text_y - img_height - 50,
            width=img_width,
            height=img_height
        )

    # Rodapé com divisória
    footer_height = 40
    c.setLineWidth(1)
    c.setStrokeColor(HexColor("#dddddd"))
    c.line(0, footer_height, page_width, footer_height)
    c.setFont("Roboto-Italic", 10)
    c.drawCentredString(page_width / 2, 20, "© 2024 GS Auditor - Documento gerado automaticamente.")

    c.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"Relatorio_{resultado.qr_value}.pdf")
