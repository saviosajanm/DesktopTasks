import datetime
from PIL import Image, ImageFont, ImageDraw
import math
import winreg

def get_desktop_background():
    key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, winreg.KEY_READ)
    wallpaper_value, _ = winreg.QueryValueEx(key, "Wallpaper")
    return wallpaper_value

def hex_to_rgb(hex_code):
    hex_code = hex_code.strip('#')
    length = len(hex_code)
    rgb_values = tuple(int(hex_code[i:i+2], 16) for i in range(0, length, 2))
    if length == 3:
        rgb_values = rgb_values * 2
    return rgb_values

def wrap_text(text):
    max_chars = 25
    lines = []
    words = text.split()
    line = ''
    i = 0
    while i < len(words):
        if len(words[i]) >= max_chars:
            words.insert(i+1, words[i][(max_chars - 2):])
            words[i] = words[i][:max_chars - 2] + "-"
        i+= 1
    for word in words:
        if len(line) + len(word) <= max_chars:
            line += '\n' + word
        else:
            lines.append(line.strip())
            line = word
    lines.append(line.strip())
    #print(lines)
    return lines

def wrap_text_x(text, font, max_width):
    max_chars = math.floor(pixels_to_characters(max_width, font.path, font.size) / 1.5)
    lines = []
    words = text.split()
    line = ''
    i = 0
    while i < len(words):
        if len(words[i]) >= max_chars:
            words.insert(i+1, words[i][(max_chars - 2):])
            words[i] = words[i][:max_chars - 2] + "-"
        i+= 1
    for word in words:
        if len(line) + len(word) <= max_chars:
            line += ' ' + word
        else:
            lines.append(line.strip())
            line = word
    lines.append(line.strip())
    return lines

def convert_to_datetime(date_str, hour_str, minute_str, ampm):
    year = int(date_str[:4])
    month = int(date_str[5:7])
    day = int(date_str[8:])
    hour = int(hour_str)
    if ampm == "PM" and hour != 12:
      hour += 12  # Convert hour to 24-hour format in PM cases (except 12 PM)
    elif ampm == "AM" and hour == 12:
      hour = 0  # Convert 12 AM to 00 in 24-hour format
    minute = int(minute_str)
    if not (1 <= hour <= 24 and 0 <= minute <= 59):
      raise ValueError("Invalid hour or minute value")
    combined_datetime = datetime.datetime(year, month, day, hour, minute)
    return combined_datetime.strftime("%Y-%m-%d %H:%M:%S")

def rgb_to_hex(rgb_tuple):
    hex_code = "#" + ''.join(f"{val:02x}" for val in rgb_tuple)
    return hex_code

def pixels_to_characters(width, font_path, font_size, text='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'):
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    chars = ''
    char_count = 0
    for char in text:
        char_width = draw.textlength(char, font=font)
        if char_count > 0 and chars[-1].islower() and char.isupper():
            char_count += 1  # Add spacing for capital letter
        if char_count + char_width <= width:
            chars += char
            char_count += char_width
        else:
            break
    return len(chars)