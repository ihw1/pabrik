from django.contrib import admin
from django.http import HttpResponseRedirect
from pabrik.models import *
from django import forms 
from django.contrib import messages
# import cStringIO as StringIO
# from xhtml2pdf import pisa
# from django.template.loader import get_template
# from django.template import Context
# from django.http import HttpResponse
# from cgi import escape


# def render_to_pdf(template_src, context_dict):
#     template = get_template(template_src)
#     context = Context(context_dict)
#     html  = template.render(context)
#     result = StringIO.StringIO()

#     pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')

#     return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
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
    list_display = ('nama','jumlah','harga','harga_partai')
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
    fields = ['produk','jumlah_produk','diskon']
    extra = 3
    readonly_fields = []
    
    def get_readonly_fields(self, request, obj=None):
        if isinstance(obj,Penjualan):
            if (obj.nomor_surat_jalan is not None and obj.nomor_surat_jalan > 0):
                return ['produk','jumlah_produk']
        return []

class Pembayaran_Inline(admin.TabularInline):
    model = Pembayaran
    extra = 1

class Penjualan_Admin(admin.ModelAdmin):
    inlines = [Penjualan_detail_Inline]
    fields = ['nomor_nota','tgl_jual','customer', 'nomor_surat_jalan', 'nota_gabungan']
    list_display = ('nomor_nota','tgl_jual','customer','harga_total','nota_gabungan','nomor_surat_jalan')
    search_fields = ['nomor_nota','customer__nama']
    actions = ['gabung_nota']
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
                    
            if (o.nomor_surat_jalan is None or o.nomor_surat_jalan <= 0):
                valid = False
                messages.error(request, "Nota " + str(o.nomor_nota) + " belum memiliki surat jalan.")

        if valid:
            nota_gabungan = Nota_gabungan.create(customer)
            nota_gabungan.save()
            for o in obj.all():
                o.nota_gabungan = nota_gabungan
                o.save()
            nota_gabungan.save()

            return HttpResponseRedirect("/admin/pabrik/nota_gabungan/"+str(nota_gabungan.pk)+"/")

    gabung_nota.short_description = 'Buat nota gabungan untuk penjualan yang dipilih'
    
    # def terkirim(self, request, obj):
    #     for o in obj.all():
    #         o.kirim()
    # terkirim.short_description = 'Tandai terkirim untuk penjualan yang dipilih'

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
            if (obj.nomor_surat_jalan is not None and obj.nomor_surat_jalan > 0):
                return ['nomor_nota','tgl_jual','customer']
        return []

admin.site.register(Penjualan, Penjualan_Admin)

class Penjualan_Inline(admin.TabularInline):
    model = Penjualan
    fields = ['nomor_nota','tgl_jual','harga_total', 'nomor_surat_jalan']
    extra = 0
    show_change_link = True
    can_delete = False
    readonly_fields = ('nomor_nota','tgl_jual','harga_total','nomor_surat_jalan')

class Nota_gabungan_Admin(admin.ModelAdmin):
    inlines = [Penjualan_Inline, Pembayaran_Inline]
    fields = ['nomor_nota','tgl_nota','tgl_tagihan','customer','harga_total']
    list_display = ('nomor_nota','tgl_nota','tgl_tagihan','customer','harga_total', 'lunas')
    search_fields = ['nomor_nota','customer__nama']
    readonly_fields = []
    list_filter = ['customer', 'tgl_tagihan']
    actions = ['download', ]

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
    
    def download(self, request, obj):
        id_list = ""
        for o in obj:
            id_list += str(o.pk) + "A"
        id_list = id_list[:len(id_list)-1]
        return HttpResponseRedirect("/pabrik/"+id_list+"/print_nota/")
# render_to_pdf(
#             'print_nota.html',
#             {
#                 'pagesize':'A4',
#                 'mylist': obj.all(),
#             }
#         )
    download.short_description = 'Print nota gabungan yang dipilih'

    def get_actions(self, request):
        actions = super(Nota_gabungan_Admin, self).get_actions(request)
        del actions['delete_selected']
        return actions

admin.site.register(Nota_gabungan, Nota_gabungan_Admin)
class CustomBahanBakuModelChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
             return "%s - Jumlah: %s; Jumlah di Outsource: %s" % (obj.nama, obj.jumlah, obj.jumlah_outsource)

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