from django.contrib import admin
from django.utils.html import format_html
from app_store.models import *
from app_cart.models import Order, OrderItem
from datetime import datetime


def change_public_day(modeadmin, request, queryset):
    queryset.update(public_day = datetime.now())


change_public_day.short_description ='Change public_day of selected products to current time '

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('e_name',)

    @admin.display(description='Tên danh mục')
    def e_name(self, obj):
        return f'{obj.name}'
    

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('e_name','e_category_name')

    @admin.display(description='Tên danh mục con')
    def e_name(self, obj):
        return f'{obj.name}'
    
    @admin.display(description='Tên danh mục cha')
    def e_category_name(self, obj):
        return f'{obj.category.name}'


class ProductAdmin(admin.ModelAdmin):
    exclude=('public_day', 'viewed')

    #list_display = ('name', 'price', 'public_day', 'viewed')
    list_display = ('e_name', 'e_price', 'e_public_day', 'e_viewed', 'e_subcategory_name' , 'e_image' )

    list_filter = ('public_day',)

    search_fields = ('name__contains',)

    actions = [change_public_day]

    @admin.display(description='Tên sản phẩm')
    def e_name(self, obj):
        return f'{obj.name}'
    
    @admin.display(description='Giá')
    def e_price(self, obj):
        return f'{"{:,}".format(int(obj.price))}'
    
    @admin.display(description='Ngày cập nhật')
    def e_public_day(self, obj):
        return f'{obj.public_day.strftime("%d/%m/%Y %H:%M:%S")}'
    
    @admin.display(description='Lượt xem')
    def e_viewed(self, obj):
        return f'{obj.viewed}'
    
    @admin.display(description='Tên danh mục')
    def e_subcategory_name(self, obj):
        return f'{obj.subcategory.name}'

    @admin.display(description='Hình ảnh')
    def e_image(self, obj):
        return format_html(f'<img src="{obj.image.url}" alt="{obj.name}" style = "height: 45px ; width: 45px" />')
    
    

    

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)

admin.site.site_header= 'Estore Administration'
