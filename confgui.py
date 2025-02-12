import tkinter as tk
from tkinter import ttk, Button
from configparser import ConfigParser
from back import update_tasks
from utils import get_desktop_background
from PIL import Image

def reset_bg():
    background_image_path = get_desktop_background()
    background_image = Image.open(background_image_path)
    background_image.save("original.png")
    update_tasks(0, 0, "pass", 0, 0)

def open_config_dialog():
    def submit_config():
        # Validate the input fields
        invalid_fields = []

        # Validate integer fields
        def validate_int(field_name, value):
            try:
                return int(value)
            except ValueError:
                invalid_fields.append(field_name)
                return None

        # Update configuration values
        box_width = validate_int("Box Width", box_width_var.get())
        font_size = validate_int("Font Size", font_size_var.get())
        box_margin = validate_int("Box Margin", box_margin_var.get())
        box_padding = validate_int("Box Padding", box_padding_var.get())
        border_radius = validate_int("Border Radius", border_radius_var.get())
        border_width = validate_int("Border Width", border_width_var.get())

        if invalid_fields:
            success_label.config(text="Invalid value in: " + ", ".join(invalid_fields), foreground="red")
            return

        config['Main']['box_width'] = str(box_width)
        config['Main']['font'] = font_var.get()
        config['Main']['font_size'] = str(font_size)
        config['Main']['box_margin'] = str(box_margin)
        config['Main']['box_padding'] = str(box_padding)
        config['Main']['border_radius'] = str(border_radius)
        config['Main']['border_width'] = str(border_width)
        config['Main']['taskbar_present'] = str(taskbar_present_var.get())

        # Save to the config file
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        # Run the update_tasks function
        update_tasks(0, 0, "pass", 0, 0)

        # Update success label
        success_label.config(text="Configuration updated successfully!", foreground="green")

        # Hide success message after 5 seconds
        dialog.after(5000, lambda: success_label.config(text=""))

    # Read or initialize the config file
    config = ConfigParser()
    config.read('config.ini')
    if not config.has_section('Main'):
        config.add_section('Main')

    # Create the dialog window
    dialog = tk.Toplevel()
    dialog.title("Update Configuration")
    dialog.geometry("285x420")  # Set new geometry
    dialog.minsize(285, 420)  # Set the minimum size of the dialog window

    # Create variables for each field, fetching current values from the config file
    box_width_var = tk.StringVar(value=config['Main'].get('box_width', ''))
    font_var = tk.StringVar(value=config['Main'].get('font', ''))
    font_size_var = tk.StringVar(value=config['Main'].get('font_size', ''))
    box_margin_var = tk.StringVar(value=config['Main'].get('box_margin', ''))
    box_padding_var = tk.StringVar(value=config['Main'].get('box_padding', ''))
    border_radius_var = tk.StringVar(value=config['Main'].get('border_radius', ''))
    border_width_var = tk.StringVar(value=config['Main'].get('border_width', ''))
    taskbar_present_var = tk.IntVar(value=int(config['Main'].get('taskbar_present', '1')))

    # Add fields with labels and input widgets
    fields = [
        ("Box Width", box_width_var, ttk.Spinbox(dialog, from_=0, to=1000, textvariable=box_width_var)),
        ("Font", font_var, ttk.Entry(dialog, textvariable=font_var)),
        ("Font Size", font_size_var, ttk.Spinbox(dialog, from_=1, to=200, textvariable=font_size_var)),
        ("Box Margin", box_margin_var, ttk.Spinbox(dialog, from_=0, to=1000, textvariable=box_margin_var)),
        ("Box Padding", box_padding_var, ttk.Spinbox(dialog, from_=0, to=1000, textvariable=box_padding_var)),
        ("Border Radius", border_radius_var, ttk.Spinbox(dialog, from_=0, to=1000, textvariable=border_radius_var)),
        ("Border Width", border_width_var, ttk.Spinbox(dialog, from_=0, to=1000, textvariable=border_width_var))
    ]

    # Add label and field pairs
    for i, (label_text, variable, widget) in enumerate(fields):
        ttk.Label(dialog, text=label_text, font=("Helvetica", 10, "bold")).grid(row=i, column=0, padx=10, pady=5, sticky="w")
        widget.grid(row=i, column=1, padx=10, pady=5)

    # Taskbar Present Radio Buttons (Yes/No) arranged in a row
    ttk.Label(dialog, text="Taskbar Present", font=("Helvetica", 10, "bold")).grid(row=len(fields), column=0, padx=10, pady=5, sticky="w")
    
    # Create radio buttons in a row
    yes_rb = ttk.Radiobutton(dialog, text="Yes", variable=taskbar_present_var, value=1)
    no_rb = ttk.Radiobutton(dialog, text="No", variable=taskbar_present_var, value=0)
    
    yes_rb.grid(row=len(fields), column=1, padx=10, pady=5, sticky="w", in_=dialog)
    no_rb.grid(row=len(fields), column=1, padx=10, pady=5, sticky="e", in_=dialog)

    if taskbar_present_var.get() == 1:
        yes_rb.state(["selected"])
    else:
        no_rb.state(["selected"])

    # Set current background as Active Button
    button_6 = tk.Button(
        dialog,
        text="Set current background as Active",
        font=("Helvetica", 10, "bold"),
        borderwidth=0,
        highlightthickness=0,
        foreground="#FFFFFF",
        background="#4d4d4d",
        command=lambda: [reset_bg(), success_label.config(text="Current background has been set as ACTIVE", foreground="green"),
                         dialog.after(5000, lambda: success_label.config(text=""))],
        relief="flat",
    )
    button_6.grid(row=len(fields) + 2, column=0, columnspan=2, pady=10)

    # Add the Update button using tk.Button
    update_button = tk.Button(dialog, text="Update", command=submit_config, font=("Helvetica", 12, "bold"))
    update_button.grid(row=len(fields) + 3, column=0, columnspan=2, pady=10)

    # Add success message label (initially empty)
    success_label = ttk.Label(dialog, text="", foreground="green", font=("Helvetica", 10, "bold"), anchor="center")
    success_label.grid(row=len(fields) + 4, column=0, columnspan=2, padx=10, pady=10)

    # Set wraplength to allow the error message to wrap within the label and prevent it from changing the window width
    success_label.config(wraplength=250)  # Wrap text within a width of 250px (adjust if needed)

