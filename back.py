import os
import json
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import ctypes
import math
import configparser
import ctypes.wintypes as win
from utils import get_desktop_background, wrap_text_x

config = configparser.ConfigParser()

def get_taskbar_height():
    # Get handle to the taskbar
    hwnd = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)
    # Get bounding rectangle of the taskbar
    rect = win.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
    height = rect.bottom - rect.top
    return height

def sort_key(x):
    date_time = x.get('date_time', '').strip()

    # Case 1: Empty string
    if date_time == '':
        return (4,)

    # Case 2: Date-only (format '%Y-%m-%d')
    try:
        # Try parsing it as date-only
        date_obj = datetime.strptime(date_time, '%Y-%m-%d')
        return (3, date_obj)  # Return as date-only, sorted last but by date
    except ValueError:
        pass  # Not a date-only, proceed to check for other cases

    # Case 3: Time-only (format '%H:%M:%S')
    try:
        # Try parsing it as time-only
        time_obj = datetime.strptime(date_time, '%H:%M:%S')
        return (1, time_obj)  # Return as time-only, sorted first, then by time
    except ValueError:
        pass  # Not time-only, proceed to check for date-time

    # Case 4: Date and time (format '%Y-%m-%d %H:%M:%S')
    try:
        # Try parsing it as date and time
        date_time_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        return (2, date_time_obj)  # Return as date-time, sorted in the middle, by date-time
    except ValueError:
        pass  # In case there's an unexpected value

    # If none of the above, return a large value for unknown or malformed dates
    return (5,)

def format_datetime(date_time_str):
    # Case 1: If it's an empty string, just return it
    if not date_time_str.strip():
        return date_time_str

    # Case 2: If it's a date-only format ('%Y-%m-%d')
    try:
        date_obj = datetime.strptime(date_time_str, '%Y-%m-%d')
        return date_time_str  # Return the date-only string as it is
    except ValueError:
        pass  # Not a date-only, proceed to next case

    # Case 3: If it's a time-only format ('%H:%M:%S')
    try:
        time_obj = datetime.strptime(date_time_str, '%H:%M:%S')
        # Convert to 12-hour format with AM/PM
        return time_obj.strftime('%I:%M %p')
    except ValueError:
        pass  # Not a time-only, proceed to next case

    # Case 4: If it's a full date-time format ('%Y-%m-%d %H:%M:%S')
    try:
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
        # Convert to 12-hour format with AM/PM and include date
        return date_time_obj.strftime('%I:%M %p, %Y-%m-%d')
    except ValueError:
        pass  # Not a valid format, return original string as is

    # If none of the above, just return the original string
    return date_time_str

