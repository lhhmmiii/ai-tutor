import os

os.environ["TESSDATA_PREFIX"] = "/usr/share/tesseract-ocr/4.00/tessdata"
import fitz


def get_tessocr(page, bbox):
    """Return OCR-ed span text using Tesseract.

    Args:
        page: fitz.Page
        bbox: fitz.Rect or its tuple
    Returns:
        The OCR-ed text of the bbox.
    """
    mat = fitz.Matrix(5, 5)
    # Step 1: Make a high-resolution image of the bbox.
    pix = page.get_pixmap(matrix=mat, clip=bbox)
    ocrpdf = fitz.open("pdf", pix.pdfocr_tobytes())
    ocrpage = ocrpdf[0]
    text = ocrpage.get_text()
    if text.endswith("\n"):
        text = text[:-1]
    return text


def extract_text_and_bbox(blocks):
    res = {"bbox": [], "text": []}
    for b in blocks:
        for line in b["lines"]:
            for s in line["spans"]:
                res["bbox"].append(s["bbox"])
                res["text"].append(s["text"])

    return res


def is_two_column_page(res, width, threshold):
    left_count = 0
    right_count = 0

    for bbox, text in zip(res["bbox"], res["text"], strict=False):
        text = text.replace(" ", "")
        text = text.replace(",", "")
        if text.isdigit() or len(text) == 1:
            continue
        if bbox[0] > width / 2:
            right_count += 1
        elif bbox[2] < width / 2:
            left_count += 1

    if left_count == 0 or right_count == 0:
        return False

    ratio = min(left_count, right_count) / max(left_count, right_count)

    return ratio > threshold


def is_scan_page(page):
    text = page.get_text()
    return text == ""


def is_two_column_paper(doc):
    num_page = len(doc)
    num_two_column_page = 0
    list_res = []
    for page in doc:
        width = page.rect.width
        blocks = page.get_text("dict", flags=0)["blocks"]
        res = extract_text_and_bbox(blocks)
        list_res.append(res)
        is_two_column = is_two_column_page(res, width, 0.7)
        if is_two_column:
            num_two_column_page += 1
    if num_two_column_page / num_page > 0.6 or num_page - num_two_column_page == 2:
        return True, list_res
    return False, list_res
