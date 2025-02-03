import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from tkinter import ttk

'''
Understanding the GUI Components
Main Window (root)
Title and Size:

Sets the window title to "WebP to JPG/PNG Converter".

Fixed window size of 500x300 pixels.

Resizable Property:

resizable(False, False) prevents the window from being resized, ensuring consistent layout.

Variables
input_folder_path & output_folder_path:

Hold the paths to the selected input and output folders.

output_format:

Stores the user's choice between 'JPEG' and 'PNG'.

Functions
convert_images():

Processes all WebP images in the input folder.

Handles exceptions and informs the user of any issues.

browse_input_folder() & browse_output_folder():

Open a directory selection dialog and update the respective path variables.

start_conversion():

Validates that input and output folders are selected.

Initiates the image conversion process.

GUI Layout Elements
Frames:

Organize GUI components into logical sections.

Labels & Entries:

Input/Output Folder Sections:

Labels prompt the user for action.

Entry fields display the selected folder paths.

Buttons trigger the folder selection dialogs.

Radio Buttons:

Allow the user to select the desired output format.

Convert Button:

Initiates the conversion process.

Styled with blue background and white text for visibility.
'''

def convert_images(input_folder, output_folder, output_format):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder at: {output_folder}")

    # List all WebP files in the input folder
    webp_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.webp')]

    if not webp_files:
        messagebox.showwarning("No WebP Images Found", "No WebP images were found in the selected folder.")
        return

    for filename in webp_files:
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

        # Update the convert_images function
        total_files = len(webp_files)
        progress['maximum'] = total_files

        for idx, filename in enumerate(webp_files):
            # ... existing code ...
            progress['value'] = idx + 1
            root.update_idletasks()

        # Reset progress bar
        progress['value'] = 0

    messagebox.showinfo("Conversion Complete", f"All images have been converted to {output_format.upper()} format.")

def browse_input_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        input_folder_path.set(folder_selected)

def browse_output_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_folder_path.set(folder_selected)

def start_conversion():
    in_folder = input_folder_path.get()
    out_folder = output_folder_path.get()
    out_format = output_format.get()

    if not in_folder or not out_folder:
        messagebox.showwarning("Missing Information", "Please select both input and output folders.")
        return

    convert_images(in_folder, out_folder, out_format)



# Main application window
root = tk.Tk()
root.title("WebP to JPG/PNG Converter")
root.geometry("500x300")
root.resizable(False, False)

# Variables to hold folder paths and output format
input_folder_path = tk.StringVar()
output_folder_path = tk.StringVar()
output_format = tk.StringVar(value='JPEG')

# Input Folder Selection
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

input_label = tk.Label(input_frame, text="Input Folder:")
input_label.pack(side=tk.LEFT)

input_entry = tk.Entry(input_frame, textvariable=input_folder_path, width=40)
input_entry.pack(side=tk.LEFT, padx=5)

input_button = tk.Button(input_frame, text="Browse", command=browse_input_folder)
input_button.pack(side=tk.LEFT)

# Output Folder Selection
output_frame = tk.Frame(root)
output_frame.pack(pady=10)

output_label = tk.Label(output_frame, text="Output Folder:")
output_label.pack(side=tk.LEFT)

output_entry = tk.Entry(output_frame, textvariable=output_folder_path, width=40)
output_entry.pack(side=tk.LEFT, padx=5)

output_button = tk.Button(output_frame, text="Browse", command=browse_output_folder)
output_button.pack(side=tk.LEFT)

# Output Format Selection
format_frame = tk.Frame(root)
format_frame.pack(pady=10)

format_label = tk.Label(format_frame, text="Output Format:")
format_label.pack(side=tk.LEFT)

jpeg_radio = tk.Radiobutton(format_frame, text='JPEG', variable=output_format, value='JPEG')
jpeg_radio.pack(side=tk.LEFT, padx=5)

png_radio = tk.Radiobutton(format_frame, text='PNG', variable=output_format, value='PNG')
png_radio.pack(side=tk.LEFT, padx=5)

# Start Conversion Button
convert_button = tk.Button(root, text="Convert Images", command=start_conversion, width=20, bg='blue', fg='white')
convert_button.pack(pady=20)

# Add a progress bar
progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=400, mode='determinate')
progress.pack(pady=10)



# Run the application
root.mainloop()
