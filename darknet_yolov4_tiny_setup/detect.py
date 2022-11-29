import cv2
import numpy as np
import datetime
import configparser
import boto3
from botocore.config import Config


config = configparser.RawConfigParser()
config.read("config.ini")

AWS_ACCESS_KEY = config["General"]["AWS_ACCESS_KEY"]
AWS_SECRET_ACCESS = config["General"]["AWS_SECRET_ACCESS"]
BUCKET_NAME = config["General"]["BUCKET_NAME"]

config = Config(connect_timeout=3600, read_timeout=3600)
s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY,
                  aws_secret_access_key=AWS_SECRET_ACCESS,
                  config=config)


def upload_image(img, num_ships):
    cv2.imwrite("./detected_ship/test.png", img)

    # detected_ships/10-30-2022-10-30-AM-5.png
    upload_filename = f"detected_ships/{datetime.datetime.now().strftime('%m-%d-%Y-%I-%M-%p')}-{num_ships}.png"

    s3.upload_file("./detected_ship/test.png",
                   BUCKET_NAME, upload_filename)


def run_detector():
    classes = None
    config_path = "./yolov4-tiny-custom.cfg"
    weights_path = "./training/yolov4-tiny-custom_best.weights"

    with open("./obj.names", 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    yolo = cv2.dnn.readNet(weights_path, config_path)

    layer_names = yolo.getLayerNames()

    output_layers = [layer_names[i-1] for i in yolo.getUnconnectedOutLayers()]
    color_red = (0, 0, 255)

    cap = cv2.VideoCapture(0)
    ctr = 0
    target_iteration = 100

    while True:

        _, img = cap.read()
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

        # Only upload the image if:
        # There are ship detected.
        # Every target_iteration iteration of ctr only.
        if num_ships > 0 and ctr >= target_iteration:
            upload_image(img, num_ships)

        if ctr >= target_iteration:
            ctr = 0
        ctr += 1

        cv2.imshow("Camera", img)

        if cv2.waitKey(1) == ord("q"):
            break


if __name__ == "__main__":
    run_detector()
