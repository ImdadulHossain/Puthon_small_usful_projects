import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def images_to_pdf(image_folder, output_pdf_path):
    image_list = []

    # Get all image files in the folder, now including .webp files
    image_files = [
        f for f in os.listdir(image_folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
    ]

    # Enhanced natural sort key with raw string
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
            with Image.open(image_path) as img:
                # Handle images with alpha channel (transparency)
                if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                    # Create a white background
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    img = img.convert("RGBA")
                    background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
                    img = background
                else:
                    img = img.convert('RGB')
                image_list.append(img.copy())
                print(f"Loaded image: {file_name}")
        except Exception as e:
            print(f"Error loading {file_name}: {e}")

    if not image_list:
        messagebox.showwarning("No Images Found", "No JPG, PNG, or WEBP images were found in the selected folder.")
        return

    # Save images as a single PDF file
    first_image = image_list.pop(0)
    first_image.save(
        output_pdf_path, "PDF", resolution=100.0, save_all=True, append_images=image_list
    )

    messagebox.showinfo("Success", f"PDF file has been created at:\n{output_pdf_path}")

def browse_image_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        image_folder_path.set(folder_selected)

def browse_output_file():
    file_selected = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        initialfile="output.pdf"
    )
    if file_selected:
        output_file_path.set(file_selected)

def start_conversion():
    in_folder = image_folder_path.get()
    out_file = output_file_path.get()

    if not in_folder or not out_file:
        messagebox.showwarning("Missing Information", "Please select both image folder and output PDF file.")
        return

    images_to_pdf(in_folder, out_file)

# Main application window
root = tk.Tk()
root.title("Images to PDF Converter")
root.geometry("500x300")
root.resizable(False, False)

# Variables to hold folder paths
image_folder_path = tk.StringVar()
output_file_path = tk.StringVar()

# Image Folder Selection
image_frame = tk.Frame(root)
image_frame.pack(pady=10)

image_label = tk.Label(image_frame, text="Image Folder:")
image_label.pack(side=tk.LEFT)

image_entry = tk.Entry(image_frame, textvariable=image_folder_path, width=40)
image_entry.pack(side=tk.LEFT, padx=5)

image_button = tk.Button(image_frame, text="Browse", command=browse_image_folder)
image_button.pack(side=tk.LEFT)

# Output PDF File Selection
output_frame = tk.Frame(root)
output_frame.pack(pady=10)

output_label = tk.Label(output_frame, text="Output PDF File:")
output_label.pack(side=tk.LEFT)

output_entry = tk.Entry(output_frame, textvariable=output_file_path, width=40)
output_entry.pack(side=tk.LEFT, padx=5)

output_button = tk.Button(output_frame, text="Browse", command=browse_output_file)
output_button.pack(side=tk.LEFT)

# Start Conversion Button
convert_button = tk.Button(root, text="Convert to PDF", command=start_conversion, width=20, bg='blue', fg='white')
convert_button.pack(pady=20)

# Run the application
root.mainloop()
