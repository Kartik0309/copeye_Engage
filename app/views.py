from flask import render_template,request,redirect,session,abort
from flask_session import Session
from deepface import DeepFace as DF
import cv2
import os
import pandas as pd
from PIL import Image as im
import numpy as np
from mask_detection import detect_mask_video
from flask_mysqldb import MySQL
from datetime import datetime

haar=cv2.CascadeClassifier('static\haarcascade_frontalface_alt.xml')
FOLDER='static/uploads/citizen'
FOLDER1='static/uploads/criminal'
FOLDER2='static/uploads/auth'
FOLDER3='static/uploads/temp'
mysql=MySQL()

def citizen():
    message=""
    if request.method == 'POST':
        temp=None
        try:
            print("Hello")
            name=request.form['name']
            age=request.form['age']
            address=request.form['address']
            image=request.files['photo']
            temp=image.filename
            image.save(os.path.join(FOLDER3,image.filename))
            image=cv2.imread(os.path.join(FOLDER3,image.filename))
            faces=haar.detectMultiScale(image,1.3,5)
            if len(faces)>1:
                message="Multiple Faces Detected"
                raise Exception("Multiple Faces")
            if len(faces)<1:
                message="No Face Detected"
                raise Exception("No Face")
            for x,y,w,h in faces:
                image=image[y:y+w,x:x+h]
                image = im.fromarray(image)
            cur=mysql.connection.cursor()
            cur.execute("INSERT INTO citizen(name,age,address) values ('{}','{}','{}');".format(name,age,address))
            cur.execute("SELECT cid from citizen where name='{}' and age='{}' and address='{}'".format(name,age,address))
            val=cur.fetchone()[0]
            cur.close()
            val=str(val)
            path=os.path.join(FOLDER,val)+'.jpg'
            image.save(path)
            os.remove(os.path.join(FOLDER3,temp))
            mysql.connection.commit()
            message="Citizen Added Successfully!"
        except:
            os.remove(os.path.join(FOLDER3,temp))
            mysql.connection.rollback()
            message="Citizen Not Added!"
    return render_template('citizen.html',message=message)




def signup():
    message=""
    if request.method=='POST':
        try:
            filename=request.form['name']
            filename_email=request.form['email']
            cur=mysql.connection.cursor()
            print("Hello1")
            cur.execute("INSERT INTO users(username,email) values ('{}','{}');".format(filename,filename_email))
            cur.execute("Select * from users where email='{}';".format(filename_email))
            uid=cur.fetchone()
            uid=str(uid[2])
            cur.close()
            path=os.path.join(FOLDER2,uid)+'.jpg'
            vid=cv2.VideoCapture(0)
            while True:
                val,frame=vid.read()
                if not val:
                    continue
                cv2.imshow('frame',frame)
                faces=haar.detectMultiScale(frame,1.3,5)
                for x,y,w,h in faces:
                    face=frame[y:y+h,x:x+w]
                    #face=np.array(face)
                    face = im.fromarray(face)
                    print("Hello2")
                    face.save(path)
                    mysql.connection.commit()
                    session['name']=filename
                    return render_template('index.html')
            raise Exception('Could not Signup')
        except:
            message="Could not signup"
            mysql.connection.rollback()
            return render_template('login.html',message=message)   
    return render_template('signup.html')


def login():
    message=""
    if request.method == 'POST':
        try:
            if len(session)!=0:
                return redirect('index')
            vid=cv2.VideoCapture(0)
            found=set()
            nframe=0
            while True:
                val,frame=vid.read()
                if not val:
                    continue
                cv2.imshow('frame',frame)
                faces=haar.detectMultiScale(frame,1.3,5)
                nframe+=1
                for x,y,w,h in faces:
                    face=frame[y:y+h,x:x+w]
                    face=np.array(face)
                    for i in os.listdir('static/uploads/auth'):
                        df=DF.verify(img1_path=face,img2_path=os.path.join('static/uploads/auth',i),enforce_detection=False,model_name='Dlib')
                        if df['verified']:
                            found.add(i.split('.')[0])
                            cur=mysql.connection.cursor()
                            cur.execute("select * from users where uid='{}';".format(next(iter(found))))
                            session['name'] = cur.fetchone()[0]
                            cur.close()
                            return render_template('index.html') 
                if nframe>=15:
                    break           
                if cv2.waitKey(50)==27:
                    break
            cv2.destroyAllWindows()
            vid.release()
            raise Exception("Failed")
            return render_template('login.html',message=message)
        except:
            message="Login Failed!! Please try again or Signup"
    if len(session)!=0:
        session.pop('name')
    return render_template('login.html',message=message)


