from ultralytics import YOLO
import json
import cv2
import math
import os
import datetime
import logging

class Bot:
    def __init__(self, id):
        self.id = id



class Methods:

    def setup_logger(self, destination_path):
        log_name = "LoxiAnalysis.log"
        logger_path = os.path.join(destination_path, log_name)
        
        if os.path.exists(logger_path):
            os.remove(logger_path)
            
        logger = logging.getLogger()
        logging.basicConfig(filename=logger_path, level=logging.INFO)
        logger.info(f" Initializing logger...")
        
        return logger


    def analyze_video(self, yolo_path, video_path, results_path):
        """
        Runs the yolo model on a video, and saves the results in json format.
        Input:
            - yolo_path (str): the path to the yolo model (best.pt);
            - video_path (str): the path to the video for analysis;
            - results_path (str): the path of the destination json file;
        """
        
        # Load your trained model
        model = YOLO(yolo_path)

        #img_path = r"C:\Users\Gamebox\Documents\Bandicam\bandicam 2026-03-29 13-10-17-024.jpg"
        # Run inference on an image
        #results = model(img_path, show=False, save=True)


        # Run tracking on a video
        results = model.track(
            source=video_path,
            show=False,
            save=True
        )

        output = []

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                
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
                output.append(detection)

        # save to file
        with open(results_path, "w") as f:
            json.dump(output, f, indent=4)


    def run_analysis(self, yolo_path, video_path, results_path, logger):
        
        # Import the model
        model = YOLO(yolo_path)
        
        # Import the video
        cap = cv2.VideoCapture(video_path)
        
        width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH) 
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        dimensions= [width, height]
        
        # get nr of fps
        fps = cap.get(cv2.CAP_PROP_FPS)
        logger.info(f" FPS: {fps}")
        
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
                        if float(box.conf[0]) > 0.5:
                            shot_flag = True
                        else:
                            continue
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
        return dimensions


    def get_nr_shots(self, bot_data, results_json):
        """
        Calculates the number of shots fired for every kill. On the first frame where the shot is identified, we count the shot, then wait for the first frame without the shot animation. 
        There is where one individual shot ends.
        Input:
            - bot_data (list): bot objects
            - results_json(str): path to the results json created by the run_analysis method.
        Output:
        - updates (adds new properties) each bot with the number of shots fired to kill it and the time of the first shot
        """
        
        with open(results_json, 'r') as json_data:
            results = json.load(json_data)

        shot_flag = False

        for bot in bot_data:
            bot.nr_shots = 0
            bot.headshots = 0
            bot.shots_frames=[]
            first_shot = True
            #print("\n------------------------------------------------------")
            #print(f"Bot {bot.id}")
            
            try:
                counter = 0
                good_shot = False
                
                # starting from 2 frames after the bot appeared in fov, to eliminate the accidental counting of shots
                for frame in range(bot.start_frame + 2, bot.end_frame):
                    if results[frame]["shot"] == True:
                        # if we have the shot animation for more than 3 frames, it means we have two consecuitve shots
                        if counter >= 2:
                            shot_flag = False
                            
                        # if we have not marked this shot
                        if not shot_flag:
                            counter = 0
                            # if it is the first shot fired for this bot, save it's data
                            if first_shot:
                                bot.first_shot = results[frame]["time"]
                                bot.first_shot_frame = frame
                                first_shot = False
                            
                            # save the start of the shot animation process
                            bot.nr_shots += 1
                            bot.shots_frames.append(frame)
                            
                            
                            #print(f"Shot at frame {frame}.")
                            
                            # if we have the headshot animation in one of the next 3 frames, mark as headshot
                            for i in range(0,3):
                                if results[frame + i]["headshot"] == True:
                                    bot.headshots += 1
                                    #print(f"Is headshot")
                                    break
                            
                            shot_flag = True
                        else:
                            counter += 1
                    else:
                        # if it is not the first frame of the shot animation, dont count it as a new shot
                        shot_flag = False
                        
                        
            except Exception as e:
                print(e)
            


    def get_data_per_bot(self, results_json):
        """
        Parse the json resulted from the model analysis. Create a list containing each robot as object (in order of appearence) and as properties:
        - t_spawn: the time it appeared in the fov
        - start_frame: the first frame of appearence
        - t_kill: the time it was killed
        - end_frame: the frame of it's kill.
        Input:
            - results_json (str): the path to the resulted json after model analysis;
        Output:
            - bot_data (list): list of Bot objects with the above properties
        """
        
        with open(results_json, 'r') as json_data:
            results = json.load(json_data)
        
        bot_flag = False
        bot_data = []
        kill_noted = False
        counter = 0
        
        for frame in results:
            try:
                if not bot_flag:
                    # if we detected a new bot
                    for detection in frame["detections"]:
                        if detection["class_name"] == "bot":
                            if not bot_flag:
                                counter += 1
                                #bot_data[counter] = {}
                                bot_data.append(Bot(counter))
                                bot_data[counter-1].t_spawn = frame["time"]
                                bot_data[counter-1].start_frame = frame["frame"]
                                bot_flag = True
                                break
                else:        
                    if frame["kill"] == True:
                        # if we did not mark this kill
                        if not kill_noted:
                            bot_data[counter-1].t_kill = frame["time"]
                            bot_data[counter-1].end_frame = frame["frame"]
                            bot_flag = False
                            kill_noted = True
                    else:
                        kill_noted = False
            except Exception as e:
                pass

        return bot_data



    def statistics_calculation(self, bot_data, results_json, crosshair):
        statistic_results ={"shots": 0, "headshots": 0, "reaction_time": 0, "time_to_kill": 0, "shot_efficiency": 0,  "headshot_percentage": 0, "flick_accuracy":0,  "time_on_target": 0}

        counter = 0

        for bot in bot_data:
            try:
                bot.reaction_time = bot.first_shot - bot.t_spawn
                bot.time_to_kill = bot.t_kill - bot.first_shot
                bot.headshot_percentage = (bot.headshots / bot.nr_shots) * 100
                bot.flick_accuracy = 0
                
                statistic_results["shots"] += bot.nr_shots
                statistic_results["headshots"] += bot.headshots
                statistic_results["reaction_time"] += (bot.first_shot - bot.t_spawn)
                statistic_results["time_to_kill"] += (bot.t_kill - bot.first_shot)
                statistic_results["shot_efficiency"] += bot.nr_shots
                statistic_results["headshot_percentage"] += (bot.headshots /bot.nr_shots)
                counter += 1
            except:
                pass
        try:
            statistic_results["reaction_time"] /= counter
            statistic_results["time_to_kill"] /= counter
            statistic_results["shot_efficiency"] /= counter
            statistic_results["headshot_percentage"] /= counter
            statistic_results["flick_accuracy"] = self.flick_accuracy(bot_data, results_json, crosshair)
            statistic_results["time_on_target"] = self.time_on_target(bot_data, results_json, crosshair)
        except Exception as e:
            print(e)

        return statistic_results


    def flick_accuracy(self, bot_data, results_json, crosshair):
        # At t_first_shot: Compute distance between crosshair and head center
        
        distanta = 0

        with open(results_json, 'r') as json_data:
            results = json.load(json_data)

        counter = 0
        for bot in bot_data:
            try:
                # in the previous frame of the first shot, compute the distance between the middle of the head and the crosshair
                for detection in results[bot.first_shot_frame - 1]["detections"]:
                    # if the model detected a head in the frame, compute the distance
                    if detection["class_name"] == "head":
                        head_center = [(detection["bbox"]["x1"] + detection["bbox"]["x2"]) / 2, (detection["bbox"]["y1"] + detection["bbox"]["y2"]) / 2]
                        break
                
                bot.flick_accuracy = math.sqrt((crosshair[0] - head_center[0])**2 + (crosshair[1] - head_center[1])**2)
                distanta += bot.flick_accuracy
                counter += 1
            except:
                pass
        
        distanta /= counter 

        return distanta


    def time_on_target(self, bot_data, results_json, crosshair):
        #   How long is the crosshair on the head before firing the final shot
        
        timp = 0

        with open(results_json, 'r') as json_data:
            results = json.load(json_data)

        counter = 0
        for bot in bot_data:
            #print("\n--------------------------------")
            #print(f"Bot {bot.id}")
            counter += 1
            bot.time_on_target = 1
            
            try:
                #print(f"Checking in range {bot.shots_frames[-1] -1} -> {bot.start_frame}")
                for frame in range(bot.shots_frames[-1] - 1, bot.start_frame, -1):
                    # check in the frame if the crosshair was at the head level
                    stop_frame = False
                    for detection in results[frame]["detections"]:
                        if detection["class_name"] == "head":
                            if detection["bbox"]["x1"] -2 <= crosshair[0] <= detection["bbox"]["x2"] + 2 and detection["bbox"]["y1"] - 2 <= crosshair[1] <= detection["bbox"]["y2"] + 2:
                                bot.time_on_target = results[bot.shots_frames[-1]]["time"] - results[frame]["time"]
                                #print("On head")
                            else:
                                stop_frame = True
                                #print(f"Stopped at {frame}")
                            break
                                
                    
                    # if we got the time on this bot, go to the next one
                    if stop_frame:
                        #print(bot.time_on_target)
                        break
                timp += bot.time_on_target

            except Exception as e:
                print(e)
        
        timp /= counter 

        return timp


    def clean_data(self, results_json):
        """
        
        """
        
        with open(results_json, 'r') as json_data:
            results = json.load(json_data)

        clean_results = []
        heads_list = []

        for data in range(len(results)):
            heads_list = []
            clean_results.append(results[data].copy())
            clean_results[data]["detections"] = []
            
            for detection in range(len(results[data]["detections"])):
                if results[data]["detections"][detection]["class_name"] == "head":
                    heads_list.append(results[data]["detections"][detection].copy())
                else:
                    clean_results[data]["detections"].append(results[data]["detections"][detection].copy())           
            
            if len(heads_list) == 1:
                clean_results[data]["detections"].append(heads_list[0].copy())
            else:
                maxim = 0
                for head in range(len(heads_list)):
                    if heads_list[head]["confidence"] > maxim:
                        maxim = heads_list[head]["confidence"]
                        true_head = head
                if maxim != 0:
                    clean_results[data]["detections"].append(heads_list[true_head].copy())
            
            
        root, tail = os.path.splitext(results_json)
        new_path = os.path.join(root + "-clean-results.json")
        with open(new_path, "w") as f:
            json.dump(clean_results, f, indent=4)
        
        return new_path
        
        
    def show_bot_data(self, bot_data, logger):
        for bot in bot_data:
            try:
                logger.info(f" ID: {bot.id}, t_spawn={"{:.2f}".format(bot.t_spawn)}, start_frame={bot.start_frame}, t_kill={"{:.2f}".format(bot.t_kill)}, end_frame={bot.end_frame}, first_shot={"{:.2f}".format(bot.first_shot)}, first_shot_frame={bot.first_shot_frame}, nr_shots={bot.nr_shots}, headshots={bot.headshots}, shots_frames: {bot.shots_frames}, reaction_time= {"{:.2f}".format(bot.reaction_time)}, time_to_kill={"{:.2f}".format(bot.time_to_kill)}, headshot_percentage={"{:.2f}".format(bot.headshot_percentage)}, flick_accuracy={"{:.2f}".format(bot.flick_accuracy)}, time_on_target={"{:.2f}".format(bot.time_on_target)}")
                print(f"ID: {bot.id}, t_spawn={bot.t_spawn}, start_frame={bot.start_frame}", end=" ")
                print(f"t_kill={bot.t_kill}, end_frame={bot.end_frame}", end=" ")
                print(f"first_shot={bot.first_shot}, first_shot_frame={bot.first_shot_frame} nr_shots={bot.nr_shots}, headshots={bot.headshots}, shots_frames: {bot.shots_frames}")
                print(f"reaction_time= {bot.reaction_time}, time_to_kill={bot.time_to_kill}, headshot_percentage={bot.headshot_percentage}, flick_accuracy={bot.flick_accuracy}, time_on_target={bot.time_on_target}")
            except Exception as e:
                pass
