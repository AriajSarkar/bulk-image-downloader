# Bulk Image Downloader

Bulk Image Downloader is a web application built with Flask (Python) for the backend and React for the frontend. It allows users to input a URL containing images and downloads those images to a specified directory on the server.

## Features

- Downloads images from a given URL
- Handles relative and absolute image URLs
- Creates a directory for each domain to organize downloaded images

## Technologies Used

- **Flask**
- **React**
- **Axios**
- **BeautifulSoup** (for HTML parsing)
- **Requests** (for HTTP requests)
- **Flask-CORS** (for Cross-Origin Resource Sharing)

## Getting Started

### Prerequisites

Make sure you have Python and Node.js installed on your machine.

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/AriajSarkar/bulk-image-downloader.git
    cd bilk-image-downloader
    ```

2. **Install backend dependencies:**

    ```bash
    cd server
    pip install -r requirements.txt
    python app.py
    ```

3. **Install frontend dependencies:**

    ```bash
    cd web
    npm install
    npm run dev
    ```

### API Endpoints

- `POST /api/download_images`: Downloads images from the provided URL.

    Example:

    ```json
    {
      "url": "https://example.com"
    }
    ```

    Response:

    ```json
    {
      "message": "Images downloaded successfully!",
      "log_messages": [
        "Successfully retrieved HTML content from https://example.com",
        "Found 5 image tags on the page",
        "Created directory: images/example.com",
        "Downloading image 1 from https://example.com/image1.jpg",
        "image1.jpg saved successfully",
        "Downloading image 2 from https://example.com/image2.jpg",
        "image2.jpg saved successfully",
        "Download completed. 0 non-image files were skipped."
      ]
    }
    ```

### Contributing

Feel free to contribute to the project by opening issues or creating pull requests. Any contributions are welcome!

### License

This project is licensed under the **MIT License**. [Learn more](LICENSE).
