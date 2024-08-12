import cv2
import numpy as np
import supervision as sv
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
 
def get_bbox_from_list(list_bbox, tracker_id):
    for bbox in list_bbox:
        if bbox[4] != None and bbox[4] == tracker_id:
            return bbox
    return None

def update_cars(detections :sv.Detections, prev_detection : sv.Detections, time_elapsed , cars):
    parked = []
    for item in prev_detection:
        car = None
        tracker_id = item[4]
        if len(cars) > 0 and tracker_id in cars:
            car = cars[item[4]]
        else:
            car = Car()
        previous_pos = item[0]
        curr_i = get_bbox_from_list(detections, tracker_id)
        if curr_i:
            current_pos = curr_i[0]
            car.updateCar(tracker_id,previous_pos, current_pos, time_elapsed)
            cars[car.car_id] = car 
        parked.append(car.car_parked)
    return parked


def process_frame_tracking(frame: np.ndarray, time_elapsed, previous_bbox ,time_counter, time_between_checks,parked, parking_site, queue, cars, model,tracker,zone ,box_annotator,label_annotator,trace_annotator,zone_annotator) -> np.ndarray:
    # detect
    results = model(frame,verbose=False)[0]
    detections = sv.Detections.from_ultralytics(results)
    #detections = detections[detections.class_id == 2]
    detections = tracker.update_with_detections(detections)
    current_parked = parked
    detection_zone_mask = zone.trigger(detections=detections)
    detection_zone_in = detections[detection_zone_mask]
    detections = detection_zone_in
    current_bbox = detections
    
    if len(current_parked) < len(detections):
        current_parked.extend([False] * (len(detections) - len(current_parked)))  # Extend list1 with zeros
    
    if previous_bbox :
        parked = update_cars(current_bbox, previous_bbox, time_elapsed, cars)
    
    previous_bbox = current_bbox
    if time_counter == int(time_elapsed):
        print(" --Reset Frame Time Counter : ", str(time_counter))  
        time_counter = time_counter + time_between_checks
        #send a notification to cygnus when a car is found parked
        list_to_pop = []
        session = requests.Session()
        session.headers.update(parking_site.header)
        notify = False
        for i in cars:
            if cars[i].car_parked is True:
                current_GMT = time.gmtime()
                time_stamp = calendar.timegm(current_GMT)
                print("Notify cygnus for car #{0} parked:{1} ".format(cars[i].car_id, cars[i].car_parked))
                tf = TrafficViolation()
                tf.id = "IllegalParking_" + str(cars[i].car_id) + "_" + str(parking_site.id) + "_" + str(time_stamp)# parking_site + timestamp to make it unique
                tf.descr = "Illegal parking for atleast {0}".format(round(cars[i].time_stationary, 2))
                tf.setLocationFromPoints(cars[i].car_position[0],cars[i].car_position[1],cars[i].car_position[2],cars[i].car_position[3])
                tf.getRefOnStreetParking().append(parking_site.id)
                tf.setData(tf.getDictObj())
                queue.put(tf)
                parking_site.getRefTrafficViolation().append(tf.id)
                notify=True
                list_to_pop.append(i)
        if notify:
            parking_site.setData(parking_site.getDictObj())
            parking_site.doPatch(parking_site.getTrafficViolationRef())
                
        for i in list_to_pop:
            cars.pop(i)

    labels = []
    for class_id, tracker_id, parked_value in zip(detections.class_id, detections.tracker_id, current_parked):
        labels.append(f"#{tracker_id} {results.names[class_id]} #parked={parked_value}")
              
    annotated_frame = box_annotator.annotate(frame.copy(), detections=detections)
    annotated_frame = label_annotator.annotate(annotated_frame, detections=detections, labels=labels)
    annotated_frame = trace_annotator.annotate(annotated_frame, detections=detections)
    annotated_frame = zone_annotator.annotate(scene=annotated_frame)
    
    return annotated_frame , time_counter, previous_bbox, parked, queue, cars # type: ignore