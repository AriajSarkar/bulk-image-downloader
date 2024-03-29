import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from colorama import Fore, Style, init
from tqdm import tqdm

# Initialize colorama
init()

def download_images(url, path):
    # Clear previous logs
    global log_messages
    log_messages = []

    # List of image extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.bmp', '.ico', '.psd', '.ai', '.apng', '.avif',
                        '.jfif', '.pjpeg', '.pjp', '.webp']

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
            log_messages.append(
                Fore.YELLOW + f"Directory already exists: {path}. Images will be downloaded into this directory." +
                Style.RESET_ALL)

        # Download each image
        for i, image in enumerate(tqdm(images, desc="Downloading images", unit="image", position=0, leave=True)):
            try:
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
                    log_messages.append(
                        Fore.RED + f"Skipping image {i + 1} due to invalid URL: {image_url}" + Style.RESET_ALL)
                    continue

                # Check if the URL is an image by looking at the extension
                if not any(full_image_url.endswith(ext) for ext in image_extensions):
                    non_image_files.append(full_image_url)
                    log_messages.append(
                        Fore.RED + f"Skipping non-image file {i + 1}: {full_image_url}" + Style.RESET_ALL)
                    continue

                # Send a GET request to the image URL
                with requests.get(full_image_url, stream=True) as image_response:
                    image_response.raise_for_status()  # Raise an exception if the GET request was unsuccessful

                    # Get the content of the response
                    image_content = image_response.content

                    # Update the image name from the URL
                    image_name = urlparse(full_image_url).path.split('/')[-1]

                    # If the image name is empty, use a default name
                    if not image_name.strip():
                        image_name = f'image_{i}.jpg'

                    # Open the file in write mode
                    with open(os.path.join(path, image_name), 'wb') as f:
                        # Write the image content to the file
                        f.write(image_content)

                    log_messages.append(Fore.GREEN + f"{image_name} saved successfully" + Style.RESET_ALL)

            except requests.exceptions.RequestException as err:
                log_messages.append(Fore.RED + f"Error downloading image {i + 1}: {err}" + Style.RESET_ALL)

        log_messages.append(
            Fore.GREEN + f"\nDownload completed. {len(non_image_files)} non-image files were skipped." + Style.RESET_ALL)

    except requests.exceptions.RequestException as err:
        log_messages.append(Fore.RED + f"Error during download: {err}" + Style.RESET_ALL)


# Main function
def main():
    while True:
        try:
            url = input("Enter the URL (or 'exit' or Ctrl+C to quit): ")
            if url.lower() == 'exit':
                break

            path = 'images'
            download_images(url, path)
            for message in log_messages:
                print(message)

        except KeyboardInterrupt:
            print("\nProgram terminated by user (Ctrl+C).")
            break


# Call the function to download images from a URL and save them to a directory
if __name__ == '__main__':
    main()
