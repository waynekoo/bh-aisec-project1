import base64
import io
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from flask import Flask, request, jsonify
from PIL import Image
import os # Import os module to work with file paths

app = Flask(__name__)

# --- 1. Define the Neural Network Architecture (Must match training architecture) ---
class DigitClassifier(nn.Module):
    """
    A simple Convolutional Neural Network (CNN) for digit classification.
    This architecture must be identical to the one used during training
    to correctly load the saved model state dictionary.
    """
    def __init__(self):
        super(DigitClassifier, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout1 = nn.Dropout(0.25)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.dropout2 = nn.Dropout(0.5)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = self.dropout1(x)
        x = x.view(-1, 64 * 7 * 7)
        x = self.dropout2(torch.relu(self.fc1(x)))
        x = self.fc2(x)
        return x

# --- 2. Image Preprocessing Function ---
def preprocess_image(image_bytes):
    """
    Preprocesses an image (bytes) to match the MNIST dataset requirements.
    - Converts to grayscale
    - Resizes to 28x28 pixels
    - Converts to PyTorch Tensor
    - Normalizes with MNIST mean and standard deviation
    - Adds a batch dimension (1, 1, 28, 28)
    """
    # Open the image using Pillow from bytes
    image = Image.open(io.BytesIO(image_bytes)).convert('L') # Convert to grayscale ('L' mode)

    # Define transformations to apply to the image for inference
    transform = transforms.Compose([
        transforms.Resize((28, 28)), # Resize to 28x28 pixels
        transforms.ToTensor(),       # Convert to PyTorch Tensor (scales to [0, 1])
        transforms.Normalize((0.1307,), (0.3081,)) # Normalize with MNIST mean and std
    ])

    # Apply transformations and add a batch dimension
    # unsqueeze(0) adds a batch dimension, changing (C, H, W) to (1, C, H, W)
    image_tensor = transform(image).unsqueeze(0)
    return image_tensor

# --- 3. Global Model Loading ---
# Determine the device to run the model on (CPU or GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device for inference: {device}")

# Define the path where the model will be mounted inside the container
# This path should match the mountPath in your Kubernetes Deployment YAML
MODEL_PATH = "/mnt/model/mnist_classifier.pth"

# Initialize the model architecture globally so it's loaded once when the app starts
inference_model = DigitClassifier()

# Load the trained model state dictionary
try:
    # Check if the model file exists at the expected mounted path
    if os.path.exists(MODEL_PATH):
        inference_model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
        inference_model.to(device) # Move model to the correct device after loading
        inference_model.eval() # Set the model to evaluation mode
        print(f"Model '{MODEL_PATH}' loaded successfully.")
    else:
        print(f"Error: Model file not found at '{MODEL_PATH}'.")
        print("Please ensure the model is mounted correctly in the container.")
        inference_model = None # Set model to None to indicate it's not loaded
except Exception as e:
    print(f"Error loading model from '{MODEL_PATH}': {e}")
    inference_model = None

@app.route('/classify/v0', methods=['POST'])
def classify_image():
    """
    Handles POST requests to the /classify/v0 endpoint.
    Expects a JSON payload with an 'image' field containing a base64 encoded image.
    Decodes the image, runs inference using the loaded PyTorch model,
    and responds with a JSON formatted response containing the predicted digit.
    """
    if inference_model is None:
        return jsonify({"error": "Model not loaded. Cannot perform classification."}), 503

    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Check if 'image' field is present in the request data
        if not data or 'image' not in data:
            return jsonify({"error": "Missing 'image' field in request body."}), 400

        # Extract the base64 encoded image string
        base64_image = data['image']

        try:
            # Decode the base64 string to bytes
            decoded_image_bytes = base64.b64decode(base64_image)
        except Exception as e:
            return jsonify({"error": f"Invalid base64 encoding: {str(e)}"}), 400

        # Preprocess the image for the model
        try:
            image_tensor = preprocess_image(decoded_image_bytes)
            image_tensor = image_tensor.to(device) # Move tensor to the correct device
        except Exception as e:
            return jsonify({"error": f"Image preprocessing failed: {str(e)}"}), 400

        # Perform inference
        with torch.no_grad(): # Disable gradient calculation during inference
            output = inference_model(image_tensor)
            # Get the predicted class (the index of the max log-probability)
            _, predicted = torch.max(output.data, 1)

        predicted_digit = predicted.item() # Get the Python integer value

        # Return the predicted digit in a JSON response
        return jsonify({"predicted_digit": predicted_digit}), 200

    except Exception as e:
        # Catch any unexpected errors and return a 500 internal server error
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # Run the Flask application
    # debug=True allows for automatic reloading on code changes and provides a debugger
    # host='0.0.0.0' makes the server accessible from any IP address
    app.run(debug=True, host='0.0.0.0', port=8081)