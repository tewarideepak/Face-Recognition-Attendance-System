from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
import csv
import cv2
import os
import numpy as np


class Face_Recognition:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")


        title_lbl=Label(self.root,text="FACE RECOGNITION",font=("times new roman",35,"bold"),bg="white",fg="green")
        title_lbl.place(x=0,y=0,width=1530,height=45)

        # 1st image

        img_top=Image.open(r"college_images\tonyy.jpg")
        img_top=img_top.resize((650,700),Image.ANTIALIAS)
        self.photoimg_top=ImageTk.PhotoImage(img_top)

        f_lbl=Label(self.root,image=self.photoimg_top)
        f_lbl.place(x=0,y=55,width=650,height=700)

        # 2nd image

        img_bottom=Image.open(r"college_images\rec.jpeg")
        img_bottom=img_bottom.resize((950,700),Image.ANTIALIAS)
        self.photoimg_bottom=ImageTk.PhotoImage(img_bottom)

        f_lbl=Label(self.root,image=self.photoimg_bottom)
        f_lbl.place(x=650,y=55,width=950,height=700)

        # Button

        b1_1=Button(f_lbl,text="Face Recognition",command=self.face_recog,cursor="hand2",font=("times new roman",18,"bold"),bg="darkgreen",fg="white")
        b1_1.place(x=400,y=640,width=200,height=40)



    # # ======== Attendance ==========

    def mark_attendance(self, i, r, n, d):
        with open("DPD.csv", "r+", newline="\n") as f:
            myDataList = f.readlines()
            name_set = set()
            for line in myDataList:
                entry = line.split(",")
                name_set.add(entry[0])

            if i not in name_set and r not in name_set and n not in name_set and d not in name_set:
                now = datetime.now()
                date_string = now.strftime("%d/%m/%Y")
                time_string = now.strftime("%H:%M:%S")
                f.writelines(f"\n{i},{r},{n},{d},{date_string},{time_string},Present")


    # ========= Face recognition ==========

    def face_recog(self):
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf, student_details):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

            coord = []

            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
                id, predict = clf.predict(gray_image[y:y+h, x:x+w])
                confidence = int((100*(1-predict/300)))

                student_id = str(id)
                if student_id in student_details:
                    n, r, d = student_details[student_id]
                    n = "".join(n)
                    r = "".join(r)
                    d = "".join(d)

                    if confidence > 77:
                        cv2.putText(img, f"Roll: {r}", (x, y-55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 128, 0), 3)
                        cv2.putText(img, f"Name: {n}", (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 128, 0), 3)
                        cv2.putText(img, f"Department: {d}", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 128, 0), 3)
                        self.mark_attendance(student_id, r, n, d)
                    else:
                        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
                        cv2.putText(img, "Unknown Face", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 3)

                    coord = [x, y, w, h]

            return coord

        def recognize(img, clf, faceCascade, student_details):
            coord = draw_boundary(img, faceCascade, 1.1, 10, (255, 25, 255), "Face", clf, student_details)
            return img

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        conn = mysql.connector.connect(host="localhost", username="root", password="Tris@12345", database="face_recognizer")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT Student_id, Name, Roll, Dep FROM student")
        student_data = my_cursor.fetchall()

        student_details = {}
        for data in student_data:
            student_details[str(data[0])] = data[1:]

        video_cap = cv2.VideoCapture(0)

        while True:
            ret, img = video_cap.read()
            img = recognize(img, clf, faceCascade, student_details)
            cv2.imshow("Welcome to Face Recognition", img)

            if cv2.waitKey(1) == 13:
                break

        video_cap.release()
        cv2.destroyAllWindows()





    # # ========= Face recognition ==========
    
    # def face_recog(self):
    #     def draw_boundary(img,classifier,scaleFactor,minNeighbors,color,text,clf):
    #         gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #         features=classifier.detectMultiScale(gray_image,scaleFactor,minNeighbors)

    #         coord=[]

    #         for (x,y,w,h) in features:
    #             cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
    #             id,predict=clf.predict(gray_image[y:y+h,x:x+w])
    #             confidence=int((100*(1-predict/300)))

    #             conn=mysql.connector.connect(host="localhost",username="root",password="Tris@12345",database="face_recognizer")
    #             my_cursor=conn.cursor()

    #             my_cursor.execute("SELECT Student_id FROM student WHERE Student_id ="+str(id))
    #             i=my_cursor.fetchone()
    #             i="+".join(i)

    #             my_cursor.execute("SELECT Name FROM student WHERE Student_id ="+str(id))
    #             n=my_cursor.fetchone()
    #             n="+".join(n)

    #             my_cursor.execute("SELECT Roll FROM student WHERE Student_id ="+str(id))
    #             r=my_cursor.fetchone()
    #             r="+".join(r)

    #             my_cursor.execute("SELECT Dep FROM student WHERE Student_id ="+str(id))
    #             d=my_cursor.fetchone()
    #             d="+".join(d)

    #             if confidence > 77:
    #                 cv2.putText(img, f"ID: {i}", (x, y-75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0,128,0), 3)
    #                 cv2.putText(img,f"Roll:{r}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,128,0),3)
    #                 cv2.putText(img,f"Name:{n}",(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,128,0),3)
    #                 cv2.putText(img,f"Department:{d}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,128,0),3)
    #                 self.mark_attendance(i,r,n,d)
    #             else:
    #                 cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
    #                 cv2.putText(img,"Unknown Face",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,0,255),3)

    #             coord=[x,y,w,h]

    #         return coord
        
    #     def recognize(img,clf,faceCascade):
    #         coord=draw_boundary(img,faceCascade,1.1,10,(255,25,255),"Face",clf)
    #         return img
        
    #     faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    #     clf=cv2.face.LBPHFaceRecognizer_create()
    #     clf.read("classifier.xml")

    #     video_cap=cv2.VideoCapture(0)

    #     while True:
    #         ret,img=video_cap.read()
    #         img=recognize(img,clf,faceCascade)
    #         cv2.imshow("Welcome to Face Recognition",img)
            
    #         if cv2.waitKey(1)==13:
    #             break
    #     video_cap.release()
    #     cv2.destroyAllWindows()





if __name__=="__main__":
    root=Tk()
    obj=Face_Recognition(root)
    root.mainloop()