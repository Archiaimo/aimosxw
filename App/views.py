from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from App.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, User, Cart, Order, \
    OrderGoods
from App.views_constant import ALL_TYPE, ORDER_TOTAL, ORDER_PRICE_UP, ORDER_PRICE_DOWN, ORDER_SALE_UP, ORDER_SALE_DOWN, \
    HTTP_USER_EXIST, HTTP_OK, ORDER_STATUS_NOT_PAY, ORDER_STATUS_NOT_RECEIVE, ORDER_STATUS_NOT_SEND
from App.views_helper import hash_str, get_total_price
from aimosxw.settings import MEDIA_KEY_PREFIX


def home(request):
    main_wheels=MainWheel.objects.all()
    main_navs=MainNav.objects.all()
    main_mustbuys=MainMustBuy.objects.all()
    main_shops=MainShop.objects.all()
    main_shop0_1 = main_shops[0:1]
    main_shop1_3 = main_shops[1:3]
    main_shop3_7 = main_shops[3:7]
    main_shop7_11 = main_shops[7:11]
    main_shows=MainShow.objects.all()
    data={
        'title':'首页',
        'main_wheels':main_wheels,
        'main_navs':main_navs,
        'main_mustbuys':main_mustbuys,
        'main_shop0_1':main_shop0_1,
        'main_shop1_3':main_shop1_3,
        'main_shop3_7': main_shop3_7,
        'main_shop7_11': main_shop7_11,
        'main_shows':main_shows,
    }
    return render(request,'home.html',context=data)

def market(request):
    return redirect(reverse('sxw:market_with_params',kwargs={
        'typeid':104749,
        'childcid':0,
        'order_rule':0,
    }))

def market_with_params(request,typeid,childcid,order_rule):
    foodtypes=FoodType.objects.all()
    goods_list=Goods.objects.filter(categoryid=typeid)
    if childcid ==ALL_TYPE:
        pass
    else:
        goods_list=goods_list.filter(childcid=childcid)

    if order_rule ==ORDER_TOTAL:
        pass
    elif order_rule == ORDER_PRICE_UP:
        goods_list=goods_list.order_by('price')
    elif order_rule == ORDER_PRICE_DOWN:
        goods_list = goods_list.order_by('-price')
    elif order_rule == ORDER_SALE_UP:
        goods_list = goods_list.order_by('productnum')
    elif order_rule == ORDER_SALE_DOWN:
        goods_list = goods_list.order_by('-productnum')

    foodtype=foodtypes.get(typeid=typeid)
    """
    全部分类：0#进口水果：103534#国产水果：103533
    切割 #
    ['全部分类：0','进口水果：103534','国产水果：103533']
    切割 ：
    [[全部分类,0],[进口水果,103534],[国产水果,103533]]
    """
    foodtypechildnames=foodtype.childtypenames
    foodtypechildname_list=foodtypechildnames.split('#')
    childname_list=[]
    for foodtypechildname in foodtypechildname_list:
        childname_list.append(foodtypechildname.split(':'))

    order_rule_list=[
        ['综合排序',ORDER_TOTAL],
        ['价格升序', ORDER_PRICE_UP],
        ['价格降序', ORDER_PRICE_DOWN],
        ['销量升序', ORDER_SALE_UP],
        ['销量降序', ORDER_SALE_DOWN],
    ]
    data={
        'foodtypes':foodtypes,
        'goods_list':goods_list,
        'typeid':int(typeid),
        'childname_list':childname_list,
        'childcid':childcid,
        'order_rule_list':order_rule_list,
        'order_rule_view':order_rule,
    }
    return render(request,'market.html',context=data)

def cart(request):
    carts=Cart.objects.filter(c_user=request.user)
    is_all_select= not carts.filter(c_is_select=False).exists()


    data={
        'title':'购物车',
        'carts':carts,
        'is_all_select':is_all_select,
        'total_price':get_total_price()
    }
    return render(request,'cart.html',context=data)

def mine(request):
    user_id = request.session.get('user_id')
    data={
        'title':'我的',
        'is_login':False,
    }
    if user_id:
        user=User.objects.get(pk=user_id)
        data['is_login']=True
        data['username']=user.u_username
        data['icon']=MEDIA_KEY_PREFIX + user.u_icon.url
        data['order_not_pay']=Order.objects.filter(o_user=user).filter(o_status=ORDER_STATUS_NOT_PAY).count()
        data['order_not_receive'] = Order.objects.filter(o_user=user).filter(o_status__in=[ORDER_STATUS_NOT_SEND,
                                                                    ORDER_STATUS_NOT_RECEIVE]).count()
    return render(request,'mine.html',context=data)


def register(request):
    if request.method == 'GET':
        data={
            'title':'注册',
        }

        return render(request,'register.html',context=data)
    elif request.method=='POST':
        username=request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        icon = request.FILES.get('icon')
#也可以用django自带的make_password来加密，check_password来检验
        #password=hash_str(password)
        password=make_password(password)

        user=User()
        user.u_username=username
        user.u_password=password
        user.u_email=email
        user.u_icon=icon

        user.save()
        return redirect(reverse('sxw:login'))


