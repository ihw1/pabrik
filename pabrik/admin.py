from django.contrib import admin
from django.http import HttpResponseRedirect
from pabrik.models import *
from django import forms 
from django.contrib import messages

class Customer_Admin(admin.ModelAdmin):
    list_display = ('nama','telp','alamat')
    search_fields = ['nama']

admin.site.register(Customer,Customer_Admin)

class Supplier_Admin(admin.ModelAdmin):
    list_display = ('nama','telp','notes')
    search_fields = ['nama']
    list_filter = ['kategori']

admin.site.register(Supplier,Supplier_Admin)

class Bahan_baku_Admin(admin.ModelAdmin):
    list_display = ('nama','jumlah','jumlah_outsource')
    search_fields = ['nama']
    readonly_fields = ['jumlah','jumlah_outsource']

admin.site.register(Bahan_baku,Bahan_baku_Admin)

class Produk_harga_special_Inline(admin.TabularInline):
    model = Produk_harga_special
    extra = 1

class Bahan_baku_produk_Inline(admin.TabularInline):
    model = Bahan_baku_produk
    extra = 1

class Produk_Admin(admin.ModelAdmin):
    inlines = [Bahan_baku_produk_Inline,Produk_harga_special_Inline]
    list_display = ('nama','jumlah',)
    search_fields = ['nama']
    readonly_fields = ['jumlah']

admin.site.register(Produk,Produk_Admin)

class Produksi_Admin(admin.ModelAdmin):
    list_display = ('produk','dari_outsource','tgl_produksi','jumlah',)
    search_fields = ['produk__nama']
    list_filter = ['produk__nama']
    
    def get_actions(self, request):
        actions = super(Produksi_Admin, self).get_actions(request)
        del actions['delete_selected']
        return actions

admin.site.register(Produk_produksi,Produksi_Admin)

class Outsource_detail_Inline(admin.TabularInline):
    model = Outsource_detail
    fields = ['bahan_baku','jumlah_outsource']
    extra = 3

class Outsource_Admin(admin.ModelAdmin):
    inlines = [Outsource_detail_Inline]
    list_display = ('tgl_outsource', 'keterangan')

    def get_actions(self, request):
        actions = super(Outsource_Admin, self).get_actions(request)
        del actions['delete_selected']
        return actions

admin.site.register(Outsource, Outsource_Admin)

class Pembelian_detail_Inline(admin.TabularInline):
    model = Pembelian_detail
    fields = ['bahan_baku','jumlah_beli']
    extra = 3

class Pembelian_Admin(admin.ModelAdmin):
    inlines = [Pembelian_detail_Inline]
    list_display = ('nomor_nota','tgl_beli')
    search_fields = ['nomor_nota']

    def get_actions(self, request):
        actions = super(Pembelian_Admin, self).get_actions(request)
        del actions['delete_selected']
        return actions

admin.site.register(Pembelian, Pembelian_Admin)

class Penjualan_detail_Inline(admin.TabularInline):
    model = Penjualan_detail
    fields = ['produk','jumlah_produk']
    extra = 3
    readonly_fields = []
    
    def get_readonly_fields(self, request, obj=None):
        if isinstance(obj,Penjualan):
            if obj.terkirim:
                return ['produk','jumlah_produk']
        return []

class Pembayaran_Inline(admin.TabularInline):
    model = Pembayaran
    extra = 1

class Penjualan_Admin(admin.ModelAdmin):
    inlines = [Penjualan_detail_Inline]
    fields = ['nomor_nota','tgl_jual','customer', 'nota_gabungan']
    list_display = ('nomor_nota','tgl_jual','customer','harga_total','nota_gabungan','terkirim')
    search_fields = ['nomor_nota','customer__nama']
    actions = ['terkirim', 'gabung_nota']
    readonly_fields = []
    list_filter = ['customer']
    
    def gabung_nota(self, request, obj):
        valid = True
        customer = None
        for o in obj.all():
            if customer == None:
                customer = o.customer
            else:
                if o.customer != customer:
                    valid = False
                    messages.error(request, "Customer yang dipilih harus sama.")

        if valid:
            nota_gabungan = Nota_gabungan.create(customer)
            nota_gabungan.save()
            for o in obj.all():
                o.nota_gabungan = nota_gabungan
                o.save()
            nota_gabungan.save()

        return HttpResponseRedirect("/admin/pabrik/nota_gabungan/"+str(nota_gabungan.pk)+"/")

    gabung_nota.short_description = 'Buat nota gabungan untuk penjualan yang dipilih'
    
    def terkirim(self, request, obj):
        for o in obj.all():
            o.kirim()
    terkirim.short_description = 'Tandai terkirim untuk penjualan yang dipilih'

    def get_actions(self, request):
        actions = super(Penjualan_Admin, self).get_actions(request)
        del actions['delete_selected']
        return actions
    
    def response_change(self, request, obj, *args, **kwargs):
        if request.POST.has_key("nota"):
            return HttpResponseRedirect("/pabrik/"+str(obj.pk)+"/nota")
    
        return super(Penjualan_Admin, self).response_change(request, obj, *args, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if isinstance(obj,Penjualan):
            if obj.terkirim:
                return ['nomor_nota','tgl_jual','customer']
        return []

admin.site.register(Penjualan, Penjualan_Admin)

class Penjualan_Inline(admin.TabularInline):
    model = Penjualan
    fields = ['nomor_nota','tgl_jual','harga_total', ]
    extra = 0
    show_change_link = True
    can_delete = False
    readonly_fields = ('nomor_nota','tgl_jual','harga_total',)

class Nota_gabungan_Admin(admin.ModelAdmin):
    inlines = [Penjualan_Inline, Pembayaran_Inline]
    fields = ['nomor_nota','tgl_nota','tgl_tagihan','customer','harga_total']
    list_display = ('nomor_nota','tgl_nota','tgl_tagihan','customer','harga_total', 'lunas')
    search_fields = ['nomor_nota','customer__nama']
    readonly_fields = []
    list_filter = ['customer', 'tgl_tagihan']

    def has_delete_permission(self, request, obj=None):
        return False

    def response_change(self, request, obj, *args, **kwargs):
        if request.POST.has_key("nota"):
            return HttpResponseRedirect("/pabrik/"+str(obj.pk)+"/nota_gabungan")
    
        return super(Nota_gabungan_Admin, self).response_change(request, obj, *args, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if isinstance(obj,Nota_gabungan):
            return ['nomor_nota', 'tgl_nota','customer', 'harga_total']
        return []

admin.site.register(Nota_gabungan, Nota_gabungan_Admin)
class CustomBahanBakuModelChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
             return "%s - Jumlah: %s; Jumlah di Mi An: %s" % (obj.nama, obj.jumlah, obj.jumlah_outsource)

class PenyusutanAdminForm(forms.ModelForm):
    bahan_baku = CustomBahanBakuModelChoiceField(queryset=Bahan_baku.objects.all()) 
    class Meta:
          model = Penyusutan
          fields = ('tgl_penyusutan', 'di_outsource', 'bahan_baku', 'sisa_di_gudang', 'jumlah_susut', 'keterangan')
    
class Penyusutan_Admin(admin.ModelAdmin):
    list_display = ('tgl_penyusutan', 'di_outsource', 'bahan_baku', 'jumlah_susut', 'keterangan')
    list_filter = ['bahan_baku__nama', 'di_outsource']
    readonly_fields = ['jumlah_susut']
    form = PenyusutanAdminForm

admin.site.register(Penyusutan,Penyusutan_Admin)