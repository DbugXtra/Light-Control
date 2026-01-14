<p align="center">
  <a href="https://donate.stripe.com/5kQ4gAa0b4pP7YQaW35EY00">
    <img src="./stripe-donate-qrcode.png"
         alt="Scan to buy us a coffee with Stripe"
         width="150"
         height="150"
         style="border: 2px solid #6772E5; border-radius: 5px;">
  </a>
  <br>
  <medium>Click or Scan to Buy us a Coffee</medium>
</p>

# 💡 RPi 5 Kasa Light Control

A fullscreen, touch-optimized Python GUI for controlling TP-Link Kasa Smart Plugs. Designed specifically for the Raspberry Pi 5 and 3.5" S2Pi touchscreen.

## ✨ Features

* **Wayland Compatible:** Optimized for the Pi 5's default display engine.
* **Touch-First UI:** Large buttons and no visible mouse cursor.
* **Live Sync:** Updates plug status every 3 seconds to reflect changes made via the Kasa app.
* **Auto-Recovery:** Automatically attempts to reconnect if the plug goes offline.

---

## 🛠 Setup & Installation

### 1. Project Directory

Ensure your files are located in `/home/<user>/Light-Control`.

### 2. Prepare the Environment

```bash
cd /home/<user>/Light-Control
python3 -m venv venv
./venv/bin/pip install python-kasa
```

### 3. Configuration

Update the `PLUG_IP` in `light-control.py` with your smart plug's IP address.

---

## 🚀 Auto-Start (Recommended Method)

On Raspberry Pi 5, launching via the desktop environment is more reliable than using a systemd service.

1. **Create the autostart directory:**
```bash
mkdir -p /home/<user>/.config/autostart
```


2. **Create the shortcut file:**
```bash
nano /home/<user>/.config/autostart/light-control.desktop
```


3. **Paste the following content:**
```ini
[Desktop Entry]
Type=Application
Name=Kasa Light Control
Comment=Launch Kasa Touchscreen UI
Exec=/home/<user>/Light-Control/venv/bin/python3 /home/<user>/Light-Control/light-control.py
Terminal=false
Categories=Utility;
```



---

## 🧪 Testing & Manual Run

If you need to run the app manually for debugging, use:

```bash
# From the project folder
./venv/bin/python3 light-control.py
```

---

## 🛠 Troubleshooting

| Issue | Solution |
| --- | --- |
| **"Plug Offline"** | Verify the IP address in the Kasa App. Ensure the Pi and Plug are on the same 2.4GHz Wi-Fi band. |
| **App won't start** | Check for errors by running manually in the terminal: `./venv/bin/python3 light-control.py` |
| **Screen turns black** | Disable screen blanking: `sudo raspi-config` -> **Display Options** -> **Screen Blanking** -> **No**. |
| **Cursor is visible** | Ensure `self.root.config(cursor="none")` is present in the `__init__` section of the script. |
---
