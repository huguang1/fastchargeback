layui.config({
    base: window.parent.baseUrl + '/layui/' //静态资源所在路径
}).use(['form', 'table', 'laydate', 'jquery'], function () {
    var token = getCookie("token");
    var table = layui.table;
    var form = layui.form;
    var laydate = layui.laydate;
    var $ = jQuery = layui.$;
    laydate.render({
        elem: '#loginTime'
        , type: 'datetime'
    });
    getPayTypeList();
    table.render({
        elem: '#payCode'
        , url: window.parent.baseUrl + '/payCode/payCodeView' //数据接口
        , page: true //开启分页
        , cols: [[ //表头
            {field: 'pay_code', title: '支付类型', align: 'center'}
            , {
                field: 'code', width: '40%', height: '100px', title: '付款二维码', templet: function (d) {
                    return '<img style="height:100px;width:100px" src="' + d.code + '" id="pic"/>';
                }
            }
            , {
                field: 'right', title: '状态', align: 'center', templet: function (d) {
                    if (d.status == 1) {
                        return "<div class=\"layui-form\"> <input type=\"checkbox\" onclick=\"changeStatus();\" status=" + d.status + " value=\"" + d.id + "\" name=\"isValid\" lay-filter=\"isValid\" checked lay-skin=\"switch\" lay-text=\"是|否\"></div>";
                    } else {
                        return "<div class=\"layui-form\"> <input type=\"checkbox\"  status=" + d.status + " value=\"" + d.id + "\" name=\"isValid\" lay-filter=\"isValid\" lay-skin=\"switch\" lay-text=\"是|否\"></div>";
                    }
                }
            },
            {field: 'comment', title: '备注', edit: 'text', align: 'center'},
            {fixed: 'right', title: '操作', align: 'center', toolbar: '#toolbar'}
        ]]
    });


    //监听工具条
    table.on('tool(payCode)', function (obj) {
        var data = obj.data;
        if (obj.event === 'del') {
            layer.confirm('确认删除？', function (index) {
                $.ajax({
                    type: 'post',
                    url: window.parent.baseUrl + '/payCode/deleteCode',
                    data: {'id': data.id},
                    headers: {'X-CSRF-TOKEN': token},
                    success: function (data) {
                        layer.msg("删除成功", {time: 1000});
                        table.reload('payCode', {});
                    }
                });
                layer.close(index);
            });

        }


    });
    //监听单元格编辑
    table.on('edit(payCode)', function (obj) {
        var value = obj.value //得到修改后的值
            , data = obj.data; //得到所在行所有键值
        var id = $(this).val();
        $.ajax({
            type: 'post',
            url: '/config/payCode/updateCodeState?id=' + data.id + "&comment=" + value,
            async: false,
            success: function (result) {
                if (result) {
                    layer.msg("修改成功");
                    active.reload();
                } else {
                    layer.msg("修改失败");
                }
            }
        })
    });
    //监听提交
    form.on('switch(isValid)', function (data) {
        var id = $(this).val();
        var status = $(this).attr("status");
        if (status == '1') {
            $(this).attr("status", "0");
            status = 0;
        } else if (status == '0') {
            $(this).attr("status", "1");
            status = 1;
        }
        $.ajax({
            type: 'post',
            url: '/config/payCode/updateCodeState',
            async: false,
            data: {'id': id, 'status': status},
            headers: {'X-CSRF-TOKEN': token},
            success: function (result) {
                if (result) {
                    layer.msg("修改成功");
                    active.reload();
                } else {
                    layer.msg("修改失败");
                }
            }
        })
    });

    active = {
        reload: function () {
            var searchKey = $('#payType');
            var payCode = searchKey.val();
            if (payCode == "0") {
                payCode = "";
            }
            // 执行重载
            table.reload('payCode', {
                page: {
                    curr: 1
                },
                where: {
                    payCode: payCode
                }
            });
        }
    };
    $('#selectbtn').on('click', function () {
        active.reload();
    });
    $('#addPic').on('click', function () {
        var pay_code = $("#payType").val();
        if (!pay_code || pay_code == 0) {
            layer.msg("请选择二维码类型");
            return false;
        }

        layer.open({
            type: 2,
            title: false,
            content: '/static/view/pay/payUpload.html?pay_code=' + pay_code,
            area: ['30%', '50%']
        });
    });


});
function getPayTypeList() {
    $.ajax({
        type: 'get',
        url: '/config/payCode/getList',
        async: false,
        success: function (result) {
            if (result.data != null) {
                //  debugger;
                var initVal = {};
                $("#payType").append('<option value="0" >请选择</option>');
                for (var i = 0; i < result.data.length; i++) {
                    var each = result.data[i];
                    $("#payType").append(
                        '<option value="' + each.pay_code + '" >' + each.item_name + '</option>');
                }
                renderForm();
            }
        }
    })
}
function renderForm() {
    layui.use('form', function () {
        var form = layui.form;
        form.render();
    });
}

