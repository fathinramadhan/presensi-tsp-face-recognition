# Face Recognition-Based Attendance System

A web-based employee attendance system developed as an academic research project for The Sounds Project (TSP). This project implements facial recognition technology using Python, Flask, MySQL, and OpenCV.

## Project Overview

This project explores the implementation of facial recognition for employee attendance recording. It uses the **Local Binary Patterns Histograms (LBPH)** algorithm provided by OpenCV to recognize registered employee faces.

The system was developed as a research and application prototype, not as a production system deployed at The Sounds Project.

## Features

- **Admin Login** – Authentication for accessing the application.
- **Employee Management** – Add, view, edit, and delete employee data.
- **Face Registration** – Capture employee facial images through a camera.
- **Face Dataset Collection** – Collect up to 100 facial images for each employee.
- **Face Recognition** – Identify registered employees using the LBPH algorithm.
- **Attendance Recording** – Record employee check-in and check-out.
- **Attendance History** – View recorded attendance data.
- **Excel Export** – Export attendance reports into Excel files.
- **Face Model Training** – Train and save the LBPH recognition model.

## Application Screenshots

### Login Page
![Login Page](screenshots/halaman%20login.png)

### Dashboard
![Dashboard](screenshots/halaman%20dashboard.png)

### Employee Data
![Employee Data](screenshots/halaman%20data%20karyawan.png)

### Add Employee
![Add Employee](screenshots/halaman%20tambah%20karyawan.png)

### Edit Employee
![Edit Employee](screenshots/halaman%20edit%20karyawan.png)

### Face Recognition Attendance
![Attendance](screenshots/halaman%20presensi.png)

### Attendance History
![Attendance History](screenshots/halaman%20riwayat%20presensi.png)

### Face Training
![Face Training](screenshots/halaman%20training%20wajah.png)

## Technologies Used

- Python
- Flask
- OpenCV (LBPH Face Recognition)
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
├── screenshots/
│   ├── halaman login.png
│   ├── halaman dashboard.png
│   ├── halaman data karyawan.png
│   ├── halaman tambah karyawan.png
│   ├── halaman edit karyawan.png
│   ├── halaman presensi.png
│   ├── halaman riwayat presensi.png
│   └── halaman training wajah.png
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

### 1. Clone the Repository

```bash
git clone https://github.com/fathinramadhan/presensi-tsp-face-recognition.git
```

### 2. Navigate to the Project Directory

```bash
cd presensi-tsp-face-recognition
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

Configure the MySQL connection in `config.py`. Prepare the `attendance_db` database and the required tables before running the application.

### 5. Prepare the Face Dataset

Register employee data and collect facial images through the application. The collected images are stored locally in the `dataset/` directory.

### 6. Train the Face Recognition Model

Run the face training process through the application. The generated LBPH model is saved locally at:

```text
trainer/trainer.yml
```

### 7. Run the Application

```bash
python app.py
```

### 8. Open the Application

```text
http://127.0.0.1:5000
```

## Notes

- This project is developed for academic research and demonstration purposes.
- Employee facial datasets are not included in this repository to protect personal data.
- The trained LBPH model is generated locally and is not included in the repository.
- MySQL must be installed and configured before running the application.
- The application is intended for local development and testing.

## Author

**Fathin Ramadhan**

GitHub: [@fathinramadhan](https://github.com/fathinramadhan)
