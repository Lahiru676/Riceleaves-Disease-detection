from fastapi import FastAPI, File, UploadFile
import uvicorn
import numpy as np
from PIL import Image
from io import BytesIO
import tensorflow as tf
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for all origins (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the Keras model
MODEL = tf.keras.models.load_model('C:/Users/Lahiru/OneDrive - University of Jaffna/Desktop/Carrier path/Projects/Riceleaves diesease/saved_models/1.keras')
CLASS_NAMES = ['bacterial_leaf_blight', 'brown_spot', 'healthy', 'leaf_blast', 'leaf_scald', 'narrow_brown_spot']

@app.get("/ping")
async def ping():
    return "pong"

def read_file_as_image(data) -> np.ndarray:
    image = Image.open(BytesIO(data)).convert("RGB")
    image = image.resize((224, 224))  # Resize image to match model input requirements if needed
    image = np.array(image) / 255.0  # Normalize pixel values if required by your model
    return image

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_data = await file.read()
    image = read_file_as_image(image_data)
    img_batch = np.expand_dims(image, 0)

    # Predict the class and confidence
    predictions = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])

    # Debugging: Print predictions to verify output
    print(f"Predictions: {predictions}")
    print(f"Predicted class: {predicted_class}, Confidence: {confidence}")

    # Return a JSON response with the prediction
    return JSONResponse(content={
        'prediction': {
            'class': predicted_class,
            'confidence': float(confidence)
        }
    })

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
