# 💡 RPi 5 Kasa Light Control

A lightweight, fullscreen Python GUI designed for the **S2Pi 3.5" Touchscreen** and **Raspberry Pi 5**. This application provides an easy-to-use interface to control a TP-Link Kasa Smart Plug.

## ✨ Features

* **Protocol Support:** Uses the modern `kasa.Discover` method (compatible with older plugs and newer Matter devices).
* **Invisible Cursor:** The mouse pointer is hidden natively via Tkinter for a clean touch experience.
* **Real-time Status:** Synchronizes with the plug state every 3 seconds (even if the light is switched via the Kasa mobile app).
* **Resilient Design:** Background threading ensures the UI never freezes during network timeouts.
---

## 🛠 Setup & Installation

### 1. Project Directory

Ensure your files are located in `/home/<user>/Light-Control`.

### 2. Prepare the Virtual Environment

```bash
cd /home/<user>/Light-Control
python3 -m venv venv
./venv/bin/pip install python-kasa
```

### 3. Configuration

Open `light-control.py` and update the `PLUG_IP` variable:

```python
PLUG_IP = "192.168.1.XXX"  # Use your plug's static IP
```

---

## 🧪 Testing

To test the interface manually while logged in via terminal or SSH, use the following command to target the local display:

```bash
DISPLAY=:0 ./venv/bin/python3 light-control.py
```

---

## ⚙️ Auto-Start (Systemd)

To have the application start automatically when the Pi boots into the desktop, create a service file:

`sudo nano /etc/systemd/system/light_control.service`

**Paste the following:**

```ini
[Unit]
Description=Kasa Touchscreen Control
After=graphical.target

[Service]
User=<user>
WorkingDirectory=/home/<user>/Light-Control
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/<user>/.Xauthority
ExecStartPre=/bin/sleep 10
ExecStart=/home/<user>/Light-Control/venv/bin/python3 light-control.py
Restart=always
RestartSec=10

[Install]
WantedBy=graphical.target
```

### Enable and Start

```bash
sudo systemctl daemon-reload
sudo systemctl enable light_control.service
sudo systemctl start light_control.service
```

---

## 🛠 Troubleshooting & Maintenance

| Action | Command |
| --- | --- |
| **Check if running** | `systemctl status light_control.service` |
| **View real-time logs** | `journalctl -u light_control.service -f` |
| **Stop the app** | `sudo systemctl stop light_control.service` |
| **Restart the app** | `sudo systemctl restart light_control.service` |

### Disabling Screen Blanking

To ensure the screen stays on and doesn't turn black after 10 minutes:

1. Run `sudo raspi-config`.
2. Navigate to **Display Options** > **Screen Blanking**.
3. Select **No** and finish.
---
