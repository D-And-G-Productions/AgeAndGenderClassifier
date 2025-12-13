FROM tensorflow/serving:latest

# Copy models into the container
COPY models /models

# Copy model config file
COPY models/models.config /models/models.config

# Expose TF Serving REST API port
EXPOSE 8501

CMD ["--model_config_file=/models/models.config", "--rest_api_port=8501"]
