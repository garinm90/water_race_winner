#!/home/fpp/.local/share/virtualenvs/serial-OoMteMnA/bin/python3.7
from serial import Serial
from serial.tools import list_ports
import requests
import xmltodict
from functools import partial
from time import sleep

BAUDRATE = 19200
SOH = b'\x01'
ETX = b'\x03'
PLAY_SOUND = b'p+'
STOP_SOUND = b'p-'
ATTRACT = b'z00Sy'
COMMAND_LINK = 'http://localhost/api/command/'
MATCHES = [PLAY_SOUND, ATTRACT]


def play_winner(player_number):
    # json_payload = [f"Player_{player_number}W", "", "true", "false"]
    r = requests.get(COMMAND_LINK + 'FSEQ Effect Start/' +
                     f'Player_{player_number}W/1/0')
    print('wemadeit')


def race_start():
    r = requests.get(COMMAND_LINK + 'FSEQ Effect Start/Marquee_Race/1/0')
    r = requests.get("http://localhost/fppxml.php?command=getRunningEffects")
    doc = xmltodict.parse(r.text)
    if isinstance(doc['RunningEffects']['RunningEffect'], list):
        print("We got a list of Dictionaries")
        for dict in doc['RunningEffects']['RunningEffect']:
            effect_name = dict['Name']
            print(f"Stoping {effect_name}")
            r = requests.post(COMMAND_LINK + 'Effect Stop',
                              json=[f"{effect_name}"])
    r = requests.get('http://localhost/api/playlists/pause')


def enable_player(player_number):
    '''
        Take the player_number and start the related enable effect for that player.
        Then check for other running enable effects. 
        If there is a list of running effects we need to stop them all and start them all
        this makes them appear to be synchronized
    '''
    payload_counter_row = [f"Enable_{str(player_number)}", "", "true", "false"]
    r = requests.post(COMMAND_LINK + 'Effect Start', json=payload_counter_row)
    payload_target_light = [
        f"Counter_{str(player_number)}", "", "true", "false"]
    r = requests.post(COMMAND_LINK + 'Effect Start', json=payload_target_light)
    r = requests.get("http://localhost/fppxml.php?command=getRunningEffects")
    doc = xmltodict.parse(r.text)
    if isinstance(doc['RunningEffects']['RunningEffect'], list):
        print("We got a list of Dictionaries")
        for dict in doc['RunningEffects']['RunningEffect']:
            effect_name = dict['Name']
            print(f"Stoping {effect_name}")
            r = requests.post(COMMAND_LINK + 'Effect Stop',
                              json=[f"{effect_name}"])
        for dict in doc['RunningEffects']['RunningEffect']:
            effect_name = dict['Name']
            print(f"Starting {effect_name}")
            payload = [f"{effect_name}", "", "true", "false"]
            r = requests.post(COMMAND_LINK + 'Effect Start',
                              json=payload)


def disable_player(player_number):
    r = requests.post(COMMAND_LINK + 'Effect Stop',
                      json=[f"Enable_{str(player_number)}"])
    r = requests.post(COMMAND_LINK + 'Effect Stop',
                      json=[f"Counter_{str(player_number)}"])


