$(function(){

    $("#all_types").click(function(){
        console.log("全部类型");
        var $all_types_container =$("#all_types_container");
        $all_types_container.show();
        var $all_type =$(this);
        var $span=$all_type.find("span").find("span");
        $span.removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");
    })
    $("#all_types_container").click(function(){
        var $all_type_container=$(this);
        $all_type_container.hide();
        var $all_type =$("#all_types");
        var $span=$all_type.find("span").find("span");
        $span.removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
    })


    $("#sort_rule").click(function(){
        console.log("排序规则");
        var $sort_rule_container =$("#sort_rule_container");
        $sort_rule_container.show();
        var $sort_rule =$(this);
        var $span=$sort_rule.find("span").find("span");
        $span.removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");
    })
    $("#sort_rule_container").click(function(){
        var $sort_rule_container=$(this);
        $sort_rule_container.hide();
        var $sort_rule =$("#sort_rule");
        var $span=$sort_rule.find("span").find("span");
        $span.removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
    })

    $(".subShopping").click(function(){
        console.log('sub');
        var $sub=$(this);
        var goodsid=$sub.attr('goodsid');
        $.get('/sxw/subtocart/',{'goodsid':goodsid},function(data){
            console.log(data);
            if (data['status'] === 302){
                window.open('/sxw/login/',target="_self");
            }else if(data['status']===200){
                $sub.prev('span').html(data['c_goods_num']);
            }
        })
    })
    $(".addShopping").click(function(){
        console.log('add');
        var $add=$(this);
        var goodsid=$add.attr('goodsid');
        $.get('/sxw/addtocart/',{'goodsid':goodsid},function(data){
            console.log(data);
            if (data['status'] === 302){
                window.open('/sxw/login/',target="_self");
            }else if(data['status']===200){
                $add.prev('span').html(data['c_goods_num']);
            }
        })
    })

})