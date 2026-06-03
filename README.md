# Dashboard-Sistem-Pembayaran-UKT-berbasis-Django

Anggota kelompok 9:
1. Citra Ayuning Ratri (25051204005)
2. Juan Raymond Binsar Taruna Silaen (25051204069)
3. Nadia Hamidah Auliyah (25051204193)
4. Zhafarina Amalia Nur Syandana (25051204194)

Dashboard Sistem Pembayaran UKT berbasis Django merupakan sistem dashboard pembayaran Uang Kuliah Tunggal (UKT) yang dibangun menggunakan bahasa pemrograman Python dengan framework Django sebagai backend dan HTML/CSS sebagai tampilan antarmuka pengguna. Sistem ini dirancang khusus untuk membantu petugas Tata Usaha (TU) dalam mengelola seluruh data pembayaran UKT mahasiswa secara terstruktur, efisien, dan akurat.

Sistem dashboard pembayaran UKT ini memiliki beberapa fitur utama sebagai berikut:

a. Login 

Fitur login berfungsi sebagai pintu masuk sistem yang hanya dapat diakses oleh petugas Tata Usaha (TU) dengan username dan password yang telah ditentukan. Kemudian Sistem melakukan validasi data kredensial secara langsung melalui file views.py dan akan menampilkan pesan kesalahan apabila username atau password tidak sesuai. Apabila login berhasil, pengguna akan diarahkan secara otomatis menuju halaman dashboard utama untuk mengakses seluruh fitur pengelolaan pembayaran UKT.

b. Dashboard

Halaman dashboard merupakan halaman utama yang menampilkan ringkasan informasi pembayaran UKT secara keseluruhan, meliputi:
1. Total mahasiswa yang terdaftar dalam sistem.
2. Jumlah mahasiswa dengan status Lunas, Cicilan, dan Belum Bayar.
3. Ringkasan keuangan berupa total tagihan, total pembayaran yang masuk, dan sisa tagihan.
4. Progress bar animasi yang menampilkan persentase total pembayaran UKT  secara keseluruhan.

Seluruh data pada dashboard dihitung secara dinamis menggunakan Django ORM dengan fungsi agregasi Sum sehingga selalu menampilkan data terkini setiap kali halaman diakses.

c. Data Pembayaran

Fitur data pembayaran menampilkan seluruh data pembayaran mahasiswa dalam bentuk tabel yang memuat informasi nama, NIM, prodi, nominal UKT, jumlah bayar, persentase pembayaran, status pembayaran, dan deadline. Pada halaman ini terdapat:
1. Form input untuk menambahkan data pembayaran baru
2. Kalkulasi otomatis persentase dan status berdasarkan nominal dan jumlah bayar
3. Fitur pencarian data berdasarkan nama atau NIM mahasiswa menggunakan  JavaScript
4. Tombol Edit untuk memperbarui data yang sudah ada
5. Tombol Hapus untuk menghapus data mahasiswa beserta data pembayarannya

d. Data Mahasiswa

Halaman data mahasiswa menampilkan daftar seluruh mahasiswa yang terdaftar dalam sistem beserta informasi NIM, prodi, dan status UKT. Halaman ini mengambil data langsung dari model Mahasiswa menggunakan method cek_status_ukt() yang merupakan implementasi dari konsep enkapsulasi dalam OOP.

e. Kartu Mahasiswa

Fitur kartu mahasiswa menampilkan informasi lengkap mahasiswa dalam bentuk kartu digital yang memuat nama, NIM, prodi, angkatan, semester, dan status keaktifan. Angkatan mahasiswa dihitung secara otomatis menggunakan method angkatan() yang mengambil dua digit pertama NIM, sedangkan status keaktifan dihitung menggunakan method status() berdasarkan jumlah semester mahasiswa.

f. Laporan

Halaman laporan menampilkan daftar mahasiswa yang telah melunasi pembayaran UKT. Data di filter secara otomatis oleh sistem berdasarkan status Lunas sehingga hanya mahasiswa yang sudah lunas yang ditampilkan. Petugas dapat mencetak laporan langsung dari browser menggunakan fitur window.print() yang telah disediakan.

g. Logout

Fitur logout berfungsi untuk mengakhiri sesi pengguna dan mengarahkan kembali ke halaman login, sehingga keamanan akses sistem tetap terjaga setelah petugas selesai menggunakan sistem.

