import base64
import requests
import os
import argparse # Import the argparse module

def send_image_for_classification(image_path, api_url):
    """
    Reads an image file, Base64 encodes it, and sends it via POST request
    to a specified API endpoint.

    Args:
        image_path (str): The path to the image file.
        api_url (str): The URL of the API endpoint.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        return

    try:
        # Read the image file in binary mode
        with open(image_path, "rb") as image_file:
            # Base64 encode the image data
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        # Prepare the JSON payload
        payload = {
            "image": encoded_image
        }

        # Set the headers for the POST request
        headers = {
            "Content-Type": "application/json"
        }

        print(f"Sending POST request to {api_url} with image {image_path}...")

        # Send the POST request
        response = requests.post(api_url, json=payload, headers=headers)

        # Print the response from the server
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Body: {response.json()}")

    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to the API at {api_url}.")
        print("Please ensure your Flask app is running and accessible at this address.")
    except requests.exceptions.MissingSchema:
        print(f"Error: Invalid URL format '{api_url}'.")
        print("Please ensure the URL includes 'http://' or 'https://'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Base64 encodes an image and sends it via POST to a classification API."
    )

    # Add arguments
    parser.add_argument(
        "image_path",
        type=str,
        help="Path to the image file (e.g., 'digit_4.png' or '/path/to/image.jpg')"
    )
    parser.add_argument(
        "server_url",
        type=str,
        help="The full URL of the classification API endpoint (e.g., 'http://localhost:8081')"
    )

    # Parse the arguments
    args = parser.parse_args()

    # Call the function with the parsed arguments
    send_image_for_classification(args.image_path, args.server_url + "/classify/v0")
