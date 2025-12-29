import pygame
import random
import json
import os
import sys
import time

# ================= CONFIG =================
SAVE_FILE = "save.json"
FPS = 60
RABBIT_SPEED = 8
TRAIL_LIFETIME = 60

# ================= SAVE =================
def load_save():
    if not os.path.exists(SAVE_FILE):
        return {
            "player": {"name": "Player"},
            "system": {"anger_level": 0}
        }
    with open(SAVE_FILE, "r") as f:
        return json.load(f)

def wipe_save():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)

save = load_save()
player_name = sys.argv[1] if len(sys.argv) > 1 else save["player"]["name"]

# ================= INIT =================
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Chocolate Rabbit")
clock = pygame.time.Clock()

WIDTH, HEIGHT = screen.get_size()

# ================= COLORS =================
BG = (30, 18, 10)
CHOCOLATE = (90, 50, 30)
TRAIL = (120, 70, 40)
WHITE = (240, 240, 240)
DARK = (10, 10, 10)

font = pygame.font.SysFont("arial", 24)

# ================= RABBIT =================
rabbit = pygame.Rect(WIDTH//2, HEIGHT//2, 40, 40)
trail = []

def move_rabbit():
    rabbit.x += random.choice([-1, 1]) * RABBIT_SPEED
    rabbit.y += random.choice([-1, 1]) * RABBIT_SPEED

    rabbit.clamp_ip(screen.get_rect())

    trail.append([rabbit.centerx, rabbit.centery, TRAIL_LIFETIME])

# ================= STORY =================
dialog = [
    f"{player_name}...",
    "This is not your desktop.",
    "This is a world inside Raspberry Pi.",
    "You tried to catch me.",
    "But chocolate cannot be caught.",
    "I lost my power to melt.",
    "I lost my power to travel screens.",
    "But my mother power remains.",
    "Talk too much...",
    "And I will erase your save."
]

dialog_index = 0
darken = False
end_triggered = False

def draw_dialog():
    text = font.render(dialog[dialog_index], True, WHITE)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT - 100))

# ================= MAIN LOOP =================
running = True
while running:
    clock.tick(FPS)
    screen.fill(BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_SPACE:
                dialog_index += 1
                save["system"]["anger_level"] += 1

                if dialog_index >= len(dialog):
                    end_triggered = True
                    darken = True

                with open(SAVE_FILE, "w") as f:
                    json.dump(save, f, indent=2)

    if not end_triggered:
        move_rabbit()

    # ===== TRAIL =====
    for t in trail[:]:
        t[2] -= 1
        pygame.draw.circle(screen, TRAIL, (t[0], t[1]), 6)
        if t[2] <= 0:
            trail.remove(t)

    # ===== RABBIT =====
    pygame.draw.ellipse(screen, CHOCOLATE, rabbit)

    # ===== DIALOG =====
    if dialog_index < len(dialog):
        draw_dialog()

    # ===== DARK END =====
    if darken:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(10)
        overlay.fill(DARK)
        screen.blit(overlay, (0, 0))

        if save["system"]["anger_level"] > 8:
            screen.fill(DARK)
            end_text = font.render(
                "You talked too much. Save deleted.", True, WHITE
            )
            screen.blit(
                end_text,
                (WIDTH//2 - end_text.get_width()//2, HEIGHT//2)
            )
            pygame.display.flip()
            time.sleep(2)
            wipe_save()
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
