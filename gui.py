from pathlib import Path
import tkinter as tk
from tkinter import ttk, Button
from tkinter.colorchooser import askcolor
import json
from tkcalendar import Calendar
import datetime
from back import update_tasks, sort_key
from utils import hex_to_rgb, wrap_text, convert_to_datetime, rgb_to_hex, get_text_color
import os
from confgui import open_config_dialog

current_dir = os.getcwd()

PREV = None
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(current_dir + "/assets/frame0")
TEXT, FILL, BORDER = (255, 255, 255), -1, (255, 255, 255)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def change_color_1():
    global BORDER
    colors = askcolor(title="Choose Border Color")
    if colors == (None, None):
        color_1.configure(bg="#f0f0f0")
        color_1.configure(fg="#000000")
        color_1.configure(text="(Default: White)")
        BORDER = (255, 255, 255)
    else:    
        color_1.configure(bg=colors[1])
        color_1.configure(text=colors[1])
        color_1.configure(fg=get_text_color(colors[1]))
        BORDER = hex_to_rgb(colors[1])
    
def change_color_2():
    global FILL
    colors = askcolor(title="Choose Fill Color")
    if colors == (None, None):
        color_2.configure(bg="#f0f0f0")
        color_2.configure(fg="#000000")
        color_2.configure(text="(Default: Transparent fill)")
        FILL = -1
    else:    
        color_2.configure(bg=colors[1])
        color_2.configure(text=colors[1])
        color_2.configure(fg=get_text_color(colors[1]))
        FILL = hex_to_rgb(colors[1])
    
def change_color_3():
    global TEXT
    colors = askcolor(title="Choose Text Color")
    if colors == (None, None):
        color_3.configure(bg="#f0f0f0")
        color_3.configure(fg="#000000")
        color_3.configure(text="(Default: White)")
        TEXT = (255, 255, 255)
    else:    
        color_3.configure(bg=colors[1])
        color_3.configure(text=colors[1])
        color_3.configure(fg=get_text_color(colors[1]))
        TEXT = hex_to_rgb(colors[1])
    
def on_mousewheel(event):
    """Allow scrolling only when there are enough items to require scrolling."""
    content_height = frame_buttons.winfo_height()
    canvas_height = canvas.winfo_height()

    if content_height > canvas_height:  # Enable scrolling only when needed
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    
def update_scroll_region():
    """Update the scroll region of the canvas and prevent scrolling beyond limits."""
    frame_buttons.update_idletasks()  # Update the frame's dimensions

    # Get the total height of the content inside the canvas
    canvas_height = canvas.winfo_height()
    content_height = frame_buttons.winfo_height()

    # Ensure scrolling only when content is taller than the canvas
    if content_height > canvas_height:
        canvas.config(scrollregion=canvas.bbox("all"))
    else:
        # Prevent extra scrolling when there are fewer items
        canvas.config(scrollregion=(0, 0, canvas.winfo_width(), canvas_height))



  
with open("tasks.json", "r") as f:
    data = json.load(f)

window = tk.Tk()
window.geometry("600x600")
window.configure(bg="#FFFFFF")
window.iconbitmap("icon.ico")
window.title("Desktop Tasks")

style = ttk.Style()
style.configure("borderless.TButton", borderwidth=0)
style.configure("borderless.TEntry", borderwidth=0)
style.configure("My.TFrame", background="#F7F7F7")  # Add a custom frame style

'''# Create frames with adjusted background
frame_left = ttk.Frame(window, width=206, height=325, style="My.TFrame")
frame_left.place(x=10, y=12)'''

frame_right = ttk.Frame(window, width=364, height=576, style="My.TFrame")
frame_right.place(x=226, y=12)

canvas = tk.Canvas(window, width=202, height=520, bg="#F7F7F7", bd=0)
canvas.place(x=10, y=12)
# Create the vertical scrollbar and configure it
scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
scrollbar.place(x=198, y=12, height=522)
# Connect the scrollbar to the canvas
canvas.config(yscrollcommand=scrollbar.set)
# Bind mouse wheel scrolling only when mouse hovers over the canvas
canvas.bind("<Enter>", lambda event: canvas.bind_all("<MouseWheel>", on_mousewheel))
canvas.bind("<Leave>", lambda event: canvas.unbind_all("<MouseWheel>"))
'''canvas.bind("<Enter>", lambda event: canvas.bind_all("<MouseWheel>", on_mousewheel))  # Mouse enters canvas
canvas.bind("<Leave>", lambda event: canvas.unbind_all("<MouseWheel>"))  # Mouse leaves canvas'''
# Create frame to hold buttons
frame_buttons = tk.Frame(canvas, bg="#F7F7F7")
canvas.create_window((0, 0), window=frame_buttons, anchor="nw")

