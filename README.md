# raspberrypi3b-usb-formatter

### Daemon startup skripti:

1. 
```
sudo nano /etc/systemd/system/usbf.service
```

2.

```bash
[Unit]
Description=USB Formatoija
After=multi-user.target

[Service]
ExecStart=/bin/bash -c "sudo /usr/bin/python3 /home/rasp/usbf/format.py"
WorkingDirectory=/home/rasp/usbf
User=root
Restart=always
Environment="SUDO_COMMAND=/usr/bin/python3 /home/rasp/usbf/format.py"

[Install]
WantedBy=multi-user.target
```

3. CTRL + X + Y + ENTER

4. Restarttaus

```bash
sudo systemctl daemon-reload
sudo systemctl restart usbf.service
```

5. Status

```bash
sudo systemctl status usbf.service
```
