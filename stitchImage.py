import cv2
import stitcher
import numpy as np 

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

feature_to_match = 'knn'

main_photo = cv2.imread('test/3/main.jpg')
query_photo = cv2.imread('test/3/left.jpg')
query2_photo = cv2.imread('test/3/right.jpg')


s = stitcher.StitchWithSift(1)
stitched_image = s.stitch(main_photo,query_photo,feature_to_match)
result = s.stitch(query2_photo,stitched_image,feature_to_match)

result=trim(result)#trim black borders

cv2.imshow("Result", result)
cv2.waitKey(0)
cv2.imwrite("OUT/FinaL_result.jpg",result)
