from django.db import models
import datetime
from django.utils import timezone
from django.http import HttpResponse
from decimal import Decimal

def nota_auto_no():
    if Penjualan.objects.count() == 0:
        return 1
    else:
        return Penjualan.objects.order_by('-nomor_nota')[0].nomor_nota + 1

def nota_gabungan_auto_no():
    if Nota_gabungan.objects.count() == 0:
        return 1
    else:
        return Nota_gabungan.objects.order_by('-nomor_nota')[0].nomor_nota + 1

# Create your models here.
class Customer(models.Model):
    nama = models.CharField(max_length=200)
    telp = models.CharField(max_length=50,blank=True, null=True)
    alamat = models.CharField(max_length=200,blank=True, null=True)
    MINGGUAN = '1M'
    BULANAN = '1B'
    JANGKA_KREDIT = (
        (MINGGUAN, 'Mingguan'),
        (BULANAN, 'Bulanan'),
    )
    jangka_waktu_kredit = models.CharField(max_length=2,
                                      choices=JANGKA_KREDIT,
                                      default=BULANAN)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.nama
    
    class Meta:
        verbose_name = "pelanggan"
        verbose_name_plural = "pelanggan"

class Supplier(models.Model):
    nama = models.CharField(max_length=200)
    telp = models.CharField(max_length=50,blank=True, null=True)
    alamat = models.CharField(max_length=200,blank=True, null=True)
    contact_person = models.CharField(max_length=100,blank=True, null=True)
    kategori = models.CharField(max_length=50,blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.nama
    
    class Meta:
        verbose_name = "supplier"
        verbose_name_plural = "supplier"

class Bahan_baku(models.Model):
    nama = models.CharField(max_length=60)
    jumlah = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    jumlah_outsource = models.DecimalField('Jmlh di Mi An', default=0, max_digits=20, decimal_places=2)
    keterangan = models.TextField(blank=True, null=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.nama
    
    class Meta:
        verbose_name = "bahan baku"
        verbose_name_plural = "bahan baku"

class Produk(models.Model):
    nama = models.CharField(max_length=60)
    jumlah = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    harga = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    keterangan = models.TextField(blank=True, null=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = "produk"

class Produk_produksi(models.Model):
    produk = models.ForeignKey(Produk)
    dari_outsource = models.BooleanField('Dari Mi An', default=False)
    tgl_produksi = models.DateField('tgl produksi')
    jumlah = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    keterangan = models.TextField(blank=True, null=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.produk.nama
    
    def minus_bahan(self, jumlah_minus):
        for bahan in self.produk.bahan_baku_produk_set.all():
            if self.dari_outsource:
                bahan.bahan_baku.jumlah_outsource -= (bahan.jumlah_bahan * jumlah_minus)
            else:
                bahan.bahan_baku.jumlah -= (bahan.jumlah_bahan * jumlah_minus)
            bahan.bahan_baku.save()
    
    def bahan_menjadi_produk(self, jumlah_barang):
        self.produk.jumlah += jumlah_barang
        self.minus_bahan(jumlah_barang)
        self.produk.save()
    
    def undo_this_product(self, jumlah_minus):
        jumlah_tambah = (0 - jumlah_minus)
        self.bahan_menjadi_produk(jumlah_tambah)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Produk_produksi.objects.get(pk=self.pk)
            if (orig.produk != self.produk or orig.dari_outsource != self.dari_outsource):
                self.bahan_menjadi_produk(self.jumlah)
                orig.undo_this_product(orig.jumlah)
            elif (orig.jumlah != self.jumlah):
                selisih = self.jumlah - orig.jumlah
                self.bahan_menjadi_produk(selisih)
        else:
            self.bahan_menjadi_produk(self.jumlah)
        
        super(Produk_produksi, self).save(*args, **kwargs)
            
    def delete(self, *args, **kwargs):
        orig = Produk_produksi.objects.get(pk=self.pk)
        orig.undo_this_product(orig.jumlah)
        super(Produk_produksi, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "produksi"
        verbose_name_plural = "produksi"

class Produk_harga_special(models.Model):
    produk = models.ForeignKey(Produk)
    customer = models.ForeignKey(Customer)
    harga = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return ''

    class Meta:
        verbose_name = "harga spesial"
        verbose_name_plural = "harga spesial"

class Bahan_baku_produk(models.Model):
    produk = models.ForeignKey(Produk)
    bahan_baku = models.ForeignKey(Bahan_baku)
    jumlah_bahan = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return ''

    class Meta:
        verbose_name = "bahan baku"
        verbose_name_plural = "bahan baku"

class Outsource(models.Model):
    tgl_outsource = models.DateField('tanggal')
    keterangan = models.TextField(blank=True, null=True)

    def delete(self, *args, **kwargs):
        for detail in self.outsource_detail_set.all():
            detail.delete()
        super(Outsource, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Kiriman ke Mi An"
        verbose_name_plural = "Kiriman ke Mi An"

class Outsource_detail(models.Model):
    outsource = models.ForeignKey(Outsource)
    bahan_baku = models.ForeignKey(Bahan_baku)
    jumlah_outsource = models.DecimalField('jumlah', default=0, max_digits=20, decimal_places=2)
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return ''
    
    def outsource_bahan_baku(self, jumlah_outsource):
        self.bahan_baku.jumlah_outsource += jumlah_outsource
        self.bahan_baku.jumlah -= jumlah_outsource
        self.bahan_baku.save()
    
    def undo_outsource_bahan_baku(self, jumlah_undo):
        jumlah_minus = (0 - jumlah_undo)
        self.outsource_bahan_baku(jumlah_minus)
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Outsource_detail.objects.get(pk=self.pk)
            self.outsource_bahan_baku(self.jumlah_outsource)
            orig.undo_outsource_bahan_baku(orig.jumlah_outsource)
        else:
            self.outsource_bahan_baku(self.jumlah_outsource)
                    
        super(Outsource_detail, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        orig = Outsource_detail.objects.get(pk=self.pk)
        orig.undo_outsource_bahan_baku(orig.jumlah_outsource)
        super(Outsource_detail, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "rincian"
        verbose_name_plural = "rincian"

class Pembelian(models.Model):
    nomor_nota = models.IntegerField(default=0)
    tgl_beli = models.DateField('tanggal')
    supplier = models.ForeignKey(Supplier)
    harga_total = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    keterangan = models.TextField(blank=True, null=True)

    def delete(self, *args, **kwargs):
        for detail in self.pembelian_detail_set.all():
            detail.delete()
        super(Pembelian, self).delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "pembelian"

class Pembelian_detail(models.Model):
    pembelian = models.ForeignKey(Pembelian)
    bahan_baku = models.ForeignKey(Bahan_baku)
    jumlah_beli = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    harga_bahan = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return ''
    
    def add_bahan_baku(self, jumlah_tambah):
        self.bahan_baku.jumlah += jumlah_tambah
        self.bahan_baku.save()
    
    def minus_bahan_baku(self, jumlah_tambah):
        jumlah_minus = (0 - jumlah_tambah)
        self.add_bahan_baku(jumlah_minus)
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Pembelian_detail.objects.get(pk=self.pk)
            if (orig.bahan_baku != self.bahan_baku):
                self.add_bahan_baku(self.jumlah_beli)
                orig.minus_bahan_baku(orig.jumlah_beli)
            elif (orig.jumlah_beli != self.jumlah_beli):
                self.add_bahan_baku((self.jumlah_beli - orig.jumlah_beli))
        else:
            self.add_bahan_baku(self.jumlah_beli)
                    
        super(Pembelian_detail, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        orig = Pembelian_detail.objects.get(pk=self.pk)
        orig.minus_bahan_baku(orig.jumlah_beli)
        super(Pembelian_detail, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "rincian"
        verbose_name_plural = "rincian"

class Nota_gabungan(models.Model):
    nomor_nota = models.IntegerField(default=nota_gabungan_auto_no, unique=True)
    tgl_nota = models.DateField('tgl nota', auto_now_add = True, blank=True, null=True)
    tgl_tagihan = models.DateField('tgl tagihan', blank=True, null=True)
    customer = models.ForeignKey(Customer)
    harga_total = models.DecimalField(default=0,max_digits=20, decimal_places=2)
    keterangan = models.TextField(blank=True, null=True)

    @classmethod
    def create(cls, customer):
        nota_gabungan = cls(customer = customer)
        if customer.jangka_waktu_kredit == Customer.MINGGUAN:
            nota_gabungan.tgl_tagihan = datetime.datetime.now()+datetime.timedelta(days=7)
        elif customer.jangka_waktu_kredit == Customer.BULANAN:
            nota_gabungan.tgl_tagihan = datetime.datetime.now()+datetime.timedelta(weeks=4)
        
        return nota_gabungan

    def lunas(self):
        bayar = 0
        for pembayaran in self.pembayaran_set.all():
            bayar += pembayaran.jumlah_bayar
        return (bayar >= self.harga_total)
    lunas.admin_order_field = ''
    lunas.boolean = True
    lunas.short_description = 'Lunas?'

    def hitung_harga_total(self):
        total = 0
        for detail in self.penjualan_set.all():
            total += detail.harga_total
        return total
    
    def save(self, *args, **kwargs):
        self.harga_total = self.hitung_harga_total()
        super(Nota_gabungan, self).save(*args, **kwargs)

    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.nomor_nota)

    class Meta:
        verbose_name_plural = "Nota Gabungan"

class Penjualan(models.Model):
    nota_gabungan = models.ForeignKey(Nota_gabungan, blank=True, null=True)
    nomor_nota = models.IntegerField(default=nota_auto_no, unique=True)
    tgl_jual = models.DateField('tanggal')
    customer = models.ForeignKey(Customer)
    harga_total = models.DecimalField(default=0,max_digits=20, decimal_places=2)
    terkirim = models.BooleanField(default=False)
    keterangan = models.TextField(blank=True, null=True)

    def kirim(self):
        if self.terkirim:
            return
        for detail in self.penjualan_detail_set.all():
            detail.produk.jumlah -= detail.jumlah_produk
            detail.produk.save()
        self.terkirim = True
        self.save()
    
    # def lunas(self):
    #     bayar = 0
    #     for pembayaran in self.penjualan_pembayaran_set.all():
    #         bayar += pembayaran.jumlah_bayar
    #     return (bayar >= self.harga_total)
    # lunas.admin_order_field = ''
    # lunas.boolean = True
    # lunas.short_description = 'Lunas?'

    def hitung_harga_total(self):
        total = 0
        for detail in self.penjualan_detail_set.all():
            total += (detail.hitung_harga() * detail.jumlah_produk)
        return total
    
    def save(self, *args, **kwargs):
        self.harga_total = self.hitung_harga_total()
        super(Penjualan, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for detail in self.penjualan_detail_set.all():
            detail.delete()
        super(Penjualan, self).delete(*args, **kwargs)

    def __unicode__(self):  # Python 3: def __str__(self):
        return ''

    class Meta:
        verbose_name_plural = "penjualan"

class Penjualan_detail(models.Model):
    penjualan = models.ForeignKey(Penjualan)
    produk = models.ForeignKey(Produk)
    jumlah_produk = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    harga_produk = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return ''

    def harga_total(self):
        return (self.jumlah_produk * self.harga_produk).quantize(Decimal('.01'))
    
    def hitung_harga(self):
        try:
            harga_special = self.produk.produk_harga_special_set.get(customer = self.penjualan.customer)
        except Produk_harga_special.DoesNotExist:
            return self.produk.harga
        return harga_special.harga
    
    def save(self, *args, **kwargs):
        if (self.penjualan.terkirim):
            return
                    
        self.harga_produk = self.hitung_harga()
        super(Penjualan_detail, self).save(*args, **kwargs)
        # update penjualan harus setelah update penjualan_detail
        self.penjualan.harga_total = self.penjualan.hitung_harga_total()
        self.penjualan.save()
            
    def delete(self, *args, **kwargs):
        if (self.penjualan.terkirim):
            return

        super(Penjualan_detail, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "rincian"
        verbose_name_plural = "rincian"

class Pembayaran(models.Model):
    nota_gabungan = models.ForeignKey(Nota_gabungan)
    tgl_bayar = models.DateField('tanggal')
    jumlah_bayar = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return ''

    class Meta:
        verbose_name_plural = "pembayaran"

class Penyusutan(models.Model):
    tgl_penyusutan = models.DateField('tanggal')
    di_outsource = models.BooleanField('Di Mi An', default=False)
    bahan_baku = models.ForeignKey(Bahan_baku)
    sisa_di_gudang = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    jumlah_susut = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    keterangan = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "penyusutan"
        verbose_name_plural = "penyusutan"

    def set_jumlah_setelah_susut(self):
        if self.di_outsource:
            self.jumlah_susut = self.bahan_baku.jumlah_outsource - self.sisa_di_gudang
            self.bahan_baku.jumlah_outsource = self.sisa_di_gudang
        else:
            self.jumlah_susut = self.bahan_baku.jumlah - self.sisa_di_gudang
            self.bahan_baku.jumlah = self.sisa_di_gudang
        self.bahan_baku.save()

    def undo_set_jumlah_bahan_setelah_susut(self):
        if self.di_outsource:
            self.bahan_baku.jumlah_outsource = self.sisa_di_gudang + self.jumlah_susut
        else:
            self.bahan_baku.jumlah = self.sisa_di_gudang + self.jumlah_susut
        self.bahan_baku.save()

    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Penyusutan.objects.get(pk=self.pk)
            orig.undo_set_jumlah_bahan_setelah_susut()
            if orig.bahan_baku.nama == self.bahan_baku.nama:
                #karena jumlah bahan baku sudah diundo
                self.bahan_baku = orig.bahan_baku
            self.set_jumlah_setelah_susut()
        else:
            self.set_jumlah_setelah_susut()
        super(Penyusutan, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        orig = Penyusutan.objects.get(pk=self.pk)
        orig.undo_set_jumlah_bahan_setelah_susut()
        super(Penyusutan, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "penyusutan"
        verbose_name_plural = "penyusutan"
