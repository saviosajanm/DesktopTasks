from pathlib import Path
import tkinter as tk
from tkinter import ttk, Button
from tkinter.colorchooser import askcolor
from tkinter.scrolledtext import ScrolledText
import json
from tkcalendar import Calendar
import datetime
from back import update_tasks
from PIL import Image
from utils import get_desktop_background, hex_to_rgb, wrap_text, convert_to_datetime, rgb_to_hex
import os

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
        BORDER = (255, 255, 255)
    else:    
        color_1.configure(bg=colors[1])
        BORDER = hex_to_rgb(colors[1])
    
def change_color_2():
    global FILL
    colors = askcolor(title="Choose Fill Color")
    if colors == (None, None):
        color_2.configure(bg="#f0f0f0")
        FILL = -1
    else:    
        color_2.configure(bg=colors[1])
        FILL = hex_to_rgb(colors[1])
    
def change_color_3():
    global TEXT
    colors = askcolor(title="Choose Text Color")
    if colors == (None, None):
        color_3.configure(bg="#f0f0f0")
        TEXT = (255, 255, 255)
    else:    
        color_3.configure(bg=colors[1])
        TEXT = hex_to_rgb(colors[1])
    
def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
  
with open("tasks.json", "r") as f:
    data = json.load(f)

window = tk.Tk()
window.geometry("600x540")
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

frame_right = ttk.Frame(window, width=364, height=516, style="My.TFrame")
frame_right.place(x=226, y=12)

canvas = tk.Canvas(window, width=202, height=460, bg="#F7F7F7", bd=0)
canvas.place(x=10, y=12)
scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
scrollbar.place(x=198, y=12, height=462)
canvas.config(yscrollcommand=scrollbar.set)
canvas.bind_all("<MouseWheel>", on_mousewheel)

# Create frame to hold buttons
frame_buttons = tk.Frame(canvas, bg="#F7F7F7")
canvas.create_window((0, 0), window=frame_buttons, anchor="nw")

buttons = [] 

# Function to create a button with data
def create_button(desc, date_time, colors):
    t = wrap_text(f"{desc}\n{date_time}")
    n = '\n'.join(str(item) for item in t).count("\n")
    button = tk.Button(
        frame_buttons,
        text= '\n'.join(str(item) for item in t),
        width=26,
        height=2 + (1 * n),
        relief="flat",
        borderwidth=2,
        highlightthickness=2,
        highlightbackground="black",
        fg = 'black',
        command=lambda d=desc, dt=date_time, c=colors: button_click_handler(d, dt, c)
    )
    button.pack(fill="x")
    buttons.append(button)

def remove_all_buttons():
    for button in buttons:
        button.destroy()
    buttons.clear()

def button_click_handler(desc, date_time, c):
    
    global PREV, FILL, BORDER, TEXT
    PREV = {
        "date_time": date_time, 
        "desc": desc, 
        "color": c
    }
    #print(date_time, desc, c)
    datetime_obj = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    date = datetime_obj.date()
    hour = int(datetime_obj.strftime("%I"))
    minute = int(datetime_obj.minute)
    am_pm = datetime_obj.strftime("%p")
    entry_1.delete(0, tk.END)  # Delete from index 0 (beginning) to END
    entry_1.insert(tk.END, desc)
    entry_2.config(value=hour)  # Use config(value=...)
    entry_3.config(value=minute)  # Use config(value=...)
    combo.set(am_pm)
    cal.selection_set(date) 
    color_1.configure(bg=rgb_to_hex(c[2]))
    if c[0] == -1:
        color_2.configure(bg="#f0f0f0")
    else:
        color_2.configure(bg=rgb_to_hex(c[0]))
    color_3.configure(bg=rgb_to_hex(c[1]))
    FILL = c[0]
    TEXT = c[1]
    BORDER = c[2]
    
# Create buttons from JSON data
for task in data:
    desc = task["desc"]
    date_time = task["date_time"]
    colors = task["color"]
    create_button(desc, date_time, colors)