'''
    The key in the dictionary corresponds with a sound file. 
    These sounds files indicate what state the game is in. 
    1C is a call for player 1 winner sound so we know to play the player 1 winner effect.
'''
sound_files = {
    b'1C': partial(play_winner, '1'),
    b'1D': partial(play_winner, '2'),
    b'1E': partial(play_winner, '3'),
    b'1F': partial(play_winner, '4'),
    b'20': partial(play_winner, '5'),
    b'21': partial(play_winner, '6'),
    b'22': partial(play_winner, '7'),
    b'23': partial(play_winner, '8'),
    b'24': partial(play_winner, '9'),
    b'25': partial(play_winner, '10'),
    b'26': partial(play_winner, '11'),
    b'27': partial(play_winner, '12'),
    b'28': partial(play_winner, '13'),
    b'29': partial(play_winner, '14'),
    b'2A': partial(play_winner, '15'),
    b'2B': partial(play_winner, '16'),
    b'3C': race_start,
    b'3D': race_start,
    b'3E': race_start,
    b'3F': race_start,
    b'40': race_start,
    b'41': race_start,
    b'09': 'Start_Sound',
    b'0A': 'Demo/Stop_Sound',
    b'0C': partial(enable_player, 1),
    b'0D': partial(enable_player, 2),
    b'0E': partial(enable_player, 3),
    b'0F': partial(enable_player, 4),
    b'10': partial(enable_player, 5),
    b'11': partial(enable_player, 6),
    b'12': partial(enable_player, 7),
    b'13': partial(enable_player, 8),
    b'14': partial(enable_player, 9),
    b'15': partial(enable_player, 10),
    b'16': partial(enable_player, 11),
    b'17': partial(enable_player, 12),
    b'18': partial(enable_player, 13),
    b'19': partial(enable_player, 14),
    b'1A': partial(enable_player, 15),
    b'1B': partial(enable_player, 16),
    b'2C': partial(disable_player, 1),
    b'2D': partial(disable_player, 2),
    b'2E': partial(disable_player, 3),
    b'2F': partial(disable_player, 4),
    b'30': partial(disable_player, 5),
    b'31': partial(disable_player, 6),
    b'32': partial(disable_player, 7),
    b'33': partial(disable_player, 8),
    b'34': partial(disable_player, 9),
    b'35': partial(disable_player, 10),
    b'36': partial(disable_player, 11),
    b'37': partial(disable_player, 12),
    b'38': partial(disable_player, 13),
    b'39': partial(disable_player, 14),
    b'3A': partial(disable_player, 15),
    b'3B': partial(disable_player, 16),
}


def get_usb_serial(ports):
    for port in ports:
        if port.product:
            print('\n========================')
            print(f'Found: {port.device}\nUSB: {port.product}')
            print('========================\n')
            return port.device


def seek_soh():
    '''
    The serial bus on this doesn't use LF or CR.
    Start and end are indicated by unprintable SOH = Start of Header
    and ETX = End of Text
    This function finds all the inbetween characters and returns them.
    '''
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
    '''
        Read serial data until end of transmission and return it.
    '''
    if(ser.in_waiting):
        data = ser.read_until(b'\x03')
        return data


def sync():
    print('Sync')
    for i in range(1, 17):
        r = requests.get('http://localhost/api/playlists/resume')
        r = requests.get(COMMAND_LINK + f'Effect Stop/Player_{str(i)}W/')
        r = requests.get(COMMAND_LINK + 'Effect Stop/Marquee_Race/1/0')
        # print(f'Disabled Winner Effects')
        # print('Restarted Attract Mode')


def play_effect(player_number):
    '''
        Look to see if the requested sound file is has an effect tied to it.
        If it does call the function for that player number
    '''
    if player_number in sound_files:
        print(player_number)
        sound_files[player_number]()


def reset_game(stop_number):
    if stop_number in sound_files:
        print('Reset')


def get_command(command):
    if any(x in command for x in MATCHES):
        print(command)
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
            commands.append(sync)
        print(commands)
        return commands
    else:
        return None


ser = Serial(port=get_usb_serial(list_ports.comports()),
             baudrate=BAUDRATE, timeout=1)

if __name__ == '__main__':
    try:
        # Find and initialize serial ports.
        ser.flushInput()
        ser.flushOutput()
        print('========================')
        print(f'Port Opened: {ser.port}')
        print(f'Baudrate @{ser.baudrate}')
        print('========================\n')

        sync()
        # Main Loop
        while True:
            a = get_buffer()
            if (a):
                '''
                    Get all commands and store them into a buffer so we don't lose any.
                    Multiple calls can be inside of one line.
                '''
                commands = get_command(a)
                '''
                    Call the functions we've been returned from the commands we recieved.
                '''
                if commands:
                    [c() for c in commands]
                    pass

    except KeyboardInterrupt as e:
        print(e)
        ser.close()
