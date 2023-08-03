import serial

# Replace 'COMX' with the actual serial port of your Arduino Nano
SERIAL_PORT = 'COM4'
BAUD_RATE = 9600

def send_packet(data):
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        ser.write(data.encode())
        response = ser.readline().decode().strip()
        print("Arduino response:", response)


while True:
    user_input = input("Enter '1' to turn on LED or '0' to turn it off (or 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break
    if user_input in ('0', '1'):
        send_packet(user_input)
    else:
        print("Invalid input. Please enter '0' or '1'.")

