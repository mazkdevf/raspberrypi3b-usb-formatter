# raspberrypi3b-usb-formatter

## Skriptin installaus
- Pythoni tarvitaan!


1. sudo pip install rpi_ws281x adafruit-circuitpython-neopixel 


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


![kuva](https://github.com/mazkdevf/raspberrypi3b-usb-formatter/assets/79049205/c7461e8e-4052-471b-987e-ed7ff4444b51)
