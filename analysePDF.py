import pdftotext
import pytesseract
import pdf2image
import tempfile
import os
from PIL import Image
from modeldb import *


def processPDF(pdfFile):

    ocrTextExraction(pdfFile)


    return None

def ocrTextExraction(f):
    path = f.path


    print(f.name)


    tempTextDir = tempfile.TemporaryDirectory
    page_counter = 1
    filepages = Page.query.filter_by(id_pdf=f.id).all()
    print(filepages)
    if len(filepages) == 0:
        print("Converting PDF to image...")
        print("path: " + str(path))
        pages = pdf2image.convert_from_path(path, 500)
        print(len(pages))

        tempImageDir = tempfile.TemporaryDirectory
        print("Temp directory after change:", tempfile.gettempdir())

        for page in pages:
            imageFilename = str(tempImageDir) +"page_" + str(page_counter) + ".jpg"
            page.save(imageFilename,'JPEG')
            textFileName = str("/Users/jeff/PycharmProjects/Annotator/uploads/texts/") +"text_page_" + str(page_counter) +"_"+str(f.id)+ ".txt"
            tf = open(textFileName,'w')
            text= str(((pytesseract.image_to_string(Image.open(imageFilename)))))
            print("text",text)
            tf.write(text)
            tf.close()
            filepage = Page(number=page_counter, path=textFileName)
            filepage.id_pdf=f.id
            db.session.add(filepage)
            db.session.commit()
            page_counter = page_counter + 1



    return None