def set_checkboxes(t, d):
    """
    Set the state of the 'Exclude Time' and 'Exclude Date' checkboxes.
    
    :param t: Boolean. If True, checks the 'Exclude Time' checkbox; unchecks otherwise.
    :param d: Boolean. If True, checks the 'Exclude Date' checkbox; unchecks otherwise.
    """
    exclude_time_var.set(t)
    excludetime()  # Trigger the related functionality

    exclude_date_var.set(d)
    excludedate()

buttons = [] 

# Function to create a button with data
def create_button(desc, date_time, colors):
    if not desc:
        desc = "-----"
    if not date_time:
        date_time = "-----"
    t = wrap_text(f"{desc}\n{date_time}")
    n = '\n'.join(str(item) for item in t).count("\n")
    button = tk.Button(
        frame_buttons,
        text='\n'.join(str(item) for item in t),
        width=26,
        height=2 + (1 * n),
        relief="flat",
        borderwidth=2,
        highlightthickness=2,
        highlightbackground="black",
        fg='black',
        bg="#f0f0f0"
    )
    button.configure(command=lambda d=desc, dt=date_time, c=colors, b=button: button_click_handler(d, dt, c, b))
    button.pack(fill="x")
    buttons.append((button, colors))
    update_scroll_region()

def remove_all_buttons():
    for button, _ in buttons:
        button.destroy()
    buttons.clear()
    update_scroll_region()

def button_click_handler(desc, date_time, colors, clicked_button):
    global PREV, FILL, BORDER, TEXT, excdate, exctime
    PREV = {
        "date_time": date_time,
        "desc": desc,
        "color": colors
    }

    # Reset all buttons to their original color
    for button, original_colors in buttons:
        button.configure(bg="#f0f0f0", fg='black')

    # Highlight the clicked button with medium grey
    clicked_button.configure(bg="#A9A9A9", fg="white")  # Medium grey and white text

    # Handle date and time parsing and updates
    current_date = datetime.date.today()
    date, hour, minute, am_pm = current_date, 1, 0, "AM"
    
    try:
        if not date_time.strip() or date_time == "-----":  # Empty string
            excdate, exctime = True, True
        elif " " in date_time:  # Full date-time
            dt = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
            date, hour, minute, am_pm = dt.date(), int(dt.strftime("%I")), dt.minute, dt.strftime("%p")
            excdate, exctime = False, False
        elif "-" in date_time:  # Date-only
            date = datetime.datetime.strptime(date_time, "%Y-%m-%d").date()
            excdate, exctime = True, False
        elif ":" in date_time:  # Time-only
            dt = datetime.datetime.strptime(date_time, "%H:%M:%S")
            hour, minute, am_pm = int(dt.strftime("%I")), dt.minute, dt.strftime("%p")
            excdate, exctime = False, True
        else:
            raise ValueError(f"Invalid date_time format: {date_time}")
    except ValueError:
        raise ValueError(f"Invalid date_time format: {date_time}")

    # Widget state updates
    cal.configure(state="normal" if not excdate else "disabled")
    entry_2.configure(state="normal" if not exctime else "disabled")
    entry_3.configure(state="normal" if not exctime else "disabled")
    combo.configure(state="readonly" if not exctime else "disabled")
    
    set_checkboxes(exctime, excdate)

    entry_1.delete(0, tk.END)  # Delete from index 0 (beginning) to END
    entry_1.insert(tk.END, desc)
    hour_var.set(int(hour))
    minute_var.set(int(minute))
    combo.set(am_pm)
    cal.selection_set(date) 
    color_1.configure(bg=rgb_to_hex(colors[2]))
    color_1.configure(text=rgb_to_hex(colors[2]))
    color_1.configure(fg=get_text_color(rgb_to_hex(colors[2])))
    if colors[0] == -1:
        color_2.configure(bg="#f0f0f0")
        color_2.configure(fg="#000000")
        color_2.configure(text="(Default: Transparent fill)")
    else:
        color_2.configure(bg=rgb_to_hex(colors[0]))
        color_2.configure(text=rgb_to_hex(colors[0]))
        color_2.configure(fg=get_text_color(rgb_to_hex(colors[0])))
    color_3.configure(bg=rgb_to_hex(colors[1]))
    color_3.configure(text=rgb_to_hex(colors[1]))
    color_3.configure(fg=get_text_color(rgb_to_hex(colors[1])))
    FILL = colors[0]
    TEXT = colors[1]
    BORDER = colors[2]

    
