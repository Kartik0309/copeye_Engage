from deepface import DeepFace as DF
import cv2
import numpy as np
haar=cv2.CascadeClassifier('static\haarcascade_frontalface_alt.xml')
import os
def test():
    vid=cv2.VideoCapture(0)
    nframe=0
    while True:
        val,frame=vid.read()
        if not val:
            continue
        faces=haar.detectMultiScale(frame,1.3,5)
        nframe+=1
        for x,y,w,h in faces:
            face=frame[y:y+h,x:x+w]
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
            face=np.array(face)
            for i in os.listdir('static/uploads/auth'):
                df=DF.verify(img1_path=face,img2_path=os.path.join('static/uploads/auth',i),enforce_detection=True,model_name='Dlib')
                if df['verified']:
                    print(df)
        cv2.imshow('frame',frame)
        if nframe>=25:
            break           
        if cv2.waitKey(50)==27:
            break
    cv2.destroyAllWindows()
    vid.release()


if __name__=='__main__':
    test()