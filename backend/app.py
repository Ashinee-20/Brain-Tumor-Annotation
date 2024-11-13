from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
import pydicom
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import logging
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/get_images', methods=['GET'])
def get_images():
    logging.info("Starting DICOM to PNG conversion for brain and annotation images")
    
    brain_dcm_path = 'assets/images/image.0100.dcm'
    annotation_dcm_path = 'assets/annotations/image.0100.dcm'
    
    # Load and plot brain image DICOM file
    brain_image = read_dicom_and_plot(brain_dcm_path)
    logging.info(f"Converted DICOM file to PNG: {brain_dcm_path}")
    
    # Load and plot annotation image DICOM file
    annotation_image = read_dicom_and_plot(annotation_dcm_path)
    logging.info(f"Converted DICOM file to PNG: {annotation_dcm_path}")
    
    # Prepare JSON response
    response = {
        'brain_image': brain_image,
        'annotation_image': annotation_image
    }
    logging.info("Preparing JSON response with encoded images")
    return jsonify(response)

def read_dicom_and_plot(dicom_path):
    logging.info(f"Reading DICOM file: {dicom_path}")
    
    # Read DICOM file
    dicom_image = pydicom.dcmread(dicom_path)
    logging.info(f"Successfully read DICOM file: {dicom_path}")
    
    # Extract pixel array (image data) from DICOM file
    pixel_array = dicom_image.pixel_array
    
    # Use matplotlib to display the image
    fig, ax = plt.subplots()
    ax.imshow(pixel_array, cmap='gray')
    ax.axis('off')  # Hide axes
    
    # Save the figure as a PNG image in memory
    buffered = io.BytesIO()
    plt.savefig(buffered, bbox_inches='tight', pad_inches=0, format='PNG')
    buffered.seek(0)  # Reset pointer to the beginning of the image in memory
    
    # Convert the PNG image to base64
    encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    # Close the plot to free memory
    plt.close(fig)
    
    return encoded_image

if __name__ == '__main__':
    app.run(debug=True)