Langkah Menjalankan

Berikut adalah langkah langkah untuk menjalankan Sistem Pembayaran UKT : 
1. Buka folder project menggunakan Visual Studio Code.
2. Buka Terminal pada Visual Studio Code.
3. Pastikan Seluruh file project dan data base telah tersedia. 
4. Jalankan server Django dengan perintah: pyhon manage.py runserver
5. Tunggu hingga server berhasil di jalankan tanpa error.
6. Buka browser kemudian akses alamat: http://127.0.0.1:8000/
7. Halaman login akan di tampilkan.
8. Masukkan username dan password admin yang telah terdaftar.
9. Setelah berhasil login, pengguna akan diarahkan ke dalam dashboard.
10. Pengguna dapat mengakses fitur fitur yang tersedia seperti data mahasiswa, detail mahasiswa, data pembayaran UKT, laporan pembayaran, serta mencetak laporan.
11. Setelah selesai menggunakan sistem, pengguna dapat menekan tombol logout untuk keluar dari aplikasi.

Sistem ini mengimplementasikan seluruh empat konsep utama Pemrograman Berorientasi Objek (PBO) yang seluruhnya diterapkan di dalam file models.py sebagai berikut:

a. Encapsulation (Enkapsulasi)

Enkapsulasi diterapkan dengan membungkus data dan method ke dalam class model Django. Seluruh atribut dan method yang berkaitan dengan data mahasiswa terbungkus di dalam class Mahasiswa, sedangkan seluruh atribut dan method yang berkaitan dengan data pembayaran terbungkus di dalam class PembayaranUKT. Akses dan manipulasi data hanya dapat dilakukan melalui method yang telah didefinisikan di dalam masing-masing class, sehingga data terlindungi dari akses langsung yang tidak terstruktur.

    class Mahasiswa(BaseModel):
        nama = models.CharField(max_length=100)
        nim = models.CharField(max_length=20)
        prodi = models.CharField(max_length=50)
        semester = models.IntegerField()

        def status(self):
            if self.semester > 8:
                return "Nonaktif"
            return "Aktif"

        def angkatan(self):
            return "20" + self.nim[:2]

        def cek_status_ukt(self):
            pembayaran = self.pembayaranukt_set.first()
            if pembayaran:
                return pembayaran.status
            return "Belum Ada Data"


    class PembayaranUKT(BaseModel):
        nominal = models.IntegerField()
        jumlah_bayar = models.IntegerField()
        persentase = models.IntegerField(default=0)
        status = models.CharField(max_length=20)
        deadline = models.DateField()

        def hitung_persentase(self):
            if self.nominal > 0:
                return int((self.jumlah_bayar / self.nominal) * 100)
            return 0

        def hitung_sisa(self):
            return self.nominal - self.jumlah_bayar

        def update_status(self):
            pct = self.hitung_persentase()
            if pct >= 100:
                return "Lunas"
            elif pct > 0:
                return "Cicilan"
            else:
                return "Belum Bayar"


b. Inheritance (Pewarisan)

Pewarisan diterapkan melalui class BaseModel yang merupakan class induk abstrak berisi atribut created_at dan updated_at. Kedua atribut ini diwariskan secara otomatis kepada seluruh class turunannya yaitu Mahasiswa dan PembayaranUKT, sehingga setiap data yang tersimpan ke database secara otomatis memiliki informasi waktu pembuatan dan waktu terakhir diperbarui tanpa perlu mendefinisikan ulang di setiap class.

    class BaseModel(models.Model):
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        class Meta:
            abstract = True

    # Mahasiswa mewarisi BaseModel
    class Mahasiswa(BaseModel):
        ...

    # PembayaranUKT mewarisi BaseModel
    class PembayaranUKT(BaseModel):
        ...


c. Abstraction (Abstraksi)

Abstraksi diterapkan melalui class BaseEntitas yang dibuat menggunakan modul ABC (Abstract Base Class) dari library bawaan Python. Class ini mendefinisikan dua method abstrak yaitu tampil_info() dan hitung() yang berfungsi sebagai kontrak atau blueprint yang mengharuskan setiap class turunannya untuk mengimplementasikan kedua method tersebut. Apabila salah satu method tidak diimplementasikan oleh class turunan, Python akan secara otomatis melempar error sehingga konsistensi implementasi terjaga.

