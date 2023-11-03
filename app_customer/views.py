from django.shortcuts import render, redirect
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.conf import settings
from app_customer.models import Customer
from app_cart.cart import Cart
from app_cart.models import Order, OrderItem
from app_store.models import Product
from django.template.loader import render_to_string
import pdfkit
import os
import base64
from app_customer.customer_libs import *


# Create your views here.

salt = '123'
def dang_nhap_dang_ky(request):
    if 's_khachhang' in request.session:
        return redirect('app_store:trang_chu')
    
    #giỏ hàng
    cart = Cart(request)

    # ============== Đăng nhập
    chuoi_kq_dang_nhap = ''
    if request.POST.get('btnDangNhap'):
        # Gán biến
        hasher = PBKDF2PasswordHasher()
        email = request.POST.get('email').strip()
        mat_khau = hasher.encode(request.POST.get('mat_khau').strip(), salt)

        # Xác thực thông tin
        khach_hang = Customer.objects.filter(email=email, password=mat_khau)
        if khach_hang.count() > 0:
            dict_khach_hang = khach_hang.values()[0]
            request.session['s_khachhang'] = dict_khach_hang
            return redirect('app_store:trang_chu')
        else:
            chuoi_kq_dang_nhap = '''
                <div class="alert alert-danger" role="alert">
                    Đăng nhập thất bại. Vui lòng kiểm tra lại thông tin.
                </div>
                '''

    # ============== Đăng ký
    # Lấy thông tin tỉnh/tp, quận/huyện, phường/xã
    du_lieu = read_json_internet('http://api.laptrinhpython.net/vietnam')

    # Tỉnh/TP
    list_provinces = []
    str_districts = []
    str_wards = []
    list_districts_2 = []
    for province in du_lieu:
        list_provinces.append(province['name'])
        # Quận/Huyện
        list_districts_1 = []
        for dictrict in province['districts']:
            d = dictrict['prefix'] + ' ' + dictrict['name']
            list_districts_1.append(d)
            list_districts_2.append(d)
            # Phường/Xã
            list_wards = []
            for ward in dictrict['wards']:
                w = ward['prefix'] + ' ' + ward['name']
                list_wards.append(w)
            else:
                str_wards.append('|'.join(list_wards))
        else:
            str_districts.append('|'.join(list_districts_1))

    chuoi_kq_dang_ky = ''
    if request.POST.get('btnDangKy'):
        # Gán biến
        hasher = PBKDF2PasswordHasher()
        ho = request.POST.get('ho').strip()
        ten = request.POST.get('ten').strip()
        email = request.POST.get('email').strip()
        mat_khau = request.POST.get('mat_khau').strip()
        xac_nhan_mat_khau = request.POST.get('xac_nhan_mat_khau').strip()
        dien_thoai = request.POST.get('dien_thoai').strip()
        dia_chi = f"{request.POST.get('dia_chi').strip()}, {request.POST.get('phuong_xa')}, {request.POST.get('quan_huyen')}, {request.POST.get('tinh_tp')}"

        if mat_khau == xac_nhan_mat_khau:
           
            # Lưu vào CSDL
            Customer.objects.create(first_name=ho,
                                    last_name=ten,
                                    email=email,
                                    password=hasher.encode(mat_khau, salt),
                                    phone=dien_thoai,
                                    address=dia_chi)

            chuoi_kq_dang_ky = '''
                <div class="alert alert-success" role="alert">
                    Đăng ký thành viên thành công.
                </div>
                '''
        else:
            chuoi_kq_dang_ky = '''
                <div class="alert alert-danger" role="alert">
                    Mật khẩu và Xác nhận mật khẩu không khớp.
                </div>
                '''

    return render(request, 'login.html', {
        'chuoi_kq_dang_ky': chuoi_kq_dang_ky,
        'chuoi_kq_dang_nhap': chuoi_kq_dang_nhap,
        'cart': cart,
        'provinces': tuple(list_provinces),
        'str_districts': tuple(str_districts),
        'str_wards': tuple(str_wards),
        'list_districts': list_districts_2,
    })


def dang_xuat(request):
    if 's_khachhang' in request.session:
        del request.session['s_khachhang']
    return redirect('app_customer:dang_nhap_dang_ky')



