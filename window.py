import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk, ImageEnhance, ImageDraw, ImageFont
from tkinterdnd2 import DND_FILES, TkinterDnD
import itertools

def drop(event):
    file_path = event.data
    if file_path:
        load_image(file_path)

def load_image(file_path):
    global img, img_label
    try:
        img = Image.open(file_path)
        img.thumbnail((400, 400))
        img_tk = ImageTk.PhotoImage(img)
        img_label.config(image=img_tk)
        img_label.image = img_tk
        show_options()
    except Exception as e:
        tk.messagebox.showerror("Error", f"Failed to load image: {str(e)}")

def show_options():
    options_frame.pack(pady=10)

def rotate_image():
    global img
    img = img.rotate(90, expand=True)
    update_image()

def resize_image():
    global img
    try:
        new_size = simpledialog.askstring("Resize", "Enter new size (width,height):")
        if new_size:
            try:
                width, height = map(int, new_size.split(','))
                if width <= 0 or height <= 0:
                    raise ValueError("Dimensions must be positive")
                img = img.resize((width, height))
                update_image()
            except ValueError as e:
                tk.messagebox.showerror("Error", "Invalid dimensions format. Use width,height (e.g., 800,600)")
    except Exception as e:
        tk.messagebox.showerror("Error", f"Failed to resize image: {str(e)}")

def adjust_gamma():
    global img
    gamma = simpledialog.askfloat("Gamma", "Enter gamma value (e.g., 1.0):")
    if gamma:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(gamma)
        update_image()

def update_image():
    img_tk = ImageTk.PhotoImage(img)
    img_label.config(image=img_tk)
    img_label.image = img_tk

def choose_screen_size():
    screen_size = simpledialog.askstring("Screen Size", "Enter screen size (width,height):")
    if screen_size:
        width, height = map(int, screen_size.split(','))
        speed = simpledialog.askinteger("Speed", "Enter movement speed (1-10):", minvalue=1, maxvalue=10)
        create_bouncing_image(width, height, speed)

def create_bouncing_image(width, height, speed):
    bounce_window = tk.Toplevel(root)
    bounce_window.geometry(f"{width}x{height}")
    bounce_window.configure(bg="black")
    
    # Add control buttons
    control_frame = tk.Frame(bounce_window, bg="black")
    control_frame.pack(side=tk.BOTTOM)
    
    is_running = True
    
    def toggle_animation():
        nonlocal is_running
        is_running = not is_running
        if is_running:
            move_image()
            toggle_btn.config(text="Pause")
        else:
            toggle_btn.config(text="Resume")
    
    toggle_btn = tk.Button(control_frame, text="Pause", command=toggle_animation)
    toggle_btn.pack(side=tk.LEFT, padx=5)
    
    bounce_img = ImageTk.PhotoImage(img)
    bounce_label = tk.Label(bounce_window, image=bounce_img, bg="black")
    bounce_label.image = bounce_img
    bounce_label.place(x=0, y=0)

    dx, dy = speed, speed

    def move_image():
        nonlocal dx, dy
        x, y = bounce_label.winfo_x(), bounce_label.winfo_y()
        if x + bounce_img.width() >= width or x <= 0:
            dx = -dx
        if y + bounce_img.height() >= height or y <= 0:
            dy = -dy
        bounce_label.place(x=x+dx, y=y+dy)
        bounce_window.after(50, move_image)

    bounce_window.after(50, move_image)

def change_color():
    colors = itertools.cycle(['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'])
    def update_color():
        try:
            label.config(fg=next(colors))
            root.after(100, update_color)
        except tk.TclError:
            pass  # Handle case where label is destroyed
    update_color()

def rotate_text(angle=0):
    def update_angle():
        nonlocal angle
        angle = (angle + 5) % 360
        rotated_image = create_rotated_text_image("BounceSome", angle)
        label.config(image=rotated_image)
        label.image = rotated_image
        root.after(50, update_angle)
    update_angle()

def create_rotated_text_image(text, angle):
    font = get_system_font()
    text_bbox = font.getbbox(text)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    image = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font, fill="white")
    rotated_image = image.rotate(angle, expand=1)
    return ImageTk.PhotoImage(rotated_image)

def get_system_font():
    system_fonts = ['arial.ttf', 'Arial.ttf', 'DejaVuSans.ttf', 'Helvetica']
    for font_name in system_fonts:
        try:
            return ImageFont.truetype(font_name, 24)
        except OSError:
            continue
    return ImageFont.load_default()

def float_text():
    dx, dy = 1, 1  # Movement speed
    is_first_update = True
    
    def update_position():
        nonlocal dx, dy, is_first_update
            
        # Get current window dimensions
        window_width = root.winfo_width()
        window_height = root.winfo_height()
        text_width = label.winfo_width()
        text_height = label.winfo_height()
        
        # Handle first update when widget sizes are ready
        if is_first_update and text_width > 0:
            is_first_update = False
            # Start from center of screen
            label.place(x=(window_width - text_width) // 2, 
                       y=(window_height - text_height) // 2)
            return
        
        x = label.winfo_x()
        y = label.winfo_y()
        
        # Update position
        next_x = x + dx
        next_y = y + dy
        
        # Check boundaries
        if next_x <= 0:
            next_x = 0
            dx = 1  # Move right
        elif next_x + text_width >= window_width:
            next_x = window_width - text_width
            dx = -1  # Move left
            
        if next_y <= 0:
            next_y = 0
            dy = 1  # Move down
        elif next_y + text_height >= window_height:
            next_y = window_height - text_height
            dy = -1  # Move up
        
        # Move the label
        label.place(x=next_x, y=next_y)
        root.after(500, update_position)
    
    # Start the animation after a short delay
    root.after(100, update_position)

def cleanup_resources():
    global img
    if img:
        img.close()

root = TkinterDnD.Tk()
root.geometry("800x600")
root.configure(bg="black")
root.title("BounceSome")

label = tk.Label(root, text="BounceSome", bg="black", fg="white", font=("Arial", 36))
label.place(relx=0.5, rely=0.5, anchor="center")

drop_label = tk.Label(root, text="Please drop a picture here", bg="black", fg="white", font=("Arial", 16))
drop_label.pack(pady=20)

img_label = tk.Label(root, bg="black")
img_label.place(x=300, y=200)

options_frame = tk.Frame(root, bg="black")
tk.Button(options_frame, text="Rotate", command=rotate_image).pack(side=tk.LEFT, padx=5)
tk.Button(options_frame, text="Resize", command=resize_image).pack(side=tk.LEFT, padx=5)
tk.Button(options_frame, text="Adjust Gamma", command=adjust_gamma).pack(side=tk.LEFT, padx=5)
tk.Button(options_frame, text="Next", command=choose_screen_size).pack(side=tk.LEFT, padx=5)

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)

change_color()
float_text()

root.mainloop()
#cursor