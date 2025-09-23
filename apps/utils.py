import io
from datetime import datetime

import barcode
import treepoem
from barcode.writer import ImageWriter
from PIL import Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader


def generate_datamatrix_image(code: str) -> io.BytesIO:
    img = treepoem.generate_barcode(barcode_type="datamatrix", data=code)
    img = img.convert("RGB")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def generate_code128_png_bytes(
        number: str,
        module_width: float = 0.08,
        module_height: float = 16.0,
        quiet_zone: float = 1.5,
        font_size: int = 6,
        side_padding: int = 2,
        top_padding: int = 1,
        bottom_padding: int = 5,
        scale_x: float = 1.0,
        dpi: int = 300,
) -> io.BytesIO:
    # 1) Generate barcode using python-barcode
    code128 = barcode.get_barcode_class("code128")
    writer = ImageWriter()
    writer_opts = {
        "module_width": module_width,
        "module_height": module_height,
        "quiet_zone": quiet_zone,
        "font_size": 6,  # Small font for internal text (we'll add our own)
        "text_distance": 1,
        "write_text": False,  # We'll add our own text
        "dpi": dpi,
    }

    barcode_obj = code128(str(number), writer=writer)
    tmp_buf = io.BytesIO()
    barcode_obj.write(tmp_buf, options=writer_opts)
    tmp_buf.seek(0)
    bc_img = Image.open(tmp_buf).convert("RGBA")

    # 2) Apply horizontal scaling if needed
    if scale_x != 1.0:
        bw0, bh0 = bc_img.size
        new_bw = max(1, int(bw0 * scale_x))
        bc_img = bc_img.resize((new_bw, bh0), resample=Image.NEAREST)

    # 3) Calculate canvas dimensions
    bw, bh = bc_img.size
    canvas_w = int(bw + side_padding * 2)
    canvas_h = int(top_padding + bh + bottom_padding + font_size + 4)

    # Create white canvas
    canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
    paste_x = side_padding
    paste_y = top_padding

    # 4) Paste barcode onto canvas
    if bc_img.mode == "RGBA":
        canvas.paste(bc_img, (paste_x, paste_y), bc_img)
    else:
        canvas.paste(bc_img, (paste_x, paste_y))

    # 5) Save to BytesIO and return
    out_buf = io.BytesIO()
    canvas.save(out_buf, format="PNG", optimize=True)
    out_buf.seek(0)
    return out_buf


def generate_sticker_58x40(c, product, gs1_code, idx, barcode_img, width, height):
    line1 = gs1_code[0:18]  # 1-qator
    line2 = gs1_code[18:28]  # 2-qator

    # === DataMatrix (chap yuqori) ===
    dm_x, dm_y = 4 * mm, height - 20 * mm
    dm_w, dm_h = 18 * mm, 18 * mm
    dm_buf = generate_datamatrix_image(gs1_code)
    c.drawImage(ImageReader(dm_buf), dm_x, dm_y, width=dm_w, height=dm_h)

    # === GS1 kodni DataMatrix ostida 2 qatorda chiqarish ===
    text_x = dm_x
    c.setFont("DejaVuSans", 4)
    c.drawString(text_x, dm_y - 2 * mm, line1)
    c.drawString(text_x, dm_y - 5 * mm, line2)

    # === Product ma’lumotlari (DataMatrix yonida, chap yuqorida) ===
    c.setFont("DejaVuSans-Bold", 6)
    c.drawString(24 * mm, height - 6 * mm, f"Артикул: {getattr(product, 'article', '')}")
    c.drawString(24 * mm, height - 12 * mm, f"Размер: {product.size}")
    c.drawString(24 * mm, height - 18 * mm, f"Цвет: {product.color}")

    # === Barcode (past o‘ngda) ===
    barcode_width, barcode_height = 35 * mm, 10 * mm
    c.drawImage(
        barcode_img,
        width - barcode_width - 4 * mm,
        4 * mm,
        width=barcode_width,
        height=barcode_height
    )
    c.setFont("DejaVuSans", 5)
    c.drawCentredString(width - (barcode_width / 2) - 4 * mm, 2 * mm, str(product.barcode))

    # === Sticker tartib raqami (past chapda) ===
    c.setFont("DejaVuSans", 10)
    c.drawString(8 * mm, 8 * mm, str(idx))

    c.showPage()


