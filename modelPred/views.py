from django.shortcuts import render
import tensorflow as tf
import numpy as np
import os
from fatsecret import Fatsecret
import json
from django.core.files.storage import default_storage
from django.conf import settings
from tensorflow.keras.preprocessing import image

#testingdirect = "F://xampp//htdocs//upload"
testingdirect = "media"
#new_model = tf.keras.models.load_model('F://xampp//htdocs//saved_model//fmodel')

new_model = tf.keras.models.load_model(
    'F://xampp//htdocs//saved_model//fmodel')

#foodmodel = tf.keras.load_model("saved_model/fmodel")
# Create your views here.
new_model.compile(optimizer=tf.keras.optimizers.SGD(lr=0.004),
                  loss=tf.keras.losses.CategoricalCrossentropy(),
                  metrics=['accuracy'])
fs = Fatsecret("896700be9d2449ce8838af1102898343",
               "d58a47e2b261425ab9191b76b8398c57")
name = [
    'apple_pie', 'baby_back_ribs', 'baklava', 'beef_carpaccio', 'beef_tartare',
    'beet_salad', 'beignets', 'bibimbap', 'bread_pudding', 'breakfast_burrito',
    'bruschetta', 'caesar_salad', 'cannoli', 'caprese_salad', 'carrot_cake',
    'ceviche', 'cheesecake', 'cheese_plate', 'chicken_curry',
    'chicken_quesadilla', 'chicken_wings', 'chocolate_cake',
    'chocolate_mousse', 'churros', 'clam_chowder', 'club_sandwich',
    'crab_cakes', 'creme_brulee', 'croque_madame', 'cup_cakes', 'deviled_eggs',
    'donuts', 'dumplings', 'edamame', 'eggs_benedict', 'escargots', 'falafel',
    'filet_mignon', 'fish_and_chips', 'foie_gras', 'french_fries',
    'french_onion_soup', 'french_toast', 'fried_calamari', 'fried_rice',
    'frozen_yogurt', 'garlic_bread', 'gnocchi', 'greek_salad',
    'grilled_cheese_sandwich', 'grilled_salmon', 'guacamole', 'gyoza',
    'hamburger', 'hot_and_sour_soup', 'hot_dog', 'huevos_rancheros', 'hummus',
    'ice_cream', 'lasagna', 'lobster_bisque', 'lobster_roll_sandwich',
    'macaroni_and_cheese', 'macarons', 'miso_soup', 'mussels', 'nachos',
    'omelette', 'onion_rings', 'oysters', 'pad_thai', 'paella', 'pancakes',
    'panna_cotta', 'peking_duck', 'pho', 'pizza', 'pork_chop', 'poutine',
    'prime_rib', 'pulled_pork_sandwich', 'ramen', 'ravioli', 'red_velvet_cake',
    'risotto', 'samosa', 'sashimi', 'scallops', 'seaweed_salad',
    'shrimp_and_grits', 'spaghetti_bolognese', 'spaghetti_carbonara',
    'spring_rolls', 'steak', 'strawberry_shortcake', 'sushi', 'tacos',
    'takoyaki', 'tiramisu', 'tuna_tartare', 'waffles'
]


def titlename(arr):
    for i in range(1):
        loc = np.where(arr[i] == np.amax(arr[i]))
        x = np.array(loc, dtype=np.int64)
        #print("location: ",loc)
        y = x[0][0]
        return name[y]


def predict(request):
    os.remove('media/upload/uploads.jpg')
    #save_path = os.path.join(settings.MEDIA_ROOT, 'uploads',request.FILES['file'])

    path = default_storage.save("upload/uploads.jpg", request.FILES['file'])
    os.remove('media/data_file.json')

    testing_generator = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1. / 255).flow_from_directory(testingdirect,
                                              target_size=(299, 299),
                                              batch_size=1)
    imgs, labels = next(testing_generator)

    pred = new_model.predict(imgs)

    name1 = []
    value = []
    arr2 = []
    serv = []

    final = pred[0]

    for j in range(3):
        for i in range(101):
            if (float(final[i]) == np.amax(final)):
                name1.append(name[i])
                value.append(final[i] * 100)
                final[i] = 0
                break

    nutrvalall = []

    for i in range(3):

        a = fs.foods_search(name1[i].replace("_", " "))
        try:
            arr2 = a[0]['food_description'].split('-')
            serv.append(arr2[0])
            nutrvalall.append(arr2[1].split('|'))

        except:
            arr2 = a['food_description'].split('-')
            serv.append(arr2[0])
            nutrvalall.append(arr2[1].split('|'))

    nutr = []
    d = []

    for j in range(3):
        for i in range(4):
            arr2 = str(nutrvalall[j][i].split(':')[1])

            d.append(arr2)
        nutr.append(d)
        d = []
    """var text = '{"employees":[' +
    '{"firstName":"John","lastName":"Doe" },' +
    '{"firstName":"Anna","lastName":"Smith" },' +
    '{"firstName":"Peter","lastName":"Jones" }]}';
    """

    response = {
        'prediction': [
            {
                "Name": name1[0],
                "Value": value[0],
                "Serving": serv[0],
                "Calories": nutr[0][0],
                "Fat": nutr[0][1],
                "Carbs": nutr[0][2],
                "Protein": nutr[0][3]
            },
            {
                "Name": name1[1],
                "Value": value[1],
                "Serving": serv[1],
                "Calories": nutr[1][0],
                "Fat": nutr[1][1],
                "Carbs": nutr[1][2],
                "Protein": nutr[1][3]
            },
            {
                "Name": name1[2],
                "Value": value[2],
                "Serving": serv[2],
                "Calories": nutr[2][0],
                "Fat": nutr[2][1],
                "Carbs": nutr[2][2],
                "Protein": nutr[2][3]
            },
        ]
    }
    cont = str(response)

    save_path = os.path.join(settings.STATIC_ROOT, 'static')

    with open("media/data_file.json", "w+") as write_file:
        json.dump(response, write_file)

    a = "'" + cont.replace("'", '"') + "'"

    context = {'resultjson': a}
    return render(request, 'modelPred/predictserver.html', context)
