#================================================================ 
#Import necessary libraries
from flask import Flask, render_template, Response, request, session
from ctypes import *
from flask_cors import CORS
from flask import Flask, request, jsonify
from pymongo import MongoClient
import bcrypt
from flask import jsonify, request
from flask import session
import datetime
import image_email_fall
import image_email_car

import math
import random
import os
import cv2
import numpy as np
import time
import darknet
from itertools import combinations
import pafy
import youtube_dl
from ultralytics import YOLO
from ultralytics.yolo.v8.detect.predict import DetectionPredictor
model=YOLO("yolov8s.pt")
netMain = None
metaMain = None
altNames = None
video_link= None
case = None


def is_close(p1, p2):
    
    dst = math.sqrt(p1**2 + p2**2)
    #=================================================================#
    return dst 

def convertBack(x, y, w, h): 
    #================================================================
    # Purpose : Converts center coordinates to rectangle coordinates
    #================================================================  
   
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax


def cvDrawBoxes_fall(detections, img):
   
    
    #================================================================
    # Purpose : Filter out Persons class from detections
    #================================================================
    if len(detections) > 0:  						# At least 1 detection in the image and check detection presence in a frame  
        centroid_dict = dict() 						# Function creates a dictionary and calls it centroid_dict
        objectId = 0								# We inialize a variable called ObjectId and set it to 0
        for detection in detections:				# In this if statement, we filter all the detections for persons only
            # Check for the only person name tag 
            name_tag = str(detection[0].decode())   # Coco file has string of all the names
            if name_tag == 'person':                
                x, y, w, h = detection[2][0],\
                            detection[2][1],\
                            detection[2][2],\
                            detection[2][3]      	# Store the center points of the detections
                xmin, ymin, xmax, ymax = convertBack(float(x), float(y), float(w), float(h))   # Convert from center coordinates to rectangular coordinates, We use floats to ensure the precision of the BBox            
                # Append center point of bbox for persons detected.
                centroid_dict[objectId] = (int(x), int(y), xmin, ymin, xmax, ymax) # Create dictionary of tuple with 'objectId' as the index center points and bbox
    #=================================================================
    
    #=================================================================
    # Purpose : Determine whether the fall is detected or not 
    #=================================================================            	
        fall_alert_list = [] # List containing which Object id is in under threshold distance condition. 
        red_line_list = []
        for id,p in centroid_dict.items():
            dx, dy = p[4] - p[2], p[5] - p[3]  	# Check the difference
            difference = dy-dx			
            if difference < 0:						
                fall_alert_list.append(id)       #  Add Id to a list
        
        for idx, box in centroid_dict.items():  # dict (1(key):red(value), 2 blue)  idx - key  box - value
            if idx in fall_alert_list:   # if id is in red zone list
                cv2.rectangle(img, (box[2], box[3]), (box[4], box[5]), (255, 0, 0), 2) # Create Red bounding boxes  #starting point, ending point size of 2
            else:
                cv2.rectangle(img, (box[2], box[3]), (box[4], box[5]), (0, 255, 0), 2) # Create Green bounding boxes
		#=================================================================#

		#=================================================================
    	# Purpose : Displaying the results
    	#================================================================= 
        def check_for_fall(activities):
            # Loop through the user's activities to check for fall detection
            for activity in activities:
                if activity.get('activity_type') == 'Fall Detection':  # Correctly check for 'Fall Detection'
                   return True  # If fall detected, return True

            return False  # If no fall detected in activities, return False
        print("Before The Fall Aler List")
        if len(fall_alert_list)!=0:
            
                text = "Fall Detected"
            
                #Uncomment the below lines for alert to email
                # makes sure that alert is generated when there are atleast 20 frames which shows that a fall has been detected
                print(" in the email function boooi")

                client = MongoClient('mongodb://localhost:27017')
                db = client['ivssdb']
                collection_logged_in_users = db['logged_in_users']
                logged_in_users = collection_logged_in_users.find()

                for user in logged_in_users:
                 user_email = user.get('email') 
                 activities = user.get('activities', [])
                 fall_detected = check_for_fall(activities)

                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
                cv2.imwrite('Fall Detected.jpg',img)
                if fall_detected:
                 print(" the email send")
                 image_email_fall.SendMail('dog.jpg',user_email)
        else:
            
            text = "Fall Not Detected"
                      # makes sure that alert is generated when there are 20 simultaeous frames of fall detection
            
        location = (10,25)												# Set the location of the displayed text
        if len(fall_alert_list)!=0:
            cv2.putText(img, text, location, cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)  # Display Text
        else:
            cv2.putText(img, text, location, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)  # Display Text

        #=================================================================#
    return img