def thong_tin_cua_toi(request):
    if 's_khachhang' not in request.session:
        return redirect('app_customer:dang_nhap_dang_ky')
    #giỏ hàng
    cart = Cart(request)
    customer = request.session.get('s_khachhang')
    #Thông tin cập nhật
    result_update_info = ''
    if request.POST.get('btnCapNhat'):
        ho = request.POST.get('ho').strip()
        ten =request.POST.get('ten').strip()
        dien_thoai =request.POST.get('dien_thoai').strip()
        dia_chi = request.POST.get('dia_chi').strip()


        obj_customer = Customer.objects.get(pk=customer['id']) 
        obj_customer.first_name = ho
        obj_customer.last_name = ten
        obj_customer.phone = dien_thoai
        obj_customer.address  = dia_chi 
        obj_customer.save()


        customer['first_name'] = ho
        customer['last_name'] = ten
        customer['phone'] = dien_thoai
        customer['address'] = dia_chi
        request.session['s_khachhang'] = customer


        result_update_info = '''
            <div class="alert alert-success" role="alert">
                Thông tin cập nhật thành công.
            </div>
            '''


    #Đổi mật khẩu
    result_change_password = ''
    if request.POST.get('btnDoiMatKhau'):
        hasher = PBKDF2PasswordHasher()
        mat_khau_hien_tai=hasher.encode(request.POST.get('mat_khau_hien_tai'), salt)
        mat_khau_moi = request.POST.get('mat_khau_moi')
        xac_nhan_mat_khau = request.POST.get('xac_nhan_mat_khau')

        obj_customer = Customer.objects.get(pk=customer['id']) 
        if mat_khau_hien_tai == obj_customer.password:
            if mat_khau_moi == xac_nhan_mat_khau:
                obj_customer.password = hasher.encode(mat_khau_moi, salt)
                obj_customer.save()
                result_change_password = '''
                <div class="alert alert-success" role="alert">
                    Đổi mật khẩu thành công.
                </div>
                '''
            else:
                result_change_password = '''
                <div class="alert alert-danger" role="alert">
                    Mật khẩu mới và Mật khẩu xác nhận không khớp.
                </div>
                '''
        else:
            result_change_password = '''
                <div class="alert alert-danger" role="alert">
                    Mật khẩu hiện tại không đúng.
                </div>
                '''

        


    #Đơn hàng

    orders = Order.objects.filter(customer = customer['id'])
    #chi tiết sản phẩm
    dict_orders = {}
    for order in orders:
        order_items = list(OrderItem.objects.filter(order=order.pk).values())
        for order_item in order_items:
            product = Product.objects.get(pk=order_item['product_id'])
            order_item['product_name'] = product.name
            order_item['product_image'] = product.image
            order_item['total'] = order.total
        else:
            dict_order_items = {
                order.pk: order_items
            }
            dict_orders.update(dict_order_items)

    return render(request, 'my-account.html', {
        'cart':cart,
        'orders':orders,
        'dict_orders': dict_orders,
        'customer': customer,
        'result_update_info': result_update_info,
        'result_change_password':result_change_password,
    })

def xuat_bao_cao_don_hang(request, order_id):
    if 's_khachhang' not in request.session:
        return redirect('app_customer:dang_nhap_dang_ky')
    customer = request.session.get('s_khachhang')
    #orders = Order.objects.filter(customer = customer['id']).values('id')
    #list_order_ids = [o['id'] for o in orders]
    #đơn hàng đã đặt
    
    order = Order.objects.get(customer = customer['id'],  pk = order_id)
    order_date = order.created.strftime('%d-%m-%Y %H:%M-%S')
    
    #chi tiets sản phẩm
    order_items = list(OrderItem.objects.filter(order=order_id).values())
    for order_item in order_items:
        product = Product.objects.get(pk=order_item['product_id'])
        order_item['product_name'] = product.name
        #Xử lý chuyển hình về nhị phân
        with open(settings.MEDIA_ROOT + str(product.image), 'rb') as img_file:
            img_string = base64.b64encode(img_file.read())
        order_item['product_image'] = img_string.decode('utf-8')
        order_item['total'] = order.total

    
    html_string = render_to_string( 'report_order.html', {
        'order_date': order_date,
        'customer': customer,
        'order_items': order_items,
        'pk': order_id,
    })
    # xử lý xuất ra tập tin PDF
    config = pdfkit.configuration(wkhtmltopdf=os.path.join(settings.STATIC_ROOT, r'wkhtmltox/bin/wkhtmltopdf.exe'))
    file_name = f'DH{order_id}.pdf'
    folder_report = os.path.join(settings.MEDIA_ROOT, 'reports/')
    path_report = folder_report + file_name
    pdfkit.from_string(html_string, path_report, configuration=config)
    

   

    return redirect(f'/media/reports/{file_name}')