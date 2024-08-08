import cv2 as cv
import mediapipe
import pyautogui

# landmarks on the face
faceMesh = mediapipe.solutions.face_mesh.FaceMesh(refine_landmarks=True)
fr = cv.VideoCapture(0);

screenWidth, screenHeight = pyautogui.size() 

while True:
    _,image = fr.read()
    # 1 for vertical flip and 0 for horizontal flip
    image = cv.flip(image, 1)

    windowHieght, windowWidth, _ = image.shape

    rgbImage = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    processImage= faceMesh.process(rgbImage)
    allFaces = processImage.multi_face_landmarks

    # print(allFaces)

    # if face exists thne only perform karo
    if allFaces:
        oneFacePoints = allFaces[0].landmark

        # jo single face liya hai uski values ko print karte jao
        # all the points are less than 1
        # 474 478 are the points for left and right eye

        # here we are tracking the right eye
        rightEye = [oneFacePoints[374], oneFacePoints[386]]
        for id, landMark in enumerate(rightEye):

            x = int(landMark.x * windowWidth);
            y = int(landMark.y * windowHieght);
            # stationary ke liye 320, 240 se upar hi aarhi hai saari values
            # print(x,y)

            # face is captured and eye is present
            if id ==1:
                # eye can move inside window hence fullScreen it
                # convert windowWidth to screenWidth 
                mouseX = int(screenWidth / windowWidth * x)
                mouseY = int(screenHeight / windowHieght * y)

                # print(mouseX, mouseY)
                pyautogui.moveTo(mouseX, mouseY)

            # now show points in the image
            # bgr format mei color
            cv.circle(image, (x,y), 2, (0,255,0)) 

        # if rightEye[0].y - rightEye[1].y <0.01:
        #     print("Right Eye Closed -> Mouse clicked")
        #     pyautogui.rightClick()
        #     pyautogui.sleep(1)  
        
        # here we are tracking the left eye
        # 145->bottom of leftEye
        # 159->top of leftEye

        leftEye = [oneFacePoints[145], oneFacePoints[159]]
        for landMark in leftEye:

            x = int(landMark.x * windowWidth);
            y = int(landMark.y * windowHieght);
            # stationary ke liye 320, 240 se upar hi aarhi hai saari values
            # print(x,y)

            # now show points in the image
            # bgr format mei color
            cv.circle(image, (x,y), 2, (0,0,255))

        # if leftEye[0].y - leftEye[1].y <0.01:
        #     print("Left Eye Closed -> Mouse clicked")
        #     pyautogui.click()
        #     pyautogui.sleep(1)

        rightEyeClosed = (rightEye[0].y - rightEye[1].y) < 0.01
        leftEyeClosed = (leftEye[0].y - leftEye[1].y) < 0.01

        if rightEyeClosed and leftEyeClosed:
            print("Both Eyes Closed -> Mouse clicked")
            pyautogui.scroll(-100)
            # pyautogui.sleep(1)
        
        elif rightEyeClosed:
            print("Right Eye Closed -> Mouse clicked")
            pyautogui.rightClick()
            pyautogui.sleep(1)

        elif leftEyeClosed:
            print("Left Eye Closed -> Mouse clicked")
            pyautogui.click()
            pyautogui.sleep(1)
              

    cv.imshow('image',image)
    exitKey = cv.waitKey(1)
    if exitKey == 27:
        break

fr.release()
cv.destroyAllWindows()