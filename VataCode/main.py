import cv2

# Replace 'your_ip_address', 'your_username', and 'your_password' with your camera details
ip_address = '192.168.50.178'
username = 'admin'
password = 'Ab12Ab12'

# Create the camera URL
# rtsp://admin:Ab12Ab12@192.168.50.178/video
# rtsp://IPADDRESS:554/live/ch00_1
camera_url = f"rtsp://{username}:{password}@{ip_address}/video"
# camera_url = f"rtsp://{ip_address}:554/live/ch00_1"

# Open the camera
cap = cv2.VideoCapture(camera_url)

while True:
    # Capture frames
    ret, frame = cap.read()

    # Display the frame (you can add PTZ controls here using OpenCV)
    cv2.imshow('IP Camera Feed', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()