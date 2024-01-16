import cv2
import mediapipe as mp
import pyfirmata2
import math

board = pyfirmata2.Arduino("COM5")
ledpin = board.get_pin("d:3:p")

img = cv2.VideoCapture(0)
img.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
img.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hand = mp_hands.Hands(max_num_hands=1)

while True:

    res, out = img.read()
    if res:
        RGB_frame = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)
        result = hand.process(RGB_frame)
        if result.multi_hand_landmarks:
            handlanmarks = result.multi_hand_landmarks[0]
            thumtip = handlanmarks.landmark[4]
            indextip = handlanmarks.landmark[8]
            distance = math.sqrt((thumtip.x - indextip.x)**2+(thumtip.y - indextip.y)**2)
            print(distance)
            #time.sleep(2)
            brightness = distance*2
            ledpin.write(brightness)
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(out, hand_landmarks, mp_hands.HAND_CONNECTIONS)
              ##  print(hand_landmarks)
        cv2.imshow("the result", out)
        if cv2.waitKey(100) == ord('q'):
            break
cv2.destroyAllWindows()

