# Item Management System - Frontend

Frontend aplikasi untuk sistem manajemen item yang terhubung dengan backend API Flask.

## Fitur

### 🔐 Autentikasi
- **Login**: Masuk ke sistem dengan username dan password
- **Register**: Membuat akun baru dengan username, email, dan password
- **Logout**: Keluar dari sistem

### 📦 Manajemen Items
- **View**: Melihat daftar semua items
- **Create**: Menambah item baru dengan nama, harga, store, dan tags
- **Edit**: Mengubah informasi item yang sudah ada
- **Delete**: Menghapus item dengan konfirmasi

### 🏪 Manajemen Stores
- **View**: Melihat daftar semua stores
- **Create**: Menambah store baru dengan nama dan deskripsi
- **Edit**: Mengubah informasi store yang sudah ada
- **Delete**: Menghapus store dengan konfirmasi

### 🏷️ Manajemen Tags
- **View**: Melihat daftar semua tags
- **Create**: Menambah tag baru dengan nama dan deskripsi
- **Edit**: Mengubah informasi tag yang sudah ada
- **Delete**: Menghapus tag dengan konfirmasi

### 📊 Dashboard
- Ringkasan jumlah items, stores, dan tags
- Daftar items terbaru
- Daftar stores terbaru
- Daftar semua tags yang tersedia

## Teknologi yang Digunakan

- **Flask**: Web framework untuk backend
- **Bootstrap 5**: Framework CSS untuk UI yang responsive
- **Font Awesome**: Icon library
- **Requests**: HTTP library untuk API calls
- **Jinja2**: Template engine

## Instalasi dan Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Pastikan Backend API Berjalan
Backend API harus berjalan di `http://127.0.0.1:5000` dengan endpoint:
- `/auth/login` - POST
- `/auth/register` - POST
- `/items` - GET, POST, PUT, DELETE
- `/stores` - GET, POST, PUT, DELETE
- `/tags` - GET, POST, PUT, DELETE

### 3. Jalankan Frontend
```bash
python app.py
```

Frontend akan berjalan di `http://127.0.0.1:8001`

## Struktur File

```
frontend/
├── app.py                 # Aplikasi Flask utama
├── requirements.txt       # Dependencies Python
├── README.md             # Dokumentasi
└── templates/            # Template HTML
    ├── base.html         # Template dasar
    ├── login.html        # Halaman login
    ├── register.html     # Halaman register
    ├── dashboard.html    # Dashboard
    ├── items.html        # Daftar items
    ├── create_item.html  # Form tambah item
    ├── edit_item.html    # Form edit item
    ├── stores.html       # Daftar stores
    ├── create_store.html # Form tambah store
    ├── edit_store.html   # Form edit store
    ├── tags.html         # Daftar tags
    ├── create_tag.html   # Form tambah tag
    └── edit_tag.html     # Form edit tag
```

## API Endpoints yang Digunakan

### Authentication
- `POST /auth/login` - Login user
- `POST /auth/register` - Register user baru

### Items
- `GET /items` - Ambil semua items
- `POST /items` - Buat item baru
- `GET /items/{id}` - Ambil detail item
- `PUT /items/{id}` - Update item
- `DELETE /items/{id}` - Hapus item

### Stores
- `GET /stores` - Ambil semua stores
- `POST /stores` - Buat store baru
- `GET /stores/{id}` - Ambil detail store
- `PUT /stores/{id}` - Update store
- `DELETE /stores/{id}` - Hapus store

### Tags
- `GET /tags` - Ambil semua tags
- `POST /tags` - Buat tag baru
- `GET /tags/{id}` - Ambil detail tag
- `PUT /tags/{id}` - Update tag
- `DELETE /tags/{id}` - Hapus tag

## Fitur UI/UX

### 🎨 Design Modern
- Interface yang clean dan modern dengan Bootstrap 5
- Responsive design untuk desktop dan mobile
- Color scheme yang konsisten

### 🔔 User Feedback
- Flash messages untuk feedback operasi CRUD
- Konfirmasi modal untuk operasi delete
- Auto-hide alerts setelah 5 detik

### 📱 Responsive
- Mobile-friendly interface
- Table responsive untuk data yang banyak
- Navigation yang mudah digunakan

### 🚀 Performance
- Lazy loading untuk data
- Optimized API calls
- Efficient state management

## Cara Penggunaan

1. **Login/Register**: Akses aplikasi dan login atau register akun baru
2. **Dashboard**: Lihat ringkasan data di dashboard
3. **Manage Items**: 
   - Lihat semua items di halaman Items
   - Tambah item baru dengan klik "Tambah Item"
   - Edit item dengan klik icon edit
   - Hapus item dengan klik icon trash
4. **Manage Stores**: 
   - Lihat semua stores di halaman Stores
   - Tambah store baru dengan klik "Tambah Store"
   - Edit store dengan klik icon edit
   - Hapus store dengan klik icon trash
5. **Manage Tags**: 
   - Lihat semua tags di halaman Tags
   - Tambah tag baru dengan klik "Tambah Tag"
   - Edit tag dengan klik icon edit
   - Hapus tag dengan klik icon trash

## Troubleshooting

### Backend API Tidak Terhubung
- Pastikan backend API berjalan di port 5000
- Cek koneksi network
- Periksa endpoint URL di `app.py`

### Session Expired
- Logout dan login kembali
- Clear browser cache jika diperlukan

### Data Tidak Muncul
- Periksa response API di browser developer tools
- Pastikan format data sesuai dengan yang diharapkan

## Contributing

1. Fork repository
2. Buat feature branch
3. Commit changes
4. Push ke branch
5. Buat Pull Request

## License

MIT License 