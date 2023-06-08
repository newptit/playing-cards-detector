import base64
import time
import cv2
import numpy as np
from connect import connect_appium
from handle_image import detect_card

driver = connect_appium()

while True:
    # Capture screen frame
    screenshot = driver.get_screenshot_as_base64()
    image_bytes = np.frombuffer(base64.b64decode(screenshot), dtype=np.uint8)
    frame = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

    # Get the height and width of the image
    height, width = frame.shape[:2]

    # Calculate the horizontal split position
    split_position = height // 2

    # Split the image horizontally
    top_half = frame[:split_position, :]
    bottom_half = frame[split_position:, :]
    h, w, c = bottom_half.shape
    print(h, w)
    bottom_half = detect_card(bottom_half)

    # Perform image processing using OpenCV
    # Add your image processing code here

    # Display the processed frame
    cv2.imshow("Processed Frame", bottom_half)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(0.1)

# Release resources
cv2.destroyAllWindows()
