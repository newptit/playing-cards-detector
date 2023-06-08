import cv2
import time
import numpy as np
import mss
from handle_image import detect_card

# 0, 50, 350, 830
# Define the screen resolution of your Android device
SCREEN_WIDTH = 350
SCREEN_HEIGHT = 770

# Create a screen capture object
with mss.mss() as sct:
    # Set the bounding box for capturing the screen
    monitor = {"top": 60, "left": 0, "width": SCREEN_WIDTH, "height": SCREEN_HEIGHT}

    while True:
        # Capture the screen
        img = np.array(sct.grab(monitor))

        # Convert the image to a format compatible with OpenCV
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        img = detect_card(img)

        # Display the captured image
        cv2.imshow("Android Screen", img)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) == ord("q"):
            break
        time.sleep(10)

# Clean up
cv2.destroyAllWindows()
