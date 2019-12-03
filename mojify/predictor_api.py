from fastai.vision import *
from skimage import io
import cv2
from bitmoji import createFromFeatures
import imutils
import pickle

MODEL_PATH = './static/models/'


model = load_learner(MODEL_PATH, 'export.pkl')

def get_prediction(image):
    classes = model.predict(image)
    features = classes[0].obj
    return createFromFeatures(features=features)


def make_prediction(input_image):
    face_cascade = cv2.CascadeClassifier('./static/models/haarcascade_frontalface_default.xml')
    fc = face_extractor(input_image, input_image, face_cascade)
    if not fc:
        input_image = ''
    img = open_image(input_image)
    features = get_prediction(img)

    return (input_image, features)


def face_extractor(origin, destination, fc):
    ## Importing image using open cv
    img = cv2.imread(origin, 1)

    ## Resizing to constant width
    img = imutils.resize(img, width=200)

    ## Finding actual size of image
    H, W, _ = img.shape

    ## Converting BGR to RGB
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ## Detecting faces on the image
    face_coord = fc.detectMultiScale(gray, 1.2, 10, minSize=(50, 50))

    ## If only one face is foung
    if len(face_coord) == 1:
        X, Y, w, h = face_coord[0]

    ## If no face found --> SKIP
    elif len(face_coord) == 0:
        return False

    ## If multiple faces are found take the one with largest area
    else:
        max_val = 0
        max_idx = 0
        for idx in range(len(face_coord)):
            _, _, w_i, h_i = face_coord[idx]
            if w_i * h_i > max_val:
                max_idx = idx
                max_val = w_i * h_i
            else:
                pass

            X, Y, w, h = face_coord[max_idx]

    ## Crop and export the image
    img_cp = img[
             max(0, Y - int(0.35 * h)): min(Y + int(1.35 * h), H),
             max(0, X - int(w * 0.35)): min(X + int(1.35 * w), W)
             ].copy()

    cv2.imwrite(destination, img_cp)
    return True