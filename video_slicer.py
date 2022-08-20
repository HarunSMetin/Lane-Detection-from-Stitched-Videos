import cv2
def sliceStart(filePath='test/4/',fileName= 'test/4/test3.mp4'):
    fullPath=filePath+fileName
    cap = cv2.VideoCapture(fullPath)

    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter("{}left.mp4".format(filePath), fourcc, fps, (round(width*0.4), height)) 
        
    for frame_idx in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
        ret, frame = cap.read()
        video_writer.write(frame[:,:round(width*0.4)])

        if cv2.waitKey(10) & 0xFF == ord('q'):
            video_writer.release()
            cap.release()
            break

    cap.release()
    video_writer.release()
    print("Left Cut Finished!")

    cap = cv2.VideoCapture(fullPath)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter("{}main.mp4".format(filePath), fourcc, fps, (round(width*0.4), height)) 
    for frame_idx in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
        
        # Read frame 
        ret, frame = cap.read()
        video_writer.write(frame[:,round(width*0.3):round(width*0.7)])

        if cv2.waitKey(10) & 0xFF == ord('q'):
            video_writer.release()
            cap.release()
            break

    cap.release()
    video_writer.release()
    print("Main Cut Finished!")

    cap = cv2.VideoCapture(fullPath)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter("{}right.mp4".format(filePath), fourcc, fps, (round(width*0.5),height)) 
    for frame_idx in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
        
        # Read frame 
        ret, frame = cap.read()
        video_writer.write(frame[:,round(width*0.5):width])

        if cv2.waitKey(10) & 0xFF == ord('q'):
            video_writer.release()
            cap.release()
            break

    cap.release()
    video_writer.release()
    print("Right Cut Finished!")
