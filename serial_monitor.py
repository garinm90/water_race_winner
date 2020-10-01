from serial import Serial
from time import sleep

ser = Serial(port='/dev/ttyUSB0', baudrate='19200', timeout=0)

if __name__ == '__main__':
    try:
        # Find and initialize serial ports.
        ser.flushInput()
        ser.flushOutput()
        print('========================')
        print(f'Port Opened: {ser.port}')
        print(f'Baudrate @{ser.baudrate}')
        print('========================\n')
        while True:
            if(ser.in_waiting):
                sleep(1)
                buffer = ser.read(ser.in_waiting)
                print(buffer)
                with open("serial.txt", "ab") as file_object:
                    # Append 'hello' at the end of file
                    file_object.write(buffer)

    except KeyboardInterrupt as e:
        print(e)
        ser.close()