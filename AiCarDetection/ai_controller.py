from email.quoprimime import body_check
from os import urandom
import cv2
import numpy as np
import supervision as sv
from sympy import principal_branch
import ultralytics
import time
import calendar
import requests
from ultralytics import YOLO
from collections import defaultdict
from supervision.geometry.core import Position
from Entities.Car import Car
from Entities.ParkingSpot import ParkingSpot
from Entities.TrafficViolation import TrafficViolation
from Entities.OnStreetParking import OnStreetParking
from queue import Empty, Queue
from threading import Thread
import Core.helper as hp
import json

previous_bbox = None
parked = []
cars = {}
time_between_checks = 10
time_counter = 0

def doPost(url, body, header={"Content-Type": "application/json",}):
    try:
        response = requests.post(url="http://localhost:5000/" + url, data=json.dumps(body), headers=header)
        print(response.json())
    except Exception as e:
        print(e)
    return response.json()

def consumer(queue):
    while True:
        try:
            item = queue.get()
        except Empty:
            continue
        else:
            print(f'Processing request item {item.getDictObj()}')
            response = item.doPost()
            time.sleep(12)
            queue.task_done()

def left_click_detect(event, x, y, flags, points):
    if (event == cv2.EVENT_LBUTTONDOWN):
        print(f"\tClick on {x}, {y}")
        points.append([x,y])
        print(points)

polygon = np.array([
    [360 , 180],
    [350, 390],
    [830, 595],
    [675, 180],
])
video_path = "AiCarDetection/Input/video.mp4"
video_info = sv.VideoInfo.from_video_path(video_path)
model = YOLO('yolov8n.pt')
# initiate annotators
tracker = sv.ByteTrack()

box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()
trace_annotator = sv.TraceAnnotator()
cap = cv2.VideoCapture(video_path)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
parking_site = OnStreetParking()
current_GMT = time.gmtime()
time_stamp = calendar.timegm(current_GMT)
parking_site.id = "ParkingSite_" + str(time_stamp)
parking_site.description = "To Be Set Street + description"
parking_site.setData(parking_site.getDictObj())
response = parking_site.doPost()
#Create a queue for notifications
queue = Queue()
consumer_thread = Thread(target=consumer,args=(queue,),daemon=True)
consumer_thread.start()
# Loop through the video frames
polygon = []
points = []
zone = None
resp =  doPost("getPolygon",body={"cm_id" : "1"})
print (resp["cm_polygon"])
polygon = np.array(json.loads(resp["cm_polygon"]))
print(polygon)
while cap.isOpened() and False: # for debug change to True
    # Read a frame from the video
    success, frame = cap.read()
    if success:
        frame = cv2.polylines(frame, polygon, False, (255, 255, 255), thickness=2)
        cv2.imshow('Frame', frame)
        key = cv2.waitKey(25)
        if (key == ord('q')):
            break
        elif (key== ord('p')): 
            polygon = [np.int32(points)] # type: ignore
            cv2.destroyWindow('Frame')
            cap.release()
            break
        cv2.setMouseCallback('Frame', left_click_detect, points)

zone = sv.PolygonZone(polygon=polygon, frame_resolution_wh=video_info.resolution_wh)
zone_annotator = sv.PolygonZoneAnnotator(zone=zone, color=sv.Color.white())
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()
    if success:
        annotated_frame, time_counter, previous_bbox, parked, queue, cars = hp.process_frame_tracking(frame,(cap.get(cv2.CAP_PROP_POS_MSEC)/1000), previous_bbox ,time_counter, time_between_checks ,parked, parking_site, queue, cars,model,tracker,zone ,box_annotator,label_annotator,trace_annotator,zone_annotator)
        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break
queue.join()
print("CLOSED ALL THREADS")
# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()

from IPython import display
display.clear_output()