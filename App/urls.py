from django.conf.urls import url, include

from App import views

urlpatterns=[
    url(r'^home/',views.home,name='home'),
    url(r'^market/', views.market, name='market'),
    url(r'^marketwithparams/(?P<typeid>\d+)/(?P<childcid>\d+)/(?P<order_rule>\d+)/',
        views.market_with_params,name='market_with_params'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^mine/', views.mine, name='mine'),
    url(r'^register/',views.register,name='register'),
    url(r'^login/',views.login,name='login'),
    url(r'^checkuser/',views.check_user,name='check_user'),
    url(r'^logout/',views.logout,name='logout'),
    url(r'^sendemail/',views.send_email,name='send_email'),
    url(r'^addtocart/',views.add_to_cart,name='add_to_cart'),
    url(r'^subtocart/',views.sub_to_cart,name='sub_to_cart'),
    url(r'^changecartstate/',views.change_cart_state,name='change_cart_state'),
    url(r'^subshopping/',views.sub_shopping,name='sub_shopping'),
    url(r'^allselect/',views.all_select,name='all_select'),
    url(r'^makeorder/',views.make_order,name='make_order'),
    url(r'^orderdetail/',views.order_detail,name='order_detail'),
    url(r'^orderlistnotpay/',views.order_list_not_pay,name='order_list_not_pay'),
    url(r'^payed/',views.payed,name='payed'),
]