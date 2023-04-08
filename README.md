<h1>
Installation
</h1>
Clone the repository: 	
	
	git clone https://github.com/HarunSMetin/Lane-Detection-from-Stitched-Videos.git
	
Navigate to the project directory: 	

	cd Lane-Detection-from-Stitched-Videos
	
Install dependencies: 

	pip install -r requirements.txt
	
Download the pre-trained model: 

	python download_model.py

Note: This application requires Python 3.6 or higher and OpenCV 4.0 or higher to be installed on your machine.

<h1>Usage</h1>

Once you have installed the dependencies and downloaded the pre-trained model, you can run the application by executing the following command:

	python lane_detection.py --video <path_to_video_file>

Replace <path_to_video_file> with the path to the stitched video file you want to process. The application will process the video and display the lane detection results in real-time.

You can also adjust the parameters of the lane detection algorithm by modifying the values in the config.py file.

<h3>stitcher.py:</h3>

This Python code performs the stitching process.
You should create an object of the class in the following way:

	obj = stitcher.StitchWithSift(mode=1)

	mode = 1: saves the outputs to the OUT folder and prints to the console
	mode = 0: no output will be saved or displayed (except the result)

	result = obj.stitch(mainPhoto, queryphoto, matchMode='bf') #or matchMode='knn'

	result: the stitched version of the main and query images.
	
<h3>video_slicer.py:</h3>

Divides a video into 3 different videos, left, center, and right.

	video_slicer(filePath='test/4/', fileName='test/4/test3.mp4')
	
Divides the test3.mp4 video into left.mp4, main.mp4, and right.mp4.
	
<h3>lane_detection.py:</h3> 

Code that detects lane markings.

	output = detectLines(image)
	output: the image with detected lane markings.
