$(function(){
    //  跳转顶层页面
    if (window != top) {
        top.location.href = location.href;
    }
    //  更新验证码
    $("#captcha").attr("src","/config/cache?t="+new Date().getTime());
    $("#captcha").on("click",function(){
        $("#captcha").attr("src","/config/cache?t="+new Date().getTime());
    })
});

// 获取登陆页面的logintoken
$(function () {
    $.ajax({
        url: '/config/getlogin/token',
        type: 'post',
        dataType: 'json',
        data: {},
        success: function (data) {
            console.log(data)
        },
        error: function () {
            console.log('服务器错误')
        }
    })
});
var box = {
    content:''
    ,btn: ['确定']
    ,yes: function () {
        window.location.href = '/static/templates/login.html';
    }
};

// 用户登陆
layui.use('layer', function () {
    var layer = layui.layer;
    $('#login_button').click(function () {
        var layer = layui.layer;
        var username = $('#username').val();
        var password = $('#password').val();
        var text = $('#verificationcode').val();
        var loginToken = cookie.get('loginToken');
        if (username && password && text){
            $.ajax({
                url: '/check/login',
                type: 'post',
                dataType: 'json',
                data: {
                    'username': username,
                    'password': password,
                    'text': text
                },
                headers: {'X-CSRF-TOKEN': loginToken},
                success: function (data) {
                    if (data.code===200){
                        window.location.href = '/static/view/index.html';
                    }else {
                        box.content = data.message;
                        layer.open(box)
                    }
                },
                error: function () {
                    box.content = '服务器错误';
                    layer.open(box)
                }
            })
        }else {
            box.content = '请输入完整参数';
            layer.open(box)
        }
    });
});
