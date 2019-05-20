import cv2

def make_line(frame, positions):

    for i in range(0,len(positions) - 1):
        cv2.line(frame, (int(positions[i][0]), int(positions[i][1])), (int(positions[i+1][0]), int(positions[i+1][1])), (0,0,255), 5)

    cv2.line(frame, (int(positions[3][0]), int(positions[3][1])), (int(positions[0][0]), int(positions[0][1])), (0, 0, 255), 5)