Karena Django memiliki sistem metaclass tersendiri yang tidak kompatibel apabila digabungkan langsung dengan ABC, maka abstraksi diimplementasikan melalui class terpisah yaitu MahasiswaInfo dan PembayaranInfo yang mewarisi BaseEntitas secara langsung.

    from abc import ABC, abstractmethod

    class BaseEntitas(ABC):

        @abstractmethod
        def tampil_info(self):
            pass

        @abstractmethod
        def hitung(self):
            pass


    class MahasiswaInfo(BaseEntitas):
        def __init__(self, nama, nim):
            self.nama = nama
            self.nim = nim

        def tampil_info(self):
            return f"{self.nama} - {self.nim}"

        def hitung(self):
            return len(self.nim)


    class PembayaranInfo(BaseEntitas):
        def __init__(self, nama, status):
            self.nama = nama
            self.status = status

        def tampil_info(self):
            return f"{self.nama} - {self.status}"

        def hitung(self):
            return 0

d. Polymorphism (Polimorfisme)

Polimorfisme diterapkan melalui method tampil_info() dan hitung() yang memiliki nama identik namun menghasilkan perilaku yang berbeda pada setiap class. Hal ini merupakan implementasi dari konsep method overriding dalam OOP, di mana setiap class mendefinisikan ulang method yang sama dengan logika yang berbeda sesuai dengan kebutuhan masing-masing class.

    # Pada class Mahasiswa, tampil_info() menampilkan nama dan NIM

    def tampil_info(self):
        return f"{self.nama} - {self.nim}"

    # hitung() mengembalikan nilai semester

    def hitung(self):
        return self.semester


    # Pada class PembayaranUKT, tampil_info() menampilkan nama dan status pembayaran

    def tampil_info(self):
        return f"{self.mahasiswa.nama} - {self.status}"

    # hitung() mengembalikan nilai persentase pembayaran

    def hitung(self):
        return self.hitung_persentase()


Dengan implementasi ini, method yang sama dapat dipanggil pada object yang berbeda dan menghasilkan output yang berbeda sesuai dengan konteks masing-masing class, yang merupakan inti dari konsep polimorfisme dalam OOP. 


<img width="544" height="268" alt="Gambar Proyek 1" src="https://github.com/user-attachments/assets/f3daa16f-1e89-4890-a13c-7e1852149ea2" />

<img width="544" height="269" alt="Gambar Proyek 2" src="https://github.com/user-attachments/assets/01a21045-126d-4c90-8448-b5a7b89f4337" />

<img width="544" height="269" alt="Gmabar Proyek 3" src="https://github.com/user-attachments/assets/58d66e09-159c-48df-b6eb-571a2cddb6e3" />

<img width="544" height="268" alt="Gambar Proyek 4" src="https://github.com/user-attachments/assets/986cf1e0-4d80-40f1-9d84-0bdcd1d6ccb8" />

<img width="544" height="271" alt="Gambar Proyek 5" src="https://github.com/user-attachments/assets/7a437e68-5dda-496b-b4d4-ed81c1e45ad3" />

<img width="544" height="271" alt="Gambar Proyek 6" src="https://github.com/user-attachments/assets/85956587-8ac4-449a-93f2-944db56db5f6" />

<img width="544" height="265" alt="Gambar Proyek 7" src="https://github.com/user-attachments/assets/27dc9fb2-d40d-4135-99a1-f29462a34504" />

<img width="544" height="269" alt="Gambar Proyek 8" src="https://github.com/user-attachments/assets/6ececc6a-2953-4f09-b517-3aa3773095ee" />

<img width="544" height="269" alt="Gambar Proyek 9" src="https://github.com/user-attachments/assets/242a3c1d-0a69-4824-950e-bf9759e45d27" />

<img width="544" height="269" alt="Gambar Proyek 10" src="https://github.com/user-attachments/assets/1cb4e9b6-dae4-4ae2-ba55-2be34f1c91bd" />

<img width="544" height="274" alt="Gambar Proyek 11" src="https://github.com/user-attachments/assets/74209530-f404-420f-a8cc-ce11a5d8143d" />

<img width="544" height="270" alt="Gambar Proyek 12" src="https://github.com/user-attachments/assets/98f1235d-1667-4beb-8956-fc1f55eb28c9" />
