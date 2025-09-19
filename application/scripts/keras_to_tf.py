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
    
        # 1st block (cnn) 
        x = layers.Conv2D(filters = 8, kernel_size = (5, 5), strides = (2,2), padding = "valid")(inputs)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('gelu')(x)

        # 2nd block (mp) 
        x = layers.MaxPool2D(pool_size = (2,2), strides = (2,2))(x)
        
        # 3rd block (cnn) 
        x = layers.Conv2D(32, kernel_size = (3, 3), padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('gelu')(x)

        # 4th block (mp) 
        x = layers.MaxPool2D(pool_size = (3, 3), strides = (2,2))(x)

        # 6th block (cnn) 
        x = layers.Conv2D(64, kernel_size = (3, 3), padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('gelu')(x)

        # 7th block (cnn) 
        x = layers.Conv2D(32, kernel_size = (3, 3), padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('gelu')(x)

        # 8th block (mp)
        x = layers.MaxPool2D(pool_size= (5,5), strides = (2,2))(x)

        # 9th block (flatten) 
        x = layers.Flatten()(x)

        # 10th block (fnn) 
        x = layers.Dense(576,  kernel_regularizer=l2(0.001))(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('gelu')(x)
        x = layers.Dropout(0.3)(x)

        # 11th block (fnn) 
        x = layers.Dense(288,  kernel_regularizer=l2(0.001))(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('gelu')(x)
        x = layers.Dropout(0.3)(x)
        
        # output
        age_output = layers.Dense(1, activation="linear", name="age_output")(x)  # Linear activation for regression
        gender_output = layers.Dense(1, activation="sigmoid", name="gender_output")(x)  # Sigmoid for binary classification
        
        model = models.Model(inputs=inputs, outputs=[age_output, gender_output])
        super().__init__(inputs=inputs, outputs=[age_output, gender_output])
    
    def get_config(self):
        """
        Returns the configuration of the model for serialization.
        """
        return super().get_config()

    @classmethod
    def from_config(cls, config):
        """
        Creates a model instance from a config dictionary.
        """
        return cls()  # Calls __init__() to rebuild the model


from tensorflow.keras.layers import Input, Resizing, GlobalAveragePooling2D, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.applications import Xception
from tensorflow.keras.utils import plot_model


@saving.register_keras_serializable()
class VersionOneModelB(models.Model):
    def __init__(self):
        # 1. Define the input layer for your native image size.
        inputs = Input(shape=(128, 128, 3))

        # 2. Add a resizing layer to adjust to the pre-trained model's expected input size.
        # check if resizing in the model is okay

        x = inputs

        # 3. Load the pre-trained model without an input_tensor.
        base_model = Xception(
                include_top=False,
                weights="imagenet",
                input_tensor=None,
                input_shape=(128,128,3),
                pooling=None,
                name="xception",)
        base_model.trainable = False

        for layer in base_model.layers[-18:]:
            layer.trainable = True

        # 4. Pass the resized tensor through the base model.
        x = base_model(x, training=False)
        x = GlobalAveragePooling2D()(x)

        # x = layers.Dense(512, kernel_regularizer=l2(0.001))(x)
        # x = layers.BatchNormalization()(x)
        # x = layers.Activation('gelu')(x)
        # x = layers.Dropout(0.5)(x)
        
        x = layers.Dense(256, kernel_regularizer=l2(0.001))(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('gelu')(x)
        x = layers.Dropout(0.5)(x)
        
        # Example heads for gender and age.
        age_output = Dense(1, activation='linear', name='age_output')(x)
        gender_output = Dense(1, activation='sigmoid', name='gender_output')(x)
        super().__init__(inputs=inputs, outputs=[age_output, gender_output])

    def get_config(self):
        """
        Returns the configuration of the model for serialization.
        """
        return super().get_config()

    @classmethod
    def from_config(cls, config):
        """
        Creates a model instance from a config dictionary.
        """
        return cls()  # Calls __init__() to rebuild the model


model = VersionFourMiniModelA()
model.summary()
model.load_weights("keras_models/custom_model_2/model.weights.h5")
model.export("models/custom_model/2")

model = VersionOneModelB()
model.summary()
model.load_weights("keras_models/feature_extraction_model_2/model.weights.h5")
model.export("models/feature_extraction_model/2")