 **Intelligent Surveillance System with Darknet YOLO**

**##Overview**

This project demonstrates a real-time intelligent surveillance system that harnesses the power of Darknet YOLO for object detection, crash detection, social distancing monitoring, fall detection, and email alerts. It integrates Python, C, React, Flask, and the YOLOv4 model to deliver a comprehensive solution.

**##Key Features**

- **Live Object Detection:** Detects objects in live video feeds using Darknet YOLOv4.
- **Crash Detection:** Identifies potential crashes or collisions in real-time.
- **Social Distancing Monitoring:** Measures distances between people to enforce social distancing guidelines.
- **Fall Detection:** Detects falls, especially among vulnerable individuals.
- **Email Alerts:** Sends notifications via email to designated recipients when specific events are detected.

**## Technology Stack**

- **Python:** Backend logic, model integration, and email functionality.
- **C:** Darknet YOLOv4 model implementation.
- **React:** User interface for viewing live camera feeds and detections.
- **Flask:** Web framework for serving the React frontend and handling API requests.

**## Project Structure**

```
darknet/build/darknet/x64/
├── backend/   # Python backend code
│   ├── app.py  # Flask application
│   ├── models/ # Object detection models
│   └── utils/  # Utility functions
├── frontend/  # React frontend code
│   ├── ivss/
│   └── public/
├── darknet/   # Darknet YOLOv4 framework
└──  # Project dependencies
```
To Run the Yolov4 Using Darknet as for this Project, You Need to Install Cmake, CUDNN, CUDA, Opencv and NVIDIA GPU.

**#Setup**

1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Build Darknet: Follow the official Darknet build instructions.
4. Download pre-trained YOLOv4 weights: Place them in the `models` directory.

**#Running the System**

1. Start the backend: `python backend/app.py`
2. Start the frontend: `cd ivss && npm run dev`

**#Usage**

1. Access the web interface at `http://localhost:5000` (or the specified port).
2. Observe live camera feeds with detections.
3. Configure email settings for alerts.

**#Additional Features**

- **Customizable Detection Classes:** Adjust the model to detect specific objects of interest.
- **Configurable Alert Thresholds:** Fine-tune the sensitivity of detection triggers.
- **Video Archiving:** Store recorded footage for later review.

**#Contributing**

We welcome contributions! Please refer to the contribution guidelines for details.
Web Developer : @MDaniyalTariq


**#License**

This project is licensed under the MIT License.
