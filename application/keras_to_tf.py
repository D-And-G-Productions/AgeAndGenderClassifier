"""
This file changes the keras model to a tf model
"""
import tensorflow as tf
from keras import layers, saving, models, utils
from keras.regularizers import l2

@saving.register_keras_serializable()
class VersionFourMiniModelA(models.Model):
    def __init__(self):
        inputs = layers.Input(shape=(128, 128, 3))
        
        # 1st block (cnn) - output size (62*62*96)
        x = layers.Conv2D(filters = 8, kernel_size = (5, 5), strides = (2,2), padding = "valid")(inputs)
        x = layers.BatchNormalization()(x)
        x = layers.LeakyReLU(alpha=0.1)(x) 

        # 2nd block (mp) - output size (31*31*96)
        x = layers.MaxPool2D(pool_size = (2,2), strides = (2,2))(x)
        
        # 3rd block (cnn) - output size (31*31*256)
        x = layers.Conv2D(32, kernel_size = (3, 3), padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.LeakyReLU(alpha=0.1)(x) 

        # 4th block (mp) - output size (15*15*256)
        x = layers.MaxPool2D(pool_size = (3, 3), strides = (2,2))(x)

        # 6th block (cnn) - output size (15*15*384)
        x = layers.Conv2D(64, kernel_size = (3, 3), padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.LeakyReLU(alpha=0.1)(x) 

        # 7th block (cnn) - output size (15*15*256)
        x = layers.Conv2D(32, kernel_size = (3, 3), padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.LeakyReLU(alpha=0.1)(x) 

        # 8th block (mp) - ouptut size (6*6*256) under 10*10 limit
        x = layers.MaxPool2D(pool_size= (5,5), strides = (2,2))(x)

        # 9th block (flatten) - output size (9216)
        x = layers.Flatten()(x)

        # 10th block (fnn) - output size (4096)
        x = layers.Dense(576,  kernel_regularizer=l2(0.001))(x)
        x = layers.LeakyReLU(alpha=0.1)(x) 
        x = layers.Dropout(0.5)(x)

        # 11th block (fnn) - output size (2048)
        x = layers.Dense(288,  kernel_regularizer=l2(0.001))(x)
        x = layers.LeakyReLU(alpha=0.1)(x) 
        x = layers.Dropout(0.5)(x)
        
        # output
        age_output = layers.Dense(1, activation="linear", name="age_output")(x)  # Linear activation for regression
        gender_output = layers.Dense(1, activation="sigmoid", name="gender_output")(x)  # Sigmoid for binary classification
        
        super().__init__(inputs=inputs, outputs=[age_output, gender_output])


model = VersionFourMiniModelA()
model.summary()
model.load_weights("keras_models/custom_model_2/model.weights.h5")
model.export("models/custom_model/2")