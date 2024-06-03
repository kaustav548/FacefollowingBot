import serial
import cv2
import numpy as np

# Connect to Arduino
arduino_port = 'COM3'  # Replace with the correct port for your Arduino
arduino_baudrate = 9600
ser = serial.Serial(arduino_port, arduino_baudrate, timeout=1)

def stream_camera_frames():
    cv2.namedWindow('Arduino Camera', cv2.WINDOW_NORMAL)

    while True:
        # Send a command to Arduino to capture an image
        ser.write(b'C')  # Assuming 'C' is the command to capture an image

        # Read image data from Arduino
        image_data = b''
        while True:
            byte = ser.read()
            if byte == b'\n':  # Assuming newline indicates the end of image data
                break
            image_data += byte

        # Convert the received image data to a NumPy array
        image_array = np.frombuffer(image_data, dtype=np.uint8)

        # Decode the image using OpenCV
        frame = cv2.imdecode(image_array, 1)

        # Display the frame
        cv2.imshow('Arduino Camera', frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close serial port and release resources
    ser.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        stream_camera_frames()

    except KeyboardInterrupt:
        # Close serial port and release resources on keyboard interrupt
        ser.close()
        cv2.destroyAllWindows()
