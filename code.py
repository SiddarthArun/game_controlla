# code.py — Pico W D-Pad using keyboard HID
# Uses built-in usb_hid + adafruit_hid Keyboard (no Gamepad needed)

import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import time

# ── Pin map + key bindings ───────────────────────────────────
#
#   GP0 ──[UP]──── GND   → Arrow Up
#   GP2 ──[DOWN]── GND   → Arrow Down
#   GP4 ──[LEFT]── GND   → Arrow Left
#   GP6 ──[RIGHT]─ GND   → Arrow Right
#
DPAD = {
    "up":    {"pin": board.GP0, "key": Keycode.UP_ARROW},
    "down":  {"pin": board.GP2, "key": Keycode.DOWN_ARROW},
    "left":  {"pin": board.GP4, "key": Keycode.LEFT_ARROW},
    "right": {"pin": board.GP6, "key": Keycode.RIGHT_ARROW},
}

# ── Setup ────────────────────────────────────────────────────
kbd = Keyboard(usb_hid.devices)

buttons = {}
for name, cfg in DPAD.items():
    io = digitalio.DigitalInOut(cfg["pin"])
    io.direction = digitalio.Direction.INPUT
    io.pull = digitalio.Pull.UP  # LOW = pressed
    buttons[name] = {"io": io, "key": cfg["key"], "pressed": False}

print("D-Pad ready.")

# ── Debounce ─────────────────────────────────────────────────
DEBOUNCE_MS = 10
last_change = {name: 0 for name in DPAD}

# ── Main loop ────────────────────────────────────────────────
while True:
    now = time.monotonic_ns() // 1_000_000

    for name, state in buttons.items():
        pressed = not state["io"].value

        if pressed != state["pressed"]:
            if (now - last_change[name]) >= DEBOUNCE_MS:
                if pressed:
                    kbd.press(state["key"])
                    print(f"D-Pad {name} pressed")
                else:
                    kbd.release(state["key"])
                    print(f"D-Pad {name} released")

                state["pressed"] = pressed
                last_change[name] = now

    time.sleep(0.005)
