# CSH letmein 

to use the virtual environment, run 
```source venv/bin/activate```

You'll also need to create a service file.
for example: 
```
[Unit]
Description=Let Me In website for CSH Alumni
After=letmein.csh.rit.edu

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/LetMeIn
StandardOutput=file:/home/pi/LetMeIn/error.log
StandardError=inherit
Restart=always

[Install]
WantedBy=multi-user.target
```
