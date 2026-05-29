# Autofill

Auto isi ~bukang~ teks dari data JSON ke gambar menggunakan Python dan Pillow.

Cara pakai:

1. Install dependencies:
   ```
   sudo apt install python3-pip -y
   pip install Pillow
   ```

2. Taruh semua page hasil export Canva ke folder `img/`. Page sudah berisi foto, karena script ini hanya menambahkan teks saja pada gambar.

3. Jalankan script `gen.py`:
   ```
   python3 gen.py
   ```

4. PDF: `merged_output.pdf`.

Kalau bingung, lihat isi folder yang sudah ada.
