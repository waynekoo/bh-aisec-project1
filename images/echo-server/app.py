import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/classify/v0', methods=['POST'])
def classify_image():
    """
    Handles POST requests to the /classify/v0 endpoint.
    Expects a JSON payload with an 'image' field containing a base64 encoded image.
    Decodes the image and returns its hexadecimal representation.
    """
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

        # Convert the decoded bytes to a hexadecimal string
        # .hex() method converts bytes to a string of hexadecimal digits
        hex_image = decoded_image_bytes.hex()

        # Return the hexadecimal representation in a JSON response
        return jsonify({"decoded": hex_image}), 200

    except Exception as e:
        # Catch any unexpected errors and return a 500 internal server error
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # Run the Flask application
    # debug=True allows for automatic reloading on code changes and provides a debugger
    # host='0.0.0.0' makes the server accessible from any IP address
    app.run(debug=True, host='0.0.0.0', port=8081)