def generate_sticker_70x40(c, product, gs1_code, idx, barcode_img, width, height):
    line1 = gs1_code[0:18]  # 1-qator
    line2 = gs1_code[18:28]  # 2-qator

    # === DataMatrix (chap yuqori) ===
    dm_x, dm_y = 2 * mm, height - 20 * mm  # biroz pastroqqa tushirildi
    dm_w, dm_h = 18 * mm, 18 * mm  # kattaroq qildik (70 mm kenglikda)
    dm_buf = generate_datamatrix_image(gs1_code)
    c.drawImage(ImageReader(dm_buf), dm_x, dm_y, width=dm_w, height=dm_h)

    # === GS1 kodni DataMatrix ostida 2 qatorda chiqarish ===
    text_x = dm_x
    c.setFont("DejaVuSans", 4.5)
    c.drawString(text_x, dm_y - 2.5 * mm, line1)
    c.drawString(text_x, dm_y - 5.5 * mm, line2)

    # === Product ma’lumotlari (DataMatrix yonida, chap yuqorida) ===
    info_x = dm_x + dm_w + 5 * mm
    top_y = height - 6 * mm

    c.setFont("DejaVuSans-Bold", 8)
    c.drawString(info_x, top_y, f"{getattr(product, 'name', '')}")

    c.setFont("DejaVuSans-Bold", 7.5)
    c.drawString(info_x, top_y - 4 * mm, f"Артикул:  {getattr(product, 'article', '')}")
    c.drawString(info_x, top_y - 8 * mm, f"Цвет:     {product.color}")
    c.drawString(info_x, top_y - 12 * mm, f"Размер:   {product.size}")
    c.drawString(info_x, top_y - 16 * mm, f"Бренд:    {getattr(product, 'brand', '')}")

    # === Barcode (past o‘ngda) ===
    barcode_width, barcode_height = 35 * mm, 10 * mm
    c.drawImage(
        barcode_img,
        width - barcode_width - 6 * mm,
        6 * mm,
        width=barcode_width,
        height=barcode_height
    )
    c.setFont("DejaVuSans", 5.5)
    c.drawCentredString(width - (barcode_width / 2) - 4 * mm, 3 * mm, str(product.barcode))

    # === Sticker tartib raqami (past chapda) ===
    c.setFont("DejaVuSans", 15)
    c.drawString(6 * mm, 6 * mm, str(idx))

    c.showPage()


def generate_sticker_100x50(c, product, gs1_code, idx, barcode_img, width, height):
    line1 = gs1_code[0:18]
    line2 = gs1_code[18:28]
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = "DejaVuSans"
    style.fontSize = 6
    # === Product title (top left) ===
    c.setFont("DejaVuSans-Bold", 10)
    c.drawString(6 * mm, height - 5 * mm, product.name)

    # === Article and Size (top right) ===
    c.setFont("DejaVuSans", 7)
    c.drawString(width - 55 * mm, height - 15 * mm, f"Размер: {product.size}")
    c.drawString(width - 55 * mm, height - 11 * mm, f"Состав: {product.material}")

    # === Index number (top right corner) ===
    c.setFont("DejaVuSans", 15)
    c.drawCentredString(width - 9 * mm, height - 12 * mm, f"{idx}")

    # === Color and Material (left side, below title) ===
    c.setFont("DejaVuSans", 7)
    c.drawString(6 * mm, height - 11 * mm, f"Арт.: {product.article}")
    c.drawString(6 * mm, height - 14 * mm, f"Цвет: {product.color}")

    # === Barcode (left side, middle) ===
    barcode_width, barcode_height = 45 * mm, 12 * mm
    c.drawImage(
        barcode_img,
        6 * mm,
        height - 28 * mm,
        width=barcode_width,
        height=barcode_height
    )
    # Barcode number below
    c.setFont("DejaVuSans", 6)
    c.drawString(14 * mm, height - 29 * mm, str(product.barcode))

    # === Manufacturer info (left side, bottom) ===
    c.setFont("DejaVuSans", 6)
    c.drawString(6 *mm , 15*mm, f"ИЗГОТОВИТЕЛЬ: {product.manufacture} {product.region}")
    c.drawString(6 * mm , 12*mm,  f"{product.city} {product.street_and_home}")
    # === DataMatrix (right side, center) ===
    dm_x, dm_y = width - 30 * mm, height - 42 * mm
    dm_w, dm_h = 24 * mm, 24 * mm
    dm_buf = generate_datamatrix_image(gs1_code)
    c.drawImage(ImageReader(dm_buf), dm_x, dm_y, width=dm_w, height=dm_h)

    # === GS1 code (below DataMatrix, right side) ===
    c.setFont("DejaVuSans", 6)
    c.drawString(dm_x, dm_y - 3 * mm, line1)
    c.drawString(dm_x, dm_y - 5 * mm, line2)

    # === EAC mark (bottom left) ===
    c.setFont("DejaVuSans-Bold", 8)
    c.drawString(5 * mm, 6 * mm, "EAC")

    # === Additional info (bottom center-right) ===
    today = datetime.now()
    month_year = today.strftime("%m.%Y")

    c.setFont("DejaVuSans", 6)
    c.drawString(15 * mm, 8 * mm, "Информация на данном стикере приоритетна")
    c.drawString(15 * mm, 6 * mm, f"Дата изготовления: {month_year}г")
    c.drawString(15 * mm, 4 * mm, "Срок годности не ограничен")
    c.drawString(15 * mm, 2 * mm, "Хранить в сухом месте")

    c.showPage()
