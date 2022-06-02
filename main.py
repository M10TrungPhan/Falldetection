from utils import*
import time 
import numpy as np
import os
from tensorflow import keras
import threading
from queue import Queue
from webfall import db
from webfall.models import History
from datetime import datetime

def detect(model, lm_list, frame):
    global label
    global k 
    lm_list = np.array(lm_list)
    lm_list = np.expand_dims(lm_list, axis=0)
    print(lm_list.shape)
    results = model.predict(lm_list)
    print(results)
    if results[0][0]>0.8:
    	k = k +1
    	print(k)
    	if k == 1:
    		fall_time = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    		filename = fall_time.replace(' ', '_').replace(':','_').replace("/","_")
    		history = History(time = fall_time, image=filename)
    		db.session.add(history)
    		db.session.commit()
    		frame_shape = np.array(frame).shape
    		ratio = frame_shape[0]/frame_shape[1]
    		frame = cv2.resize(frame,(int(600/ratio),600))    		
    		cv2.imwrite('G:/DHBK/Thesis/Project_thesis/webfall/static/last_fall/lastfall.jpg',frame)   		
    		cv2.imwrite('G:/DHBK/Thesis/Project_thesis/webfall/static/fall/'+ filename +'.jpg',frame)
    		with open('G:/DHBK/Thesis/Project_thesis/webfall/static/last_fall/time.txt', mode='w') as f:
                 f.write(fall_time)   
    	label = 'Fall'
    	
    else:
        k = 0
        label = 'No Fall'    
PeoplePose = PeoplePose()
model = keras.models.load_model('model.h5') 
lm_list = [[0 for i in range(132)] for x in range(49)]
k = 0
label ='No Fall'
label_video ='5'
name_video = label_video +'.mp4'
cTime = 0
pTime = 0
no_frame = 0
warmup_frames =1
i =0
cap = cv2.VideoCapture(name_video)
while cap.isOpened():
	no_frame +=1
	ret, frame = cap.read()
	if ret:
		frame_save = frame.copy()
		frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
		results = PeoplePose.pose.process(frameRGB)
		if results.pose_landmarks:
			lm = PeoplePose.make_landmark_timestep(results)
			lm_list.append(lm)
			# Dua vao model nhan dien			
			if len(lm_list)==50:
				t1 = threading.Thread(target = detect, args=(model,lm_list,frame_save,))
				t1.start()
				lm_list = []												
		cTime = time.time()
		fps= 1/(cTime-pTime)
		pTime = cTime
		# Draw FPS frame
		cv2.putText(frame, label,(10,50),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),2 )
		cv2.putText(frame, str(int(fps))+'/'+str(int(no_frame)),(200,50),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),2)
		frame_shape = np.array(frame).shape
		ratio = frame_shape[0]/frame_shape[1]
		frame = cv2.resize(frame,(int(600/ratio),600))
		cv2.imshow('Fall Detection',frame)
		if cv2.waitKey(10) & 0xFF ==ord('q'):
			break
	else:
		break		
cap.release()
cv2.destroyAllWindows()



