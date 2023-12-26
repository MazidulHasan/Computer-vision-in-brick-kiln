import cv2
import datetime
import time
import os

# Set the RTSP URL of your IP camera
rtsp_url = "rtsp://admin:Ab12Ab12@192.168.50.77:554/live/ch00_1"

# Set the video capture object
cap = cv2.VideoCapture(rtsp_url)

# Set the video writer object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 25  # Adjust as needed
out = cv2.VideoWriter()

# Set the duration and interval
duration = 2 * 60  # 2 minutes
interval = 15 * 60  # 15 minutes

# Create a folder for saving videos
output_folder = "D:/Vata Project/videos"
os.makedirs(output_folder, exist_ok=True)

try:
    while True:
        # Capture video frames
        frames = []
        start_time = time.time()

        while (time.time() - start_time) < duration:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)

        # Check if frames were captured
        if frames:
            # Generate timestamp for the video file name
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            video_filename = os.path.join(output_folder, f"video_{timestamp}.avi")

            # Open the video writer
            out.open(video_filename, fourcc, fps, (frames[0].shape[1], frames[0].shape[0]))

            # Write frames to the video file
            for frame in frames:
                out.write(frame)

            # Release the video writer
            out.release()

            print(f"Video saved: {video_filename}")

        # Wait for the specified interval
        time.sleep(interval - duration)

except KeyboardInterrupt:
    # Release the video capture object
    cap.release()

    # Release the video writer object
    out.release()

    print("Program terminated by user.")
