import zipfile

keras_zip_path = 'keras_models/feature_extraction_model_2.keras'
extract_path = 'keras_models/feature_extraction_model_2'

with zipfile.ZipFile(keras_zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

print(f"Extracted {keras_zip_path} to {extract_path}")