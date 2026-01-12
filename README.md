```markdown
# 💡 RPi 5 Kasa Light Control

A Python-based touchscreen interface for TP-Link Kasa smart plugs, optimized for the Raspberry Pi 5 with an S2Pi 3.5" display.

## 🛠 Setup
1. **Directory:** `/home/<user>/Light-Control`
2. **Environment:**
   ```bash
   python3 -m venv venv
   ./venv/bin/pip install python-kasa
```

## 🧪 Testing Locally

To test the script manually (especially via SSH), use:

```bash
DISPLAY=:0 ./venv/bin/python3 light-control.py
```

## ⚙️ Auto-Start Configuration

Create the service file:
`sudo nano /etc/systemd/system/light-control.service`

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

## 📋 Commands

* **Enable:** `sudo systemctl enable light-control.service`
* **Start:** `sudo systemctl start light-control.service`
* **Stop:** `sudo systemctl stop light-control.service`
* **Logs:** `journalctl -u light-control.service -f`
