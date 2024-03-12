# Bulk Image Downloader

## Overview

The Bulk Image Downloader script is a Python tool crafted for effortlessly downloading images from a specified URL, neatly organizing them in a local directory. Powered by BeautifulSoup for HTML parsing, requests for HTTP interactions, and tqdm for an intuitive download progress display, this script ensures a seamless image retrieval experience. It adeptly handles both relative and absolute image URLs, filtering out non-image files while providing comprehensive logging with color-coded messages for success, errors, and warnings.

## Features

- **Image Downloads:** Fetch images from a designated URL with ease.
- **URL Handling:** Support for both relative and absolute image URLs.
- **Skip Functionality:** Skips non-image files and offers a detailed download summary.
- **Logging:** Provides vivid color-coded messages for clear feedback.

## Requirements

- Python 3.x
- Python pip
- Git
- **Dependencies:**
  - `requests`
  - `beautifulsoup4`
  - `tqdm`
  - `colorama`

## Installation

1. **Clone the Repository:**

    For Termux:
    ```bash
    apt update
    apt upgrade
    apt update
    pkg install python-pip git
    ```

    ```bash
    git clone https://github.com/AriajSarkar/bulk-image-downloader.git
    ```

2. **Navigate to the Project Directory:**
    ```bash
    cd bulk-image-downloader
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Application:**
    ```bash
    python app.py
    ```

## Contributing

Feel free to contribute to the project by submitting issues or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
