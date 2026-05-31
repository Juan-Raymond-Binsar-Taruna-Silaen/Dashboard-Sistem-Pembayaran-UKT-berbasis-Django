from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Mahasiswa, PembayaranUKT


def format_rupiah(angka):
    return f"{angka:,.0f}".replace(",", ".")


def login_view(request):
    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'NCJAccess' and password == 'ipk4.0':
            return redirect('/dashboard/')
        else:
            return render(request, 'login.html', {
        'error' : 'username atau password salah'})
    return render(request, 'login.html')


def dashboard(request):

    data = PembayaranUKT.objects.select_related(
        'mahasiswa'
    ).all().order_by('-id')

    total_mahasiswa = Mahasiswa.objects.count()

    lunas = PembayaranUKT.objects.filter(
        status='Lunas'
    ).count()

    cicilan = PembayaranUKT.objects.filter(
        status='Cicilan'
    ).count()

    belum = PembayaranUKT.objects.filter(
        status='Belum Bayar'
    ).count()

    total_tagihan = (
        PembayaranUKT.objects.aggregate(
            Sum('nominal')
        )['nominal__sum'] or 0
    )

    total_masuk = (
        PembayaranUKT.objects.aggregate(
            Sum('jumlah_bayar')
        )['jumlah_bayar__sum'] or 0
    )

    sisa_tagihan = total_tagihan - total_masuk

    progress = 0

    if total_tagihan > 0:
        progress = int(
            (total_masuk / total_tagihan) * 100
        )

    return render(request, 'dashboard.html', {
        'data': data,
        'total_mahasiswa': total_mahasiswa,
        'lunas': lunas,
        'cicilan': cicilan,
        'belum': belum,
        'total_tagihan': format_rupiah(total_tagihan),
        'total_masuk': format_rupiah(total_masuk),
        'sisa_tagihan': format_rupiah(sisa_tagihan),
        'progress': progress,
    })

def mahasiswa(request):
    data_mahasiswa = Mahasiswa.objects.all()
    return render(request, 'mahasiswa.html',{
        'data_mahasiswa' : data_mahasiswa
    })

def detail_mahasiswa(request, id):
    mahasiswa = get_object_or_404(Mahasiswa, id=id)

    return render(request, 'detail_mahasiswa.html', {
        'mhs' : mahasiswa
    })

def tambah(request):

    if request.method == 'POST':

        nama = request.POST['nama']
        nim = request.POST['nim']
        prodi = request.POST['prodi']
        semester = request.POST['semester']
        nominal = int(request.POST['nominal'])
        jumlah_bayar = int(request.POST['jumlah_bayar'])
        status = request.POST['status']
        deadline = request.POST['deadline']

        mahasiswa = Mahasiswa.objects.create(
            nama=nama,
            nim=nim,
            prodi=prodi,
            semester=int(semester)
        )

        p = PembayaranUKT(
            mahasiswa=mahasiswa,
            nominal=nominal,
            jumlah_bayar=jumlah_bayar,
            status=status,
            deadline=deadline
        )

        p.persentase = p.hitung_persentase()
        p.status = p.update_status()
        p.save()

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
        pembayaran.deadline = request.POST['deadline']

        # PANGGIL METHOD DARI MODEL — bukan hitung manual di sini
        pembayaran.persentase = pembayaran.hitung_persentase()
        pembayaran.status = pembayaran.update_status()

        pembayaran.mahasiswa.save()
        pembayaran.save()

        return redirect('/dashboard/')

    return render(request, 'edit.html', {
        'data': pembayaran
    })

def hapus(request, id):
    pembayaran = PembayaranUKT.objects.get(id=id)
    pembayaran.mahasiswa.delete()  
    pembayaran.delete()
    return redirect('/dashboard/')


def pembayaran(request):

    if request.method == 'POST':

        nama = request.POST['nama']
        nim = request.POST['nim']
        prodi = request.POST['prodi']
        semester = request.POST['semester']
        nominal = int(request.POST['nominal'])
        jumlah_bayar = int(request.POST['jumlah_bayar'])
        deadline = request.POST['deadline']

        mahasiswa = Mahasiswa.objects.create(
            nama=nama,
            nim=nim,
            prodi=prodi,
            semester=semester
        )

        p = PembayaranUKT(
            mahasiswa=mahasiswa,
            nominal=nominal,
            jumlah_bayar=jumlah_bayar,
            deadline=deadline
        )

        p.persentase = p.hitung_persentase()
        p.status = p.update_status()
        p.save()

        return redirect('/pembayaran/')

    data = PembayaranUKT.objects.select_related('mahasiswa').all()

    for item in data:
        item.nominal_fmt = format_rupiah(item.nominal)
        item.jumlah_bayar_fmt = format_rupiah(item.jumlah_bayar)

    return render(request, 'pembayaran.html', {
        'data': data
    })
def laporan(request):

    data = PembayaranUKT.objects.select_related(
        'mahasiswa'
    ).filter(status='Lunas')

    return render(request, 'laporan.html', {
        'data': data
    })

def detail_laporan(request, id):

    data = PembayaranUKT.objects.select_related(
        'mahasiswa'
    ).get(id=id)

    return render(request, 'detail_laporan.html',{
        'data': data
    })

def logout_view(request):
    return redirect('/')