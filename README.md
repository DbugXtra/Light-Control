
---

# 💡 RPi 5 Kasa Touch-Control

A lightweight, efficient Python GUI for controlling a TP-Link Kasa Smart Plug using a 3.5" S2Pi touchscreen and a PIR motion sensor.

## 📋 Features

* **Real-time Status:** Automatically polls the plug status every 3 seconds to reflect changes made via the Kasa app.
* **Motion Activation:** Turns the screen backlight ON/OFF based on room occupancy to save power and screen life.
* **Pi 5 Optimized:** Uses a Virtual Environment (`venv`) and `systemd` for 2026-standard Raspberry Pi OS compatibility.
* **Low Resource:** Built with Tkinter to stay well within the 2GB RAM limit of the Pi 5.

---

## 🛠 Hardware Setup

| Component | Pin / Connection |
| --- | --- |
| **S2Pi Screen** | Connected via GPIO Header |
| **PIR Sensor VCC** | 5V (Pin 2 or 4) |
| **PIR Sensor GND** | Ground (Pin 6) |
| **PIR Data Pin** | **GPIO 17** (Pin 11) |
| **Backlight Control** | **GPIO 18** (Common for S2Pi) |

---

## 🚀 Installation & Setup

### 1. Clone & Prepare Environment

```bash
# Create project directory
mkdir ~/light_control
cd ~/light_control

# Create virtual environment
python3 -m venv venv

# Install dependencies
./venv/bin/pip install python-kasa gpiozero

```

### 2. Configure the Script

1. Save the `light_control.py` script (provided in previous steps) into `~/light_control/`.
2. Edit the script and update the `PLUG_IP` variable with your Kasa Plug's IP address.
* *Tip: You can find the IP in the Kasa Mobile App under Device Settings > Device Info.*



### 3. Setup Auto-Start (Systemd)

Create the service file:

```bash
sudo nano /etc/systemd/system/light_control.service

```

Paste the following configuration (replace `your_username` with your actual username, e.g., `pi`):

```ini
[Unit]
Description=Kasa Touchscreen Control
After=network-online.target

[Service]
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/your_username/.Xauthority
ExecStart=/home/your_username/light_control/venv/bin/python3 /home/your_username/light_control/light_control.py
Restart=always
RestartSec=5
User=your_username

[Install]
WantedBy=graphical.target

```

### 4. Enable the Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable light_control.service
sudo systemctl start light_control.service

```

---

## 🖥 User Interface Layout

The UI is designed for a **480x320** resolution:

* **Top Bar:** Displays connection status and "Light is ON/OFF".
* **Center Green Button:** Sends a turn-on command.
* **Bottom Red Button:** Sends a turn-off command.
* **Background:** Changes to dark green when active for quick visual confirmation.

---

## 🛠 Troubleshooting

* **Screen stays black:** Ensure the `BACKLIGHT_PIN` in the script matches your screen's specific hardware pin (usually 18).
* **Buttons don't respond:** Check your Wi-Fi connection and verify the Plug IP address.
* **Check logs:** Run `journalctl -u light_control.service -f` to see real-time error messages.

---
