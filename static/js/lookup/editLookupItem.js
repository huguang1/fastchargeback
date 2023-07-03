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

function inputDataHandle(data) {
    //动态加载下拉框
    var objSelect = document.getElementById("groupCode");
    for (var i = 0; i < data.length; i++) {
        objSelect.options.add(new Option(data[i].groupCode, data[i].groupName));
    }
    renderForm();
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
                url: "/config/lookupitem/save",
                data: data.field,
                headers: {'X-CSRF-TOKEN': token},
                dataType: "json",
                success: function (obj) {
                    if (obj) {
                        layer.msg("保存成功！");
                        setTimeout(function () {
                            var index = parent.layer.getFrameIndex(window.name);
                            parent.layer.close(index);
                            window.parent.location.reload();
                        }, 1000);
                    } else {
                        layer.msg("已存在的itemCode,groupCode的组合!");
                    }
                }
            });
            return false;
        });

        // 初始化数据
        $(function () {
            var Request = GetRequest();
            var lookupItemId = Request['id'];
            var groupCode = Request['groupCode'];
            var parentGroupCode = Request['parentGroupCode'];
            alert(parentGroupCode);
            if (lookupItemId) {
                $.ajax({
                    type: "get",
                    url: "/config/lookupitem/info",
                    data: {
                        id: lookupItemId
                    },
                    success: function (obj) {
                        $.ajax({
                            type: 'get',
                            url: '/config/lookupgroup/list',
                            success: function (result) {
                                //动态加载下拉框
                                var objSelect = document.getElementById("groupCode");
                                var data = result.data;
                                var y;
                                for (var i = 0; i < data.length; i++) {
                                    objSelect.options.add(new Option(data[i].group_name, data[i].group_code));
                                }
                                renderForm();
                                $("#groupCode option[value=" + obj.data.groupCode + "]").prop("selected", true);
                                form.render("select");
                            }
                        });
                        $.ajax({
                            type: 'get',
                            url: '/config/lookupitem/getLookupItemByGroupCode?groupCode=' + parentGroupCode,
                            success: function (result) {
                                //动态加载下拉框
                                var objSelect = document.getElementById("parentItemCode");
                                var data = result;
                                for (var i = 0; i < data.length; i++) {
                                    objSelect.options.add(new Option(data[i].itemName, data[i].itemCode));
                                }
                                renderForm();
                                $("#parentItemCode option[value=" + obj.parentItemCode + "]").prop("selected", true);
                                form.render("select");
                            }
                        });
                        form.val('mainForm', obj.data);
                    }
                });
            } else {
                $.ajax({
                    type: 'get',
                    url: '/config/lookupgroup/list',
                    success: function (result) {
                        //动态加载下拉框
                        var objSelect = document.getElementById("groupCode");
                        var data = result.data;
                        var y;
                        for (var i = 0; i < data.length; i++) {
                            objSelect.options.add(new Option(data[i].group_name, data[i].group_code));
                        }
                        renderForm();
                        $("#groupCode option[value=" + groupCode + "]").prop("selected", true);
                        form.render("select");
                    }
                })
                $.ajax({
                    type: 'get',
                    url: '/config/lookupitem/getLookupItemByGroupCode?groupCode=' + parentGroupCode,
                    success: function (result) {
                        //动态加载下拉框
                        var objSelect = document.getElementById("parentItemCode");
                        var data = result;
                        for (var i = 0; i < data.length; i++) {
                            objSelect.options.add(new Option(data[i].itemName, data[i].itemCode));
                        }
                        renderForm();
                    }
                })
                form.val('mainForm');
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
