# LoxiAnalysisApp
LoxiAnalysis is an application that uses a trained YOLO model to analyse a Valorant vieo gameplay. In the end, it calculates statistics about the aim of an individual, generating a score and offering suggestions for impovement.

Analysis:
- I exported the images, frame by frame, from real Valorant gameplay (The Range mode). Using Label Studio, I annotated the images, marking: the bot, head, shot, headshot and kill. I exported the dataset as YOLO with images.
- For model training, I used the YOLO 26 model developed by Ultralytics and the dataset exported from Label Studio.
- With the model trained, I could run it on any video from The Range and obtain data from every frame.
- I centralized the data per bot. 
- I started to calculate statistics that are important in aim analysis: reaction time, headshot percentage, time to kill, shot efficiency, flick accuracy, time on target. 
- Now, I am working on calculating the final score (still looking into the low and high limits of every statistic).

UI:
- Used PySide6;
- still working on the analysis part, the UI is extremely basic.
- there will not be users, maybe in the future.