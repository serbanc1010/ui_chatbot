## Python UI chatbot

The chatbot for the coding task is written in Python 3.8 and uses the tkinter package for the GUI.  As a prerequisite, you need the have the tk library installed on your system.  Below is an example of installation on an Ubuntu system:

`sudo apt install python3.8-tk`

To run the app, simply call the chatbot.py file:

`python3 chatbot.py`

You'll need either a Linux system with a GUI or a Linux system configured for X11 forwarding (`X11Forwarding yes` must be specified in `/etc/ssh/sshd_config`) and a SSH client running an X server (I used Ubuntu server and MobaXterm) to connect to it.
