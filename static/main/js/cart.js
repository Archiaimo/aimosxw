$(function (){
    $(".confirm").click(function(){
        console.log("change state");
        var $confirm=$(this);
        var $li=$confirm.parents("li");
        var cartid=$li.attr('cartid');
        $.getJSON("/sxw/changecartstate/",{'cartid':cartid},function (data){
            console.log(data);
            if (data['status']===200){
                $("#total_price").html(data['total_price']);
                if(data['c_is_select']){
                    $confirm.find("span").find("span").html("√");
                }else{
                    $confirm.find("span").find("span").html("");
                }
                if (data['is_all_select']){
                    $(".all_select span span").html("√");
                }else{
                    $(".all_select span span").html("");
                }
            }
        })
    })
    $(".subShopping").click(function(){
        var $sub=$(this);
        var $li =$sub.parents("li");
        var cartid=$li.attr("cartid");
        $.getJSON("/sxw/subshopping/",{"cartid":cartid},function(data){
            console.log(data);
            if (data['status']===200){
                 $("#total_price").html(data['total_price']);
                if (data['c_goods_num']>0){
                    var $span =$sub.next("span");
                    $span.html(data['c_goods_num']);
                }else{
                    $li.remove();
                }
            }
        })
    })
    $(".all_select").click(function(){
        var $all_select=$(this);
        var select_list=[];
        var unselect_list=[];
        $(".confirm").each(function(){
            var $confirm=$(this);
            var cartid =$confirm.parents("li").attr("cartid");
            if($confirm.find("span").find("span").html().trim()){
                select_list.push(cartid);
            }else{
                unselect_list.push(cartid);
            }
        })
        console.log(select_list);
        console.log(unselect_list);
        if(unselect_list.length > 0 ){
            $.getJSON('/sxw/allselect/',{'cart_list':unselect_list.join('#')},function(data){
                console.log(data);
                if(data['status']===200){
                    $(".confirm").find("span").find("span").html("√");
                    $all_select.find("span").find("span").html("√");
                    $("#total_price").html(data['total_price']);
                }
            })
        }else{
            if (select_list.length > 0){
                $.getJSON('/sxw/allselect/',{'cart_list':select_list.join('#')},function(data){
                console.log(data);
                if(data['status']===200){
                    $(".confirm").find("span").find("span").html("");
                    $all_select.find("span").find("span").html("");
                    $("#total_price").html(data['total_price']);
                }
            })
            }
        }
    })
    $("#make_order").click(function(){
        var select_list=[];
        var unselect_list=[];
        $(".confirm").each(function(){
            var $confirm=$(this);
            var cartid =$confirm.parents("li").attr("cartid");
            if($confirm.find("span").find("span").html().trim()){
                select_list.push(cartid);
            }else{
                unselect_list.push(cartid);
            }
        })
        if(select_list.length === 0){
            return
        }
        $getJSON("/sxw/makeorder/",function(data){
            console.log(data);
            if(data['status'] === 200){
                window.open('/sxw/orderdetail/?orderid=' + data['order_id'],target='_self');
            }
        })
    })
})