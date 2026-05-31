from django.shortcuts import render, redirect
from .models import Mahasiswa, PembayaranUKT


def login(request):
    return render(request, 'login.html')


def dashboard(request):

    data = PembayaranUKT.objects.all()

    total = data.count()
    lunas = data.filter(status="Lunas").count()

    progress = 0
    if total > 0:
        progress = round((lunas / total) * 100)

    return render(request, 'dashboard.html', {
        'data': data,
        'progress': progress
    })


def tambah(request):

    if request.method == 'POST':

        nama = request.POST['nama']
        nim = request.POST['nim']
        prodi = request.POST['prodi']
        semester = request.POST['semester']

        nominal = int(request.POST['nominal'])
        jumlah_bayar = int(request.POST['jumlah_bayar'])

        persentase = int((jumlah_bayar / nominal) * 100)

        if persentase >= 100:
            status = "Lunas"
        elif persentase > 0:
            status = "Cicilan"
        else:
            status = "Belum Bayar"

        deadline = request.POST['deadline']

        mahasiswa = Mahasiswa.objects.create(
            nama=nama,
            nim=nim,
            prodi=prodi,
            semester=semester
        )

        PembayaranUKT.objects.create(
            mahasiswa=mahasiswa,
            nominal=nominal,
            jumlah_bayar=jumlah_bayar,
            persentase=persentase,
            status=status,
            deadline=deadline
        )

        return redirect('/dashboard/')

    return render(request, 'tambah.html')

def edit(request, id):

    pembayaran = PembayaranUKT.objects.get(id=id)

    if request.method == 'POST':

        pembayaran.mahasiswa.nama = request.POST['nama']
        pembayaran.mahasiswa.nim = request.POST['nim']
        pembayaran.mahasiswa.prodi = request.POST['prodi']
        pembayaran.mahasiswa.semester = request.POST['semester']

        pembayaran.nominal = int(request.POST['nominal'])
        pembayaran.jumlah_bayar = int(request.POST['jumlah_bayar'])

        pembayaran.persentase = int(
            (pembayaran.jumlah_bayar / pembayaran.nominal) * 100
        )

        if pembayaran.persentase >= 100:
            pembayaran.status = "Lunas"

        elif pembayaran.persentase > 0:
            pembayaran.status = "Cicilan"

        else:
            pembayaran.status = "Belum Bayar"

        pembayaran.deadline = request.POST['deadline']

        pembayaran.mahasiswa.save()
        pembayaran.save()

        return redirect('/dashboard/')

    return render(request, 'edit.html', {
        'data': pembayaran
    })

def pembayaran(request):

    return render(request, 'pembayaran.html', {
        'data': data
    })

def mahasiswa(request):

    data = Mahasiswa.objects.all().order_by('-id')

    return render(request, 'mahasiswa.html', {
        'data': data
    })

def hapus(request, id):

    pembayaran = PembayaranUKT.objects.get(id=id)

    mahasiswa = pembayaran.mahasiswa

    pembayaran.delete()

    mahasiswa.delete()

    return redirect('/dashboard/')
    
def logout(request):
    return redirect('/')