def index():
    return render_template('index.html')

def find_criminal():
    if request.method == 'GET':
        return abort(404)
    vid=cv2.VideoCapture(0)
    found=list(dict())
    nframe=0
    while True:
        val,frame=vid.read()
        if not val:
            continue
        cv2.imshow('frame',frame)
        faces=haar.detectMultiScale(frame,1.3,5)
        nframe+=1
        for x,y,w,h in faces:
            face=frame[y:y+h,x:x+w]
            face=np.array(face)
            for i in os.listdir('static/uploads/criminal'):
                df=DF.verify(img1_path=face,img2_path=os.path.join('static/uploads/criminal',i),enforce_detection=False,model_name='Dlib')
                if df['verified']:
                    now = datetime.now()
                    temp={'id':i.split('.')[0],'time':now}
                    if len(found)==0 or found[-1]['id']!=temp['id']:
                        found.append(temp)
        if nframe>=25:
            break           
        if cv2.waitKey(50)==27:
            break
    cv2.destroyAllWindows()
    vid.release()
    cur=mysql.connection.cursor()
    for x in found:
        cur.execute("select name from criminal where caseid='{}';".format(x['id']))
        x['name']=cur.fetchone()[0]
    cur.close()
    return render_template('criminal.html',found=found)

def criminal():
    message=""
    if request.method=='POST':
        f=request.files['upload']
        filename=request.form['upload-name']
        caseid=request.form['upload-caseid']
        filename_new=filename.split(' ')
        filename_new='_'.join(filename_new)
        cur=mysql.connection.cursor()
        cur.execute("insert into criminal(name,caseid) values ('{}','{}');".format(filename,caseid))
        path=os.path.join(FOLDER1,caseid)+'.jpg'
        f.save(path)
        cur.close()
        mysql.connection.commit()
        message="Criminal Added Successfully!!"  
        return render_template('criminal.html',message=message)   
    return render_template('criminal.html',message=message)

def facemask():
    found=None
    if request.method == 'POST':
        found=detect_mask_video.mask_detect()
    return render_template('facemask.html',found=found)

def find_lost():
    if request.method == 'GET':
        return abort(404)
    vid=cv2.VideoCapture(0)
    found=list(dict())
    nframe=0
    cur=mysql.connection.cursor()
    cur.execute("SELECT cid from citizen where lost=1;")
    var=list(cur.fetchall())
    while True:
        val,frame=vid.read()
        if not val:
            continue
        cv2.imshow('frame',frame)
        faces=haar.detectMultiScale(frame,1.3,5)
        nframe+=1
        for x,y,w,h in faces:
            face=frame[y:y+h,x:x+w]
            face=np.array(face)
            for i in var:
                j=str(i[0])
                df=DF.verify(img1_path=face,img2_path=os.path.join('static/uploads/citizen',j)+'.jpg',enforce_detection=False,model_name='Dlib')
                if df['verified']:
                    cur.execute("update citizen set lost=0 where cid='{}';".format(j))
                    cur.execute("Select * from citizen where cid='{}';".format(j))
                    cnt=cur.fetchone()
                    temp={'id':cnt[0],'name':cnt[1],'age':cnt[2],'address':cnt[3]}
                    if len(found)==0 or found[-1]['id']!=temp['id']:
                        found.append(temp)
        if nframe>=25:
            break           
        if cv2.waitKey(50)==27:
            break
    cur.close()
    mysql.connection.commit()
    cv2.destroyAllWindows()
    vid.release()
    return render_template('lost_found.html',found=found)

def lost_found():
    if request.method=='POST':
        f=request.files['upload']
        filename=request.form['upload-name']
        filename_new=filename.split(' ')
        filename_new='_'.join(filename_new)
        path=os.path.join(FOLDER3,filename_new)+'.jpg'
        f.save(path)
        img=cv2.imread(path)
        faces=haar.detectMultiScale(img,1.3,5)
        for x,y,w,h in faces:
            face=img[y:y+h,x:x+w]
            face=np.array(face)
            cur=mysql.connection.cursor()
            for i in os.listdir('static/uploads/citizen'):
                df=DF.verify(img1_path=face,img2_path=os.path.join('static/uploads/citizen',i),enforce_detection=False,model_name='Dlib')
                first=i.split('.')[0]
                if df['verified']:
                    cur.execute("update citizen set lost=1 where cid='{}';".format(first))
            cur.close()
            mysql.connection.commit()
        return render_template('lost_found.html',val=True,path=path,found=None)   
    return render_template('lost_found.html',val=False,path=None,found=None)