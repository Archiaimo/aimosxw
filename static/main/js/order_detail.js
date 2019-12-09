$(function(){
    $("#alipay").click(function(){
        console.log("支付");
        var orderid=$(this).attr('orderid');
        $.getJSON('/sxw/payed/',{'orderid':orderid},function(data){
            console.log(data);
            if(data['status']===200){
                window.open('/sxw/mine/',target='_self');
            }
        })
    })
})