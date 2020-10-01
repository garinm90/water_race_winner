#! /usr/bin/python3
import gpiozero
import subprocess
import signal
import time

button = gpiozero.Button('GPIO22', pull_up=False)

def reset_service():
    restart = subprocess.run(['sudo', 'systemctl', 'restart', 'main-py.service'])
    if (restart.returncode == 0):
        print('Successfully Restart')
        return
    else:
        print(restart.stdout)

# On first boot up the main service will come up too fast

if __name__ == '__main__':    
    button.when_activated = reset_service
    signal.pause()
