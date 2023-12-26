import cv2
from datetime import datetime

def capture_image(rtsp_url, output_folder):
    # Open RTSP stream
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("Error: Couldn't open RTSP stream.")
        return

    # Read a frame
    ret, frame = cap.read()

    if ret:
        # Generate a timestamp for the image filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Construct the output path with the timestamp
        output_path = f"{output_folder}/image_{timestamp}.jpg"

        # Save the frame as an image
        cv2.imwrite(output_path, frame)
        print(f"Image captured and saved to {output_path}")
    else:
        print("Error: Couldn't read frame from RTSP stream.")

    # Release the video capture object
    cap.release()

if __name__ == "__main__":
    # Specify your RTSP URL and local output folder
    rtsp_url = "rtsp://admin:Ab12Ab12@192.168.50.77:554/live/ch00_1"
    output_folder = "D:/Vata Project/images"

    # Capture image from RTSP stream
    capture_image(rtsp_url, output_folder)
