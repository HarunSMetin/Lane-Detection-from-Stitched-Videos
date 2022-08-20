import cv2
import numpy as np 

import stitcher
import lane_detection as ld
import video_slicer

def trim(frame):

    if not np.sum(frame[0]):
        return trim(frame[1:])

    elif not np.sum(frame[-1]):
        return trim(frame[:-2])

    elif not np.sum(frame[:,0]):
        return trim(frame[:,1:]) 

    elif not np.sum(frame[:,-1]):
        return trim(frame[:,:-2])    
    return frame

whichVideo="video1"
filePath='test/4/{}/'.format(whichVideo)
fileName='test.mp4'
"""videoSlicer.sliceStart(filePath,fileName)"""
fullPath= filePath+fileName

cap = cv2.VideoCapture(fullPath)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

capMain = cv2.VideoCapture('{}main.mp4'.format(filePath))
capLeft = cv2.VideoCapture('{}left.mp4'.format(filePath))
capRight = cv2.VideoCapture('{}right.mp4'.format(filePath))

video_writer = cv2.VideoWriter("output_of_{}.mp4".format(whichVideo), fourcc, fps, (width, height)) 

feature_to_match = 'knn'
for frame_idx in range(int(capMain.get(cv2.CAP_PROP_FRAME_COUNT))):

    retM, frameM = capMain.read()   
    retL, frameL = capLeft.read()
    retR, frameR = capRight.read()

    s = stitcher.StitchWithSift(0)
    stitched_image = s.stitch(frameR,frameM,feature_to_match)
    stitched_image=trim(stitched_image)
    result = s.stitch(stitched_image,frameL,feature_to_match)
    result=trim(result)#trim black borders
    try:
        laneDetected = ld.detectLines(result)
        cv2.imshow('Video Player', laneDetected.astype(np.uint8))
        video_writer.write(laneDetected.astype(np.uint8))
    except:
        cv2.imshow('Video Player', result.astype(np.uint8))
        video_writer.write(result.astype(np.uint8))

    # Breaking out of the loop
    if cv2.waitKey(10) & 0xFF == ord('q'):
        capMain.release()
        capLeft.release()
        capRight.release()
        video_writer.release()
        break

# Close down everything
capMain.release()
capLeft.release()
capRight.release()
video_writer.release()
cv2.destroyAllWindows()