################################################################################################################################



class Analysis:
    def __init__(self, results_location, yolo_path, video_path):
        timestamp = str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
        results_path = os.path.join(results_location, timestamp)
        
        os.mkdir(results_path)
        self.results_json = os.path.join(results_path, "bot-data.json")
        
        self.yolo_path = yolo_path
        self.video_path = video_path
        #self.results_location = results_location
        
        self.utils = Methods()
        
        self.logger = self.utils.setup_logger(results_path)

        self.logger.info(f" ---Starting a new run---")
        self.logger.info(f" Video for analysis: {video_path}")
        self.logger.info(f" Results location: {results_location}")
        
    
    def normalize_data(self, statistics):
        limits = {"reaction_time": {"range": [0, 2], "mode": "ascending"}, "time_to_kill": {"range": [0, 2], "mode": "ascending"}, "flick_accuracy": {"range": [0, 40], "mode": "ascending"}, "time_on_target": {"range": [0, 1], "mode": "ascending"}, "headshot_percentage": {"range": [0, 1], "mode": "descending"}, "shot_efficiency": {"range": [1, 5], "mode": "ascending"}}
        
        normalized_stats = {}
        
        for stat in statistics.items():
            try:
                lower_bound = limits[stat[0]]["range"][0]
                upper_bound = limits[stat[0]]["range"][1]

                if limits[stat[0]]["mode"] == "ascending":
                    normalized_stats[stat[0]] = (upper_bound - stat[1]) / (upper_bound - lower_bound)
                    if normalized_stats[stat[0]] < 0:
                        normalized_stats[stat[0]] = 0
                    #print(f"Stat {stat[0]}: value {stat[1]}  ==>  normalized={normalized_stats[stat[0]]}")

                else:
                    normalized_stats[stat[0]] = (stat[1] - lower_bound) / (upper_bound - lower_bound)
                    if normalized_stats[stat[0]] > 1:
                        normalized_stats[stat[0]] = 1
            except Exception as e:
                print(e)
                
        return normalized_stats


    def calculate_score(self, normalized_stats):
        weights = {"reaction_time": 0.18 , "time_to_kill": 0.12, "flick_accuracy": 0.24, "time_on_target": 0.08, "headshot_percentage": 0.22, "shot_efficiency": 0.16}
        score = 0
        
        for stats in normalized_stats.items():
            score += stats[1] * weights[stats[0]]
        
        return score


    def run(self):
        """
        
        """
        # Run the model on the desired video
        self.logger.info(f" Analysing video. Results will be saved at {self.results_json}")
        image_dimensions =  self.utils.run_analysis(self.yolo_path, self.video_path, self.results_json, self.logger)
        
        self.logger.info(f" Video analysis done.")
        self.logger.info(f" Image dimensions: {image_dimensions}")
        
        crosshair = [image_dimensions[0]/2, image_dimensions[1]/2]
        self.logger.info(f" Crosshair coordonates: {crosshair}")
        self.logger.info(f" Cleaning the data...")
        
        # clean data (head duplicates)
        clean_dataset = self.utils.clean_data(self.results_json)
        self.logger.info(f" Clean data saved at {clean_dataset}!")
        
        # Get initial data per bot
        self.logger.info(f" Getting data per bot ...")
        bot_data = self.utils.get_data_per_bot(clean_dataset)
        
        # Calculate nr of shots/kill and atribute it to the respective bot object
        self.logger.info(" Calculating the number of shots ...")
        self.utils.get_nr_shots(bot_data, clean_dataset)

        self.logger.info(" Calculating statistics ...")
        statistics = self.utils.statistics_calculation(bot_data, clean_dataset, crosshair)
        
        self.utils.show_bot_data(bot_data, self.logger)
        
        print(f"\nStatistica: {statistics}")
        self.logger.info(f" Statistics: {statistics}")
        
        norm = self.normalize_data(statistics)
        self.logger.info(f" Normalized: {norm}")
        print(f"\nNormalized: {norm}")
        
        scor = self.calculate_score(norm)
        print(scor)
        self.logger.info(f" Final score: {scor}")
        
        self.logger.info(" Done!")    
        
        return statistics