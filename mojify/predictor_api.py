import pickle
from skimage import io
from bitmoji import createFromFeatures

MODEL_PATH = './static/models/facial_feature_classification.pickle'


# model = pickle.load(open(MODEL_PATH, 'rb'))

def get_prediction(image):
    # classes = model.predict(image)
    features = ['Gray_Hair',
                'Eyeglasses',
                'No_Beard',
                'Bushy_Eyebrows',
                'Bags_Under_Eyes',
                'Wearing_Lipstick',
                'Big_Lips',
                'Double_Chin',
                'Chubby',
                'Narrow_Eyes',
                'Pale_Skin']
    return createFromFeatures(features=features)


def make_prediction(input_image):
    if not input_image:
        input_image = ''
    img = io.imread(input_image)
    features = get_prediction(img)

    return (input_image, features)