def cvDrawBoxes_social(detections, img):
   
    #================================================================
    # Purpose : Filter out Persons class from detections and get 
    #           bounding box centroid for each person detection.
    #================================================================
    if len(detections) > 0:  						# At least 1 detection in the image and check detection presence in a frame  
        centroid_dict = dict() 						# Function creates a dictionary and calls it centroid_dict
        objectId = 0								# We inialize a variable called ObjectId and set it to 0
        for detection in detections:				# In this if statement, we filter all the detections for persons only
            # Check for the only person name tag 
            name_tag = str(detection[0].decode())   # Coco file has string of all the names
            if name_tag == 'person':                
                x, y, w, h = detection[2][0],\
                            detection[2][1],\
                            detection[2][2],\
                            detection[2][3]      	# Store the center points of the detections
                xmin, ymin, xmax, ymax = convertBack(float(x), float(y), float(w), float(h))   # Convert from center coordinates to rectangular coordinates, We use floats to ensure the precision of the BBox            
                # Append center point of bbox for persons detected.
                centroid_dict[objectId] = (int(x), int(y), xmin, ymin, xmax, ymax) # Create dictionary of tuple with 'objectId' as the index center points and bbox
                objectId += 1 #Increment the index for each detection      
    #=================================================================#
    
    #=================================================================
    # Purpose : Determine which person bbox are close to each other
    #=================================================================            	
        red_zone_list = [] # List containing which Object id is in under threshold distance condition. 
        red_line_list = []
        for (id1, p1), (id2, p2) in combinations(centroid_dict.items(), 2): # Get all the combinations of close detections, #List of multiple items - id1 1, points 2, 1,3
            dx, dy = p1[0] - p2[0], p1[1] - p2[1]  	# Check the difference between centroid x: 0, y :1
            distance = is_close(dx, dy) 			# Calculates the Euclidean distance
            if distance < 75.0:						# Set our social distance threshold - If they meet this condition then..
                if id1 not in red_zone_list:
                    red_zone_list.append(id1)       #  Add Id to a list
                    red_line_list.append(p1[0:2])   #  Add points to the list
                if id2 not in red_zone_list:
                    red_zone_list.append(id2)		# Same for the second id 
                    red_line_list.append(p2[0:2])
        
        for idx, box in centroid_dict.items():  # dict (1(key):red(value), 2 blue)  idx - key  box - value
            if idx in red_zone_list:   # if id is in red zone list
                cv2.rectangle(img, (box[2], box[3]), (box[4], box[5]), (255, 0, 0), 2) # Create Red bounding boxes  #starting point, ending point size of 2
            else:
                cv2.rectangle(img, (box[2], box[3]), (box[4], box[5]), (0, 255, 0), 2) # Create Green bounding boxes
		#=================================================================#

		#=================================================================
    	# Purpose : Display Risk Analytics and Show Risk Indicators
    	#=================================================================        
        text = "People at Risk: %s" % str(len(red_zone_list)) 			# Count People at Risk
        location = (10,25)												# Set the location of the displayed text
        cv2.putText(img, text, location, cv2.FONT_HERSHEY_SIMPLEX, 1, (246,86,86), 2, cv2.LINE_AA)  # Display Text

        for check in range(0, len(red_line_list)-1):					# Draw line between nearby bboxes iterate through redlist items
            start_point = red_line_list[check] 
            end_point = red_line_list[check+1]
            check_line_x = abs(end_point[0] - start_point[0])   		# Calculate the line coordinates for x  
            check_line_y = abs(end_point[1] - start_point[1])			# Calculate the line coordinates for y
            if (check_line_x < 75) and (check_line_y < 25):				# If both are We check that the lines are below our threshold distance.
                cv2.line(img, start_point, end_point, (255, 0, 0), 2)   # Only above the threshold lines are displayed. 
        #=================================================================#
    return img    

