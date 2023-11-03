from django.shortcuts import render, redirect, reverse
from django. core.mail import send_mail, EmailMultiAlternatives
from rest_framework import viewsets, permissions
from django.http import JsonResponse
from django.conf import settings
from app_store.models import Slider, Brand, SubCategory, Product, Contact
from app_store.serializer import ProductSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app_cart.cart import Cart
from app_cart.views import them_vao_gio_hang
import feedparser
from urllib.parse import urlencode



# Create your views here.
def trang_chu(request):
    # Slider
    sliders = Slider.objects.all()

    # Brand
    brands = Brand.objects.all()

    # Thiết bị gia đình
    subcategories_tbgd = SubCategory.objects.filter(category=1).values('id')
    list_id_subcategories_tbgd = [item['id'] for item in list(subcategories_tbgd)]
    products_tbgd = Product.objects.filter(subcategory__in=list_id_subcategories_tbgd).order_by('-public_day')[:20]

    # Đồ dùng nhà bếp
    subcategories_ddnb = SubCategory.objects.filter(category=2).values('id')
    list_id_subcategories_ddnb = [item['id'] for item in list(subcategories_ddnb)]
    products_ddnb = Product.objects.filter(subcategory__in=list_id_subcategories_ddnb).order_by('-public_day')[:20]

    #giỏ hàng
    cart = Cart(request)

    return render(request, 'index.html', {
        'sliders': sliders,
        'brands': brands,
        'products_tbgd': products_tbgd,
        'products_ddnb': products_ddnb,
        'cart': cart,
    })


def trang_chu_2(request):
    # Slider
    sliders = Slider.objects.all()

    # Brand
    brands = Brand.objects.all()

    # Thiết bị gia đình
    subcategories_tbgd = SubCategory.objects.filter(category=1).values('id')
    list_id_subcategories_tbgd = [item['id'] for item in list(subcategories_tbgd)]
    products_tbgd = Product.objects.filter(subcategory__in=list_id_subcategories_tbgd).order_by('-public_day')[:20]

    # Đồ dùng nhà bếp
    subcategories_ddnb = SubCategory.objects.filter(category=2).values('id')
    list_id_subcategories_ddnb = [item['id'] for item in list(subcategories_ddnb)]
    products_ddnb = Product.objects.filter(subcategory__in=list_id_subcategories_ddnb).order_by('-public_day')[:20]

    # Tính số lần truy cập
    so_lan = 0
    if request.COOKIES.get('so_lan_truy_cap'):
        so_lan = int(request.COOKIES.get('so_lan_truy_cap'))

    response = render(request, 'index-2.html', {
        'sliders': sliders,
        'brands': brands,
        'products_tbgd': products_tbgd,
        'products_ddnb': products_ddnb,
    })

    response.set_cookie('so_lan_truy_cap', so_lan + 1, 5)

    return response


def danh_muc(request, id_subcategory):

    #giỏ hàng
    cart = Cart(request)

    # Đọc danh sách subcategory
    subcategories = SubCategory.objects.order_by('name')

    # Brand
    brands = Brand.objects.all()


    # Lọc sản phẩm theo danh mục
    if id_subcategory == 0:
        products = Product.objects.order_by('-public_day')
        subcategory_name = f'Tất cả sản phẩm ({products.count()})'
    else:
        products = Product.objects.filter(subcategory=id_subcategory).order_by('-public_day')
        subcategory = SubCategory.objects.get(pk=id_subcategory)
        subcategory_name = f'{subcategory.name} ({products.count()})'
    
    #lọc theo giá
    keyword = ''
    price = ''
    if request.GET.get('gia'):
        price = request.GET.get('gia') #
        from_price, to_price = price.split('-')
        '''
         __lte -> Less than or equal
         __gte -> Greater than or equal
         __lt -> Less than
         __gt -> Greater than
        '''
        if id_subcategory == 0:
            keyword = request.GET.get('tu_khoa').strip()
            products = Product.objects.filter(price__gte=from_price).order_by('-public_day')
            if to_price != '':
                products = Product.objects.filter(price__gte=from_price,
                                                  price__lt=to_price).order_by('-public_day')
                if keyword != '':
                    products = Product.objects.filter(price__gte=from_price,
                                                      price__lt=to_price,
                                                      name__contains=keyword).order_by('-public_day')
            subcategory_name = f'Tất cả sản phẩm ({products.count()})' 
        else:
            
            products = Product.objects.filter(subcategory=id_subcategory,
                                              price__gte=from_price).order_by('-public_day')
            if to_price != '':
                products = Product.objects.filter(subcategory=id_subcategory,
                                                  price__gte=from_price,
                                                  price__lt=to_price).order_by('-public_day')
                if keyword != '':
                    products = Product.objects.filter(subcategory=id_subcategory,
                                                  price__gte=from_price,
                                                  price__lt=to_price,
                                                  name__contains=keyword).order_by('-public_day')
            subcategory = SubCategory.objects.get(pk=id_subcategory)
            subcategory_name = f'{subcategory.name} ({products.count()})' 

    # Phân trang
    stories_per_page = 9
    page = request.GET.get('trang', 1)
    paginator = Paginator(products, stories_per_page)
    try:
        products_pager = paginator.page(page)
    except PageNotAnInteger:
        products_pager = paginator.page(1)
    except EmptyPage:
        products_pager = paginator.page(paginator.num_pages)

    return render(request, 'product-list.html', {
        'subcategories': subcategories,
        'products_pager': products_pager,
        'products': products,
        'subcategory_name': subcategory_name,
        'brands': brands,
        'cart': cart,
        'keyword': keyword,
    })


