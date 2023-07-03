layui.config({
    base: window.parent.baseUrl + '/layui/' //静态资源所在路径
}).use(['table', 'laydate', 'jquery', 'form'], function () {
    var token = getCookie("token");
    var table = layui.table;
    var laydate = layui.laydate;
    var form = layui.form;
    var $ = jQuery = layui.$;
    laydate.render({
        elem: '#loginTime'
        , type: 'datetime'
    });

    var tableIns = table.render({
        elem: '#payinfo'
        , url: window.parent.baseUrl + '/payinfo/all'
        , method: 'get'
        , cols: [
            [
                {title: '序号', templet: '#indexTpl', type: 'numbers'}
                , {field: 'payment_name', title: '平台名称'}
                , {field: 'item_name', title: '支付类型名称'}
                , {field: 'pay_code', title: '支付编码'}
                , {
                field: 'pay_model', title: '支付设备', templet: function (obj) {
                    if (obj.pay_model == 1) {
                        return 'PC';
                    } else if (obj.pay_model == 2) {
                        return 'WAP';
                    } else if (obj.pay_model == 3) {
                        return '网银内部';
                    } else if (obj.pay_model == 4) {
                        return '网银外部';
                    } else {
                        return '';
                    }
                }
            }
                , {field: 'icon', title: '图标名称'}
                , {
                field: 'rate_type', title: '佣金类型', templet: function (obj) {
                    if (obj.rate_type == 1) {
                        return '费率';
                    } else if (obj.rate_type == 2) {
                        return '单笔';
                    } else {
                        return '';
                    }
                }
            }
                , {field: 'rate', title: '比例/费用'}
                , {field: 'state', title: '状态', templet: '#switchState', unresize: true}
                , {field: 'min_switch', title: '最小金额开关', templet: '#switchMinSwitch', unresize: true}
                , {field: 'min_amount', title: '最小金额'}
                , {field: 'max_switch', title: '最大金额开关', templet: '#switchMaxSwitch', unresize: true}
                , {field: 'max_amount', title: '最大金额'}
                , {field: 'point_switch', title: '小数开关', templet: '#switchPointSwitch', unresize: true}
                , {fixed: 'right', title: '操作', align: 'center', toolbar: '#toolbar'}
            ]
        ]
        , page: true //是否显示分页
        , limit: 10
        , limits: [5, 10, 100]
        //添加权限控制
        , done: function () {
            //查看是否有查询的权限进行按钮控制
            // if(!checkShiro('add')){
            //     $("#addbtn").hide();
            // }
            // if(!checkShiro('select')){
            //     $("#selectbtn").hide();
            // }
            // if(!checkShiro('delete')){
            //     $(".del").hide();
            // }
            // if(!checkShiro('update')){
            //     $(".edit").hide();
            // }
        }
    });
    $('#selectbtn').on('click', function () {
        active.reload();
    });


    active = {
        reload: function () {
            var searchKey = $('#searchKey');
            var payType = $('#payType');
            // 执行重载
            table.reload('payinfo', {
                page: {
                    curr: 1
                },
                where: {
                    paymentCode: searchKey.val(),
                    itemCode: payType.val(),
                }
            });
        }
    };

    //监听工具条
    table.on('tool(userFilter)', function (obj) {
        var data = obj.data;
        if (obj.event === 'edit') {
            layer.open({
                type: 2,
                title: false,
                content: '/static/view/pay/editPayInfo.html?id=' + data.id,
                area: ['70%', '90%'],
                end: function () {
                    active.reload();
                }
            });
        } else if (obj.event === 'delete') {
            layer.confirm('确认删除？', function (index) {
                $.ajax({
                    type: 'post',
                    url: window.parent.baseUrl + '/payinfo/deleteById',
                    data: {
                        id: data.id
                    },
                    headers: {'X-CSRF-TOKEN': token},
                    success: function (data) {
                        layer.msg(data.message, {time: 1000});
                        active.reload();
                    }
                })
                layer.close(index);
            });
        }
    });

    $('#addPayInfo').on('click', function () {
        layer.open({
            type: 2,
            title: false,
            content: '/static/view/pay/editPayInfo.html',
            area: ['70%', '90%'],
            end: function () {
                active.reload();
            }
        });

    });


    $(function () {
        $.ajax({
            type: "GET",
            url: "/config/lookupitem/getLookupItemByGroupCodePage?groupCode=PAY_TYPE&state=1",
            data: {},
            dataType: "json",
            success: function (data) {
                for (var i = 0 in data.data) {
                    if (data.data[i] && data.data[i].item_code) {
                        $("#payType").append(
                            "<option value=" + data.data[i].item_code + ">"
                            + data.data[i].item_name + "</option>");
                    }
                }
                form.render();
            }
        })
    })

});