def cvDrawBoxes_vehicle(detections, img):
   
    #================================================================
    # Purpose : Filter out Cars class from detections and get 
    #           bounding box centroid for each car detection.
    #================================================================
    if len(detections) > 0:  						# At least 1 detection in the image and check detection presence in a frame  
        centroid_dict = dict() 						# Function creates a dictionary and calls it centroid_dict
        objectId = 0								# We inialize a variable called ObjectId and set it to 0
        for detection in detections:				# In this if statement, we filter all the detections for cars only
            # Check for the only car name tag 
            name_tag = str(detection[0].decode())   # Coco file has string of all the names
            if name_tag == 'car':                
                x, y, w, h = detection[2][0],\
                            detection[2][1],\
                            detection[2][2],\
                            detection[2][3]      	# Store the center points of the detections
                xmin, ymin, xmax, ymax = convertBack(float(x), float(y), float(w), float(h))   # Convert from center coordinates to rectangular coordinates, We use floats to ensure the precision of the BBox            
                # Append center point of bbox for cars detected.
                centroid_dict[objectId] = (int(x), int(y), xmin, ymin, xmax, ymax) # Create dictionary of tuple with 'objectId' as the index center points and bbox
                objectId += 1 #Increment the index for each detection      
    #=================================================================#
    
    #=================================================================
    # Purpose : Determine which car boxes are close to each other
    #=================================================================            	
        vehicle_red_zone_list = [] # List containing which Object id is in under threshold distance condition. 
        vehicle_red_line_list = []
        for (id1, p1), (id2, p2) in combinations(centroid_dict.items(), 2): # Get all the combinations of close detections, #List of multiple items - id1 1, points 2, 1,3
            #dx, dy = p1[0] - p2[0], p1[1] - p2[1]  	# Check the difference between centroid x: 0, y :1
            #distance = is_close(dx, dy) 			# Calculates the Euclidean distance
            
            #if distance < 50.0:						# Set our distance threshold - If they meet this condition then..
            
            if not ((p1[2]>=p2[4]) or (p1[4]<=p2[2]) or (p1[5]<=p2[3]) or (p1[3]>=p2[5])):
                if id1 not in vehicle_red_zone_list:
                    vehicle_red_zone_list.append(id1)       #  Add Id to a list
                    vehicle_red_line_list.append(p1[0:2])   #  Add points to the list
                if id2 not in vehicle_red_zone_list:
                    vehicle_red_zone_list.append(id2)		# Same for the second id 
                    vehicle_red_line_list.append(p2[0:2])
        
        for idx, box in centroid_dict.items():  # dict (1(key):red(value), 2 blue)  idx - key  box - value
            if idx in vehicle_red_zone_list:   # if id is in red zone list
                cv2.rectangle(img, (box[2], box[3]), (box[4], box[5]), (255, 0, 0), 2) # Create Red bounding boxes  #starting point, ending point size of 2
            else:
                cv2.rectangle(img, (box[2], box[3]), (box[4], box[5]), (0, 255, 0), 2) # Create Green bounding boxes
		#=================================================================#

		#=================================================================
    	# Purpose : Displaying the results and sending an alert message
    	#================================================================= 
        def check_for_car(activities):
            # Loop through the user's activities to check for fall detection
            for activity in activities:
                if activity.get('activity_type') == 'Vehicle Detection':  # Correctly check for 'Fall Detection'
                   return True  # If fall detected, return True

            return False  # If no fall detected in activities, return False
        
        if len(vehicle_red_zone_list)!=0:
                text = "Crash Detected"  
                client = MongoClient('mongodb://localhost:27017')
                db = client['ivssdb']
                collection_logged_in_users = db['logged_in_users']
                logged_in_users = collection_logged_in_users.find()

                for user in logged_in_users:
                 user_email = user.get('email') 
                 activities = user.get('activities', [])
                 fall_detected = check_for_car(activities)

                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
                cv2.imwrite('car_crash.jpg',img)
                if fall_detected:
                  print(" the email send")
                  image_email_car.SendMail('dog.jpg',user_email)

        else:
            text = "Crash Not Detected"
            
        location = (10,25)												# Set the location of the displayed text
        if len(vehicle_red_zone_list)!=0:
            cv2.putText(img, text, location, cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)  # Display Text
        else:
            cv2.putText(img, text, location, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)  # Display Text
            
    return img
    
