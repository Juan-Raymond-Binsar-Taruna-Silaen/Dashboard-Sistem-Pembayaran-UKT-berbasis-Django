from django.db import models
from abc import ABC, abstractmethod


#ABSTRACTION
class BaseEntitas(ABC):

    @abstractmethod
    def tampil_info(self):
        pass

    @abstractmethod
    def hitung(self):
        pass


#INHERITANCE
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Mahasiswa(BaseModel):

    nama = models.CharField(max_length=100)
    nim = models.CharField(max_length=20)
    prodi = models.CharField(max_length=50)
    semester = models.IntegerField()

    #POLYMORPHISM
    def tampil_info(self):
        return f"{self.nama} - {self.nim}"

    def hitung(self):
        return self.semester

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

    def __str__(self):
        return self.nama

class PembayaranUKT(BaseModel): 

    mahasiswa = models.ForeignKey(
        Mahasiswa,
        on_delete=models.CASCADE
    )
    nominal = models.IntegerField()
    jumlah_bayar = models.IntegerField()
    persentase = models.IntegerField(default=0)
    status = models.CharField(max_length=20)
    deadline = models.DateField()

    #POLYMORPHISM
    def tampil_info(self):
        return f"{self.mahasiswa.nama} - {self.status}"

    def hitung(self):
        return self.hitung_persentase()

    def hitung_persentase(self):
        if self.nominal > 0:
            return int((self.jumlah_bayar / self.nominal) * 100)
        return 0

    def hitung_sisa(self):
        return self.nominal - self.jumlah_bayar

    def sisa_pembayaran(self):
        return self.nominal - self.jumlah_bayar

    def update_status(self):
        pct = self.hitung_persentase()
        if pct >= 100:
            return "Lunas"
        elif pct > 0:
            return "Cicilan"
        else:
            return "Belum Bayar"

    def __str__(self):
        return f"{self.mahasiswa.nama} - {self.status}"


#ABSTRACTION TERPISAH
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