def add():
    desc = entry_1.get()
    date = cal.selection_get()
    hour = entry_2.get()
    minute = entry_3.get()
    ampm = combo.get()
    #print(desc, date, hour, minute, ampm, TEXT, BORDER, FILL)
    date_time = convert_to_datetime(str(date), hour, minute, ampm)
    update_tasks(date_time, desc, "add", (FILL, TEXT, BORDER))
    create_button(desc, date_time, list((FILL, TEXT, BORDER)))
    new()

def delete():
    desc = entry_1.get()
    date = cal.selection_get()
    hour = entry_2.get()
    minute = entry_3.get()
    ampm = combo.get()
    #print(desc, date, hour, minute, ampm, TEXT, BORDER, FILL)
    date_time = convert_to_datetime(str(date), hour, minute, ampm)
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
    #print(PREV)
    desc = entry_1.get()
    date = cal.selection_get()
    hour = entry_2.get()
    minute = entry_3.get()
    ampm = combo.get()
    #print(desc, date, hour, minute, ampm, TEXT, BORDER, FILL)
    date_time = convert_to_datetime(str(date), hour, minute, ampm)
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
    global FILL, BORDER, TEXT
    entry_1.delete(0, tk.END)  # Delete from index 0 (beginning) to END
    entry_1.insert(tk.END, "")
    entry_2.config(value=1)  # Use config(value=...)
    entry_3.config(value=0)  # Use config(value=...)
    combo.set("AM")
    cal.selection_set(datetime.datetime.now()) 
    color_1.configure(bg="#f0f0f0")
    color_2.configure(bg="#f0f0f0")
    color_3.configure(bg="#f0f0f0")
    FILL, BORDER, TEXT = -1, (255, 255, 255), (255, 255, 255)

def reset_bg():
    background_image_path = get_desktop_background()
    background_image = Image.open(background_image_path)
    background_image.save("original.png")
    update_tasks(0, 0, "pass", 0, 0)
    
def set_config():
    update_tasks(0, 0, "pass", 0, 0)

def clear_all():
    with open('tasks.json', 'w') as f:
        json.dump([], f)
    remove_all_buttons()
    update_tasks(0, 0, "pass", 0, 0)

# Update canvas content area after button creation
frame_buttons.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

button_image_1 = tk.PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=new,
    relief="flat"
)
button_1.place(x=10.0, y=485.0, width=206.0, height=42.0)

button_image_2 = tk.PhotoImage(file=relative_to_assets("button_4.png"))
button_2 = Button(
    frame_right,
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=delete,
    relief="flat"
)
button_2.place(x=173.0, y=440.0, width=59.0, height=29.0)

button_image_3 = tk.PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    frame_right,
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=edit,
    relief="flat"
)
button_3.place(x=232.0, y=440.0, width=59.0, height=29.0)

button_image_4 = tk.PhotoImage(file=relative_to_assets("button_2.png"))
button_4 = Button(
    frame_right,
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=add,
    relief="flat"
)
button_4.place(x=291.0, y=440.0, width=59.0, height=29.0)

button_5 = Button(
    frame_right,
    text="Update Configuration",
    borderwidth=0,
    highlightthickness=0,
    background="#b3b3b3",
    command=set_config,
    relief="flat",
)
button_5.place(x=13.0, y=440.0, width=155.0, height=29.0)

button_6 = Button(
    frame_right,
    text="Set this background as tasks background",
    borderwidth=0,
    highlightthickness=0,
    foreground="#FFFFFF",
    background="#4d4d4d",
    command=reset_bg,
    relief="flat",
)
button_6.place(x=13.0, y=480.0, width=232.0, height=29.0)

button_7 = Button(
    frame_right,
    text="Clear All",
    borderwidth=0,
    highlightthickness=0,
    foreground="#FFFFFF",
    background="#831308",
    command=clear_all,
    relief="flat",
)
button_7.place(x=250.0, y=480.0, width=99.0, height=29.0)

