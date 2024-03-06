from flask import Flask, request, render_template
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from colorama import Fore, Style, init

# Initialize colorama
init()

app = Flask(__name__)
log_messages = [] # List to store log messages

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form.get('url')
        path = 'images'
        download_images(url, path)
        return render_template('index.html', message="Images downloaded successfully!", log_messages=log_messages)
    return render_template('index.html')

def download_images(url, path):
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

        log_messages.append(Fore.GREEN + f"Successfully retrieved HTML content from {url}" + Style.RESET_ALL)

        # Get the content of the response
        page_content = response.content

        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(page_content, 'html.parser')

        # Find all image tags
        images = soup.find_all('img')
        log_messages.append(Fore.GREEN + f"Found {len(images)} image tags on the page" + Style.RESET_ALL)

        # Create the directory if it doesn't already exist
        if not os.path.exists(path):
            os.makedirs(path)
            log_messages.append(Fore.GREEN + f"Created directory: {path}" + Style.RESET_ALL)
        else:
            log_messages.append(Fore.YELLOW + f"Directory already exists: {path}. Images will be downloaded into this directory." + Style.RESET_ALL)

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
                log_messages.append(Fore.RED + f"Skipping image {i + 1} due to invalid URL: {image_url}" + Style.RESET_ALL)
                continue

            # Check if the URL is an image by looking at the extension
            if not any(full_image_url.endswith(ext) for ext in image_extensions):
                non_image_files.append(full_image_url)
                log_messages.append(Fore.RED + f"Skipping non-image file {i + 1}: {full_image_url}" + Style.RESET_ALL)
                continue

            # Send a GET request to the image URL
            image_response = requests.get(full_image_url)
            image_response.raise_for_status()  # Raise an exception if the GET request was unsuccessful

            log_messages.append(Fore.GREEN + f"Downloading image {i + 1} from {full_image_url}" + Style.RESET_ALL)

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
                log_messages.append(Fore.GREEN + f"{image_name} saved successfully" + Style.RESET_ALL)

        log_messages.append(Fore.GREEN + f"\nDownload completed. {len(non_image_files)} non-image files were skipped." + Style.RESET_ALL)

    except requests.exceptions.HTTPError as errh:
        log_messages.append(Fore.RED + "HTTP Error:",errh + Style.RESET_ALL)
    except requests.exceptions.ConnectionError as errc:
        log_messages.append(Fore.RED + "Error Connecting:",errc + Style.RESET_ALL)
    except requests.exceptions.Timeout as errt:
        log_messages.append(Fore.RED + "Timeout Error:",errt + Style.RESET_ALL)
    except requests.exceptions.RequestException as err:
        log_messages.append(Fore.RED + "Something went wrong with the request:",err + Style.RESET_ALL)

# Call the function to download images from a URL and save them to a directory
if __name__ == '__main__':
    app.run(debug=True)