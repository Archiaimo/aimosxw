$(function(){
    $("#not_login").click(function(){
        window.open("/sxw/login/",target="_self");
    })
    $("#regis").click(function(){
        window.open("/sxw/register/",target="_self");
    })
    $("#not_pay").click(function(){
        window.open('/sxw/orderlistnotpay/',target="_self");
    })
})