# Create buttons from JSON data
data.sort(key = sort_key)
for task in data:
    desc = task["desc"]
    date_time = task["date_time"]
    colors = task["color"]
    create_button(desc, date_time, colors)
    
exctime = False
excdate = False

def add():
    global PREV
    PREV = None
    desc = entry_1.get()
    date = cal.selection_get()
    hour = entry_2.get()
    minute = entry_3.get()
    ampm = combo.get()
    #print(desc, date, hour, minute, ampm, TEXT, BORDER, FILL)
    date_time = convert_to_datetime(str(date), hour, minute, ampm, exctime, excdate)
    update_tasks(date_time, desc, "add", (FILL, TEXT, BORDER))
    create_button(desc, date_time, list((FILL, TEXT, BORDER)))
    new()

def delete():
    global PREV
    PREV = None
    desc = entry_1.get()
    date = cal.selection_get()
    hour = entry_2.get()
    minute = entry_3.get()
    ampm = combo.get()
    #print(desc, date, hour, minute, ampm, TEXT, BORDER, FILL)
    date_time = convert_to_datetime(str(date), hour, minute, ampm, exctime, excdate)
    
    update_tasks(date_time, desc, "delete", (FILL, TEXT, BORDER))
    remove_all_buttons()
    colors = [FILL, TEXT, BORDER]
    for i in range(len(colors)):
        if type(colors[i]) == tuple:
            colors[i] = list(colors[i])
    with open("tasks.json", "r") as f:
        data = json.load(f)
    for task in data:
        desc = task["desc"]
        date_time = task["date_time"]
        colors = task["color"]
        create_button(desc, date_time, colors)
    new()

def edit():
    desc = entry_1.get()
    date = cal.selection_get()
    hour = entry_2.get()
    minute = entry_3.get()
    ampm = combo.get()
    #print(desc, date, hour, minute, ampm, TEXT, BORDER, FILL)
    date_time = convert_to_datetime(str(date), hour, minute, ampm, exctime, excdate)
    update_tasks(date_time, desc, "edit", (FILL, TEXT, BORDER), PREV)
    remove_all_buttons()
    with open("tasks.json", "r") as f:
        data = json.load(f)
    for task in data:
        desc = task["desc"]
        date_time = task["date_time"]
        colors = task["color"]
        create_button(desc, date_time, colors)
    new()

def new():
    global FILL, BORDER, TEXT, PREV
    PREV = None
    entry_1.delete(0, tk.END)  # Delete from index 0 (beginning) to END
    entry_1.insert(tk.END, "")
    hour_var.set(int(1))
    minute_var.set(int(0))
    combo.set("AM")
    cal.selection_set(datetime.datetime.now())
    color_1.configure(bg="#f0f0f0")
    color_1.configure(fg="#000000")
    color_1.configure(text="(Default: White)")
    color_2.configure(bg="#f0f0f0")
    color_2.configure(fg="#000000")
    color_2.configure(text="(Default: Transparent fill)")
    color_3.configure(bg="#f0f0f0")
    color_3.configure(fg="#000000")
    color_3.configure(text="(Default: White)")
    FILL, BORDER, TEXT = -1, (255, 255, 255), (255, 255, 255)
    for button, original_colors in buttons:
        button.configure(bg="#f0f0f0", fg='black')


    
def set_config():
    #update_tasks(0, 0, "pass", 0, 0)
    open_config_dialog()

def clear_all():
    with open('tasks.json', 'w') as f:
        json.dump([], f)
    remove_all_buttons()
    update_tasks(0, 0, "pass", 0, 0)

