from fastapi import FastAPI
from pydantic import BaseModel
from supabase import create_client, Client
from mangum import Mangum


SUPABASE_URL = "https://irbeulpuchvaxuvdsvyc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlyYmV1bHB1Y2h2YXh1dmRzdnljIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUwNDc5MzksImV4cCI6MjA3MDYyMzkzOX0.UrAV2PM7T2vl9IzyFrAfRwwVHFoyxswp-x5pax7MsqE"  
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

last_rfid_uid: str | None = None

app = FastAPI(title="Supabase FastAPI Absensi Sekolah", version="1.0.0")

class kelas(BaseModel):
        nama_kelas: str

class jurusan(BaseModel):
        nama_jurusan: str

class pararel(BaseModel):
        nama_pararel: str
        
class siswa(BaseModel):
        nama_siswa: str
        nis: str
        rfid_uid : str
        kelas_id : int
        jurusan_id : int
        pararel_id : int
        
class absensi(BaseModel):
        siswa_id: int
        tanggal_absen: str | None = None

class RFIDData(BaseModel):
    rfid_uid: str
    
@app.get("/")
def read_root():
    return {"message": "Selamat Datang di API Absensi Sekolah"}
        
# INI CRUD KELAS
@app.post("/kelas")
def tambah_kelas(kelas : kelas):
    data = supabase.table("kelas").insert({"nama_kelas": kelas.nama_kelas}).execute()
    return {"message": "Berhasil Menambahkan Kelas", "data": data.data}

@app.get("/kelas")
def list_kelas(kelas : kelas):
    data = supabase.table("kelas").select("*").execute()
    return {"message": "Berhasil Mendapatkan Data Kelas", "data": data.data}

# INI CRUD JURUSAN
@app.post("/jurusan")
def tambah_jurusan(jurusan : jurusan):
    data = supabase.table("jurusan").insert({"nama_jurusan": jurusan.nama_jurusan}).execute()
    return {"message": "Berhasil Menambahkan Jurusan", "data": data.data}

@app.get("/jurusan")
def list_jurusan():
    data = supabase.table("jurusan").select("*").execute()
    return {"message": "Berhasil Mendapatkan Data Jurusan", "data": data.data}

# INI CRUD PARAREL
@app.post("/pararel")
def tambah_pararel(pararel : pararel):
    data = supabase.table("pararel").insert({"nama_pararel": pararel.nama_pararel}).execute()
    return {"message": "Berhasil Menambahkan Pararel", "data": data.data}

@app.get("/pararel")
def list_pararel():
    data = supabase.table("pararel").select("*").execute()
    return {"message": "Berhasil Mendapatkan Data Pararel", "data": data.data}

# INI CRUD SISWA
@app.get("/siswa")
def list_siswa():
    data = supabase.table("siswa").select("id, nama_siswa, nis, rfid_uid,kelas(id, nama_kelas), jurusan(id, nama_jurusan), pararel(id, nama_pararel) ").execute()
    return {"message": "Berhasil Mendapatkan Data Siswa", "data": data.data}

@app.post("/siswa")
def tambah_siswa(siswa: siswa):
    data = supabase.table("siswa").insert({
        "nama_siswa": siswa.nama_siswa,
        "nis": siswa.nis,
        "rfid_uid": siswa.rfid_uid,
        "kelas_id": siswa.kelas_id,
        "jurusan_id": siswa.jurusan_id,
        "pararel_id": siswa.pararel_id
    }).execute()
    return {"message": "Berhasil Menambahkan Siswa", "data": data.data}


# INI CRUD ABSENSI
@app.get("/absensi")
def list_absensi():
    data = supabase.table("absensi").select("id, tanggal_absen, jam_absen, status, keterangan, siswa(id, nama_siswa, nis, rfid_uid)").execute()
    return {"message": "Berhasil Mendapatkan Data Absensi", "data": data.data}

@app.post("/absensi")
def tambah_absensi(absensi: absensi):
    data = supabase.table("absensi").insert({
        "siswa_id": absensi.siswa_id,
        "tanggal_absen": absensi.tanggal_absen,
    }).execute()
    return {"message": "Berhasil Menambahkan Absensi", "data": data.data}

# === POST UID RFID ===
@app.post("/rfid")
def post_rfid(data: RFIDData):  
    global last_rfid_uid
    last_rfid_uid = data.rfid_uid
    return {
        "message" : "UID RFID Berhasil Diterima",
        "uid" : last_rfid_uid
    }

#  === GET UID RFID ===
@app.get("/rfid")
def get_rfid():
    if last_rfid_uid is None:
        return {"message": "Tidak ada UID RFID yang diterima"}
    return {
        "message": "UID RFID terakhir",
        "uid": last_rfid_uid
    }

handler = Mangum(app)