from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

app = Flask(__name__)
CORS(app)
log_messages = []  # List to store log messages

@app.route('/api/download_images', methods=['GET', 'POST'])
def download_images():
    if request.method == 'POST':
        url = request.form.get('url')
        path = 'images'
        download_images_from_url(url, path)
        return jsonify({'message': "Images downloaded successfully!", 'log_messages': log_messages})

def download_images_from_url(url, path):
    # List of image extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.bmp', '.ico', '.psd', '.ai', '.apng', '.avif', '.jfif', '.pjpeg', '.pjp', '.webp']
    non_image_files = []  # List to store non-image files with 'src' attribute

    # Extract domain name from the url and create a new path
    domain_name = urlparse(url).netloc
    path = os.path.join(path, domain_name)

    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the GET request was unsuccessful
        log_messages.append(f"Successfully retrieved HTML content from {url}")

        # Get the content of the response
        page_content = response.content

        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(page_content, 'html.parser')

        # Find all image tags
        images = soup.find_all('img')
        log_messages.append(f"Found {len(images)} image tags on the page")

        # Create the directory if it doesn't already exist
        if not os.path.exists(path):
            os.makedirs(path)
            log_messages.append(f"Created directory: {path}")
        else:
            log_messages.append(f"Directory already exists: {path}. Images will be downloaded into this directory.")

        # Download each image
        for i, image in enumerate(images):
            # Get the URL of the image
            image_url = image.get('src')

            # Check if the URL is valid and starts with 'http' or 'https'
            if image_url and image_url.startswith(('http', 'https')):
                # Use urljoin to handle relative URLs
                full_image_url = urljoin(url, image_url)
            elif image_url and image_url.startswith('/'):
                # Handle relative URLs that start with '/'
                full_image_url = urljoin(url, image_url)
            else:
                # Skip this image if the URL is not valid
                log_messages.append(f"Skipping image {i + 1} due to invalid URL: {image_url}")
                continue

            # Check if the URL is an image by looking at the extension
            if not any(full_image_url.endswith(ext) for ext in image_extensions):
                non_image_files.append(full_image_url)
                log_messages.append(f"Skipping non-image file {i + 1}: {full_image_url}")
                continue

            # Send a GET request to the image URL
            image_response = requests.get(full_image_url)
            image_response.raise_for_status()  # Raise an exception if the GET request was unsuccessful
            log_messages.append(f"Downloading image {i + 1} from {full_image_url}")

            # Get the content of the response
            image_content = image_response.content

            # Get the image name from the URL
            image_name = urlparse(full_image_url).path.split('/')[-1]

            # If the image name is empty, use a default name
            if not image_name.strip():
                image_name = f'image_{i}.jpg'

            # Open the file in write mode
            with open(os.path.join(path, image_name), 'wb') as f:
                # Write the image content to the file
                f.write(image_content)
                log_messages.append(f"{image_name} saved successfully")

        log_messages.append(f"\nDownload completed. {len(non_image_files)} non-image files were skipped.")

    except requests.exceptions.HTTPError as errh:
        log_messages.append(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        log_messages.append(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        log_messages.append(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        log_messages.append(f"Something went wrong with the request: {err}")

# Call the function to download images from a URL and save them to a directory
if __name__ == '__main__':
    app.run(debug=True)