def login(request):
    if request.method=='GET':
        error_message=request.session.get('error_message')
        data={
            'title':'登录',
        }
        if error_message:
            del request.session['error_message']
            data['error_message']=error_message

        return render(request,'login.html',context=data)
    elif request.method=='POST':
        username=request.POST.get('username')
        password = request.POST.get('password')

        users=User.objects.filter(u_username=username)
        if users.exists():
            user=users.first()
            if check_password(password,user.u_password):
                request.session['user_id']=user.id
                return redirect(reverse('sxw:mine'))
            else:
                request.session['error_message']='密码错误'
                return redirect(reverse('sxw:login'))
        request.session['error_message']='用户不存在'
        return redirect(reverse('sxw:login'))


def check_user(request):
    username=request.GET.get('username')
    users=User.objects.filter(u_username=username)
    data={
        'status':HTTP_OK,
        'msg':'user can use',
    }
    if users.exists():
        data['status']=HTTP_USER_EXIST
        data['msg']='user already exist'
    else:
        pass
    return JsonResponse(data=data)


def logout(request):
    request.session.flush()
    return redirect(reverse('sxw:mine'))


def send_email(request):
    subject='sxw activete'
    message='hello'
    from_email='Archi_aimo@163.com'
    reciptient_list=['907458025@qq.com']
    send_mail(subject=subject,message=message,from_email=from_email,
              recipient_list=reciptient_list)

    return HttpResponse('send success')


def add_to_cart(request):
    goodsid=request.GET.get('goodsid')
    carts=Cart.objects.filter(c_user=request.user).filter(c_goods_id=goodsid)
    if carts.exists():
        cart_obj=carts.first()
        cart_obj.c_goods_num = cart_obj.c_goods_num + 1
    else:
        cart_obj=Cart()
        cart_obj.c_goods_id=goodsid
        cart_obj.c_user=request.user
    cart_obj.save()
    data={
        'status':200,
        'msg':'add success',
        'c_goods_num':cart_obj.c_goods_num
    }
    return JsonResponse(data=data)


def sub_to_cart(request):
    goodsid = request.GET.get('goodsid')
    carts = Cart.objects.filter(c_user=request.user).filter(c_goods_id=goodsid)
    data = {
        'status': 200,
        'msg': 'add success',
    }
    if carts.exists():
        cart_obj = carts.first()
        if cart_obj.c_goods_num > 1:
            cart_obj.c_goods_num = cart_obj.c_goods_num - 1
            cart_obj.save()
            data['c_goods_num'] = cart_obj.c_goods_num
        else:
            cart_obj.delete()
            data['c_goods_num'] = 0

    return JsonResponse(data=data)


def change_cart_state(request):
    cart_id=request.GET.get('cartid')
    cart_obj=Cart.objects.get(pk=cart_id)
    cart_obj.c_is_select=not cart_obj.c_is_select
    cart_obj.save()
    is_all_select=not Cart.objects.filter(c_user=request.user).filter(c_is_select=False).exists()
    data={
        'status':200,
        'msg':'change ok',
        'c_is_select':cart_obj.c_is_select,
        'is_all_select':is_all_select,
        'total_price': get_total_price(),
    }
    return JsonResponse(data=data)


def sub_shopping(request):
    cart_id = request.GET.get('cartid')
    cart_obj = Cart.objects.get(pk=cart_id)
    data = {
        'status':200,
        'msg':'ok',
    }
    if cart_obj.c_goods_num > 1:
        cart_obj.c_goods_num = cart_obj.c_goods_num - 1
        cart_obj.save()
        data['c_goods_num']=cart_obj.c_goods_num
    else:
        cart_obj.delete()
        data['c_goods_num']=0
    data['total_price'] = get_total_price()
    return JsonResponse(data=data)


def all_select(request):
    cart_list=request.GET.get('cart_list')
    cart_list=cart_list.split('#')
    carts=Cart.objects.filter(id__in=cart_list)
    for cart_obj in carts:
        cart_obj.c_is_select = not cart_obj.c_is_select
        cart_obj.save()

    print(cart_list)
    data={
        'status':200,
        'msg':'ok',
        'total_price':get_total_price(),
    }
    return JsonResponse(data=data)


def make_order(request):
    carts=Cart.objects.filter(c_user=request.user).filter(c_is_select=True)
    order=Order()
    order.o_user=request.user
    order.o_price=get_total_price()
    order.save()
    for cart_obj in carts:
        ordergoods=OrderGoods()
        ordergoods.o_order=order
        ordergoods.o_goods_num=cart_obj.c_goods_num
        ordergoods.o_goods=cart_obj.c_goods
        ordergoods.save()
        cart_obj.delete()
    data={
        'status':200,
        'msg':'ok',
        'order_id':order.id
    }
    return JsonResponse(data=data)


def order_detail(request):
    order_id=request.GET.get('orderid')
    order=Order.objects.get(pk=order_id)
    data={
        'title':'订单详情',
        'order':order,
    }
    return render(request,'order_detail.html',context=data)


def order_list_not_pay(request):
    orders=Order.objects.filter(o_user=request.user).filter(o_status=ORDER_STATUS_NOT_PAY)
    data={
        'title':'订单列表',
        'orders':orders,
    }
    return render(request,'order_list_not_pay.html',context=data)


def payed(request):
    order_id=request.GET.get('orderid')
    order=Order.objects.get(pk=order_id)
    order.o_status=ORDER_STATUS_NOT_SEND
    order.save()
    data={
        'status':200,
        'msg':'payed success',
    }
    return JsonResponse(data)