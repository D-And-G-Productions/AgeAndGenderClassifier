# will need access to the models folder to build the image. Request access from the authors
FROM tensorflow/serving:latest
# Copy models from your laptop into the container image
COPY ./models /models
# Set the command to run automatically
ENV MODEL_CONFIG_FILE=/models/models.config