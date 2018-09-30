import RPi.GPIO as GPIO
import time
import socket
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
pwm = GPIO.PWM(12, 100)
pwm.start(5)
theta = 0
gyro_x_offset = 0.0
gyro_y_offset = 0.0
gyro_z_offset = 0.0

count = 0
num_callibration_itrs = 60
debug = False
print("waiting for device...")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('192.168.42.8', 5005))
print("Device Connected")

while True:
    data,addr = sock.recvfrom(1024)
    line = data.split(',')
    if len(line) == 3:  #receiroved complete packet
        gyro_x = float(line[0])
        gyro_y = float(line[1])
        gyro_z = float(line[2])
        if count < num_callibration_itrs:
            gyro_x_offset += gyro_x
            gyro_y_offset += gyro_y
            gyro_z_offset += gyro_z
            count += 1
        elif count == num_callibration_itrs and num_callibration_itrs != 0:
            gyro_x_offset /= num_callibration_itrs
            gyro_y_offset /= num_callibration_itrs
            gyro_z_offset /= num_callibration_itrs
          
            count += 1

        #Publish Ros Imu message
        else:
            gyro_x -= gyro_x_offset
            gyro_y -= gyro_y_offset
            gyro_z -= gyro_z_offset

            #discretize readings to round off noise
            gyro_x = float(int(gyro_x*100))/100.0;
            gyro_y = float(int(gyro_y*100))/100.0;
            gyro_z = float(int(gyro_z*100))/100.0;
            duty = int((90-(9*gyro_y)) / 10.0 + 2.5)
            print("Duty: ",duty)
            pwm.ChangeDutyCycle(duty)

