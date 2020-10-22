import cv2
import numpy as np 

def contornos(nombre):
    cap = cv2.VideoCapture(nombre)
    font = cv2.FONT_HERSHEY_COMPLEX
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    if(cap.isOpened() == False):
        print("Error")
    
    
# Variables de inicialización del programa   
    lower = 0
    upper = 60
    p1 = 0
    p2 = 0
    p3 = 0
    pista = np.zeros(shape=(6,3))
    pistar = np.zeros(shape=(3,3))
    speed = np.zeros(shape=(3,9))
    data = np.zeros(shape=(3,3))
    maskp = np.zeros(shape=(int(height),int(width)))
    masko = maskp.astype(np.uint8)
    factor = [0.036413,0.04076,0.045109]
  
#Detección de pista y obtención de información necesaria
    while True:
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        count = 0
        #Detección de pistas por rango de colores
        while True:
            
            lower_blue = np.array([lower, 70, 50])
            upper_blue = np.array([upper,255,255])
            mask = cv2.inRange(hsv,lower_blue,upper_blue)
            mask[:,0:480] = 0
            mask[:,1440:1920] = 0
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    
            for cnt in contours:
               area = cv2.contourArea(cnt)
               approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
               x = approx.ravel()[0]
               y = approx.ravel()[1]
    
    
               if area > 60000:
                    f= cv2.boundingRect(cnt)
                    pista[count,0] = 1
                    pista[count,1] = f[1]+10
                    pista[count,2] = f[1]+f[3]-20
                    mask[0:f[1],:] = 0
                    mask[(f[1]+f[3]):1080,:] = 0
                    maskp = maskp + mask
                    
            lower = lower + 60
            upper = upper + 60
            count = count + 1     
    
            if count > 5:
                break
        
        break

#Compresión de la informcación de la pista    
    count = 0
    fila = 0
    while True:
        
        if pista[count,0] == 1:
            pistar[fila,:] = pista[count,:]
            fila = fila+1
            count = count + 1
        elif pista[count,0] == 0:
            count = count + 1
        if fila == 3:
            break
            
    
# Detección de las objetos e información de posición   
    print(count)
    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        count = 0
        #Mascaras de segmentación de objetos
        while True:
            if pista[count,0] == 1:
                if count == 0:
                    lower = 60
                    upper = 360
                    lower_blue = np.array([lower, 0, 0])
                    upper_blue = np.array([upper,255,255])
                    mask = cv2.inRange(hsv,lower_blue,upper_blue)
                    mask[:,0:480] = 0
                    mask[:,1440:1920] = 0
                elif count == 5:
                    lower = 0
                    upper = 300
                    lower_blue = np.array([lower, 0, 0])
                    upper_blue = np.array([upper,255,255])
                    mask = cv2.inRange(hsv,lower_blue,upper_blue)
                    mask[:,0:480] = 0
                    mask[:,1440:1920] = 0
                else:
                    upper = 60*count
                    lower = 60*(count+1)
                    lower_alt = np.array([0, 0, 0])
                    upper_alt = np.array([360,255,255])
                    lower_blue = np.array([lower, 0, 0])
                    upper_blue = np.array([upper,255,255])
                    mask1 = cv2.inRange(hsv,lower_alt,upper_blue)
                    mask2 = cv2.inRange(hsv,lower_blue,upper_alt)
                    mask = mask1 + mask2
                    mask[:,0:420] = 0
                    mask[:,1500:1920] = 0
            
                limitupper = int(pista[count,1])
                limitlower = int(pista[count,2])
                mask[0:limitupper,:] = 0
                mask[limitlower:1080,:] = 0
                masko = masko + mask    
            count = count + 1
            if count == 5:
                break
    
    
        contours, _ = cv2.findContours(masko, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
        #Detección de objeto y ubicación de pistas
        for cnt in contours:
            area = cv2.contourArea(cnt)
            approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
            x = approx.ravel()[0]
            y = approx.ravel()[1]
    
    
            if area > 4000 and area < 13000:
                cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
                M = cv2.moments(cnt)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                if pistar[0,1] < cY < pistar[0,2]:
                    speed[0,0] = 1
                    if 970 < cX < 1010:
                        speed[0,1] = 1
                        if p1 < 5:
                            speed[1,2+p1] = cX
                            p1 = p1 + 1
                elif pistar[1,1] < cY < pistar[1,2]:
                    speed[1,0] = 1
                    if 970 < cX < 1010:
                        speed[1,1] = 1
                        if p2 < 5:
                            speed[1,2+p2] = cX
                            p2 = p2 + 1
                elif pistar[2,1] < cY < pistar[2,2]:
                    speed[2,0] = 1
                    if 970 < cX < 1010:
                        speed[2,1] = 1
                        if p3 < 5:
                            speed[2,2+p3] = cX
                            p3 = p3 + 1        
    
                
                
                if len(approx) > 4 and len(approx) < 8:
                    cv2.putText(frame, "Pista", (x, y), font, 1, (0, 0, 0))
        
        cv2.imshow("Frame",frame)
        cv2.imshow("Mask", masko)
        cv2.imshow("Pista", maskp)
        masko[:,:] = 0


#Calculo de la velocidad y dirección    
    count = 0
    while True:
        col = 0
        print(1)
        if speed[count,0] == 1:
            while True:
                if speed[count,7] == 0:
                    speed[count,7] = speed[count,2+col]-speed[count,3+col]
                else:
                    speed[count,7] = (speed[count,7]+speed[count,2+col]-speed[count,3+col])/2
                col = col+1
                if col < 4:
                    if speed[count,7] < 0:
                        speed[count,7]=speed[count,7]*-1
                        speed[count,7] = speed[count,7]*factor[count]/0.033123
                        speed[count,8]=1
                    break
        count = count + 1
        if count > 2:
            break
        
        
#Empaquetado de informacion
    data [:,0] = speed[:,0]
    data [:,1] = speed[:,7]
    data [:,2] = speed[:,8]
    

        
    cap.release()
    cv2.destroyAllWindows()
    return data


