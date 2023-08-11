from ultralytics import YOLO
import numpy
import cv2
import math
import serial

model_path = r"C:\Users\Ashling Mccarthy\Programming\gait analysis\Stride\pose1.pt"
model = YOLO(model_path)

# Replace 'COMX' with the actual serial port of your Arduino Nano
SERIAL_PORT = 'COM4'
BAUD_RATE = 9600
buttonPressed = 1 #when button pressed in website make this 1, else 0
pronationAngle = "30" #whatever angle the thing calculated

def calc_angle(list_of_points):
    angles = []
    for index in range(0, 8, 4):
        # under leg
        x1, y1 = list_of_points[index]
        x2, y2 = list_of_points[index+1]
        m1 = (x2 - x1) / (y2 - y1)
        # upper leg
        x1, x2 = list_of_points[index+2]
        y1, y2 = list_of_points[index+3]
        m2 = (x2 - x1) / (y2 - y1)
        m = abs((m2-m1)/(1+(m2*m1)))
        q = numpy.arctan(m)
        q = math.degrees(q)
        angles.append(q)
    return angles
def calculate_points(image_path):
    image_path = image_path
    img = cv2.imread(image_path)

    results = model(image_path)[0]
    list_of_points = []
    for result in results:
        for points in result.keypoints.to().data:
            for keypoint in points:
                x = int(keypoint[0])
                y = int(keypoint[1])
                list_of_points.append((x, y))
                cv2.putText(img, str('.'), (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    #cv2.imshow('img', img)
    #cv2.waitKey(0)
    return list_of_points

def send_packet(data):
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        ser.write(data.encode())
        response = ser.readline().decode().strip()
        print("Arduino response:", response)

if __name__ == "__main__":
    list_of_points = (calculate_points("ashlingfeet.jpeg"))
    left_foot, right_foot = calc_angle(list_of_points)
    print('left foot angle:', round(left_foot, 2))
    print('right foot angle: ', round(right_foot, 2))
    
    while True:
        user_input = input("press enter to recieive infor, press 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        elif buttonPressed == 1:
            send_packet(pronationAngle)
        else:
            print("Invalid input. Please enter '0' or '1'.")
        