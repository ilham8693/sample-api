# import package
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel # parent class untuk buat schema di request body
import pandas as pd
from datetime import datetime # untuk mendapatkan waktu terkini

# membuat objek FastAPI
app = FastAPI()

# membuat endpoint -> ketentuan untuk client membuat request
# function (get, put, post, delete)
# url(/...)

# endpoint pertama/root untuk mendapatkan pesan "selamat datang"
@app.get("/")
def getWelcome(): # function untuk menghandle endpoint diatas
    return {
        "msg": "Selamat Datang!"
    }

# enpoint untuk menampilkan semua isi dataset
@app.get("/data")
def getData():
    # melakukan proses pengambilan data dati CSV
    df = pd.read_csv('dataset.csv')

    # mengembalikan reponse isi dataset
    return df.to_dict(orient="records")

# routing/path parameter -> url dinamis -> menyesuaikan dengan data yang ada di server
# endpoint untuk menampilkan data sesuai dengan lokasi
# data dari Rusia -> /data/russia
# data dari Zimbabwe -> /data/zimbabwe
@app.get("/data/{location}")
def getData(location: str):
    # melakukan proses pengambilan data dati CSV
    df = pd.read_csv('dataset.csv')

    # filter data berdasarkan parameter
    result = df[df.location == location]

    # validate hasil ada
    if len(result) == 0:
        # menampilkan pesan error -> data tidak ditemukan
        raise HTTPException(status_code=404, detail="Data not found!")

    # mengembalikan reponse isi dataset
    return result.to_dict(orient="records")

# endpoint untuk menghapus data berdasarkan id
password = 'ilham123'
@app.delete("/data/{id}")
def deleteData(id: int, api_key: str = Header(None)):
    # proses authentication
    if api_key == None or api_key != password:
        #kalau tidak ada kasih pesan error -> Tidak ada akses
        raise HTTPException(status_code=404, details="You don't have access!")
    
    # melakukan proses pengambilan data dati CSV
    df = pd.read_csv('dataset.csv')

    # filter data berdasarkan parameter
    result = df[df.id == id]

    # validate hasil ada
    if len(result) == 0:
        # menampilkan pesan error -> data tidak ditemukan
        raise HTTPException(status_code=404, detail="Data not found!")

    # proses hapus data
    # condition
    result = df[df.id != id]

    # update csv/dataset
    result.to_csv('dataset.csv', index=False)

    return {"msg": "Data has been deleted!"}


class Profile(BaseModel):
    id: int
    name: str
    age: int
    location: str

# endpoint untuk nambah data baru
# perlu ada request body -> perlu membuat schama/model
@app.post("/data")
def createData(profile: Profile):
    # melakukan proses pengambilan data dati CSV
    df = pd.read_csv('dataset.csv')

    # proses menambah baris data
    newData = pd.DataFrame({
        'id': [profile.id],
        'name': [profile.name],
        'age': [profile.age],
        'location': [profile.location],
        'created_at': [datetime.now().date()]
    })

    # concat
    df= pd.concat([df, newData])

    # update csv/dataset
    df.to_csv('dataset.csv', index=False)

    return {"msg": "Data has been created!"}



   

# untuk matiin fastapi
# ctrl + c

