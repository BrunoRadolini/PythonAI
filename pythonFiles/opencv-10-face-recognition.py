import cv2
import face_recognition as FR

font = cv2.FONT_HERSHEY_SIMPLEX

donFace = FR.load_image_file('D:/Source/Python/demoImages/known/Donald Trump.jpg')
donFaceLoc = FR.face_locations(donFace)[0]
donFaceEncode = FR.face_encodings(donFace)[0]

nancyFace = FR.load_image_file('D:/Source/Python/demoImages/known/Nancy Pelosi.jpg')
nancyFaceLoc = FR.face_locations(nancyFace)[0]
nancyFaceEncode = FR.face_encodings(nancyFace)[0]

penceFace = FR.load_image_file('D:/Source/Python/demoImages/known/Mike Pence.jpg')
penceFaceLoc = FR.face_locations(penceFace)[0]
penceFaceEncode = FR.face_encodings(penceFace)[0]

knownEncodings = [donFaceEncode, nancyFaceEncode, penceFaceEncode]
names = ['Donald Trump', 'Nancy Pelosi', 'Mike Pence']

unknownFace = FR.load_image_file('D:/Source/Python/demoImages/unknown/u5.jpg')
unknownFaceBGR = cv2.cvtColor(unknownFace, cv2.COLOR_RGB2BGR)
unknownFaceLocations = FR.face_locations(unknownFace)

unknownFaceEncodings = FR.face_encodings(unknownFace, unknownFaceLocations)

for faceLocation, unknownFaceEncoding in zip(unknownFaceLocations, unknownFaceEncodings):
	top, right, bottom, left = faceLocation
	print(faceLocation)
	cv2.rectangle(unknownFaceBGR, (left, top), (right,bottom), (0,255,255), 2)
	name = 'Unknown person'
	matches = FR.compare_faces(knownEncodings, unknownFaceEncoding)
	print('matches', matches)
	if True in matches:
		matchIndex = matches.index(True)
		name = names[matchIndex];
		print('Matched', name)

	cv2.putText(unknownFaceBGR, name, (left + 3,top - 5), font, 1, (0,255,255),2)


cv2.imshow('Recognise', unknownFaceBGR)
cv2.waitKey(5000)