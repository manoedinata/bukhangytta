import openpyxl
import json

wb = openpyxl.load_workbook('051_Hendra_SEMUA DATAKU DI SINI!.xlsx', data_only=True)
ws = wb["Mahasiswa"]

data = []
for row in ws.iter_rows(min_row=3, min_col=5, values_only=True):
    nrp, nama, status, _, _, panggilan, kota_asal, ttl, fi = row

    # if status == "Tidak Mengikuti": continue
    if not kota_asal and status != "Tidak Mengikuti":
        print(f"Warning: Missing 'Asal Kota' for NRP {nrp} - {nama}")
 
    tba = {
        "NRP": str(nrp).strip(),
        "Nama": str(nama).strip(),
        "Nama Panggilan": str(panggilan).strip() if status != "Tidak Mengikuti" else "-",
        "Asal Kota": str(kota_asal).strip() if status != "Tidak Mengikuti" else "-",
        "Tempat, Tanggal Lahir": str(ttl).strip() if status != "Tidak Mengikuti" else "-",
        "Status": True if status != "Tidak Mengikuti" else False
    }
    data.append(tba)
    
with open("data.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=True)
