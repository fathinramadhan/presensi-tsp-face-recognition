# Face Recognition Attendance System

A web-based employee attendance system developed using Python, Flask, MySQL, and OpenCV. This application uses facial recognition technology to identify employees and record attendance automatically.

## Project Overview

The Face Recognition Attendance System is designed to simplify employee attendance management through facial recognition. It uses the Local Binary Patterns Histograms (LBPH) algorithm from OpenCV to recognize registered employee faces.

## Features

- **Face Registration** – Register employee facial data.
- **Face Recognition** – Identify employees using facial recognition.
- **Automatic Attendance** – Record employee attendance after successful face recognition.
- **Employee Management** – Manage employee information.
- **Attendance History** – View employee attendance records.
- **Excel Export** – Export attendance reports into Excel files.
- **Face Model Training** – Train the LBPH recognition model using employee face datasets.

## Technologies

- Python
- Flask
- OpenCV (LBPH)
- MySQL
- NumPy
- Pillow
- OpenPyXL
- HTML, CSS, JavaScript

## Project Structure

```text
presensi-tsp-face-recognition/
├── haarcascade/
│   └── haarcascade_frontalface_default.xml
├── static/
│   └── images/
├── templates/
├── app.py
├── config.py
├── trainer.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

**1. Clone the repository**

```bash
git clone https://github.com/fathinramadhan/presensi-tsp-face-recognition.git
```

**2. Open the project directory**

```bash
cd presensi-tsp-face-recognition
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure MySQL**

Configure your MySQL database connection in `config.py` and prepare the required database and tables.

**5. Run the application**

```bash
python app.py
```

**6. Open the application**

```text
http://127.0.0.1:5000
```

## Notes

- Employee face datasets are not included in this repository for privacy reasons.
- The LBPH training model is generated locally through the training process.
- MySQL must be installed and configured before running the application.
- This project is intended for local development and demonstration.

## Author

**Fathin Ramadhan**

GitHub: [@fathinramadhan](https://github.com/fathinramadhan)
