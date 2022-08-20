import cv2
import numpy as np
import matplotlib.pyplot as plt
import imageio
def find_key_points(main_photo_gray,query_photo_gray,printMode):
        descriptor = cv2.SIFT_create()
        keypoints_main_img, features_main_img = descriptor.detectAndCompute(main_photo_gray, None)
        keypoints_query_img, features_query_img = descriptor.detectAndCompute(query_photo_gray, None)
        if(printMode):
                print("Query Image Number of KeyPoints",len(keypoints_query_img))
                print("Query Image Shape of Features:",features_query_img.shape)
                """
                for keypoint in keypoints_query_img:
                        x,y = keypoint.pt
                        size = keypoint.size 
                        orientation = keypoint.angle
                        response = keypoint.response 
                        octave = keypoint.octave
                        class_id = keypoint.class_id
                        print("X:",x," Y:",y)
                        print("Size",size)
                        print("Angle:",orientation)
                        print("response:",response)
                        print("octave:",octave)
                        print("class_id:",class_id)
                """
                # keypoints and features detected on both images

                fig, (ax1,ax2) = plt.subplots(nrows=1, ncols=2, figsize=(15,8), constrained_layout=False)
                plt.title("Sift Features")
                ax1.imshow(cv2.drawKeypoints(main_photo_gray, keypoints_main_img, None, color=(0,255,0)))
                ax1.set_xlabel("(Main Photo)")

                ax2.imshow(cv2.drawKeypoints(query_photo_gray,keypoints_query_img,None,color=(0,255,0)))
                ax2.set_xlabel("(Query Photo)")

                plt.savefig("OUT/Sift_features.jpeg")
        return (keypoints_main_img, features_main_img ,keypoints_query_img, features_query_img)

def matching_keys_BF(features_main_img, features_query_img,printMode):
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
        best_matches = bf.match(features_main_img,features_query_img)
        rawMatches = sorted(best_matches, key = lambda x:x.distance)
        if(printMode):
                print("Raw matches (Brute force):", len(rawMatches))
        return rawMatches

def matching_keys_KNN(features_main_img, features_query_img, ratio,printMode):
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
        rawMatches = bf.knnMatch(features_main_img, features_query_img, k=2)
        if(printMode):
                print("Raw matches (KNN):", len(rawMatches))
        matches = []

        for m,n in rawMatches:
            if m.distance < n.distance * ratio:
                matches.append(m)
        return matches

def match_features(main_photo,keypoints_main_img,features_main_img,query_photo,keypoints_query_img,features_query_img,mode,printMode):
        if(printMode): 
                print(mode,"matched features Lines")

        fig = plt.figure(figsize=(20,8))

        if mode == 'bf':
                matches = matching_keys_BF(features_main_img, features_query_img,printMode=printMode)
                mapped_features_image = cv2.drawMatches(main_photo,keypoints_main_img,query_photo,keypoints_query_img,matches[:100],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        elif mode == 'knn':
                matches = matching_keys_KNN(features_main_img, features_query_img, ratio=0.75,printMode=printMode)
                mapped_features_image = cv2.drawMatches(main_photo, keypoints_main_img, query_photo, keypoints_query_img, np.random.choice(matches,100),None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        
        if(printMode):        
                plt.title("Mapped Features with {}".format(mode))
                plt.imshow(mapped_features_image)
                plt.axis('off')
                plt.savefig( "OUT/"+mode + "_matching.jpeg")
        return matches

def homography_stitching(keypoints_main_img, keypoints_query_img, matches, reprojThresh):

        keypoints_main_img = np.float32([kp.pt for kp in keypoints_main_img])
        keypoints_query_img = np.float32([kp.pt for kp in keypoints_query_img])
        
        if len(matches) > 4:
            points_main = np.float32([keypoints_main_img[m.queryIdx] for m in matches])
            points_query = np.float32([keypoints_query_img[m.trainIdx] for m in matches])
            (H, status) = cv2.findHomography(points_main, points_query, cv2.RANSAC, reprojThresh)

            return (matches, H, status)
        else:
            return None

class StitchWithSift:

    def __init__(self,mode=1) :
        self.matchMode='bf'
        self.mode=mode     

    def stitch(self,main_photo,query_photo,matchMode='bf'):
        self.matchMode=matchMode
        self.main_photo = cv2.cvtColor(main_photo,cv2.COLOR_BGR2RGB)
        self.main_photo_gray = cv2.cvtColor( self.main_photo, cv2.COLOR_RGB2GRAY)
        self.query_photo = cv2.cvtColor(query_photo,cv2.COLOR_BGR2RGB)
        self.query_photo_gray = cv2.cvtColor(self.query_photo , cv2.COLOR_RGB2GRAY)
        
        keypoints_main_img, features_main_img ,keypoints_query_img, features_query_img = find_key_points(self.main_photo_gray,self.query_photo_gray,printMode=self.mode)   
        features_matchings=match_features( self.main_photo,keypoints_main_img,features_main_img,self.query_photo,keypoints_query_img,features_query_img,matchMode,printMode=self.mode)
        
        M = homography_stitching(keypoints_main_img, keypoints_query_img, features_matchings, reprojThresh=4)
        
        if M is None:
            print("Error!")

        (matches, Homography_Matrix, status) = M
        if(self.mode):
                print("Homography_Matrix:\n",Homography_Matrix)

        width = self.query_photo.shape[1] + self.main_photo.shape[1]
        height = min(self.query_photo.shape[0], self.main_photo.shape[0])
        if(self.mode):
                print("Width :", width, "\nHeight :",height ) 

        result = cv2.warpPerspective(self.main_photo, Homography_Matrix,  (width, height))

        result[0:height, 0:self.query_photo.shape[1]] = self.query_photo[0:height,:]
        result = cv2.cvtColor(result,cv2.COLOR_RGB2BGR)
        if(self.mode):
                cv2.imwrite("OUT/result_without_trim.jpg",result)

        return result