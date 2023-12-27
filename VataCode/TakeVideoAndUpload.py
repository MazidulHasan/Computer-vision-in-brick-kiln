import cv2
import datetime
import os
import time
import pyrebase

#firebase Credentials
firebaseConfig = {
    'apiKey': "AIzaSyCw9nBF4EMtkM3FpK2ONtOdmkRFQjpp-3U",
    'authDomain': "computervision-f3825.firebaseapp.com",
    'databaseURL': "https://computervision-f3825-default-rtdb.firebaseio.com",
    'projectId': "computervision-f3825",
    'storageBucket': "computervision-f3825.appspot.com",
    'messagingSenderId': "811571419343",
    'appId': "1:811571419343:web:a41770b10d5c521db7ffba",
    'measurementId': "G-921FTZZHHR"
}

firebase = pyrebase.initialize_app(firebaseConfig) 
storage = firebase.storage()

rtsp_url = "rtsp://admin:Ab12Ab12@192.168.50.77:554/live/ch00_1"
cap = cv2.VideoCapture(rtsp_url)

# Set the video writer object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 15  # Adjust as needed (reduced for Raspberry Pi)
resolution = (426, 240)  # Reduced resolution for Raspberry Pi
out = cv2.VideoWriter()

# Set the duration (1 minute)
duration = 10  # 10 s

# Create a folder for saving videos
output_folder = "D:/Computer-vision-in-brick-kiln/videos/"
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
    videoFilename = f"video_{timestamp}.avi"
    video_filename = os.path.join(output_folder, videoFilename)

    # Rename the temporary file to the final filename
    os.rename(os.path.join(output_folder, "temp_video.avi"), video_filename)

    print(f"Video saved: {video_filename}")

except KeyboardInterrupt:
    pass  # Allow the program to end when interrupted

finally:
    # Release the video capture object
    cap.release()
    #send video to firebase
    print("Uploading file..."+videoFilename)
    local_file_path = output_folder+videoFilename
    storage.child('Videos/'+video_filename).put(local_file_path)
    print("Uploading done")
    print("Program ended.")
