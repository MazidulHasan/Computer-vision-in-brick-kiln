from picamera import PiCamera
import datetime
import os
import time

# Set the RTSP URL of your IP camera
rtsp_url = "rtsp://admin:Ab12Ab12@192.168.50.77:554/live/ch00_1"

# Set the output folder
output_folder = "/home/pi/videos"  # Adjust the path accordingly
video_duration = 60  # 1 minute

try:
    # Initialize the PiCamera
    with PiCamera() as camera:
        # Set resolution and framerate
        camera.resolution = (640, 480)  # Adjust resolution as needed
        camera.framerate = 15  # Adjust framerate as needed

        # Allow the camera to warm up
        time.sleep(2)

        # Capture video
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        video_filename = f"{output_folder}/video_{timestamp}.h264"
        camera.start_recording(video_filename)
        camera.wait_recording(video_duration)
        camera.stop_recording()

        print(f"Video saved: {video_filename}")

except KeyboardInterrupt:
    pass  # Allow the program to end when interrupted

print("Program ended.")
