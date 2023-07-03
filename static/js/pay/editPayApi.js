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
            var token = getCookie("token");
            $.ajax({
                type: "post",
                url: "/config/payapi/save",
                data: data.field,
                headers: {'X-CSRF-TOKEN': token},
                dataType: "json",
                success: function (obj) {
                    if (obj.code = 200) {
                        layer.msg("保存成功！");
                        setTimeout(function () {
                            var index = parent.layer.getFrameIndex(window.name);
                            parent.layer.close(index);
                        }, 1000);
                    } else {
                        layer.msg("保存失败！");
                    }
                }
            });
            return false;
        });

        // 初始化数据
        $(function () {
            var Request = GetRequest();
            var apiId = Request['id'];
            $.ajax({
                type: 'get',
                url: '/config/lookupitem/getLookupItemByGroupCodePage?groupCode=NOTIFY_TYPE&state=1',
                async: false,
                success: function (result) {
                    //动态加载下拉框
                    var objSelect = document.getElementById("notifyType");
                    var data = result.data;
                    for (var i = 0; i < data.length; i++) {
                        objSelect.options.add(new Option(data[i].item_name, data[i].item_code));
                    }
                    renderForm();
                }
            });
            if (typeof(apiId) == "undefined") {
                form.val('mainForm', {
                    "state": true,
                    "httpType": "POST",
                    "signType": "MD5"
                });
            } else {
                $.ajax({
                    type: "get",
                    url: "/config/payapi/info",
                    data: {
                        id: apiId
                    },
                    success: function (obj) {
                        form.val('mainForm', obj.data);
                        $('#paymentCode').attr('disabled', true);
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

function renderForm() {
    layui.use('form', function () {
        var form = layui.form;//高版本建议把括号去掉，有的低版本，需要加()
        form.render();
    });
};