# Update canvas content area after button creation
frame_buttons.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

button_1 = Button(
    text="New",
    font=("Helvetica", 12, "bold"),
    bg="#faff00",
    fg="black",
    borderwidth=0,
    highlightthickness=0,
    command=new,
    relief="flat",
    activebackground="#e5e500"  # Slight darken when clicked
)

# Button 2: "Delete" button
button_2 = Button(
    frame_right,
    text="Delete",
    font=("Helvetica", 12, "bold"),
    bg="#c30000",
    fg="white",
    borderwidth=0,
    highlightthickness=0,
    command=delete,
    relief="flat",
    activebackground="#9c0000"
)

# Button 3: "Edit" button
button_3 = Button(
    frame_right,
    text="Edit",
    font=("Helvetica", 12, "bold"),
    bg="#00a3fe",
    fg="black",
    borderwidth=0,
    highlightthickness=0,
    command=edit,
    relief="flat",
    activebackground="#008ec7"
)

# Button 4: "Add" button
button_4 = Button(
    frame_right,
    text="Add",
    font=("Helvetica", 12, "bold"),
    bg="#05e900",
    fg="black",
    borderwidth=0,
    highlightthickness=0,
    command=add,
    relief="flat",
    activebackground="#04c700"
)

button_1.place(x=10.0, y=545.0, width=206.0, height=42.0)

button_2.place(x=110.0, y=515.0, width=65.0, height=29.0)

button_3.place(x=180.0, y=515.0, width=65.0, height=29.0)

button_4.place(x=250.0, y=515.0, width=100.0, height=29.0)

button_5 = Button(
    frame_right,
    text="Update Configuration",
    font=("Helvetica", 10, "bold"),
    fg="black",
    borderwidth=0,
    highlightthickness=0,
    background="#b3b3b3",
    command=set_config,
    relief="flat",
)
button_5.place(x=13.0, y=550.0, width=337.0, height=29.0)

button_6 = Button(
    frame_right,
    text="Clear All",
    font=("Helvetica", 11, "bold"),
    borderwidth=0,
    highlightthickness=0,
    foreground="#FFFFFF",
    background="#831308",
    command=clear_all,
    relief="flat",
)
button_6.place(x=13.0, y=515.0, width=92.0, height=29.0)


entry_1 = ttk.Entry(frame_right, style="borderless.TEntry", foreground="#000716")
entry_1.place(x=13.0, y=32.0, width=337.0, height=28.0)

hour_var = tk.StringVar(value=1)  # Create a StringVar for hour
minute_var = tk.StringVar(value=0)  # Create a StringVar for minute

# Function to handle mouse wheel scrolling for Spinboxes
def on_spinbox_scroll(event):
    if event.delta > 0:
        event.widget.invoke('buttonup')  # Scroll up
    else:
        event.widget.invoke('buttondown')  # Scroll down

# Create the Spinboxes
entry_2 = tk.Spinbox(frame_right, textvariable=hour_var, from_=1, to=12, increment=1)
entry_2.place(x=13.0, y=122.0, width=105.0, height=30.0)
entry_3 = tk.Spinbox(frame_right, textvariable=minute_var, from_=0, to=59, increment=1)
entry_3.place(x=130.0, y=122.0, width=105.0, height=30.0)

# Bind the mouse wheel to the Spinboxes for scrolling
entry_2.bind("<Enter>", lambda event: entry_2.bind("<MouseWheel>", on_spinbox_scroll))
entry_2.bind("<Leave>", lambda event: entry_2.unbind("<MouseWheel>"))

entry_3.bind("<Enter>", lambda event: entry_3.bind("<MouseWheel>", on_spinbox_scroll))
entry_3.bind("<Leave>", lambda event: entry_3.unbind("<MouseWheel>"))


combo = ttk.Combobox(
    frame_right,
    state="readonly",
    values=["AM", "PM"]
)
combo.set("AM")
combo.place(x=245.0, y=122.0, width=105.0, height=30.0)

current_datetime = datetime.datetime.now()
current_year = current_datetime.year
current_day = current_datetime.day
current_month = current_datetime.month
#entry_4 = ttk.Entry(frame_right, style="borderless.TEntry", foreground="#000716")
#entry_4.place(x=137.0, y=92.0, width=113.0, height=26.0)
cal = Calendar(frame_right, selectmode = 'day',
               year = current_year, month = current_month,
               day = current_day)
