import mediapipe as mp
import cv2
import numpy as np


class PeoplePose:
    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    mpDraw = mp.solutions.drawing_utils
    
    def make_landmark_timestep(self,results):
        # print(results.pose_landmarks.landmark)
        c_lm = []
        for id, lm in enumerate(results.pose_landmarks.landmark):
            c_lm.append(lm.x)
            c_lm.append(lm.y)
            c_lm.append(lm.z)
            c_lm.append(lm.visibility)
        return c_lm


    def draw_landmark_on_image(self,mpDraw, results, img):
        # Draw connections
        mpDraw.draw_landmarks(img, results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        
        # Draw mark
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            # print(id,lm)
            cx, cy = int(lm.x +w), int(lm.y +h)
            cv2.circle(img, (cx,cy), 5, (0,0,255),  cv2.FILLED)
        return img




