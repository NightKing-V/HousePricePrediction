import pandas as pd
import os
import pickle
import joblib
from sklearn.preprocessing import StandardScaler

component_path = 'app/Model/'

async def predict(bedrooms: int, bathrooms: int, house_size_sqft: float, land_size_perch: float, location: str):
    try:    
        # Load model components
        model, scaler, feature_columns = await load_model_components()

        # Base input dictionary
        input_data = {
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'house_size_sqft': house_size_sqft,
            'land_size_perch': land_size_perch,
        }

        # Add one-hot encoded location fields
        for col in feature_columns:
            if col.startswith('location_'):
                input_data[col] = 1 if col == f'location_{location}' else 0
            elif col not in input_data:
                input_data[col] = 0  # Handle other engineered features

        # Create DataFrame and ensure column order matches training
        input_df = pd.DataFrame([input_data])[feature_columns]

        # Scale (only numeric fields were scaled during training)
        input_scaled = scaler.transform(input_df)

        # Predict
        prediction = model.predict(input_scaled)[0]

        return {"predicted_price": float(round(prediction, 2))}
    except Exception as e:
        print(f"Error during prediction: {e}")
        raise



async def load_model_components():
    try:
        model = joblib.load(os.path.join(component_path, 'model.pkl'))
        scaler = joblib.load(os.path.join(component_path, 'scaler.pkl'))
        feature_columns = joblib.load(os.path.join(component_path, 'features.pkl'))

        return model, scaler, feature_columns
    except Exception as e:
        print(f"Error loading model components: {e}")
        raise
