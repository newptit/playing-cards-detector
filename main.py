import cv2
import os

import Cards

# Load the screenshot image
screenshot = cv2.imread('screenshot.jpg')
# Load the train rank and suit images
path = os.path.dirname(os.path.abspath(__file__))
train_ranks = Cards.load_ranks( path + '/Card_Imgs/')
train_suits = Cards.load_suits( path + '/Card_Imgs/')

# Convert the screenshot to grayscale
gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

# Apply a blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Perform edge detection
edges = cv2.Canny(blurred, 50, 150)
cv2.imshow('edges', edges);


# Find contours in the edge map
# cv2.RETR_EXTERNAL for EXTERNAL
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter contours based on area and aspect ratio to isolate card regions
min_card_area = 30000
max_card_area = 40000
min_aspect_ratio = 0.5
max_aspect_ratio = 0.8

card_contours = []
cards = []
k = 0
print(len(contours))
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    print(k)
    area = cv2.contourArea(contour)
    # w = 162, h = 239
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = float(w) / h

    if min_card_area < area < max_card_area and min_aspect_ratio < aspect_ratio < max_aspect_ratio:
        card_contours.append(contour)
        cards.append(Cards.preprocess_card(contour, screenshot))
        # Find the best rank and suit match for the card.
        cards[k].best_rank_match, cards[k].best_suit_match, cards[k].rank_diff, cards[k].suit_diff = Cards.match_card(
            cards[k], train_ranks, train_suits)

        # Draw center point and match result on the image.
        image = Cards.draw_results(screenshot, cards[k])
        k = k + 1


# Sort card contours from left to right, top to bottom
card_contours = sorted(card_contours, key=lambda c: (cv2.boundingRect(c)[1], cv2.boundingRect(c)[0]))

# Draw bounding rectangles around the card contours
for contour in card_contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # text = f"Size: {w}x{h}"
    # cv2.putText(screenshot, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Display the screenshot with bounding rectangles
cv2.imshow('Detected Cards', screenshot)
cv2.waitKey(0)
cv2.destroyAllWindows()
