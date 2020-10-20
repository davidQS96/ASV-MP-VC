

def contornos(cap):
    while True:
        ret, frame = cap.read()
        blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([38, 86, 0])
        upper_blue = np.array([121,255,255])
        mask = cv2.inRange(hsv,lower_blue,upper_blue)
    
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
        for cnt in contours:
            area = cv2.contourArea(cnt)
            approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
            x = approx.ravel()[0]
            y = approx.ravel()[1]

            if area > 400:
                cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
    
    
        cv2.imshow("Frame",frame)
        cv2.imshow("Mask", mask)
        key = cv2.waitKey(1)
        if key == 27:
            break
    

        
    cap.release()
    cv2.destroyAllWindows()