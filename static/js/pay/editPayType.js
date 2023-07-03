function GetRequest() {
    var url = location.search;
    var theRequest = new Object();
    if (url.indexOf("?") != -1) {
        var str = url.substr(1);
        strs = str.split("&");
        for (var i = 0; i < strs.length; i++) {
            theRequest[strs[i].split("=")[0]] = unescape(strs[i].split("=")[1]);
        }
    }
    return theRequest;
}

layui.use(['form', 'layedit', 'laydate', 'jquery'],
    function () {
        var form = layui.form, layer = layui.layer, layedit = layui.layedit, laydate = layui.laydate;
        var $ = layui.jquery;

        // 自定义验证规则
        form.verify({});

        // 监听提交
        form.on('submit(mainSub)', function (data) {
            if (data.field.state == "on") {
                data.field.state = "1";
            } else {
                data.field.state = "0";
            }
            data.field.groupCode = 'PAY_TYPE';
            var token = getCookie("token");
            console.log(data.field);
            $.ajax({
                type: "post",
                url: "/config/lookupitem/save",
                data: data.field,
                headers: {'X-CSRF-TOKEN': token},
                dataType: "json",
                success: function (obj) {
                    if (obj.code = 200) {
                        layer.msg("保存成功！");
                        setTimeout(function () {
                            var index = parent.layer.getFrameIndex(window.name);
                            parent.layer.close(index);
                            window.parent.location.reload();
                        }, 1000);
                    } else {
                        layer.msg("保存失败!  ");
                    }
                }
            });
            return false;
        });

        // 初始化数据
        $(function () {
            var Request = GetRequest();
            var payTypeId = Request['id'];
            if (typeof(payTypeId) == "undefined") {
                /*form.val('mainForm', {
                 "state" : true,
                 "httpType" : "POST",
                 "signType" : "MD5"
                 });*/
            } else {
                $.ajax({
                    type: "get",
                    url: "/config/lookupitem/info",
                    data: {
                        id: payTypeId
                    },
                    success: function (obj) {
                        form.val('mainForm', obj.data);
                    }
                });
            }
        });

    });
function getCookie(sName) {
    var aCookie = document.cookie.split("; ");
    for (var i = 0; i < aCookie.length; i++) {
        var aCrumb = aCookie[i].split("=");
        if (sName == aCrumb[0])
            return unescape(aCrumb[1]);
    }
    return null;
}