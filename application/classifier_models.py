from tensorflow.keras import layers, models
from tensorflow.keras.applications import ResNet152V2
from tensorflow.keras.regularizers import l2
from tensorflow.keras.saving import register_keras_serializable


@register_keras_serializable()
class ConvolutionalPredictionModel(models.Model):
    def __init__(self):
        inputs = layers.Input(shape=(128, 128, 3))

        # 1st block (cnn) - output size (62*62*96)
        x = layers.Conv2D(filters=8, kernel_size=(5, 5), strides=(2, 2), padding="valid")(inputs)
        x = layers.BatchNormalization()(x)
        x = layers.LeakyReLU(alpha=0.1)(x)

        # 2nd block (mp) - output size (31*31*96)
        x = layers.MaxPool2D(pool_size=(2, 2), strides=(2, 2))(x)

        # 3rd block (cnn) - output size (31*31*256)
        x = layers.Conv2D(16, kernel_size=(3, 3), padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.LeakyReLU(alpha=0.1)(x)

        # 4th block (mp) - output size (15*15*256)
        x = layers.MaxPool2D(pool_size=(3, 3), strides=(2, 2))(x)

        # 6th block (cnn) - output size (15*15*384)
        x = layers.Conv2D(32, kernel_size=(3, 3), padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.LeakyReLU(alpha=0.1)(x)

        # 7th block (cnn) - output size (15*15*256)
        x = layers.Conv2D(16, kernel_size=(3, 3), padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.LeakyReLU(alpha=0.1)(x)

        # 8th block (mp) - ouptut size (6*6*256) under 10*10 limit
        x = layers.MaxPool2D(pool_size=(5, 5), strides=(2, 2))(x)

        # 9th block (flatten) - output size (9216)
        x = layers.Flatten()(x)

        # 10th block (fnn) - output size (4096)
        x = layers.Dense(576, kernel_regularizer=l2(0.001))(x)
        x = layers.LeakyReLU(alpha=0.1)(x)
        x = layers.Dropout(0.5)(x)

        # 11th block (fnn) - output size (2048)
        x = layers.Dense(288, kernel_regularizer=l2(0.001))(x)
        x = layers.LeakyReLU(alpha=0.1)(x)
        x = layers.Dropout(0.5)(x)

        # output
        age_output = layers.Dense(1, activation="linear", name="age_output")(x)  # Linear activation for regression
        gender_output = layers.Dense(1, activation="sigmoid", name="gender_output")(
            x
        )  # Sigmoid for binary classification

        super().__init__(inputs=inputs, outputs=[age_output, gender_output])


@register_keras_serializable()
class FeatureExtractionModel(models.Model):
    def __init__(self):
        # 1. Define the input layer for your native image size.
        inputs = layers.Input(shape=(128, 128, 3))

        # 2. Add a resizing layer to adjust to the pre-trained custom_model's expected input size.
        # check if resizing in the custom_model is okay

        x = inputs

        # 3. Load the pre-trained custom_model without an input_tensor.
        base_model = ResNet152V2(weights='imagenet', include_top=False)
        base_model.trainable = False

        # 4. Pass the resized tensor through the base custom_model.
        x = base_model(x, training=False)
        x = layers.GlobalAveragePooling2D()(x)

        x = layers.Dense(512, kernel_regularizer=l2(0.001))(x)
        x = layers.BatchNormalization()(x)
        x = layers.LeakyReLU(alpha=0.1)(x)
        x = layers.Dropout(0.5)(x)

        x = layers.Dense(256, kernel_regularizer=l2(0.001))(x)
        x = layers.BatchNormalization()(x)
        x = layers.LeakyReLU(alpha=0.1)(x)
        x = layers.Dropout(0.5)(x)

        # Example heads for gender and age.
        age_output = layers.Dense(1, activation='linear', name='age_output')(x)
        gender_output = layers.Dense(1, activation='sigmoid', name='gender_output')(x)
        super().__init__(inputs=inputs, outputs=[age_output, gender_output])
