import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import zipfile
import tempfile
import shutil

def extract_images_from_zip(zip_file_path):
    temp_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    print(f"Extracted images to {temp_dir}")
    return temp_dir

def images_to_pdf(image_folder, output_pdf_path):
    image_list = []

    # Get all image files in the folder, including subdirectories
    image_files = []
    for root, dirs, files in os.walk(image_folder):
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                full_path = os.path.join(root, f)
                image_files.append(full_path)

    # Enhanced natural sort key with raw string
    def natural_sort_key(filename):
        filename = os.path.basename(filename)
        return [
            int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', filename)
        ]

    sorted_files = sorted(image_files, key=natural_sort_key)

    # Load images
    for file_path in sorted_files:
        try:
            with Image.open(file_path) as img:
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
                print(f"Loaded image: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"Error loading {file_path}: {e}")

    if not image_list:
        messagebox.showwarning("No Images Found", "No JPG, PNG, or WEBP images were found in the selected folder or ZIP file.")
        return

    # Save images as a single PDF file
    first_image = image_list.pop(0)
    first_image.save(
        output_pdf_path, "PDF", resolution=100.0, save_all=True, append_images=image_list
    )

    messagebox.showinfo("Success", f"PDF file has been created at:\n{output_pdf_path}")

def browse_folder():
    folder_selected = filedialog.askdirectory(title="Select Image Folder")
    if folder_selected:
        input_path.set(folder_selected)
        update_output_path_based_on_input()

def browse_zip_file():
    file_selected = filedialog.askopenfilename(
        filetypes=[("ZIP files", "*.zip")],
        title="Select ZIP File"
    )
    if file_selected:
        input_path.set(file_selected)
        update_output_path_based_on_input()

def browse_output_file():
    file_selected = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        initialfile=os.path.basename(output_file_path.get())  # Use the current output file name
    )
    if file_selected:
        output_file_path.set(file_selected)

def update_output_path_based_on_input():
    in_path = input_path.get()
    if in_path:
        base_name = os.path.splitext(os.path.basename(in_path))[0]
        # Set default output directory (can be customized)
        default_output_dir = os.path.dirname(in_path)
        default_output_file = os.path.join(default_output_dir, f"{base_name}.pdf")
        output_file_path.set(default_output_file)

def browse_input():
    if input_type.get() == 'folder':
        browse_folder()
    elif input_type.get() == 'zip':
        browse_zip_file()

def start_conversion():
    in_path = input_path.get()
    out_file = output_file_path.get()

    if not in_path or not out_file:
        messagebox.showwarning("Missing Information", "Please select an input source and specify an output PDF file.")
        return

    try:
        if input_type.get() == 'folder':
            images_to_pdf(in_path, out_file)
        elif input_type.get() == 'zip':
            temp_dir = extract_images_from_zip(in_path)
            images_to_pdf(temp_dir, out_file)
            # Clean up temporary directory
            shutil.rmtree(temp_dir)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# Main application window
root = tk.Tk()
root.title("Images to PDF Converter")
root.geometry("550x350")
root.resizable(False, False)

# Variables to hold user selections
input_path = tk.StringVar()
output_file_path = tk.StringVar()
input_type = tk.StringVar(value='folder')

# Input Type Selection
input_type_frame = tk.Frame(root)
input_type_frame.pack(pady=10)

input_type_label = tk.Label(input_type_frame, text="Select Input Type:")
input_type_label.pack(side=tk.LEFT)

folder_radio = tk.Radiobutton(input_type_frame, text='Folder', variable=input_type, value='folder')
folder_radio.pack(side=tk.LEFT, padx=5)

zip_radio = tk.Radiobutton(input_type_frame, text='ZIP File', variable=input_type, value='zip')
zip_radio.pack(side=tk.LEFT, padx=5)

# Input Path Selection
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

input_label = tk.Label(input_frame, text="Input Path:")
input_label.pack(side=tk.LEFT)

input_entry = tk.Entry(input_frame, textvariable=input_path, width=40)
input_entry.pack(side=tk.LEFT, padx=5)

input_button = tk.Button(input_frame, text="Browse", command=browse_input)
input_button.pack(side=tk.LEFT)

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
