from ultralytics import YOLO
import json, cv2

def run_analysis(yolo_path, video_path, results_path):
    """ Get the results json with data per frame."""
    # Import the model
    model = YOLO(yolo_path)
    
    # Import the video
    cap = cv2.VideoCapture(video_path)
    
    width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH) 
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    dimensions= [width, height]
    
    # get nr of fps
    fps = cap.get(cv2.CAP_PROP_FPS)
    #self.logger.info(f" FPS: {fps}")
    
    frame_idx = 0
    timeline = []
    
    # Iterate through each frame
    while True:
        # read frame
        ret, frame = cap.read()
        
        # Check if is end of video
        if not ret:
            break
        
        # Create a timestamp for the frame
        timestamp = frame_idx / fps
        
        # Run YOLO
        detections = model(frame)
        
        # Format results
        shot_flag = False
        kill_flag = False
        headshot_flag = False
        
        frame_detections = []
        for r in detections:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                
                if model.names[int(box.cls[0])] == 'shot':
                    shot_flag = True
                elif model.names[int(box.cls[0])] == 'kill':
                    kill_flag = True
                elif model.names[int(box.cls[0])] == 'headshot':
                    headshot_flag = True
                
                detection = {
                    "class_id": int(box.cls[0]),
                    "class_name": model.names[int(box.cls[0])],
                    "confidence": float(box.conf[0]),
                    "bbox": {
                        "x1": x1,
                        "y1": y1,
                        "x2": x2,
                        "y2": y2
                        }
                    }
                frame_detections.append(detection)
                    
        # Save the frame data
        frame_data = {
            "frame": frame_idx,
            "time": timestamp,
            "detections": frame_detections,
            "shot": shot_flag,
            "headshot" : headshot_flag,
            "kill": kill_flag
        }
                
        # Append the frame data to the timeline
        timeline.append(frame_data)
        
        # Set id for the next frame
        frame_idx += 1
        
    # save to file
    with open(results_path, "w") as f:
        json.dump(timeline, f, indent=4)
    
    # Release the video
    cap.release()


def run_on_video(yolo_p, video_p):
    """To save the annotated video."""
    
    model = YOLO(yolo_p)
    results = model.predict(video_p, save=True, project=r"C:\Users\bianc\Desktop\outputs", name="annotated_videos", exist_ok=True)

    try:
        for r in results:
            print(r.save_dir)
            break
        print(results[0].save_dir)
    except Exception as e:
        print(e)
        
yolo_path = r"C:\Users\bianc\Desktop\Facultate\Licenta\LoxiAnalysisApp\files\best.pt"
video_path = r"C:\Users\bianc\Desktop\Facultate\Licenta\Fisiere\Video\1.4.1.mp4"
results_path = r"C:\Users\bianc\Desktop\detections-1.json"

#run_analysis(yolo_path, video_path, results_path)
run_on_video(yolo_path, video_path)