import cv2
import face_recognition as fr
import pickle
import os

knownSubfolder = 'demoImages\\known';
knownFolder = os.path.join(os.getcwd(), knownSubfolder);
knownFiles = [f for f in os.listdir(knownFolder) if os.path.isfile(os.path.join(knownFolder, f))]
knownEncodings = []
knownNames = []

for faceFile in knownFiles:
	faceName = os.path.splitext(faceFile)[0]
	print('Loading ', faceName)
	faceFile = os.path.join(knownFolder, faceFile)
	faceImage = fr.load_image_file(faceFile)
	print('Getting locations ', faceName)
	faceLocation = fr.face_locations(faceImage)[0]
	print('Encoding ', faceName)
	faceEncoding = fr.face_encodings(faceImage)[0]
	knownEncodings.append(faceEncoding)
	knownNames.append(faceName)
	print('Done ', faceName)

with open('training_data.pk1','wb') as file:
	pickle.dump(knownNames, file)
	pickle.dump(knownEncodings, file)



