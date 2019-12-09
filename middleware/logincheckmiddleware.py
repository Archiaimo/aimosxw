from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from App.models import User
REQUIRE_LOGIN=[
    '/sxw/cart/',
    '/sxw/orderdetail/',
    '/sxw/orderlistnotpay/',
]
REQUIRE_LOGIN_JSON=[
    '/sxw/addtocart/',
    '/sxw/changecartstate/',
    '/sxw/makeorder/',
]
class LoginMiddleware(MiddlewareMixin):
    def process_request(self,request):
        if request.path in REQUIRE_LOGIN_JSON:
            user_id=request.session.get('user_id')
            if user_id:
                try:
                    user=User.objects.get(pk=user_id)
                    request.user=user
                except:
                    data={
                        'status':301,
                        'msg':'user not avaliable'
                    }
                    return JsonResponse(data=data)
                    #return redirect(reverse('sxw:login'))
            else:
                data = {
                    'status': 301,
                    'msg': 'user not login'
                }
                return JsonResponse(data=data)
                #return redirect(reverse('sxw:login'))
        if request.path in REQUIRE_LOGIN:
            user_id = request.session.get('user_id')
            if user_id:
                try:
                    user = User.objects.get(pk=user_id)
                    request.user = user
                except:
                    return redirect(reverse('sxw:login'))
            else:
                return redirect(reverse('sxw:login'))
