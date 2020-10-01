from serial import Serial
from serial.serialutil import LF
from serial.tools import list_ports
import requests
from functools import partial
from time import sleep
from threading import Timer

BAUDRATE = 19200
SOH = b'\x01'
ETX = b'\x03'
PLAY_SOUND = b'p+'
STOP_SOUND = b'p-'
ATTRACT = b'z00Sy'
COMMAND_LINK = 'http://localhost/api/command/'
MATCHES = [PLAY_SOUND, ATTRACT]

def play_winner(player_number):
    json_payload = [f"Player_{player_number}W", "", "true", "false"]
    r = requests.post(COMMAND_LINK + 'Effect Start', json=json_payload)
    print('wemadeit')
    winner_timer.start()

def race_start():
    r = requests.get('http://localhost/api/playlists/pause')



sound_files = {
    b'1C' : partial(play_winner, '1'),
    b'1D' : partial(play_winner, '2'),
    b'1E' : partial(play_winner, '3'),
    b'1F' : partial(play_winner, '4'),
    b'20' : partial(play_winner, '5'),
    b'21' : partial(play_winner, '6'), 
    b'22' : partial(play_winner, '7'), 
    b'23' : partial(play_winner, '8'), 
    b'24' : partial(play_winner, '9'), 
    b'25' : partial(play_winner, '10'), 
    b'26' : partial(play_winner, '11'), 
    b'27' : partial(play_winner, '12'), 
    b'28' : partial(play_winner, '13'), 
    b'29' : partial(play_winner, '14'), 
    b'2A' : partial(play_winner, '15'), 
    b'2B' : partial(play_winner, '16'), 
    b'3C' : race_start,
    b'3D' : race_start,
    b'3E' : race_start,
    b'3F' : race_start,
    b'40' : race_start,
    b'41' : race_start,
    b'09' : 'Start_Sound',
    b'0A' : 'Demo/Stop_Sound',
}

    

def get_usb_serial(ports):
    for port in ports:
        if port.product:
            print('\n========================')
            print(f'Found: {port.device}\nUSB: {port.product}')
            print('========================\n')
            return port.device

def seek_soh():
    byte_list = []
    if (ser.in_waiting):
        byte_char = ser.read(ser.in_waiting)
        print(byte_char)
        if (byte_char == b'\x01'):
            byte_list.append(byte_char)
            while 1:
                if (ser.in_waiting):
                    byte_char = ser.read(ser.in_waiting)
                    byte_list.append(byte_char)
                    if byte_char == b'\x03':
                        break
        if byte_list:
            return bytes(b''.join(byte_list))

def get_buffer():
    if(ser.in_waiting):
        data = ser.read_until(b'\x03')
        return data

def sync():
    print('Sync')
    winner_timer.cancel()
    for i in range(1, 17):
        r = requests.get('http://localhost/api/playlists/resume')
        r = requests.get(COMMAND_LINK + f'Effect Stop/Player_{str(i)}W/')
        # print(f'Disabled Winner Effects')
        # print('Restarted Attract Mode')
    
    
def play_effect(player_number):
    if player_number in sound_files:
        print(player_number)
        sound_files[player_number]()

def reset_game(stop_number):
    if stop_number in sound_files:
        print('Reset')
    
def get_command(command):
    print(command)
    if any(x in command for x in MATCHES):
        index = 0
        commands = []
        play_requests = command.find(PLAY_SOUND)
        sync_requests = command.find(ATTRACT)
        if(play_requests >= 0):
            while index >= 0:
                index = command.find(PLAY_SOUND, index+1)
                if index < 0:
                    break
                player_number = command[index+2:index+4]
                play_effect_partial = partial(play_effect, player_number)
                commands.append(play_effect_partial)
        elif(sync_requests >= 0):
            print(command)
            commands.append(sync)
        print(commands)
        return commands
    else:
        return None

ser = Serial(port=get_usb_serial(list_ports.comports()), baudrate=BAUDRATE, timeout=1)

if __name__ == '__main__':
    try:
        # Find and initialize serial ports.
        ser.flushInput()
        ser.flushOutput()
        print('========================')
        print(f'Port Opened: {ser.port}')
        print(f'Baudrate @{ser.baudrate}')
        print('========================\n')

        winner_timer = Timer(15, sync)
        # Main Loop
        while True:
            a = get_buffer()
            if (a):
                commands = get_command(a)
                if commands:
                    [c() for c in commands]
                    pass


    except KeyboardInterrupt as e:
        print(e)
        ser.close()
