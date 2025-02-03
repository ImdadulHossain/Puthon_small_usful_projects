import os
from PIL import Image
from tqdm import tqdm
import argparse

'''
# Command-line interface argument parsing
parser = argparse.ArgumentParser(description='Convert WebP images to JPEG or PNG')
parser.add_argument('input_folder', help='Path to the folder containing WebP images')
parser.add_argument('output_folder', help='Path to the output folder')
parser.add_argument('output_format', choices=['JPEG', 'PNG'], help='Output format: JPEG or PNG')

args = parser.parse_args()'''

# In your function:
# For progress Bar
#for filename in tqdm(os.listdir(input_folder)):

def convert_webp_to_jpg_or_png(input_folder, output_folder, output_format):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder at: {output_folder}")
    else:
        print(f"Using existing output folder at: {output_folder}")

    # Iterate over files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.webp'):
            input_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + '.' + output_format.lower()
            output_path = os.path.join(output_folder, output_filename)

            try:
                with Image.open(input_path) as img:
                    img = img.convert("RGB")
                    img.save(output_path, format=output_format.upper())
                    print(f"Converted {filename} to {output_filename}")
            except Exception as e:
                print(f"Failed to convert {filename}: {e}")

# Example usage:
input_folder = r'C:\Users\titil\Downloads\Programs\AI GENERATED'  # Replace with the path to your folder containing WebP images
output_folder = r'C:\Users\titil\Downloads\Programs\converted'  # Replace with your desired output folder name

# Choose output format: 'JPEG' or 'PNG'
output_format = 'JPEG'

#convert_webp_to_jpg_or_png(input_folder, output_folder, output_format)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert WebP images to JPG or PNG.')
    parser.add_argument('input_folder', help='Folder containing WebP images')
    parser.add_argument('output_folder', help='Folder to save converted images')
    parser.add_argument('output_format', choices=['JPEG', 'PNG'], help='Desired output format')
    args = parser.parse_args()

    convert_webp_to_jpg_or_png(args.input_folder, args.output_folder, args.output_format)

