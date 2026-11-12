from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from config import db_config
from trainer import train_model
import os
import shutil
import cv2
import numpy as np
import base64
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "rahasia123"
app.secret_key = "absensi_rahasia"


UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ==========================
# LOGIN
# ==========================
@app.route("/", methods=["GET", "POST"])
def login():

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT * FROM admin WHERE username=%s AND password=%s"
        value = (username, password)

        cursor.execute(sql, value)
        admin = cursor.fetchone()

        conn.close()

        if admin:
            session["admin"] = admin
            return redirect("/dashboard")
        else:
            return render_template("login.html")

    conn.close()
    return render_template("login.html")


# ==========================
# DATA KARYAWAN
# ==========================
@app.route("/karyawan")
def karyawan():

     if "admin" not in session:
          return redirect("/")

     conn = mysql.connector.connect(**db_config)
     cursor = conn.cursor(dictionary=True)

     cursor.execute("SELECT * FROM karyawan")
     data = cursor.fetchall()

     conn.close()

     return render_template("karyawan.html", data=data)


# ==========================
# TAMBAH KARYAWAN
# ==========================
@app.route("/tambah_karyawan", methods=["GET", "POST"])
def tambah_karyawan():

    if "admin" not in session:
        return redirect("/")

    if request.method == "POST":

        nama = request.form["nama"]
        jabatan = request.form["jabatan"]
        divisi = request.form["divisi"]
        no_hp = request.form["no_hp"]
        email = request.form["email"]

        foto = request.files["foto"]

        import uuid

        # upload foto
        if foto and foto.filename != "":

            nama_foto = str(uuid.uuid4()) + "_" + foto.filename

            lokasi = "static/uploads/" + nama_foto

            foto.save(lokasi)

            foto_akhir = nama_foto

        else:

            foto_akhir = ""


        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()


        cursor.execute(
            """
            INSERT INTO karyawan
            (nama, jabatan, divisi, no_hp, email, foto)
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (
                nama,
                jabatan,
                divisi,
                no_hp,
                email,
                foto_akhir
            )
        )


        conn.commit()

        id_karyawan = cursor.lastrowid


        cursor.close()
        conn.close()


        return redirect(f"/ambil_dataset/{id_karyawan}")


    return render_template("tambah_karyawan.html")

# ==========================
# EDIT KARYAWAN
# ==========================
@app.route("/edit_karyawan/<int:id>", methods=["GET", "POST"])
def edit_karyawan(id):

    if "admin" not in session:
        return redirect("/")

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)


    if request.method == "POST":

        cursor.execute(
            "SELECT foto FROM karyawan WHERE id=%s",
            (id,)
        )

        data_lama = cursor.fetchone()

        foto_lama = data_lama["foto"]


        nama = request.form["nama"]
        jabatan = request.form["jabatan"]
        divisi = request.form["divisi"]
        no_hp = request.form["no_hp"]
        email = request.form["email"]


        foto = request.files["foto"]


        # jika upload foto baru
        if foto and foto.filename != "":

            import uuid

            nama_foto = str(uuid.uuid4()) + "_" + foto.filename

            lokasi = "static/uploads/" + nama_foto

            foto.save(lokasi)

            foto_akhir = nama_foto


        else:

            foto_akhir = foto_lama



        cursor.execute(
            """
            UPDATE karyawan
            SET nama=%s,
                jabatan=%s,
                divisi=%s,
                no_hp=%s,
                email=%s,
                foto=%s
            WHERE id=%s
            """,
            (
                nama,
                jabatan,
                divisi,
                no_hp,
                email,
                foto_akhir,
                id
            )
        )


        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/karyawan")



    cursor.execute(
        "SELECT * FROM karyawan WHERE id=%s",
        (id,)
    )

    data = cursor.fetchone()


    cursor.close()
    conn.close()


    return render_template(
        "edit_karyawan.html",
        data=data
    )

# ==========================
# DASHBOARD
# ==========================
@app.route("/dashboard")
def dashboard():

    print(session)

    if "admin" not in session:
        return redirect("/")

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Total Karyawan
    cursor.execute("SELECT COUNT(*) FROM karyawan")
    total_karyawan = cursor.fetchone()[0]


    # Hadir Hari Ini
    cursor.execute("""
        SELECT COUNT(*)
        FROM presensi
        WHERE tanggal = CURDATE()
    """)
    hadir_hari_ini = cursor.fetchone()[0]


    # Belum Hadir
    belum_hadir = total_karyawan - hadir_hari_ini


    # Recent Attendance Hari Ini
    cursor.execute("""
        SELECT
            karyawan.nama,
            presensi.jam_masuk,
            presensi.jam_pulang,
            presensi.status
        FROM presensi
        JOIN karyawan
            ON presensi.id_karyawan = karyawan.id
        WHERE presensi.tanggal = CURDATE()
        ORDER BY presensi.id DESC
        LIMIT 5
    """)

    recent_attendance = cursor.fetchall()

    print(recent_attendance)


    cursor.close()
    conn.close()


    return render_template(
        "dashboard.html",
        total_karyawan=total_karyawan,
        hadir_hari_ini=hadir_hari_ini,
        belum_hadir=belum_hadir,
        recent_attendance=recent_attendance
    )


@app.route("/logout")
def logout():
    print("LOGOUT DIJALANKAN")  
    session.clear()
    return redirect("/")


@app.route("/proses_training")
def proses_training():

    print("MULAI TRAINING")

    if "admin" not in session:
        return redirect("/")


    berhasil, jumlah = train_model()


    print("Total wajah:", jumlah)


    if berhasil:
        session["total_wajah"] = jumlah
        flash(f"Training selesai. Total wajah yang dilatih : {jumlah}")


    return redirect("/training")
# ==========================
# HAPUS KARYAWAN
# ==========================


@app.route("/hapus_karyawan/<int:id>")
def hapus_karyawan(id):

    print("ID YANG DIHAPUS:", id)   

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Ambil nama file foto
    cursor.execute("SELECT foto FROM karyawan WHERE id=%s", (id,))
    data = cursor.fetchone()

    if data and data[0]:
        path_foto = os.path.join(app.config["UPLOAD_FOLDER"], data[0])

        if os.path.exists(path_foto):
            os.remove(path_foto)


        # HAPUS DATASET WAJAH
    # HAPUS DATASET WAJAH
    folder_dataset = os.path.join(
        "dataset",
        f"User_{id}"
    )

    if os.path.exists(folder_dataset):


        shutil.rmtree(folder_dataset)

        print("Dataset terhapus:", folder_dataset)


    # Hapus riwayat presensi dulu
    cursor.execute(
        "DELETE FROM presensi WHERE id_karyawan=%s",
        (id,)
    )


    # Baru hapus data karyawan
    cursor.execute(
        "DELETE FROM karyawan WHERE id=%s",
        (id,)
    )

    conn.commit()

    conn.close()

    return redirect("/karyawan")
# ==========================
# AMBIL DATASET WAJAH
# ==========================
@app.route("/ambil_dataset/<int:id>")
def ambil_dataset(id):

    if "admin" not in session:
        return redirect("/")

    dataset_path = f"dataset/User_{id}"

    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    return render_template(
        "ambil_dataset.html",
        id=id
    )

# ==========================
# HALAMAN PRESENSI
# ==========================
@app.route("/presensi")
def presensi():


    if "admin" not in session:
        return redirect("/")
    
    return render_template("presensi.html")


# ==========================
# HALAMAN Training
# ==========================
@app.route("/training")
def training():

    if "admin" not in session:
        return redirect("/")

    import os

    model_ready = os.path.exists(
        "trainer/trainer.yml"
    )


    total_wajah = session.get(
        "total_wajah"
    )


    return render_template(
        "training.html",
        model_ready=model_ready,
        total_wajah=total_wajah
    )

# ==========================
# Mulai Training
# ==========================
@app.route("/mulai_training")
def mulai_training():

    if "admin" not in session:
        return redirect("/")

    import subprocess

    subprocess.run(["python", "trainer.py"])

    return render_template("training_sukses.html")

# ==========================
# RIWAYAT PRESENSI
# ==========================
@app.route("/riwayat_presensi")
def riwayat_presensi():


    if "admin" not in session:
        return redirect("/")
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            presensi.id,
            karyawan.nama,
            karyawan.jabatan,
            karyawan.divisi,
            presensi.tanggal,
            presensi.jam_masuk,
            presensi.jam_pulang,
            presensi.status
        FROM presensi
        JOIN karyawan
        ON presensi.id_karyawan = karyawan.id
        ORDER BY presensi.id DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("riwayat_presensi.html", data=data)


@app.route("/presensi_masuk")
def presensi_masuk():

    if "admin" not in session:
        return redirect("/")

    if not os.path.exists("trainer/trainer.yml"):
        flash("Model wajah belum tersedia. Lakukan training terlebih dahulu.")
        return redirect("/training")

    return render_template(
        "kamera_presensi.html",
        jenis="masuk"
    )



@app.route("/presensi_pulang")
def presensi_pulang():

    if "admin" not in session:
        return redirect("/")

    if not os.path.exists("trainer/trainer.yml"):
        flash("Model wajah belum tersedia. Lakukan training terlebih dahulu.")
        return redirect("/training")

    return render_template(
        "kamera_presensi.html",
        jenis="pulang"
    )


from openpyxl import Workbook
from flask import send_file
import os


@app.route("/export_excel")
def export_excel():

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)


    cursor.execute("""
        SELECT 
            nama,
            jabatan,
            divisi,
            tanggal,
            jam_masuk,
            jam_pulang,
            status
        FROM presensi
        JOIN karyawan 
        ON presensi.id_karyawan = karyawan.id
    """)


    data = cursor.fetchall()


    wb = Workbook()

    ws = wb.active
    ws.title = "Riwayat Presensi"

    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.utils import get_column_letter


    ws.append([
        "Nama",
        "Jabatan",
        "Divisi",
        "Tanggal",
        "Jam Masuk",
        "Jam Pulang",
        "Status"
    ])

        # Style header
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")
        cell.fill = PatternFill(
            start_color="DDDDDD",
            end_color="DDDDDD",
            fill_type="solid"
        )


    for row in data:

        ws.append([
            row["nama"],
            row["jabatan"],
            row["divisi"],
            row["tanggal"],
            row["jam_masuk"],
            row["jam_pulang"],
            row["status"]
        ])

# Atur lebar kolom otomatis

    for column in ws.columns:

        max_length = 0

        column_letter = get_column_letter(column[0].column)

        for cell in column:
            if cell.value:
                max_length = max(
                    max_length,
                    len(str(cell.value))
                )

        ws.column_dimensions[column_letter].width = max_length + 5

    cursor.close()
    conn.close()


    file_path = "exports/riwayat_presensi.xlsx"

    wb.save(file_path)


    return send_file(
        file_path,
        as_attachment=True
    )



@app.route("/api/dataset/<int:id>", methods=["POST"])
def simpan_dataset(id):

    if "admin" not in session:
        return {"message": "Akses ditolak"}, 401

    try:
        data = request.get_json()
        image_data = data["image"].split(",")[1]
        image_bytes = base64.b64decode(image_data)

        image_array = np.frombuffer(
            image_bytes,
            dtype=np.uint8
        )

        frame = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR
        )

        if frame is None:
            return {
                "count": 0,
                "message": "Gambar tidak terbaca",
                "done": False
            }

        face_detector = cv2.CascadeClassifier(
            "haarcascade/haarcascade_frontalface_default.xml"
        )

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        dataset_path = f"dataset/User_{id}"
        os.makedirs(dataset_path, exist_ok=True)

        foto_tersimpan = len([
            f for f in os.listdir(dataset_path)
            if f.endswith(".jpg")
        ])

        if foto_tersimpan >= 100:
            return {
                "count": foto_tersimpan,
                "message": "Dataset sudah mencapai 100 foto",
                "done": True
            }

        if len(faces) == 0:
            return {
                "count": foto_tersimpan,
                "message": "Wajah belum terdeteksi",
                "done": False
            }

        x, y, w, h = max(
            faces,
            key=lambda face: face[2] * face[3]
        )

        face = gray[y:y+h, x:x+w]
        nomor = foto_tersimpan + 1

        cv2.imwrite(
            f"{dataset_path}/User.{id}.{nomor}.jpg",
            face
        )

        foto_tersimpan += 1

        return {
            "count": foto_tersimpan,
            "message": f"Foto berhasil disimpan: {foto_tersimpan}/100",
            "done": foto_tersimpan >= 100
        }

    except Exception as e:
        return {
            "count": 0,
            "message": str(e),
            "done": False
        }, 500


@app.route("/api/presensi/<jenis>", methods=["POST"])
def proses_presensi_browser(jenis):

    print("ENDPOINT PRESENSI TERPANGGIL:", jenis, flush=True)

    if "admin" not in session:
        return {"message": "Akses ditolak", "done": True}, 401

    if jenis not in ["masuk", "pulang"]:
        return {"message": "Jenis presensi tidak valid", "done": True}, 400

    conn = None
    cursor = None

    try:
        data = request.get_json()
        image_data = data["image"].split(",")[1]
        image_bytes = base64.b64decode(image_data)

        image_array = np.frombuffer(
            image_bytes,
            dtype=np.uint8
        )

        frame = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR
        )

        if frame is None:
            return {"message": "Gambar tidak terbaca", "done": False}

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier(
            "haarcascade/haarcascade_frontalface_default.xml"
        )

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5
        )

        if len(faces) == 0:
            return {
                "message": "Wajah belum terdeteksi",
                "done": False
            }

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("trainer/trainer.yml")

        x, y, w, h = max(
            faces,
            key=lambda face: face[2] * face[3]
        )
        print("PROSES PENGENALAN WAJAH DIJALANKAN", flush=True)

        id_karyawan, confidence = recognizer.predict(
            gray[y:y+h, x:x+w]
        )

        print("ID KARYAWAN:", id_karyawan, flush=True)
        print("FOTO DITERIMA - WAJAH TERDETEKSI", flush=True)
        print("CONFIDENCE:", confidence, flush=True)

        if confidence > 60:
            return {
                "message": "Wajah tidak dikenali. Coba lagi.",
                "done": False
            }
            

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT nama FROM karyawan WHERE id=%s",
            (id_karyawan,)
        )

        hasil = cursor.fetchone()

        if not hasil:
            return {
                "message": "Data karyawan tidak ditemukan",
                "done": False
            }

        nama = hasil[0]

        sekarang = datetime.now()
        tanggal = sekarang.strftime("%Y-%m-%d")
        jam = sekarang.strftime("%H:%M:%S")

        if jenis == "masuk":

            cursor.execute(
                """
                SELECT id FROM presensi
                WHERE id_karyawan=%s AND tanggal=%s
                """,
                (id_karyawan, tanggal)
            )

            cek = cursor.fetchone()

            if cek:
                pesan = f"{nama}, sudah melakukan presensi masuk"
            else:
                cursor.execute(
                    """
                    INSERT INTO presensi
                    (id_karyawan, tanggal, jam_masuk, status)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (id_karyawan, tanggal, jam, "Hadir")
                )

                conn.commit()
                pesan = f"Presensi masuk berhasil. Selamat datang, {nama}!"

        else:

            cursor.execute(
                """
                SELECT jam_masuk, jam_pulang
                FROM presensi
                WHERE id_karyawan=%s AND tanggal=%s
                """,
                (id_karyawan, tanggal)
            )

            cek = cursor.fetchone()

            if cek is None:
                pesan = f"{nama}, belum melakukan presensi masuk"
            elif cek[1] is not None:
                pesan = f"{nama}, sudah melakukan presensi pulang"
            else:
                cursor.execute(
                    """
                    UPDATE presensi
                    SET jam_pulang=%s
                    WHERE id_karyawan=%s AND tanggal=%s
                    """,
                    (jam, id_karyawan, tanggal)
                )

                conn.commit()
                pesan = f"Presensi pulang berhasil. Sampai jumpa, {nama}!"

        return {
            "message": pesan,
            "done": True,
            "nama": nama
        }

    except Exception as e:
        print("ERROR PRESENSI:", e)

        return {
            "message": "Terjadi kesalahan saat memproses presensi",
            "done": False
        }, 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



if __name__ == "__main__":
    app.run(debug=False)
