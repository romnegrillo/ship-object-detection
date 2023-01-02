import cv2
import imutils
import numpy as np
import datetime
import configparser

classes = None
config_path = "./yolov4-tiny-custom.cfg"
weights_path = "./training/yolov4-tiny-custom_best.weights"

with open("./obj.names", 'r') as f:
    classes = [line.strip() for line in f.readlines()]

yolo = cv2.dnn.readNet(weights_path, config_path)

layer_names = yolo.getLayerNames()

output_layers = [layer_names[i-1] for i in yolo.getUnconnectedOutLayers()]
color_red = (0, 0, 255)


img = cv2.imread("test.jpg")
height, width, _ = img.shape

blob = cv2.dnn.blobFromImage(
    img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
yolo.setInput(blob)
outputs = yolo.forward(output_layers)

class_ids = []
confidences = []
boxes = []
num_ships = 0
for output in outputs:
    for detection in output:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        if (confidence > 0.1):
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            x = int(center_x - w/2)
            y = int(center_y - h/2)

            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)
            

indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.1, 0.1)
num_ships = len(indices)

for i in range(len(boxes)):
    if i in indices:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        start = (x, y)
        end = (x+w, y+h)

        cv2.rectangle(img, start, end, (0, 255, 0), 2)
        cv2.putText(img, label, (x, y-20),
                    cv2.FONT_HERSHEY_PLAIN, 1, color_red, 2)

img = imutils.resize(img, width=1000)
cv2.imshow("Sample Image", img)
print("Press enter to exit...")
cv2.waitKey(0)
