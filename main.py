import tkinter as tk
from PIL import Image, ImageTk
import random
import time
import threading
import os


class GiorgosApp:
    def __init__(self, idle_path, walk_path, gesture_path, lines_path):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "pink")

        self.size = 200
        self.follow_radius = 120
        self.canvas = tk.Canvas(self.root, width=self.size, height=self.size, bg='pink', highlightthickness=0)
        self.canvas.pack()

        # Load images
        self.idle_image = ImageTk.PhotoImage(Image.open(idle_path).resize((self.size, self.size), Image.Resampling.NEAREST))
        self.walk_image = ImageTk.PhotoImage(Image.open(walk_path).resize((self.size, self.size), Image.Resampling.NEAREST))
        self.gesture_image = ImageTk.PhotoImage(Image.open(gesture_path).resize((self.size, self.size), Image.Resampling.NEAREST))

        self.current_image = self.canvas.create_image(0, 0, anchor='nw', image=self.idle_image)
        self.canvas.bind("<Button-1>", self.animate_gesture)

        self.vx = 0
        self.vy = 0
        self.running = True
        self.gesturing = False
        self.last_wander_time = time.time()

        # Load quote lines
        self.quote_label = None
        self.quote_visible = False
        self.lines_path = lines_path
        with open(lines_path, 'r', encoding='utf-8') as f:
            self.quotes = [line.strip() for line in f if line.strip()]

        # Start behavior and quote threads
        threading.Thread(target=self.behavior_loop, daemon=True).start()
        threading.Thread(target=self.say_random_quote_loop, daemon=True).start()

    def animate_gesture(self, event=None):
        if not self.gesturing:
            self.gesturing = True
            self.canvas.itemconfig(self.current_image, image=self.gesture_image)
            self.root.after(400, self.end_gesture)

    def end_gesture(self):
        if not self.quote_visible:  # Only go back to idle if not showing a quote
            self.gesturing = False
            self.canvas.itemconfig(self.current_image, image=self.idle_image)

    def say_random_quote_loop(self):
        while self.running:
            time.sleep(random.randint(10, 20))  # Wait between 10 and 20 seconds
            if not self.quote_visible and not self.gesturing:
                quote = random.choice(self.quotes)
                self.show_quote(quote)

    def show_quote(self, text):
        self.quote_visible = True
        self.gesturing = True
        self.canvas.itemconfig(self.current_image, image=self.gesture_image)

        if self.quote_label:
            self.quote_label.destroy()

        parts = [part.strip() for part in text.split('-') if part.strip()]
        current_index = 0

        def show_part(index):
            nonlocal current_index
            if self.quote_label:
                self.quote_label.destroy()

            self.quote_label = tk.Label(
                self.root,
                text=parts[index],
                bg="white",
                fg="black",
                font=("Arial", 10),
                wraplength=180,
                justify="center",
                bd=2,
                relief="solid"
            )
            self.quote_label.place(x=20, y=0)

            current_index += 1
            if current_index < len(parts):
                self.root.after(2000, lambda: show_part(current_index))
            else:
                self.root.after(4000, hide)

        def hide():
            if self.quote_label:
                self.quote_label.destroy()
                self.quote_label = None
            self.quote_visible = False
            self.gesturing = False
            self.canvas.itemconfig(self.current_image, image=self.idle_image)

        show_part(current_index)


    def behavior_loop(self):
        while self.running:
            time.sleep(0.016)

            try:
                mx, my = self.root.winfo_pointerx(), self.root.winfo_pointery()
                x, y = self.root.winfo_x(), self.root.winfo_y()

                center_x = x + self.size // 2
                center_y = y + self.size // 2

                dx = mx - center_x
                dy = my - center_y
                dist = (dx**2 + dy**2)**0.5

                if dist > self.follow_radius:
                    direction_x = dx / dist
                    direction_y = dy / dist
                    speed = min(6, dist * 0.1)
                    new_x = x + direction_x * speed
                    new_y = y + direction_y * speed
                    self.root.geometry(f"+{int(new_x)}+{int(new_y)}")

                    if not self.gesturing:
                        self.canvas.itemconfig(self.current_image, image=self.walk_image)
                else:
                    if not self.gesturing:
                        self.canvas.itemconfig(self.current_image, image=self.idle_image)

                    if time.time() - self.last_wander_time > 3:
                        offset_x = random.randint(-20, 20)
                        offset_y = random.randint(-20, 20)
                        self.last_wander_time = time.time()
                        if not self.gesturing:
                            self.canvas.itemconfig(self.current_image, image=self.walk_image)
                        for _ in range(10):
                            x += offset_x / 10
                            y += offset_y / 10
                            self.root.geometry(f"+{int(x)}+{int(y)}")
                            time.sleep(0.02)
            except:
                pass

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    idle_path = os.path.join(script_dir, "giorgos1.png")
    walk_path = os.path.join(script_dir, "giorgoswalkleft.png")
    gesture_path = os.path.join(script_dir, "giorgos2.png")
    lines_path = os.path.join(script_dir, "georgioslines.txt")

    app = GiorgosApp(idle_path, walk_path, gesture_path, lines_path)
    app.run()
