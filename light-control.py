import asyncio
import tkinter as tk
from kasa import SmartPlug
from gpiozero import MotionSensor, DigitalOutputDevice
import threading
import time

# --- CONFIGURATION ---
PLUG_IP = "192.168.1.XXX"  # Change to your actual Kasa Plug IP
PIR_PIN = 17                # GPIO for PIR Motion Sensor
BACKLIGHT_PIN = 18          # GPIO for Screen Backlight (Check S2Pi manual)

class KasaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kasa Touch Control")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')

        # Initialize Hardware
        self.plug = SmartPlug(PLUG_IP)
        self.pir = MotionSensor(PIR_PIN)
        
        # Using DigitalOutputDevice for the backlight to ensure clean ON/OFF
        self.backlight = DigitalOutputDevice(BACKLIGHT_PIN, initial_value=True)
        
        # Setup GUI elements
        self.setup_ui()
        
        # Hardware Event Triggers
        self.pir.when_motion = self.wake_screen
        self.pir.when_no_motion = self.sleep_screen

        # Start the background status polling thread
        self.update_status_loop()

    def setup_ui(self):
        """Creates a high-contrast UI optimized for 3.5 inch resistive touchscreens"""
        # Status Header
        self.status_label = tk.Label(
            self.root, text="INITIALIZING...", 
            font=("Arial", 16, "bold"), bg="black", fg="yellow"
        )
        self.status_label.pack(pady=(20, 10))

        # Action Buttons
        btn_font = ("Arial", 22, "bold")
        
        self.on_btn = tk.Button(
            self.root, text="LIGHT ON", bg="#27ae60", fg="white",
            activebackground="#2ecc71", font=btn_font,
            command=lambda: self.run_async(self.turn_on)
        )
        self.on_btn.pack(fill="both", expand=True, padx=30, pady=10)

        self.off_btn = tk.Button(
            self.root, text="LIGHT OFF", bg="#c0392b", fg="white",
            activebackground="#e74c3c", font=btn_font,
            command=lambda: self.run_async(self.turn_off)
        )
        self.off_btn.pack(fill="both", expand=True, padx=30, pady=10)

    # --- ASYNC BRIDGE ---
    def run_async(self, coro):
        """Bridge between Tkinter (Synchronous) and Kasa (Asynchronous)"""
        threading.Thread(target=lambda: asyncio.run(coro()), daemon=True).start()

    async def turn_on(self):
        try:
            await self.plug.turn_on()
            self.root.after(0, self.refresh_ui, True)
        except Exception:
            self.root.after(0, self.handle_error)

    async def turn_off(self):
        try:
            await self.plug.turn_off()
            self.root.after(0, self.refresh_ui, False)
        except Exception:
            self.root.after(0, self.handle_error)

    # --- STATUS POLLING ---
    def update_status_loop(self):
        """Checks the plug state every 3 seconds to keep UI synced with Kasa App"""
        def poll():
            while True:
                try:
                    asyncio.run(self.plug.update())
                    is_on = self.plug.is_on
                    self.root.after(0, self.refresh_ui, is_on)
                except Exception:
                    self.root.after(0, self.handle_error)
                time.sleep(3)
        
        threading.Thread(target=poll, daemon=True).start()

    def refresh_ui(self, is_on):
        """Updates UI theme based on current state"""
        if is_on:
            self.status_label.config(text="● LIGHT IS ON", fg="#2ecc71")
            self.root.configure(bg="#0a1a0a") # Very dark green background
        else:
            self.status_label.config(text="○ LIGHT IS OFF", fg="#7f8c8d")
            self.root.configure(bg="black")

    def handle_error(self):
        self.status_label.config(text="⚠ PLUG OFFLINE", fg="#e74c3c")

    # --- SCREEN POWER MANAGEMENT ---
    def wake_screen(self):
        self.backlight.on()

    def sleep_screen(self):
        self.backlight.off()

if __name__ == "__main__":
    root = tk.Tk()
    # Forces the application to take up the full 3.5" screen
    root.geometry("480x320") 
    app = KasaApp(root)
    root.mainloop()