def san_pham(request, id_product):

    #giỏ hàng
    cart = Cart(request)

    # Đọc danh sách subcategory
    subcategories = SubCategory.objects.order_by('name')

    # Brand
    brands = Brand.objects.all()

    # Chi tiết sản phẩm
    product = Product.objects.get(pk=id_product)

    # Sản phẩm liên quan
    subcategory = product.subcategory
    related_products = Product.objects.filter(subcategory=subcategory.pk).exclude(pk=id_product).order_by('-public_day')[:20]
    
    #tên danh mục
    subcategory_name = subcategory.name

    # lấy id danh mục
    subcategory_id = subcategory.pk

    #them_vao_gio_hang
    quantity = 1
    if request.POST.get('btnThemVaoGioHang'):
        quantity = int(request.POST.get('quantity'))
        them_vao_gio_hang(request, id_product, quantity)
        cart = Cart(request)


    return render(request, 'product-detail.html', {
        'subcategories': subcategories,
        'brands': brands,
        'product': product,
        'related_products': related_products,
        'cart': cart,
        'subcategory_name': subcategory_name,
        'subcategory_id': subcategory_id,
        'cart':cart,
        'quantity': quantity,
    })


def lien_he(request):

    #giỏ hàng
    cart = Cart(request)
    chuoi_ket_qua = ''
    if request.POST.get("ho_ten"):
        #gán biến
        ho_ten=request.POST.get('ho_ten')
        dien_thoai=request.POST.get('dien_thoai')
        email=request.POST.get('email')
        tieu_de=request.POST.get('tieu_de')
        tin_nhan=request.POST.get('tin_nhan')

        lien_he = Contact(name=ho_ten,
                          phone_number=dien_thoai,
                          email=email,
                          subject=tieu_de,
                          message=tin_nhan)
        lien_he.save()

         # gửi mail khi không có định dạng HTML
        #noi_dung = 'Chúng tôi nhận được tin nhắn của bạn với nội dung như sau: \n ' 
        #noi_dung += f'{tin_nhan} \n'
        #noi_dung += ' Chúng tôi sẽ phản hồi trong thời gian sớm nhất. Xin chân thành cảm ơn!'
        sender = settings.EMAIL_HOST_USER
        danh_sach_nguoi_nhan  = [email, sender]
        #send_mail(tieu_de, noi_dung, sender,danh_sach_nguoi_nhan)


         # gửi mail khi không có định dạng HTML
        noi_dung = '<p>Chúng tôi nhận được tin nhắn của bạn với nội dung như sau: </p>  ' 
        noi_dung += f'<p><b>{tin_nhan} </b></p>'
        noi_dung += '<p>Chúng tôi sẽ phản hồi trong thời gian sớm nhất. Xin chân thành cảm ơn!  </p>'
        msg = EmailMultiAlternatives(tieu_de, noi_dung, sender,danh_sach_nguoi_nhan)
        msg.attach_alternative(noi_dung,'text/html')
        msg.send()


        chuoi_ket_qua = '''
        <div class="alert alert-success" role="alert">
            Gửi thông tin thành công!
        </div>
        '''
        
        


    return render(request, 'contact.html', {
        'cart': cart,
        'chuoi_ket_qua': chuoi_ket_qua,
    })




def tim_kiem(request):
     #giỏ hàng
    cart = Cart(request)

    # Đọc danh sách subcategory
    subcategories = SubCategory.objects.order_by('name')

    # Brand
    brands = Brand.objects.all()

    #tìm kiếm
    subcategory_name =''
    keyword = ''
    if request.GET.get('tu_khoa'):
        keyword = request.GET.get('tu_khoa').strip()
        products = Product.objects.filter(name__contains=keyword).order_by('-public_day')
        subcategory_name = f'Tìm thấy {products.count()} sản phẩm'

    if request.GET.get('gia'):
        price = request.GET.get('gia')
        keyword = request.GET.get('tu_khoa')
        base_url = reverse('app_store:danh_muc', kwargs={'id_subcategory':0})
        query_tring = urlencode({
            'gia': price,
            'tu_khoa': keyword,
        })
        url = f'{base_url}?{query_tring}'
        return redirect(url)

    # Phân trang:
    
    stories_per_page = 9
    page = request.GET.get('trang', 1)
    paginator = Paginator(products, stories_per_page)
    try:
        products_pager = paginator.page(page)
    except PageNotAnInteger:
        products_pager = paginator.page(1)
    except EmptyPage:
        products_pager = paginator.page(paginator.num_pages)

    return render(request, 'product-list.html', {
        'subcategories': subcategories,
        'products_pager': products_pager,
        'products': products,
        'subcategory_name': subcategory_name,
        'brands': brands,
        'cart': cart,
        'keyword': keyword,
    })




# test chức năng ( của web stories)
def rss(request):
    newfeed = feedparser.parse('http://feeds.feedburner.com/bedtimeshortstories/LYCF')
    entries = newfeed['entries']
    # print(entries[0].keys())
    return render(request,"rss.html", {
        'entries': entries,
    })



#cahsc 1 để đưa thông tin sản phảm ra ngoài
def products_service(request):
    products = Product.objects.all()
    list_products = list(products.values('id', 'name', 'price', 'image'))
    return JsonResponse(list_products, safe=False)


# cashc 2

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.order_by('-public_day')
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAdminUser] #  đọc/ghi
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # chỉ đọc