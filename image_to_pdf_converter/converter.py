from PIL import Image
import os
import re

def images_to_pdf(image_folder, output_pdf_path):
    # List to hold image objects
    image_list = []

    # Get all image files in the folder
    image_files = [
        f for f in os.listdir(image_folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]

    # Enhanced natural sort key
    def natural_sort_key(filename):
        return [
            int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', filename)
        ]

    sorted_files = sorted(image_files, key=natural_sort_key)

    # Load images
    for file_name in sorted_files:
        image_path = os.path.join(image_folder, file_name)
        try:
            img = Image.open(image_path).convert('RGB')
            image_list.append(img)
            print(f"Loaded image: {file_name}")
        except Exception as e:
            print(f"Error loading {file_name}: {e}")

    if not image_list:
        print("No images found in the folder.")
        return

    # Save images as a single PDF file
    first_image = image_list.pop(0)
    first_image.save(
        output_pdf_path, "PDF", resolution=100.0, save_all=True, append_images=image_list
    )

    print(f"Successfully saved images to {output_pdf_path}")

# Example usage:
image_folder = r'C:\Users\titil\Downloads\Programs\converted'   # Replace with the path to your images
output_pdf = r'C:\Users\titil\Downloads\Programs\converted\output_file10.pdf'               # Specify output PDF file name

images_to_pdf(image_folder, output_pdf)