#entry_image_1 = tk.PhotoImage(file=relative_to_assets("entry_1.png"))
entry_1 = ttk.Entry(frame_right, style="borderless.TEntry", foreground="#000716")
entry_1.place(x=13.0, y=32.0, width=337.0, height=28.0)

#entry_image_2 = tk.PhotoImage(file=relative_to_assets("entry_2.png"))
#entry_2 = ttk.Entry(frame_right, style="borderless.TEntry", foreground="#000716")
entry_2 = tk.Spinbox(frame_right, from_= 1, to = 12, increment=1)
entry_2.place(x=13.0, y=92.0, width=96.0, height=36.0)

entry_3 = tk.Spinbox(frame_right, from_= 0, to = 59, increment=1)
entry_3.place(x=13.0, y=167.0, width=96.0, height=36.0)

combo = ttk.Combobox(
    frame_right,
    state="readonly",
    values=["AM", "PM"]
)
combo.set("AM")
combo.place(x=13.0, y=222.0, width=96.0, height=26.0)

entry_image_4 = tk.PhotoImage(file=relative_to_assets("entry_4.png"))
current_datetime = datetime.datetime.now()
current_year = current_datetime.year
current_day = current_datetime.day
current_month = current_datetime.month
#entry_4 = ttk.Entry(frame_right, style="borderless.TEntry", foreground="#000716")
#entry_4.place(x=137.0, y=92.0, width=113.0, height=26.0)
cal = Calendar(frame_right, selectmode = 'day',
               year = current_year, month = current_month,
               day = current_day)
cal.place(x=122.0, y=92.0, width=227.0, height=156.0)

label1 = ttk.Label(frame_right, text="Description:", anchor="w", background="#F7F7F7", font=("Inter SemiBold", 12))
label1.place(x=13.0, y=7.0)

label2 = ttk.Label(frame_right, text="Hour:", anchor="w", background="#F7F7F7", font=("Inter SemiBold", 12))
label2.place(x=13.0, y=67.0)

label3 = ttk.Label(frame_right, text="Fill:", anchor="w", background="#F7F7F7", font=("Inter SemiBold", 12))
label3.place(x=13.0, y=257.0)

label4 = ttk.Label(frame_right, text="Text:", anchor="w", background="#F7F7F7", font=("Inter SemiBold", 12))
label4.place(x=13.0, y=317.0)

label5 = ttk.Label(frame_right, text="Border:", anchor="w", background="#F7F7F7", font=("Inter SemiBold", 12))
label5.place(x=13.0, y=377.0)

label6 = ttk.Label(frame_right, text="Date:", anchor="w", background="#F7F7F7", font=("Inter SemiBold", 12))
label6.place(x=122.0, y=67.0)

label7 = ttk.Label(frame_right, text="Minute:", anchor="w", background="#F7F7F7", font=("Inter SemiBold", 12))
label7.place(x=13.0, y=142.0)


color_1 = Button(
    frame_right,
    text="Choose border  (Default: White)",
    borderwidth=0,
    highlightthickness=0,
    foreground="#000716",
    command=change_color_1,
    relief="flat",
)
color_1.place(x=13.0, y=400.0, width=337.0, height=28.0)

color_2 = Button(
    frame_right,
    text="Choose fill (Default: transparent fill)",
    borderwidth=0,
    highlightthickness=1,
    foreground="#000716",
    command=change_color_2,
    relief="flat"
)
color_2.place(x=13.0, y=282.0, width=337.0, height=28.0)

color_3 = Button(
    frame_right,
    text="Choose text (Default: White)",
    borderwidth=0,
    highlightthickness=0,
    foreground="#000716",
    command=change_color_3,
    relief="flat"
)
color_3.place(x=13.0, y=342.0, width=337.0, height=28.0)

window.resizable(False, False)
window.mainloop()