def cvDrawBoxes_object(detections, img):
    # Colored labels dictionary
    color_dict = {
        'person' : [0, 255, 255], 'bicycle': [238, 123, 158], 'car' : [24, 245, 217], 'motorbike' : [224, 119, 227],
        'aeroplane' : [154, 52, 104], 'bus' : [179, 50, 247], 'train' : [180, 164, 5], 'truck' : [82, 42, 106],
        'boat' : [201, 25, 52], 'traffic light' : [62, 17, 209], 'fire hydrant' : [60, 68, 169], 'stop sign' : [199, 113, 167],
        'parking meter' : [19, 71, 68], 'bench' : [161, 83, 182], 'bird' : [75, 6, 145], 'cat' : [100, 64, 151],
        'dog' : [156, 116, 171], 'horse' : [88, 9, 123], 'sheep' : [181, 86, 222], 'cow' : [116, 238, 87],'elephant' : [74, 90, 143],
        'bear' : [249, 157, 47], 'zebra' : [26, 101, 131], 'giraffe' : [195, 130, 181], 'backpack' : [242, 52, 233],
        'umbrella' : [131, 11, 189], 'handbag' : [221, 229, 176], 'tie' : [193, 56, 44], 'suitcase' : [139, 53, 137],
        'frisbee' : [102, 208, 40], 'skis' : [61, 50, 7], 'snowboard' : [65, 82, 186], 'sports ball' : [65, 82, 186],
        'kite' : [153, 254, 81],'baseball bat' : [233, 80, 195],'baseball glove' : [165, 179, 213],'skateboard' : [57, 65, 211],
        'surfboard' : [98, 255, 164],'tennis racket' : [205, 219, 146],'bottle' : [140, 138, 172],'wine glass' : [23, 53, 119],
        'cup' : [102, 215, 88],'fork' : [198, 204, 245],'knife' : [183, 132, 233],'spoon' : [14, 87, 125],
        'bowl' : [221, 43, 104],'banana' : [181, 215, 6],'apple' : [16, 139, 183],'sandwich' : [150, 136, 166],'orange' : [219, 144, 1],
        'broccoli' : [123, 226, 195],'carrot' : [230, 45, 209],'hot dog' : [252, 215, 56],'pizza' : [234, 170, 131],
        'donut' : [36, 208, 234],'cake' : [19, 24, 2],'chair' : [115, 184, 234],'sofa' : [125, 238, 12],
        'pottedplant' : [57, 226, 76],'bed' : [77, 31, 134],'diningtable' : [208, 202, 204],'toilet' : [208, 202, 204],
        'tvmonitor' : [208, 202, 204],'laptop' : [159, 149, 163],'mouse' : [148, 148, 87],'remote' : [171, 107, 183],
        'keyboard' : [33, 154, 135],'cell phone' : [206, 209, 108],'microwave' : [206, 209, 108],'oven' : [97, 246, 15],
        'toaster' : [147, 140, 184],'sink' : [157, 58, 24],'refrigerator' : [117, 145, 137],'book' : [155, 129, 244],
        'clock' : [53, 61, 6],'vase' : [145, 75, 152],'scissors' : [8, 140, 38],'teddy bear' : [37, 61, 220],
        'hair drier' : [129, 12, 229],'toothbrush' : [11, 126, 158]
    }
    
    for detection in detections:
        x, y, w, h = detection[2][0],\
            detection[2][1],\
            detection[2][2],\
            detection[2][3]
        name_tag = str(detection[0].decode())
        for name_key, color_val in color_dict.items():
            if name_key == name_tag:
                color = color_val 
                xmin, ymin, xmax, ymax = convertBack(
                float(x), float(y), float(w), float(h))
                pt1 = (xmin, ymin)
                pt2 = (xmax, ymax)
                cv2.rectangle(img, pt1, pt2, color, 1)
                cv2.putText(img,
                            detection[0].decode() +
                            " [" + str(round(detection[1] * 100, 2)) + "]",
                            (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            color, 2)
    return img


def cvDrawBoxes(detections, img):
    """
    :param:
    detections = total detections in one frame
    img = image from detect_image method of darknet

    :return:
    img with bbox
    """
    # Colored labels dictionary
    color_dict = {
        'person' : [0, 255, 255], 'bicycle': [238, 123, 158], 'car' : [24, 245, 217], 'motorbike' : [224, 119, 227],
        'aeroplane' : [154, 52, 104], 'bus' : [179, 50, 247], 'train' : [180, 164, 5], 'truck' : [82, 42, 106],
        'boat' : [201, 25, 52], 'traffic light' : [62, 17, 209], 'fire hydrant' : [60, 68, 169], 'stop sign' : [199, 113, 167],
        'parking meter' : [19, 71, 68], 'bench' : [161, 83, 182], 'bird' : [75, 6, 145], 'cat' : [100, 64, 151],
        'dog' : [156, 116, 171], 'horse' : [88, 9, 123], 'sheep' : [181, 86, 222], 'cow' : [116, 238, 87],'elephant' : [74, 90, 143],
        'bear' : [249, 157, 47], 'zebra' : [26, 101, 131], 'giraffe' : [195, 130, 181], 'backpack' : [242, 52, 233],
        'umbrella' : [131, 11, 189], 'handbag' : [221, 229, 176], 'tie' : [193, 56, 44], 'suitcase' : [139, 53, 137],
        'frisbee' : [102, 208, 40], 'skis' : [61, 50, 7], 'snowboard' : [65, 82, 186], 'sports ball' : [65, 82, 186],
        'kite' : [153, 254, 81],'baseball bat' : [233, 80, 195],'baseball glove' : [165, 179, 213],'skateboard' : [57, 65, 211],
        'surfboard' : [98, 255, 164],'tennis racket' : [205, 219, 146],'bottle' : [140, 138, 172],'wine glass' : [23, 53, 119],
        'cup' : [102, 215, 88],'fork' : [198, 204, 245],'knife' : [183, 132, 233],'spoon' : [14, 87, 125],
        'bowl' : [221, 43, 104],'banana' : [181, 215, 6],'apple' : [16, 139, 183],'sandwich' : [150, 136, 166],'orange' : [219, 144, 1],
        'broccoli' : [123, 226, 195],'carrot' : [230, 45, 209],'hot dog' : [252, 215, 56],'pizza' : [234, 170, 131],
        'donut' : [36, 208, 234],'cake' : [19, 24, 2],'chair' : [115, 184, 234],'sofa' : [125, 238, 12],
        'pottedplant' : [57, 226, 76],'bed' : [77, 31, 134],'diningtable' : [208, 202, 204],'toilet' : [208, 202, 204],
        'tvmonitor' : [208, 202, 204],'laptop' : [159, 149, 163],'mouse' : [148, 148, 87],'remote' : [171, 107, 183],
        'keyboard' : [33, 154, 135],'cell phone' : [206, 209, 108],'microwave' : [206, 209, 108],'oven' : [97, 246, 15],
        'toaster' : [147, 140, 184],'sink' : [157, 58, 24],'refrigerator' : [117, 145, 137],'book' : [155, 129, 244],
        'clock' : [53, 61, 6],'vase' : [145, 75, 152],'scissors' : [8, 140, 38],'teddy bear' : [37, 61, 220],
        'hair drier' : [129, 12, 229],'toothbrush' : [11, 126, 158]
    }
    
    for detection in detections:
        x, y, w, h = detection[2][0],\
            detection[2][1],\
            detection[2][2],\
            detection[2][3]
        name_tag = str(detection[0].decode())
        for name_key, color_val in color_dict.items():
            if name_key == name_tag:
                color = color_val 
                xmin, ymin, xmax, ymax = convertBack(
                float(x), float(y), float(w), float(h))
                pt1 = (xmin, ymin)
                pt2 = (xmax, ymax)
                cv2.rectangle(img, pt1, pt2, color, 1)
                cv2.putText(img,
                            detection[0].decode() +
                            " [" + str(round(detection[1] * 100, 2)) + "]",
                            (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            color, 2)
    return img


def gen_frames(): 
    global case
    global metaMain, netMain, altNames, video_link
    configPath = "./cfg/yolov4.cfg"                                 # Path to cfg
    weightPath = "./yolov4.weights"                                 # Path to weights
    metaPath = "./cfg/coco.data"                                         # Path to meta data
    if not os.path.exists(configPath):                                   # Checks whether file exists otherwise return ValueError  
        raise ValueError("Invalid config path `" +
                         os.path.abspath(configPath)+"`")
    if not os.path.exists(weightPath):
        raise ValueError("Invalid weight path `" +
                         os.path.abspath(weightPath)+"`")
    if not os.path.exists(metaPath):
        raise ValueError("Invalid data file path `" +
                         os.path.abspath(metaPath)+"`")
    if netMain is None:                                                  # Checks the metaMain, NetMain and altNames. Loads it in script
        netMain = darknet.load_net_custom(configPath.encode(
            "ascii"), weightPath.encode("ascii"), 0, 1)                  # batch size = 1
    if metaMain is None:
        metaMain = darknet.load_meta(metaPath.encode("ascii"))
    if altNames is None:
        try:
            with open(metaPath) as metaFH:
                metaContents = metaFH.read()
                import re
                match = re.search("names *= *(.*)$", metaContents,
                                  re.IGNORECASE | re.MULTILINE)
                if match:
                    result = match.group(1)
                else:
                    result = None
                try:
                    if os.path.exists(result):
                        with open(result) as namesFH:
                            namesList = namesFH.read().strip().split("\n")
                            altNames = [x.strip() for x in namesList]
                except TypeError:
                    pass
        except Exception:
            pass  
    
    
    
    
    
    if live_video==1:
        url = video_link
        cap = cv2.VideoCapture(url)
        camera = cv2.VideoCapture()
        camera.open(url) 
        
    else:
        for ch in video_link:
              if ch == '&':
                video_link = video_link[:video_link.index(ch)]
     
        url = video_link   
        video = pafy.new(url) #yt videos
        best = video.getbest(preftype="any") #yt videos
        cap = cv2.VideoCapture()
        cap.open(best.url)  
        camera = cv2.VideoCapture()
        camera.open(best.url)    
        
        
      
    frame_width = int(cap.get(3))                                        # Returns the width and height of capture video   
    frame_height = int(cap.get(4))
    new_height, new_width = frame_height // 2, frame_width // 2
    
    #print("Video Reolution: ",(width, height))
    
    print("Starting the YOLO loop...")

    # Create an image we reuse for each detect
    darknet_image = darknet.make_image(new_width, new_height, 3)         # Create image according darknet for compatibility of network
    
    while True:                                                          # Load the input frame and write output frame.
        prev_time = time.time()
        ret, frame_read = cap.read()
        # Check if frame present :: 'ret' returns True if frame present, otherwise break the loop.
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)          # Convert frame into RGB from BGR and resize accordingly
        frame_resized = cv2.resize(frame_rgb, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

        darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())    # Copy that frame bytes to darknet_image

        detections = darknet.detect_image(netMain, metaMain, darknet_image, thresh=0.25)   # Detection occurs at this line and return detections, for customize we can change
        
        if case == 'object':
            image = cvDrawBoxes_object(detections, frame_resized)        # Call the function cvDrawBoxes_object() for colored bounding box per class
        elif case == 'social':
            image = cvDrawBoxes_social(detections, frame_resized)        # Call the function cvDrawBoxes_social() for colored bounding box per class
        elif case == 'fall':
            image = cvDrawBoxes_fall(detections, frame_resized)          # Call the function cvDrawBoxes_fall() for colored bounding box per class
        elif case == 'vehicle':
            image = cvDrawBoxes_vehicle(detections, frame_resized)       # Call the function cvDrawBoxes_vehicle() for colored bounding box per class
        elif case =='Live':
            image= cvDrawBoxes(detections,frame_resized)
        
          
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ret, buffer = cv2.imencode('.jpg', image)
        frame = buffer.tobytes()
                
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

#Deploying the app using flask
#Initialize the Flask app
from flask_session import Session
from flask import session

import secrets
from datetime import datetime
live_video=0


app = Flask(__name__)
CORS(app,supports_credentials=True)

secret_key = secrets.token_hex(16)
app.secret_key = secret_key


client = MongoClient('mongodb://localhost:27017')
db = client['ivssdb']
collection = db['users']
collection_contacts = db['Contacts']
collection_activity = db['Activity']
collection_logged_in_users = db['logged_in_users']


temp_email= None
@app.route('/api/start-recording',methods=['GET','POST'])
def start_recording(): 
    global live_video
    live_video=1
    
    global case
    global video_link
    video_link='http://192.168.1.2:8080/video'
    case='Live'
    
    video_feed_url = 'http://localhost:5000/video_feed'
    
    return jsonify({"video_feed_url": video_feed_url})

@app.route('/api/user-data', methods=['GET','POST'])
def get_user_data():
    # Query to find user by email
    user_data = collection_logged_in_users.find_one({'email': temp_email})
    
    if user_data:
        last_login = user_data.get('last_login', None)
        

        activities = user_data.get('activities', [])
        activity_types = [activity.get('activity_type') for activity in activities]
    
        response_data={
        'email': temp_email,
            'last_login': last_login,
            'servicesUsed': activity_types
     }
        return response_data
    else:
        return None, None


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Email and password are required'}), 400

    email = data['email']
    password = data['password']

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    if collection.find_one({'email': email}):
        return jsonify({'message': 'User already exists'}), 409

    collection.insert_one({'email': email, 'password': hashed_password})
    return jsonify({'message': 'User registered successfully'})


@app.route('/login', methods=['POST','GET'])
def login():
    data = request.get_json()
    if 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Email and password are required'}), 400

    email = data['email']
    password = data['password']

    user = collection.find_one({'email': email})
    
    global temp_email  # Access the global variable

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        user_activity = collection_activity.find({'email': email}, {'_id': 0})

        activities = list(user_activity)
        temp_email = email

        current_time=datetime.utcnow()
        

        collection_logged_in_users.insert_one({'email': email, 'activities': activities,'last_login': current_time})
        # Return login success message along with user email and activities
        user_data = collection.find_one({'email': email}, {'_id': 0, 'password': 0})
        return jsonify({'message': 'Login successful','user': user_data,'activities': activities}), 200
        # return jsonify({'message': 'Login successful', 'email': email, 'activities': activities}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

@app.route('/', methods=['GET'])  # Define route for the root URL
def index():
    return jsonify({'message': 'Welcome to the backend!'})

@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data received'}), 400

    # Extract form data
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    subject = data.get('subject')
    message = data.get('message')

    if not name or not email or not phone or not subject or not message:
        return jsonify({'message': 'Incomplete form data'}), 400

    # Store form data in MongoDB (collection1 for contacts)
    contact_data = {
        'name': name,
        'email': email,
        'phone': phone,
        'subject': subject,
        'message': message
    }
    collection_contacts.insert_one(contact_data)

    return jsonify({'message': 'Form data received and stored successfully'})



@app.route('/api/start-fall-detection', methods=['POST','GET'])
def start_fall_detection():
    global video_link
    global case
    data = request.json
    video_link = data.get('videoLink')
    case = 'fall'
    global temp_email

    session['email']=temp_email

    user_email = session.get('email')

    print(" Retrieve the data of email in Fall Detection",user_email)

   
    
    activity_data = {
        'email': user_email,
        'activity_type': 'Fall Detection',  # Customize this based on the activity
        # Add more details about the activity if needed
    }
    collection_activity.insert_one(activity_data)
    collection_logged_in_users.update_one(
        {'email': user_email},
        {'$push': {'activities': activity_data}}
    )
    video_feed_url = 'http://localhost:5000/video_feed'  # Replace this with your actual video feed URL
    user_data = collection_logged_in_users.find_one({'email': user_email}, {'_id': 0, 'activities': 0})

    return {
        'status': 'success',
        'message': 'Fall detection initiated',
        'videoFeedUrl': video_feed_url,
        'user': user_data
    }

@app.route('/api/Objectdetection', methods=['POST','GET'])
def start_Object_detection():
    global video_link
    global case
    data = request.json
    video_link = data.get('videoLink')
    case = 'object'
    global temp_email

    session['email']=temp_email

    user_email = session.get('email')

    print(" Retrieve the data of email in Object Detection",user_email)

   
    
    activity_data = {
        'email': user_email,
        'activity_type': 'Object Detection',  # Customize this based on the activity
        # Add more details about the activity if needed
    }
    collection_activity.insert_one(activity_data)
    collection_logged_in_users.update_one(
        {'email': user_email},
        {'$push': {'activities': activity_data}}
    )

    video_feed_url = "http://localhost:5000/video_feed"  # Replace this with your actual video feed URL


    user_data = collection_logged_in_users.find_one({'email': user_email}, {'_id': 0, 'activities': 0})

    return {
        'status': 'success',
        'message': 'Fall detection initiated',
        'videoFeedUrl': video_feed_url,
        'user': user_data
    }

@app.route('/api/Socialdetection', methods=['POST','GET'])
def start_Social_detection():
    global video_link
    global case
    data = request.json
    video_link = data.get('videoLink')
    case = 'social'
    global temp_email

    session['email']=temp_email

    user_email = session.get('email')

    print(" Retrieve the data of email in Soical Detection",user_email)

   
    
    activity_data = {
        'email': user_email,
        'activity_type': 'Social Distancing',  # Customize this based on the activity
        # Add more details about the activity if needed
    }
    collection_activity.insert_one(activity_data)
    collection_logged_in_users.update_one(
        {'email': user_email},
        {'$push': {'activities': activity_data}}
    )

    video_feed_url = "http://localhost:5000/video_feed"  # Replace this with your actual video feed URL
    user_data = collection_logged_in_users.find_one({'email': user_email}, {'_id': 0, 'activities': 0})

    return {
        'status': 'success',
        'message': 'Fall detection initiated',
        'videoFeedUrl': video_feed_url,
        'user': user_data
    }


@app.route('/api/vehciledetection', methods=['POST','GET'])
def start_Vehcile_detection():
    global video_link
    global case
    data = request.json
    video_link = data.get('videoLink')
    case = 'vehicle'
    global temp_email

    session['email']=temp_email

    user_email = session.get('email')

    print(" Retrieve the data of email in Vehcile Detection",user_email)

   
    
    activity_data = {
        'email': user_email,
        'activity_type': 'Vehicle Detection',  # Customize this based on the activity
        # Add more details about the activity if needed
    }
    collection_activity.insert_one(activity_data)
    collection_logged_in_users.update_one(
        {'email': user_email},
        {'$push': {'activities': activity_data}}
    )
    
    video_feed_url = "http://localhost:5000/video_feed"  # Replace this with your actual video feed URL
    user_data = collection_logged_in_users.find_one({'email': user_email}, {'_id': 0, 'activities': 0})

    return {
        'status': 'success',
        'message': 'Fall detection initiated',
        'videoFeedUrl': video_feed_url,
        'user': user_data
    }




	
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)