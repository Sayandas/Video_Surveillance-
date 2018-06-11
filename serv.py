import cv2
import time
import math
import datetime
import numpy as np
from PIL import ImageTk,Image

from tkinter import*

root = Tk()
root.geometry("1600x800+0+0")
root.title("V I D E O   S U R V E I L L A N C E")

def secs_diff(endTime, begTime):
    diff = (endTime - begTime).total_seconds()
    return diff


def get_speed(pixels, ftperpixel, secs):
    if secs > 0.0:
        return ((pixels * ftperpixel) / secs) * 0.681818
    else:
        return 0.0


def vid():
    car = cv2.CascadeClassifier("cars.xml")
    print('jdkk')
    cap = cv2.VideoCapture("car.mp4")
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    # ty = cv2.BackgroundSubtractorMOG2()
    initial_time = datetime.datetime.now()
    c = 0
    b = []
    v = 0
    FOV = 53.5
    DISTANCE = 76
    IMAGEWIDTH = 640
    mph=0
    frame_width_ft = 2 * (math.tan(math.radians(FOV * 0.5)) * DISTANCE)
    ftperpixel = frame_width_ft / float(IMAGEWIDTH)


    for i in range(0, 1000000, +1):
        new = []
        for j in range(0, 2):
            new.append(0)
        b.append(new)
    u=0
    while True:

        ret, img = cap.read()
        initial_time = datetime.datetime.now()
        ##    print timestamp
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        fe = car.detectMultiScale(gray, 1.1, 5)
        ##  cv2.line(img,(400,100),(1000,100),(200,200,0),2)
        ##  cv2.rectangle(img,(300,100),(1200,300),(0,255,0),3)
        c = 0
        v += 1
        u+=1
        for (x, y, w, h) in fe:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 4)
            timestamp = datetime.datetime.now()
            secs = secs_diff(timestamp, initial_time)
            x1 = w / 2
            y1 = h / 2
            cx = x + int(x1)
            cy = y + int(y1)
            centroid = (cx, cy)
            ##        print cy
            if (int(cy) > b[c][1]):
                diff = cy - b[c][1]
            mph = get_speed(diff, ftperpixel, secs)
            mph *= 100
            if (mph > 1000):
                mph /= 100
            elif (mph > 100):
                mph /= 10
            mph = int(mph)
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (cx, cy)
            fontScale = 1
            fontColor = (255, 255, 0)
            lineType = 2

            cv2.putText(img, str(mph) + 'km/h',bottomLeftCornerOfText,font,fontScale,fontColor,lineType,cv2.LINE_AA)
            cv2.imshow('Video', img)

            ##        print (mph/1000) , 'KM'
            ##        print '--'

            ##        if(centroid!=(0,0)):
            ##            b[c][0]=int(centroid[0])
            ##            b[c][1]=int(centroid[1])
            ##            print b[c][0],b[c][1]
            b[c][0] = int(centroid[0])
            b[c][1] = int(centroid[1])
            c += 1

        ##    print c
        ##    print ' '

        # cv2.imshow('Video',img)
        k = cv2.waitKey(33)
        if(u<=299):
            print(u)
        else:
            break
        if (k == 27):
            break

    cap.release()
    cv2.destroyAllWindows()




topframe=Frame(root, width=1600, height = 50  )
topframe.pack()

lbl1=Label(topframe,font=('arial',50,'bold'),bg="purple",text="V I D E O    S U R V E I L L A N C E", fg= "white",bd=10,anchor='w').pack()

f3=Frame(root,width=400,height =20).pack()

f1=Frame(root,width=400,height =20).pack()
localtime=str(datetime.date.today())
Label(f1 ,font=('arial',20,'bold'), text='D A T E : ' + localtime ).pack() #lebel which  is showed

f4=Frame(root,width=400,height =80).pack()

f2=Frame(root,width=450,height =2).pack()
msg1=" 1) Click the 'OPEN CAMERA' button to open camera "
msg2=" 2) Press 'Esc' Button to close camera "
msg3=" 3) Clik on 'QUIT' to exit "
Label(f2,font=('arial',20,'bold'),text=msg1,fg="blue").pack()
Label(f2,font=('arial',20,'bold'),text=msg2,fg="blue").pack()
Label(f2,font=('arial',20,'bold'),text=msg3,fg="blue").pack()

f5=Frame(root,width=400,height =80).pack()

midbu=Frame(root, width=200,height = 400)
midbu.pack()

button=Button(midbu ,text="O P E N   C A M E R A",fg="white",bg="black", font=('arial',20,'bold') , command=vid)
button.pack()
f7=Frame(root,width=100,height=50).pack()
f6=Frame(root,width=100,height=100)
f6.pack()


button2=Button(f6, text="Q U I T",fg="white",bg="black", font=('arial',20,'bold') , command=quit)
button2.pack()



root.mainloop()

