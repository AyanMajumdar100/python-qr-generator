# Python QR Generator

## Overview

**Python QR Generator** is a desktop-based Python application with a clean GUI that allows you to generate QR codes from URLs quickly and easily. The app provides a live preview of the QR code and lets you download it as a PNG file. Designed for simplicity, it ensures fast QR generation with high error correction.

## Features

- GUI-based QR code generation (Tkinter)
- Supports multiple QR types (URL, WiFi, WhatsApp, Text, Email) – URL fully implemented & rest are coming soon...
- Live QR code preview before saving
- Download QR codes as PNG images
- Threaded generation to keep the GUI responsive
- URL validation to prevent invalid QR codes
- Clean and responsive layout

## Tech Stack

- **Language**: Python  
- **GUI**: Tkinter  
- **QR Generation**: qrcode  
- **Image Handling**: PIL (Pillow)  

## Setup & Run Instructions

### 1. Clone the repository
```bash
git clone https://github.com/AyanMajumdar100/python-qr-generator.git
cd python-qr-generator
````

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### 4. Install required packages

```bash
pip install qrcode[pil] pillow
```

> `tkinter` comes bundled with Python.

### 5. Run the application

```bash
py main.py
```

## Application Screenshots

### 1. Initial screen of the app

![Screen 1](https://raw.githubusercontent.com/AyanMajumdar100/python-qr-generator/main/app-screenshots/Screen%201.png)

### 2. QR code generated preview

![Screen 2](https://raw.githubusercontent.com/AyanMajumdar100/python-qr-generator/main/app-screenshots/Screen%202.png)

### 3. Downloadable QR code as PNG

![Download Screen](https://raw.githubusercontent.com/AyanMajumdar100/python-qr-generator/main/app-screenshots/Download%20screen.png)

## Project Structure

```text
python-qr-generator/
│
├── main.py
├── assets/
│   ├── Poppins-Regular.ttf
│   └── Poppins-SemiBold.ttf
├── src/
│   ├── __init__.py
│   ├── logic.py
│   └── ui.py
├── app-screenshots/
│   ├── Screen 1.png
│   ├── Screen 2.png
│   ├── Coming soon screen.png
│   ├── No URL screen.png
│   └── Download screen.png
├── .gitignore
└── LICENSE
```

## License

This project uses a **proprietary license**.
Refer to the `LICENSE` file for more information.

Built for generating QR codes quickly and easily 
Happy coding with **Python QR Generator** 

```
