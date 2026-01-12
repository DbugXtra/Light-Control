import asyncio
import tkinter as tk
from kasa import SmartPlug
import threading
import time

# --- CONFIGURATION ---
PLUG_IP = "192.168.1.XXX"  # Replace with your TP-Link Plug IP

class KasaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kasa Touch Control")
        
        # Optimized for 3.5" S2Pi Screen
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')

        # Initialize Kasa Plug
        self.plug = SmartPlug(PLUG_IP)
        
        # Setup UI
        self.setup_ui()
        
        # Start the background status polling thread
        self.update_status_loop()

    def setup_ui(self):
        """High-contrast UI for 480x320 resolution"""
        self.status_label = tk.Label(
            self.root, text="CONNECTING...", 
            font=("Arial", 16, "bold"), bg="black", fg="yellow"
        )
        self.status_label.pack(pady=(20, 10))

        btn_font = ("Arial", 22, "bold")
        
        # Large ON Button
        self.on_btn = tk.Button(
            self.root, text="LIGHT ON", bg="#27ae60", fg="white",
            activebackground="#2ecc71", font=btn_font,
            command=lambda: self.run_async(self.turn_on)
        )
        self.on_btn.pack(fill="both", expand=True, padx=30, pady=10)

        # Large OFF Button
        self.off_btn = tk.Button(
            self.root, text="LIGHT OFF", bg="#c0392b", fg="white",
            activebackground="#e74c3c", font=btn_font,
            command=lambda: self.run_async(self.turn_off)
        )
        self.off_btn.pack(fill="both", expand=True, padx=30, pady=10)

    # --- ASYNC LOGIC ---
    def run_async(self, coro):
        """Runs Kasa commands in a background thread to keep GUI responsive"""
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

    # --- STATUS REFRESH ---
    def update_status_loop(self):
        """Periodically syncs UI with the actual plug state"""
        def poll():
            while True:
                try:
                    asyncio.run(self.plug.update())
                    is_on = self.plug.is_on
                    self.root.after(0, self.refresh_ui, is_on)
                except Exception:
                    self.root.after(0, self.handle_error)
                time.sleep(3) # Check every 3 seconds
        
        threading.Thread(target=poll, daemon=True).start()

    def refresh_ui(self, is_on):
        """Updates colors and text based on plug state"""
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