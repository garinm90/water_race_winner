#! /home/fpp/.local/share/virtualenvs/serial-OoMteMnA/bin/python
from threading import Timer
import requests
from game import Game, GameOver, GameStart, Attract
from serial import Serial
from serial.tools import list_ports

BAUDRATE = 19200
SOH = b'\x01'
ETX = b'\x03'
WINNER_COMMAND = b':Winner'
SYNC_COMMAND = b'Sync'
GAME_START = b'Game Start'
ALT_START = b'400Null'
COMMAND_LINK = 'http://localhost/api/command/'
PLAYER_ENABLE = b':Enabled'
PLAYER_DISABLE = b':Disabled'
# Iterate through serial ports and return USB serial device.
PLAYER_NUMBER = {
    b"1": "1",
    b"2": "2",
    b"3": "3",
    b"4": "4",
    b"5": "5",
    b"6": "6",
    b"7": "7",
    b"8": "8",
    b"9": "9",
    b":": "10",
    b";": "11",
    b"<": "12",
    b"=": "13",
    b">": "14",
    b"?": "15",
    b"@": "16"
}

game_state = Game()


def setup_overlay_models():
    payload = {
        "RGB": [
            255,
            255,
            255
        ]
    }
    for i in range(1, 17):
        r = requests.put(
                f'http://localhost/api/overlays/model/Player_{str(i)}/fill', json=payload)


def stop_winner_effect():
    for i in range(1, 17):
        r = requests.get(COMMAND_LINK + f'Effect Stop/Player_{str(i)}W/')
        print(r.status_code)
        print(f'Player Number {str(i)} stopped')


def sync_game():
    r = requests.get('http://localhost/api/playlists/resume')
    if r.status_code == 200:
        print('Starting Attract')




def pause_attract():
    if (isinstance(game_state.state, Attract)):
        for i in range(1, 17):
            payload = {'State': 0}
            r = requests.put(
                f'http://localhost/api/overlays/model/Player_{str(i)}/state', json=payload)
            print(r.status_code)
            print(r.url)
        r = requests.get('http://localhost/api/playlists/pause')
        game_state.change(GameStart)
        if r.status_code == 200:
            print('Paused Playlist')


def play_winner(winner_number):
    if isinstance(game_state.state, GameStart):
        json_payload = [f"Player_{winner_number}W", "", "true", "false"]
        r = requests.post(COMMAND_LINK + 'Effect Start', json=json_payload)
        game_state.change(GameOver)
        winner_timer.start()
        return


def reset_attract():
    if (isinstance(game_state.state, GameOver)):
        game_state.change(Attract)
        winner_timer.cancel()
        sync_game()
        stop_winner_effect()

def get_usb_serial():
    for port in ports:
        if port.product:
            print('\n========================')
            print(f'Found: {port.device}\nUSB: {port.product}')
            print('========================\n')
            return port.device


def disable_player(player_number):
    payload = {'State': 0}
    r = requests.put(f'http://localhost/api/overlays/model/Player_{player_number}/state', json=payload)


def enable_player(player_number):
    payload = {'State': 1}
    r = requests.put(f'http://localhost/api/overlays/model/Player_{player_number}/state', json=payload)


def seek_soh():
    byte_list = []
    ser.in_waiting
    if (ser.in_waiting):
        byte_char = ser.read(ser.in_waiting)
        if (byte_char == b'\x01'):
            byte_list.append(byte_char)
            while 1:
                if (ser.in_waiting):
                    byte_char = ser.read(1)
                    byte_list.append(byte_char)
                    if byte_char == b'\x03':
                        break
        if byte_list:
            return bytes(b''.join(byte_list))


def get_command(byte_list):
    if byte_list:
        print(byte_list)
        i = byte_list.find(WINNER_COMMAND)
        if(i > 0):
            winner_number = byte_list[i-2:i]
            winner_number = winner_number.decode('ascii').lstrip('0')
            play_winner(winner_number)
        i = byte_list.find(GAME_START)
        k = byte_list.find(ALT_START)
        if(i > 0 or k > 0):
            pause_attract()
        i = byte_list.find(SYNC_COMMAND)
        if(i > 0 and isinstance(game_state.state, GameOver)):
            game_state.change(Attract)
            winner_timer.cancel()
            sync_game()
            stop_winner_effect()
        i = byte_list.find(PLAYER_ENABLE)
        if(i > 0 and isinstance(game_state.state, Attract)):
            player_number = byte_list[i-2:i]
            player_number = player_number.decode('ascii').lstrip('0')
            enable_player(player_number)
        i = byte_list.find(PLAYER_DISABLE)
        if(i > 0 and isinstance(game_state.state, Attract)):
            player_number = byte_list[i-2:i]
            player_number = player_number.decode('ascii').lstrip('0')
            disable_player(player_number)



# Setup Game State




if __name__ == '__main__':
    try:
        # Find and initialize serial ports.
        ports = list_ports.comports()
        ser = Serial(port=get_usb_serial(), baudrate=BAUDRATE, timeout=0)
        ser.flushInput()
        ser.flushOutput()
        print('========================')
        print(f'Port Opened: {ser.port}')
        print(f'Baudrate @{ser.baudrate}')
        print('========================\n')


        # Resume lights if they are left paused
        sync_game()
        # Disable all the winner flashes if one has been left on
        stop_winner_effect()
        # Make sure all players are disabled.
        for i in range(1, 17):
            disable_player(str(i))

        # Set lights to white but hidden for enabling and disabling players
        setup_overlay_models()
        # Setup a timer incase we don't recieve the sync command we timeout the winner and go back into the attract mode
        winner_timer = Timer(15, reset_attract)

        while True:
            get_command(seek_soh())
    except KeyboardInterrupt as e:
        print(e)
        ser.close()
