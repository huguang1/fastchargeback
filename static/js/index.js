
var baseUrl = "/config";
//获取登录用户的菜单列表
var base = {
    projectName:"/config"
};

//  排序函数
function orderSort(a,b){
    return a.order-b.order
}
var box = {
    content:''
    ,btn: ['确定']
    ,yes: function () {
        window.location.href = '/static/templates/login.html';
    }
};

layui.use('layer', function () {
   $(function () {
        initUser();
        /**
         * 获取用户信息
         */
        function initUser(){
            var token = getCookie('token');
            if (token){
                $.ajax({
                    url: baseUrl + "/init/getUserName",
                    type: "post",
                    dataType: 'json',
                    headers: {'X-CSRF-TOKEN': token},
                    success: function (response) {
                        if (response.code != 200) {
                            window.location.href = "/static/templates/login.html";
                        }
                        $("#nameh3").html(response.message);
                        $("#logout").attr("href","/static/templates/logout.html");
                    },
                    error: function (e) {
                        box.content = '服务器错误，请重新登陆！';
                        layer.open(box);
                    }
                })
            }else {
                box.content = '用户已过期，请重新登陆！';
                layer.open(box);
            }
        }

        $.ajax({
            url : baseUrl + "/menu/userMenuList",
            type : "get",
            async:false,
            contentType: 'application/json',
            success : function(data) {
                var menuList = data;
                var html = "";
                $.each(menuList,function(index,item){
                    var children = item.children;
                    if (children) {
                        children.sort(orderSort);
                    }
                });
                menuList.sort(orderSort);
                $.each(menuList,function(i,item){
                    //初始化给订单展开
                    var str =  '<li class="layui-nav-item">';
                    var children = item.children;
                    var childrenstr = '';
                    if(children && children.length > 0){
                        //这里改js判断图标，后面数据库添加字段直接显示
                        var icon = item.icon;
                        str += '<a href="javascript:;"><i class="'+ icon +'"></i> <span>'+item.description+'</span></a>';
                        childrenstr = '<dl class="layui-nav-child">';

                        $.each(children,function(i,child){
                            var listicon = child.icon;
                            var mStr ='<dd>'+
                                '<a href="' + child.url +'" target="myFrame"><i class="'+ listicon +'"></i><span> '+child.description+'</span></a>'+
                                '   </dd>';
                            childrenstr += mStr;
                        });
                        childrenstr += '</dl>';
                    }else{
                        str = '<a href="' + item.url +'" target="myFrame"><i class="layui-icon layui-icon-home"></i><span>' + item.description + '</span></a>';
                    }
                    html += (str + childrenstr + '</li>');
                });
                html += "<li style='height:45px'></li>";

                layui.use('element', function(){
                    var element = layui.element;
                    $("#menutree").append(html);
                    element.render();
                    //…
                });
            },
            error : function(e) {
                console.log(e);
            }
        });
    });
});