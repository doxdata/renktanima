import cv2
import numpy as np

def tanımla_renk(frame, renk_adi):
    renk_isimleri = {"mavi": (255, 0, 0), "yesil": (0, 255, 0), "kirmizi": (0, 0, 255), "sari": (0, 255, 255)}

    if renk_adi in renk_isimleri:
        renk_kodu = renk_isimleri[renk_adi]
    else:
        print("Geçersiz renk adı!")
        return None

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower, upper = renk_alanlari(renk_adi)
    mask = cv2.inRange(hsv_frame, lower, upper)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), renk_kodu, 2)
            cv2.putText(frame, renk_adi.capitalize(), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, renk_kodu, 2)

    return frame

def renk_alanlari(renk_adi):
    if renk_adi == "mavi":
        return np.array([100, 50, 50]), np.array([140, 255, 255])
    elif renk_adi == "yesil":
        return np.array([40, 50, 50]), np.array([80, 255, 255])
    elif renk_adi == "kirmizi":
        return np.array([0, 100, 100]), np.array([10, 255, 255])
    elif renk_adi == "sari":
        return np.array([20, 50, 50]), np.array([40, 255, 255])
    else:
        return None, None

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    renkler = ["mavi", "yesil", "kirmizi", "sari"]
    for renk in renkler:
        frame = tanımla_renk(frame, renk)

    cv2.imshow("Renk Tanıma", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