def update_tasks(date_time="", desc="", action="pass", colors=(-1, (255, 255, 255), (255, 255, 255)), prev = -1):
    if not desc:
        desc = "-----"
    if not date_time:
        date_time = "-----"
    config.read('config.ini')
    
    # Check if tasks.json exists and is not empty
    if os.path.exists('tasks.json') and os.path.getsize('tasks.json') > 0:
        # Load tasks from JSON file
        with open('tasks.json', 'r') as f:
            tasks = json.load(f)
    else:
        # Initialize tasks as an empty list
        tasks = []

        # Get desktop background image path
    background_image_path = get_desktop_background()
    # Create image with specified resolution and desktop background
    background_image = Image.open(background_image_path)
    if not os.path.isfile("original.png"):
        background_image.save("original.png")
    resolution = background_image.size  # Extract resolution from background image
    #print(resolution)

    # Add or remove task based on action
    if action == 'add':
        tasks.append({'date_time': date_time, 'desc': desc, 'color': colors})
        with open('tasks.json', 'w') as f:
            json.dump(tasks, f)
    elif action == 'delete':
        colors = list(colors)
        for i in range(len(colors)):
            if type(colors[i]) == tuple:
                colors[i] = list(colors[i])

        for i, task in enumerate(tasks):
            if task['date_time'] == date_time and task['desc'] == desc and task["color"] == colors:
                tasks.pop(i)  # Remove only the first occurrence
                break  # Stop after deleting the first match

        if len(tasks) == 0:
            background_image.save("output.png")
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, os.path.abspath("original.png").encode(), 0)
        with open('tasks.json', 'w') as f:
            json.dump(tasks, f)
    elif action == "edit":
        if prev:
            colors_x = list(prev["color"])
            for i in range(len(colors_x)):
                if type(colors_x[i]) == tuple:
                    colors_x[i] = list(colors_x[i])
            for i in range(len(tasks)):
                if tasks[i]['date_time'] == prev["date_time"] and tasks[i]['desc'] == prev["desc"] and tasks[i]["color"] == colors_x:
                    tasks[i]['date_time'], tasks[i]['desc'], tasks[i]["color"] = date_time, desc, colors
            with open('tasks.json', 'w') as f:
                json.dump(tasks, f)
            if len(tasks) == 0:
                background_image.save("output.png")
                SPI_SETDESKWALLPAPER = 20
                ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, os.path.abspath("original.png").encode(), 0)

    # Sort tasks by date_time (ascending)
    #tasks.sort(key=lambda x: datetime.strptime(x['date_time'], '%Y-%m-%d %H:%M:%S'))
    tasks.sort(key=sort_key)
    
    image = Image.new("RGBA", resolution, (255, 255, 255, 0))
    image.paste(Image.open("original.png"), (0, 0))
    draw = ImageDraw.Draw(image)

    # Define font and margin
    font = ImageFont.truetype("./fonts/" + config['Main']['font'] + ".ttf", int(config['Main']['font_size']))
    
    margin = int(config['Main']['box_margin'])
    padding = int(config['Main']['box_padding'])

    # Define box width and initial position
    box_width = (resolution[0] // int(config['Main']['box_width']))
    x = resolution[0] - margin  # Start from the right side
    y = margin

    # Calculate spacing relative to image resolution
    spacing_ratio = resolution[1] // 100  # Adjust spacing as needed
    spacing = spacing_ratio  # Double spacing between boxes

    # Draw boxes for each task
    for task in tasks:
        # Format date and time
        date_time_str = format_datetime(task['date_time'])
        desc_lines = wrap_text_x(task['desc'], font, box_width)

        # Calculate text height based on description and date_time
        box_height = math.floor((font.size * len(desc_lines) * 2.5) + (2 * padding))
        
        # Define color for text
        # White text color on black background
        # Draw rectangle for task box with negative color border
        if task["color"][0] != -1:
            draw.rounded_rectangle([x - box_width, y, x, y + box_height], outline=tuple(task["color"][2]), radius=int(config['Main']['border_radius']), fill=tuple(task["color"][0]), width=int(config['Main']['border_width']))
        else:
            draw.rounded_rectangle([x - box_width, y, x, y + box_height], outline=tuple(task["color"][2]), radius=int(config['Main']['border_radius']), width=int(config['Main']['border_width']))
        
        # Calculate text position within box
        text_x = x - box_width
        text_y = y + padding

        # Add text to task box with negative color
        for line in desc_lines:
            text_width = draw.textlength(line, font=font)
            text_x = x - box_width + (box_width - text_width) // 2
            draw.text((text_x, text_y), line, fill=tuple(task["color"][1]), font=font)
            text_y += font.size * 2
        
        
        text_width = draw.textlength(date_time_str, font=font)
        text_x = x - box_width + (box_width - text_width) // 2
        draw.text((text_x, text_y), date_time_str, fill=tuple(task["color"][1]), font=font)

        # Update y position for next box
        y += box_height + spacing  # Add spacing between boxes

        # Move to next column if y position exceeds image height
        if y + box_height > (resolution[1] - (get_taskbar_height() if int(config['Main']['taskbar_present']) == 1 else 0)):
            x -= box_width + spacing
            y = margin

    # Save the image
    image.save("output.png")
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, os.path.abspath("output.png").encode(), 0)
