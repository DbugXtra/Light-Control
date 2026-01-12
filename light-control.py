import asyncio
import tkinter as tk
from kasa import Discover
import threading
import time

# --- CONFIGURATION ---
PLUG_IP = "192.168.1.XXX"  # Replace with your TP-Link Plug IP

class KasaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kasa Touch Control")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')

        # State variable for the device object
        self.device = None
        
        self.setup_ui()
        
        # Start the background logic
        self.update_status_loop()

    def setup_ui(self):
        """High-contrast UI for 480x320 resolution"""
        self.status_label = tk.Label(
            self.root, text="CONNECTING...", 
            font=("Arial", 16, "bold"), bg="black", fg="yellow"
        )
        self.status_label.pack(pady=(20, 10))

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

    def run_async(self, coro):
        threading.Thread(target=lambda: asyncio.run(coro()), daemon=True).start()

    async def _ensure_connected(self):
        """Initializes device using the new discovery method if not already connected"""
        if self.device is None:
            try:
                # This is the new recommended way to connect to a single device
                self.device = await Discover.discover_single(PLUG_IP)
            except Exception:
                return False
        return True

    async def turn_on(self):
        if await self._ensure_connected():
            try:
                await self.device.turn_on()
                self.root.after(0, self.refresh_ui, True)
            except Exception:
                self.root.after(0, self.handle_error)

    async def turn_off(self):
        if await self._ensure_connected():
            try:
                await self.device.turn_off()
                self.root.after(0, self.refresh_ui, False)
            except Exception:
                self.root.after(0, self.handle_error)

    def update_status_loop(self):
        """Periodically syncs UI with the actual plug state"""
        def poll():
            while True:
                # Use a new event loop for this thread's async calls
                asyncio.run(self._poll_logic())
                time.sleep(3)

        threading.Thread(target=poll, daemon=True).start()

    async def _poll_logic(self):
        if await self._ensure_connected():
            try:
                await self.device.update()
                is_on = self.device.is_on
                self.root.after(0, self.refresh_ui, is_on)
            except Exception:
                self.root.after(0, self.handle_error)
        else:
            self.root.after(0, self.handle_error)

    def refresh_ui(self, is_on):
        if is_on:
            self.status_label.config(text="● LIGHT IS ON", fg="#2ecc71")
            self.root.configure(bg="#0a1a0a")
        else:
            self.status_label.config(text="○ LIGHT IS OFF", fg="#7f8c8d")
            self.root.configure(bg="black")

    def handle_error(self):
        self.status_label.config(text="⚠ PLUG OFFLINE", fg="#e74c3c")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("480x320") 
    app = KasaApp(root)
    root.mainloop()