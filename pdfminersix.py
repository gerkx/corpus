# from io import StringIO, BytesIO

# from pdfminer.converter import TextConverter, HTMLConverter, PDFConverter
# from pdfminer.layout import LAParams
# from pdfminer.pdfdocument import PDFDocument
# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.pdfpage import PDFPage
# from pdfminer.pdfparser import PDFParser

# from pdfminer import high_level as hl

# output_string = StringIO()
# beep = ""
# with open('samples/pdf/Ainsworth_2004_CDA.pdf', 'rb') as in_file:
#     parser = PDFParser(in_file)
#     doc = PDFDocument(parser)
#     rsrcmgr = PDFResourceManager()
#     # device = TextConverter(rsrcmgr, output_string, laparams=LAParams(detect_vertical=True, all_texts=True))
#     device = TextConverter(rsrcmgr=rsrcmgr, outfp=output_string, laparams=LAParams())
#     interpreter = PDFPageInterpreter(rsrcmgr, device)
#     for idx, page in enumerate(PDFPage.create_pages(doc)):
#         if idx == 2:
#             interpreter.process_page(page)

# print(output_string.getvalue())

# print(hl.extract_pages('samples/pdf/Ainsworth_2004_CDA.pdf'))
# print(hl.extract_text('samples/pdf/Ainsworth_2004_CDA.pdf'))
# print(hl.extract_text_to_fp(inf='samples/pdf/Ainsworth_2004_CDA.pdf', outfp=output_string, output_type='tag'))

from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator

import pytesseract
from PIL import Image as IMG

import os.path as path

from pdf2image import convert_from_path, convert_from_bytes

fp = open('samples/pdf/hospitality.pdf', 'rb')
rsrcmgr = PDFResourceManager()
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
pages = PDFPage.get_pages(fp)

texto = []

for idx, page in enumerate(pages):
    if idx == 1:
        print('Processing next page...')
        interpreter.process_page(page)
        layout = device.get_result()
        for idx, lobj in enumerate(layout):
            if isinstance(lobj, LTTextBox) and lobj.index ==  0:
                texto.append({
                    "text": lobj.get_text(),
                    "bbox": lobj.bbox
                })
                # x, y, text = lobj.bbox[0], lobj.bbox[3], lobj.get_text()
                # print(lobj)

                # print('At %r is text: %s' % ((x, y), text))
#####################################
# pdf_path = path.join(path.dirname(__file__), 'samples/pdf/hospitality.pdf')
# pdf = convert_from_path(
#     pdf_path=pdf_path, 
#     dpi=350, poppler_path="F:\\_Code\\pop\\bin", 
#     first_page = 2, last_page = 2, 
#     fmt="png",
#     # output_folder = path.join(path.dirname(__file__), 'samples/pdf'),
#     # output_file = "boop"
# )[0]
################################################################
# print(texto)
pdf = path.join(path.dirname(__file__), 'samples/pdf/boop0001-2.png')

pytesseract.pytesseract.tesseract_cmd = "F:\\_Code\\tes\\tesseract.exe"

pdfImg = IMG.open(pdf)
pdfImgDimensions = pdfImg.size
pdfImgDPI = pdfImg.info['dpi']

def points_to_pixels(pt_val, dpi):
    return pt_val * (dpi/72.0)

def create_crop_box(bbox, pil_img):
    img_dim = pil_img.size
    img_dpi = pil_img.info['dpi']
    bounds = [points_to_pixels(bound, img_dpi[0]) for bound in bbox]
    rect = [
        bounds[0],
        img_dim[1] - bounds[3],
        bounds[2],
        img_dim[1] - bounds[1] ,
    ]
    return rect



crop_box = create_crop_box(texto[0]['bbox'], pdfImg)
sample01 = pdfImg.crop(crop_box)

txt = pytesseract.image_to_string(sample01)
print(txt)