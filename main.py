import tkinter as tk
from PIL import Image, ImageTk
import random
import time
import threading
import os


class GiorgosApp:
    def __init__(self, idle_path, walk_path, gesture_path):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "pink")

        self.size = 256
        self.canvas = tk.Canvas(self.root, width=self.size, height=self.size, bg='pink', highlightthickness=0)
        self.canvas.pack()

        # Load images
        self.idle_image = ImageTk.PhotoImage(
            Image.open(idle_path).resize((self.size, self.size), Image.Resampling.NEAREST)
        )
        self.walk_image = ImageTk.PhotoImage(
            Image.open(walk_path).resize((self.size, self.size), Image.Resampling.NEAREST)
        )
        self.gesture_image = ImageTk.PhotoImage(
            Image.open(gesture_path).resize((self.size, self.size), Image.Resampling.NEAREST)
        )

        self.current_image = self.canvas.create_image(0, 0, anchor='nw', image=self.idle_image)

        self.canvas.bind("<Button-1>", self.animate_gesture)

        self.running = True
        self.start_behavior_threads()

    def animate_gesture(self, event=None):
        self.canvas.itemconfig(self.current_image, image=self.gesture_image)
        self.root.after(400, lambda: self.canvas.itemconfig(self.current_image, image=self.idle_image))

    def move_giorgos(self):
        while self.running:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = random.randint(0, screen_width - self.size)
            y = random.randint(0, screen_height - self.size)

            # Set walking image
            self.canvas.itemconfig(self.current_image, image=self.walk_image)

            # Animate smooth movement
            for _ in range(30):
                current_x = self.root.winfo_x()
                current_y = self.root.winfo_y()
                step_x = (x - current_x) // 10
                step_y = (y - current_y) // 10
                self.root.geometry(f"+{current_x + step_x}+{current_y + step_y}")
                time.sleep(0.05)

            # Go back to idle
            self.canvas.itemconfig(self.current_image, image=self.idle_image)

            time.sleep(5)

    def look_at_mouse(self):
        while self.running:
            try:
                mouse_x = self.root.winfo_pointerx()
                mouse_y = self.root.winfo_pointery()
                window_x = self.root.winfo_x()
                window_y = self.root.winfo_y()

                # If mouse is close, "look" (change image, or later add face direction)
                if abs(mouse_x - window_x) < 200 and abs(mouse_y - window_y) < 200:
                    self.canvas.itemconfig(self.current_image, image=self.idle_image)
                time.sleep(2)
            except:
                pass

    def start_behavior_threads(self):
        threading.Thread(target=self.move_giorgos, daemon=True).start()
        threading.Thread(target=self.look_at_mouse, daemon=True).start()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    idle_path = os.path.join(script_dir, "giorgos1.png")
    walk_path = os.path.join(script_dir, "giorgoswalkleft.png")
    gesture_path = os.path.join(script_dir, "giorgos2.png")

    app = GiorgosApp(idle_path, walk_path, gesture_path)
    app.run()