cal.place(x=13.0, y=160.0, width=337.0, height=160.0)

label1 = ttk.Label(frame_right, text="Description:", anchor="w", background="#F7F7F7", font=("Inter SemiBold", 12))
label1.place(x=13.0, y=7.0)

label2 = ttk.Label(frame_right, text="Hour:", anchor="w", background="#F7F7F7", font=("Inter SemiBold", 12))
label2.place(x=13.0, y=100.0)

label3 = ttk.Label(frame_right, text="Fill:", anchor="w", background="#F7F7F7", font=("Inter SemiBold", 12))
label3.place(x=13.0, y=327.0)

label4 = ttk.Label(frame_right, text="Text:", anchor="w", background="#F7F7F7", font=("Inter SemiBold", 12))
label4.place(x=13.0, y=387.0)

label5 = ttk.Label(frame_right, text="Border:", anchor="w", background="#F7F7F7", font=("Inter SemiBold", 12))
label5.place(x=13.0, y=447.0)

label6 = ttk.Label(frame_right, text=":", anchor="w", background="#F7F7F7", font=("Inter SemiBold", 12))
label6.place(x=120.0, y=125.0)

label7 = ttk.Label(frame_right, text="Minute:", anchor="w", background="#F7F7F7", font=("Inter SemiBold", 12))
label7.place(x=120.0, y=100.0)


color_1 = Button(
    frame_right,
    text="(Default: White)",
    borderwidth=0,
    highlightthickness=0,
    foreground="#000000",
    command=change_color_1,
    relief="flat",
)
color_1.place(x=13.0, y=470.0, width=337.0, height=28.0)

color_2 = Button(
    frame_right,
    text="(Default: Transparent fill)",
    borderwidth=0,
    highlightthickness=1,
    foreground="#000000",
    command=change_color_2,
    relief="flat"
)
color_2.place(x=13.0, y=350.0, width=337.0, height=28.0)

color_3 = Button(
    frame_right,
    text="(Default: White)",
    borderwidth=0,
    highlightthickness=0,
    foreground="#000000",
    command=change_color_3,
    relief="flat"
)
color_3.place(x=13.0, y=410.0, width=337.0, height=28.0)

# Add the variable for the Checkbutton
exclude_date_var = tk.BooleanVar(value=False)  # Tracks whether the checkbox is selected or not
exclude_time_var = tk.BooleanVar(value=False)  # Tracks whether the checkbox is selected or not

# Function to disable or enable calendar based on checkbox
def excludedate():
    global excdate
    if exclude_date_var.get():  # If checkbox is selected
        cal.configure(state="disabled")
        excdate = True
    else:  # If checkbox is not selected
        cal.configure(state="normal")
        excdate = False

# Function to disable or enable time-related widgets based on checkbox
def excludetime():
    global exctime
    if exclude_time_var.get():  # If checkbox is selected
        # Disable the widgets
        entry_2.configure(state="disabled")
        entry_3.configure(state="disabled")
        combo.configure(state="disabled")
        exctime = True
    else:  # If checkbox is not selected
        # Enable the widgets
        entry_2.configure(state="normal")
        entry_3.configure(state="normal")
        combo.configure(state="readonly")  # Restore the combobox to readonly
        exctime = False

# Set the background color of the checkbuttons using ttk.Style
style = ttk.Style()
style.configure("TCheckbutton",
                background="#F7F7F7",  # Set background for the checkbutton
                padding=5)  # Optional: add padding to make it look better

# Add the checkbox to the GUI
exclude_date_checkbox = ttk.Checkbutton(
    frame_right,
    text="Exclude Date",
    variable=exclude_date_var,
    command=excludedate,
    style="TCheckbutton"
)
exclude_date_checkbox.place(x=10.0, y=70.0, width=100.0, height=28.0)

exclude_time_checkbox = ttk.Checkbutton(
    frame_right,
    text="Exclude Time",
    variable=exclude_time_var,
    command=excludetime,
    style="TCheckbutton"
)
exclude_time_checkbox.place(x=110.0, y=70.0, width=100.0, height=28.0)

window.resizable(False, False)
window.mainloop()
