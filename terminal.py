import tkinter as tk
import json
import sys
import os
import time

SAVE_FILE = "save.json"

# ================= SAVE =================
def load_save():
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE, "r") as f:
        return json.load(f)

def wipe_save():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)

save = load_save()

player_name = sys.argv[1] if len(sys.argv) > 1 else "User"

# ================= WINDOW =================
root = tk.Tk()
root.title("Chocolate Rabbit")
root.configure(bg="#2b1b0e")
root.attributes("-fullscreen", True)

canvas = tk.Canvas(root, bg="#2b1b0e", highlightthickness=0)
canvas.pack(fill="both", expand=True)

w = root.winfo_screenwidth()
h = root.winfo_screenheight()

# ================= RABBIT =================
rabbit = canvas.create_oval(
    w//2 - 40, h//2 - 40,
    w//2 + 40, h//2 + 40,
    fill="#5a2e1a", outline="#ffcccc", width=3
)

text = canvas.create_text(
    w//2, h//2 + 80,
    text="Chocolate Rabbit is watching you...",
    fill="white",
    font=("Arial", 20)
)

stage = 0
anger = save["system"]["anger_level"] if save else 0

# ================= DIALOG =================
DIALOG = [
    f"{player_name}...",
    "You reached the end of the screen.",
    "I lost my power to melt.",
    "I lost my power to jump between screens.",
    "But my mother power remains.",
    "If you talk to me too much...",
    "I will reset your save.",
    "This is not a joke.",
    "Press SPACE to continue.",
]

def update_text():
    canvas.itemconfig(text, text=DIALOG[stage])

# ================= INPUT =================
def on_key(event):
    global stage, anger

    if event.keysym == "space":
        stage += 1

        anger += 1
        if save:
            save["system"]["anger_level"] = anger
            with open(SAVE_FILE, "w") as f:
                json.dump(save, f, indent=2)

        if stage >= len(DIALOG):
            final_event()
        else:
            update_text()

    elif event.keysym == "Escape":
        root.destroy()

# ================= FINAL =================
def final_event():
    canvas.itemconfig(
        text,
        text="You talked too much.\nSave deleted.\nRestarting adventure..."
    )

    root.update()
    time.sleep(2)

    wipe_save()
    root.destroy()

# ================= MOVE RABBIT =================
dx, dy = 3, 2

def move_rabbit():
    global dx, dy
    x1, y1, x2, y2 = canvas.coords(rabbit)

    if x1 <= 0 or x2 >= w:
        dx *= -1
    if y1 <= 0 or y2 >= h:
        dy *= -1

    canvas.move(rabbit, dx, dy)
    root.after(16, move_rabbit)

# ================= START =================
update_text()
move_rabbit()

root.bind("<Key>", on_key)
root.mainloop()
