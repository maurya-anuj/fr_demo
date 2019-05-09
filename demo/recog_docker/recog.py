# It helps in identifying the faces
import cv2, sys, numpy, os, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import simplejson
import time
import base64
import http.server
import socketserver
import logging

size = 4
haar_file = 'haarcascade_frontalface_default.xml'
datasets = 'data'
data_lock = threading.Lock()
file_lock = threading.Lock()
logging.basicConfig(filename="logfile.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        f = open("index.html", "r")
        self.wfile.write(f.read())

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        print("in post method")
        logger.info("post recieved")
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        # Convert back to binary
        png_original = base64.b64decode(self.data_string)
        print("self.path", self.path)
        print(self.path.split('/'))
        none, name, count = self.path.split('/')
        # path_default = os.path.join(datasets, name.replace('/', ''))
        # print(path_default)
        path = datasets + "/" + name
        print(path, name)
        if not os.path.isdir(path):
            print("directory present at :"+ path)
            os.mkdir(path)	
        # Write to a file to show conversion worked
        with file_lock:
            print("in data lock")
            with open("%s/%s.png"%(path, count), 'wb') as f_output:
                print("%s/%s.png"%(path, count))
                # logger.info("path at :%s/1.png"%path)
                f_output.write(png_original)
        return


def run(server_class=HTTPServer, handler_class=S, port=8000):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    logger.info('Starting httpd...')
    print('Starting httpd...')
    print(time.asctime(), 'Server started on port', port)
    print('....')
    print('ctrl-c to quit server.')
    close = False
    try:
        httpd.serve_forever()
        if close:
            raise
            # server.server_close()
    except KeyboardInterrupt:
        httpd.server_close()
        print(time.asctime(), "Server Stopped")
    except:
        httpd.server_close()
        print(time.asctime(), "Server Stopped")


# Part 1: Create fisherRecognizer
print('Recognizing Face Please Be in sufficient Lights...')

# Create a list of images and a list of corresponding names
(images, lables, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            lable = id
            with data_lock:
                images.append(cv2.imread(path, 0))
                lables.append(int(lable))
            print(type(images), type(lable))
        id += 1
(width, height) = (130, 100)


def update_data():
    global id
    global images
    global lables
    global names
    global model
    while True:
        time.sleep(2)
        (images_p, lables_p, names_p, id) = ([], [], {}, 0)
        for (subdirs, dirs, files) in os.walk(datasets):
            for subdir in dirs:
                names_p[id] = subdir
                subjectpath = os.path.join(datasets, subdir)
                for filename in os.listdir(subjectpath):
                    path = subjectpath + '/' + filename
                    lable_p = id
                    with file_lock:
                        images_p.append(cv2.imread(path, 0))
                    lables_p.append(int(lable_p))
                id += 1
        (images_p, lables_p) = [numpy.array(lis) for lis in [images_p, lables_p]]
        model_p = cv2.face.LBPHFaceRecognizer_create()
        model_p.train(images_p, lables_p)
        with data_lock:
            names = names_p
            images = images_p
            lables = lables_p
            model = model_p


# Create a Numpy array from the two lists above
# (images, lables) = [numpy.array(lis) for lis in [images, lables]]
# print(type(images), type(lable))

# OpenCV trains a model from the images
# NOTE FOR OpenCV2: remove '.face'
(images, lables) = [numpy.array(lis) for lis in [images, lables]]
print(type(images), lables, type(lables))
model = cv2.face.LBPHFaceRecognizer_create()
model.train(images, lables)

# run update thread in parallel
update_data = threading.Thread(target=update_data)
update_data.daemon = True
update_data.start()

# run http server in parallel
server_run = threading.Thread(target=run)
server_run.daemon = True
server_run.start()

# Part 2: Use fisherRecognizer on camera stream
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
webcam = cv2.VideoCapture(0)
logger.info("while:true")
while True:
    (_, im) = webcam.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (width, height))
        with data_lock:
            # Try to recognize the face
            prediction = model.predict(face_resize)
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if prediction[1] < 500:
            with data_lock:
                cv2.putText(im, '% s - %.0f' % (names[prediction[0]], prediction[1]), (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1,
                            (0, 255, 0))
        else:
            cv2.putText(im, 'not recognized', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

    cv2.imshow('OpenCV', im)

    key = cv2.waitKey(10)
    if key == 27:
        break

