import os
from pdf2image import convert_from_path
from PIL import Image, ImageFilter
from fpdf import FPDF
import argparse
import tempfile
import fitz
import io

# Convert PDF to images
def convert_pdf_to_images(pdf_path, output_folder, dpi):
    pages = convert_from_path(pdf_path, dpi)

    image_paths = []
    for i, page in enumerate(pages):
        image_path = os.path.join(output_folder, f"page_{i}.png")
        page.save(image_path, 'PNG')
        image_paths.append(image_path)    
    return image_paths

#def convert_images_to_pdf(image_paths, output_pdf):
#    pdf = FPDF(orientation='L', unit='mm', format=(90, 160))
#    #pdf.set_auto_page_break(auto=True, margin=15)
#
#    for image_path in image_paths:
#        image = Image.open(image_path)
#        pdf.add_page()
#        pdf.image(image_path, 0, 0, 160, 90)
#    
#    pdf.output(output_pdf)

def apply_blur_to_pixmap(pixmap, blur_radius=10):
    # Convert the Pixmap to a Pillow image (PIL)
    pil_image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)    
    pil_image = pil_image.filter(ImageFilter.GaussianBlur(blur_radius))       
    img_byte_arr = io.BytesIO()
    pil_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)    
    new_pixmap = fitz.Pixmap(img_byte_arr)    
    return new_pixmap

def merge_pdfs(input_pdf, magic_text, image_paths, output_pdf):
    document = fitz.open(input_pdf)    

    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text = page.get_text("text")

        if magic_text in text.lower():

            # load image:
            img = fitz.Pixmap(image_paths[page_num])
            #img = apply_blur_to_pixmap(img, 20)
            page_width = page.rect.width
            page_height = page.rect.height

            # replace page
            document.delete_page(page_num)
            new_page = document.new_page(page_num, page_width, page_height)
            new_page.insert_image(new_page.rect, pixmap=img)

    # Save compressed    
    document.ez_save(output_pdf)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process input and output PDF files.')
    parser.add_argument('--dpi', type=int, default=300, help='DPI for image conversion')
    parser.add_argument('--magic', type=str, default="do not copy and paste code", help="the magic words to replace slides")
    parser.add_argument('input_pdf', type=str, help='Input PDF file')
    args = parser.parse_args()

    # Run Conversion
    with tempfile.TemporaryDirectory() as temp_dir:
        pdf_path = args.input_pdf        
        output_pdf = pdf_path[:-4] + '_nocopy.pdf'

        #output_folder = 'image'
        #output_pdf = 'result/cpp_workshop.pdf'
        image_paths = convert_pdf_to_images(pdf_path, temp_dir, args.dpi)        
        merge_pdfs(pdf_path, args.magic, image_paths, output_pdf)