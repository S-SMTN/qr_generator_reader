# QR Generator & Scanner (Django + Docker)

## Project Overview

This project is a Django web application for working with QR codes.

It includes two main parts:

- QR Code Generator
- QR Code Scanner (POST + Live modes)

---

## QR Code Generator

The QR generator creates a QR code from a random 16-byte token.

The token is generated using:

```python
secrets.token_urlsafe(16)
```
The generated value is encoded into a QR code and rendered as an SVG image (base64 format).

---

## QR Code Scanner

QR codes are scanned using the device camera (laptop or smartphone).

Two scanning modes are implemented:

### 1. POST Mode
- The user captures a frame from the camera
- The image is sent to the backend via a POST request
- The backend decodes the QR code and returns the result

### 2. Live Mode (AJAX)
- The camera runs in real time
- The frontend sends frames to the backend via AJAX requests
- The backend returns the decoded result instantly

Scanning stops automatically after successful detection

---

## QR Decoding Libraries

The project uses two QR decoding libraries:

### OpenCV
- cv2.QRCodeDetector()
- Fast and lightweight QR recognition
- Used as the first decoding method

### QReader
- More robust for damaged or complex QR codes
- Used as a fallback if OpenCV fails

### Notes

- Both POST and Live scanning modes are supported
- OpenCV is used first, QReader as fallback
- QR generator returns image in .svg format
- By default, frontend sends images in .png format converted to base64 url string
- Backend can also handle images in .svg format for decoding
- QR codes are generated from random tokens
- Fully containerized with Docker

---

## Tech Stack
- Python 3.13
- Django
- OpenCV
- QReader
- CairoSVG
- qrcode
- Docker
- Nginx

---

## Local Setup

### 1. Clone repository

```
git clone https://github.com/S-SMTN/qr_generator_reader.git
cd qr_generator_reader
```

### 2. Create .env file

Create a .env file in the project root:

```
DJANGO_SECRET_KEY=your_secret_key
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 3. Install Docker

Make sure Docker and Docker Compose are installed.

Check:

```
docker --version
docker compose version
```

### 4. Run project

```
docker compose up --build
```

### 5. Open in browser

```
http://127.0.0.1:8000
```

---

## Database

This project does not use a database.

---

## Camera Access

Scanning requires camera access.

---

License

MIT