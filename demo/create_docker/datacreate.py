# Creating database
# It captures images and stores them in data
# folder under the folder name of sub_data
import cv2
import sys
import requests
import os
import base64

if sys.version_info[0] == 3:
    from tkinter import *  ## notice lowercase 't' in tkinter here
else:
    # for Python2
    from Tkinter import *  ## notice capitalized T in Tkinter

# need to solve issue for py versions
from tkinter.messagebox import *

datasets = 'data'
url = 'http://127.0.0.1:8001'


def send_to_http(name, no, image):
    retval, buffer = cv2.imencode('.png', image)
    jpg_as_text = base64.b64encode(buffer)
    head = {
            'name': name + "/" + str(no),
            'Content-Type': 'image/png',
            'length': str(len(jpg_as_text))
            }
    print(jpg_as_text)

    r = requests.post(url=url, data=jpg_as_text, headers=head)

    print(type(r), r.status_code)



# '0' is used for my webcam,
# if you've any other camera
# attached use '1' like this
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
webcam = cv2.VideoCapture(0)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 1366, 768)

while True:
    (_, im) = webcam.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 4)
    key = cv2.waitKey(1)
    if key % 256 == 32:
        master = Tk()
        Label(master, text="First Name").grid(row=0)
        master.geometry("220x50+500+700")
        master.resizable(width=False, height=False)
        e1 = Entry(master)


        def answer(self):
            count = 1
            # defining the size of images
            (width, height) = (130, 100)
            sub_data = e1.get()
            path = os.path.join(datasets, sub_data)
            if not os.path.isdir(path):
                os.mkdir(path)
            while count < 30:
                (_, im) = webcam.read()
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 4)
                for (x, y, w, h) in faces:
                    cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    face = gray[y:y + h, x:x + w]
                    face_resize = cv2.resize(face, (width, height))
                    cv2.imwrite('% s/% s.png' % (path, count), face_resize)
                    # send_to_http(sub_data, count, face_resize)
                    print('Image:' + sub_data + ' written at:' + path)
                count += 1
            master.destroy()

        e1.bind('<Return>', func=answer)

        # These are sub data sets of folder,
        # for my faces I've used my name you can
        # change the label here

        e1.grid(row=0, column=1)


        def callback():
            if askyesno('Verify', 'Really quit?'):
                webcam.release()
                exit(0)
            else:
                showinfo('No', 'Quit has been cancelled')

        Button(master, text='Quit', command=callback).grid(row=3, column=0, sticky=W, pady=4)
        Button(master, text='Answer', command=answer).grid(row=3, column=1, sticky=W, pady=4)
        mainloop()

    cv2.imshow('image', im)

    if key == 27:
        break
