import cv2
import datetime
import os
import time

rtsp_url = "rtsp://admin:Ab12Ab12@192.168.50.77:554/live/ch00_1"
cap = cv2.VideoCapture(rtsp_url)

# Set the video writer object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 15  # Adjust as needed (reduced for Raspberry Pi)
resolution = (640, 480)  # Reduced resolution for Raspberry Pi
out = cv2.VideoWriter()

# Set the duration (1 minute)
duration = 1 * 60  # 1 minute

# Create a folder for saving videos
output_folder = "/home/pi/videos"
os.makedirs(output_folder, exist_ok=True)

try:
    # Capture video frames
    start_time = time.time()

    # Open the video writer with reduced buffer size
    out.open(os.path.join(output_folder, f"temp_video.avi"), fourcc, fps, resolution)
    out.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    while (time.time() - start_time) < duration:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame to the specified resolution
        frame = cv2.resize(frame, resolution)

        # Write frame to the video file
        out.write(frame)

        # Release frame from memory
        del frame

    # Release the video writer
    out.release()

    # Generate timestamp for the video file name
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = os.path.join(output_folder, f"video_{timestamp}.avi")

    # Rename the temporary file to the final filename
    os.rename(os.path.join(output_folder, "temp_video.avi"), video_filename)

    print(f"Video saved: {video_filename}")

except KeyboardInterrupt:
    pass  # Allow the program to end when interrupted

finally:
    # Release the video capture object
    cap.release()

    print("Program ended.")
