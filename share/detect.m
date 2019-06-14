% 파일에서 첫 프레임 불러오기
%v = FlirMovieReader('faceRecognitionA8300sc-000003.ats')
frame = imread('output2.jpg');
frame1 = im2double(frame);
frame2 = imadjust(frame1);

% 첫 프레임에서 얼굴 detection
faceDetector = vision.CascadeObjectDetector;
bbox = step(faceDetector, frame2);
dispFrame = insertObjectAnnotation(frame2, 'rectangle', bbox, 'face');
figure, imshow(dispFrame)
