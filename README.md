stitcher.py : 


	Stitch işlemini yapan python kod.
	obj = stitcher.StitchWithSift( mode = 1 ) 
	şeklinde içindeki classın bir objesini oluşturmalısınız
	
	mode = 1 : çıktıları OUT klasörüne kaydet, Consola print et
	mode = 0 : herhangi bir çıktı kaydedilmeyecek ve gösterilmeyecek(Sonuç hariç) 
	
	result = obj.stitch(mainPhoto,queryphoto,matchMode='bf') #ya da matchMode='knn'
	
	result : main ve query image'ı stitch edilmiş halidir.

video_slicer.py:


	Bir videoyu 3 farklı videoya böler. sol,orta,sağ şeklinde.
	video_slicer(filePath='test/4/',fileName= 'test/4/test3.mp4')
	test3.mp4 videosunu left.mp4, main.mp4, right.mp4 şeklinde ayırır

lane_detection.py:


	Şerit tespiti yapan kod.
	output = detectLines(image) 
	output : şeritleri tespit edilmiş resimdir.
	
