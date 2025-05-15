import cv2
import numpy as np
from PIL import Image

def detect_cheque_border(image):
    """Detects the cheque's full boundary using adaptive thresholding and contour filtering."""
    try:
        # Convert PIL Image to OpenCV format
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Convert to grayscale
        gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

        # Apply Adaptive Thresholding to improve cheque detection
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 4
        )

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cheque_contour = None
        max_area = 0
        img_height, img_width = image_cv.shape[:2]

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)

            # Ensure it’s large enough and has a valid aspect ratio (cheques are wide rectangles)
            if 2.5 < aspect_ratio < 6.5 and w > 0.6 * img_width and h > 0.2 * img_height:
                area = cv2.contourArea(contour)
                if area > max_area:
                    max_area = area
                    cheque_contour = (x, y, w, h)

        if cheque_contour:
            x, y, w, h = cheque_contour

            # Expand the bounding box slightly to avoid cutting off details
            padding_x = int(0.02 * img_width)  # 2% padding of image width
            padding_y = int(0.02 * img_height)  # 2% padding of image height

            x = max(0, x - padding_x)
            y = max(0, y - padding_y)
            w = min(img_width - x, w + 2 * padding_x)
            h = min(img_height - y, h + 2 * padding_y)

            # Crop cheque from image
            cheque_cropped = image_cv[y:y+h, x:x+w]

            # Convert back to PIL format
            cheque_image = Image.fromarray(cv2.cvtColor(cheque_cropped, cv2.COLOR_BGR2RGB))
            return cheque_image

        return image  # Return original image if cheque detection fails

    except Exception as e:
        raise Exception(f"Error detecting cheque: {e}")
    
