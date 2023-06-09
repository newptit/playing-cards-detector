# should use opencv-python==4.5.5.62
import cv2
import os

import Cards


# sort the cards base on y and x of list tuple card (x, y, name)
def sort_cards(cards):
    return sorted(cards, key=lambda card: (card[1], card[0]))
    return cards

def detect_card(screenshot):
    # Load the train rank and suit images
    path = os.path.dirname(os.path.abspath(__file__))
    train_ranks = Cards.load_ranks(path + '/images/')
    train_suits = Cards.load_suits(path + '/images/')

    # Convert the screenshot to grayscale
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Apply a blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Perform edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edge map
    # cv2.RETR_EXTERNAL for EXTERNAL
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area and aspect ratio to isolate card regions
    min_card_area = 30000
    max_card_area = 44000
    min_aspect_ratio = 0.5
    max_aspect_ratio = 0.8
    RATIO = 1
    # RATIO = 700 / 1440

    card_contours = []
    cards = []
    result = []
    k = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        # w = 162, h = 239
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h

        if min_card_area * RATIO * RATIO < area < max_card_area * RATIO * RATIO and min_aspect_ratio < aspect_ratio < max_aspect_ratio:
            # Check if the x, y exists in the array
            exists = any(
                cv2.boundingRect(card_contour)[0] == x and cv2.boundingRect(card_contour)[1] == y for card_contour
                in card_contours)
            if exists:
                continue
            card_contours.append(contour)
            cards.append(Cards.preprocess_card(contour, screenshot))
            # Find the best rank and suit match for the card.
            cards[k].best_rank_match, cards[k].best_suit_match, cards[k].rank_diff, cards[
                k].suit_diff = Cards.match_card(
                cards[k], train_ranks, train_suits)

            # Draw center point and match result on the image.
            item = Cards.draw_results(screenshot, cards[k])
            result.append(item)
            k = k + 1

    # Sort card contours from left to right, top to bottom
    # card_contours = sorted(card_contours, key=lambda c: (cv2.boundingRect(c)[1], cv2.boundingRect(c)[0]))

    # Draw bounding rectangles around the card contours
    # for contour in card_contours:
    #     x, y, w, h = cv2.boundingRect(contour)
    #     cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # text = f"Size: {w}x{h}"
    # cv2.putText(screenshot, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the screenshot with bounding rectangles
    # Cards.saveImg(screenshot)
    return screenshot


# screenshot = cv2.imread('screenshot.jpg')
# detect_card(screenshot)