import tkinter as tk
import json
import os
import sys

SAVE_FILE = "save.json"

# ================= SAVE =================
def load_save():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)

save = load_save()

# ================= ROOT =================
root = tk.Tk()
root.title("raspi~$")
root.configure(bg="black")
root.attributes("-fullscreen", True)
root.protocol("WM_DELETE_WINDOW", lambda: None)

FONT = ("Courier", 14)
stage = "terminal"
player_name = ""

# ================= TERMINAL =================
text = tk.Text(
    root,
    bg="black",
    fg="#00ff00",
    insertbackground="#00ff00",
    font=FONT,
    borderwidth=0
)
text.pack(fill="both", expand=True)
text.focus()

def write(msg):
    text.insert("end", msg)
    text.see("end")

write(
    "raspi~$ boot\n"
    "Booting Training OS...\n\n"
    "Enter your name:\n"
    "raspi~$ "
)

# ================= TRAINING =================
def start_training():
    global stage
    stage = "training"

    root.attributes("-fullscreen", False)
    root.overrideredirect(True)
    root.geometry("420x240+100+100")
    root.configure(bg="white")

    for w in root.winfo_children():
        w.destroy()

    canvas = tk.Canvas(root, bg="white", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # arrow parts
    arrow_line = canvas.create_line(0, 0, 0, 0, width=4, fill="black")
    arrow_head = canvas.create_polygon(0, 0, 0, 0, 0, 0, fill="black")

    hint_text = canvas.create_text(
        210, 200,
        text="Enter — continue | Escape — exit",
        font=("Arial", 11),
        fill="gray"
    )

    message = canvas.create_text(
        210, 40,
        text="",
        font=("Arial", 14),
        fill="black"
    )

    # steps: window pos, arrow start/end, text
    steps = [
        {"win": (100, 100), "arrow": (40, 120, 160, 120), "text": "This is your workspace"},
        {"win": (600, 120), "arrow": (160, 60, 60, 60), "text": "Windows can move freely"},
        {"win": (300, 400), "arrow": (40, 160, 160, 80), "text": "Follow visual instructions"},
        {"win": (800, 300), "arrow": (160, 160, 60, 80), "text": "Training almost complete"}
    ]

    step = -1

    def apply_step():
        data = steps[step]
        x, y = data["win"]
        root.geometry(f"+{x}+{y}")

        x1, y1, x2, y2 = data["arrow"]
        canvas.coords(arrow_line, x1, y1, x2, y2)
        canvas.coords(
            arrow_head,
            x2, y2,
            x2 - 15, y2 - 8,
            x2 - 15, y2 + 8
        )
        canvas.itemconfig(message, text=data["text"])

    def next_step(event=None):
        nonlocal step
        step += 1
        if step >= len(steps):
            finish_training()
            return
        apply_step()

    root.bind("<Return>", next_step)
    root.bind("<Escape>", lambda e: root.destroy())

    next_step()

# ================= FINISH =================
def finish_training():
    save["player"] = {"name": player_name}
    save["system"] = {"training_complete": True}
    save_data(save)

    root.destroy()
    # запуск следующей программы RabbitGame.py
    os.execv(sys.executable, [sys.executable, "RabbitGame.py"])

# ================= INPUT =================
def on_enter(event):
    global player_name

    if stage != "terminal":
        return "break"

    line = text.get("insert linestart", "insert lineend")
    cmd = line.replace("raspi~$ ", "").strip()
    write("\n")

    if player_name == "":
        player_name = cmd
        write(f"Welcome, {player_name}\n")
        write("Type 'start' to begin training or 'run' to launch the game\nraspi~$ ")
    elif cmd.lower() == "start":
        start_training()
    elif cmd.lower() == "run":
        # сохраняем имя
        save["player"] = {"name": player_name}
        save_data(save)

        # запускаем другую программу
        root.destroy()
        os.execv(sys.executable, [sys.executable, "rabbit_game.py"])
    else:
        write("Command not found\nraspi~$ ")

    return "break"

def on_escape(event):
    root.destroy()

# ================= BINDS =================
text.bind("<Return>", on_enter)
root.bind("<Escape>", on_escape)

root.mainloop()
