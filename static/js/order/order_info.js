layui.use(['table', 'layer', 'form', 'laydate', 'laytpl'],
    function () {
        var $ = layui.jquery, layer = layui.layer, form = layui.form, laydate = layui.laydate, laytpl = layui.laytpl;
        var table = layui.table;

        var nowTime = new Date().valueOf();
        var max = null;

        getSum();

        var start = laydate.render({
            elem: '#start_time',
            type: 'datetime',
            max: nowTime,
            value: getMonthAgo(),
            btns: ['clear', 'confirm'],
            done: function (value, date) {
                endMax = end.config.max;
                end.config.min = date;
                end.config.min.month = date.month - 1;
            }
        });
        var end = laydate.render({
            elem: '#end_time',
            type: 'datetime',
            max: nowTime,
            done: function (value, date) {
                if ($.trim(value) == '') {
                    var curDate = new Date();
                    date = {
                        'date': curDate.getDate(),
                        'month': curDate.getMonth() + 1,
                        'year': curDate.getFullYear()
                    };
                }
                start.config.max = date;
                start.config.max.month = date.month - 1;
            }
        });

        var options = {
            elem: '#orderInfo',
            url: '/config/order/ordergrid',
            height: 'full-180',
            page: true,
            where: {
                startTime: start.config.value
            },
            text: {
                none: '暂无相关数据'
            },
            even: true,
            cols: [[ // 表头
                {
                    type: 'numbers',
                    title: "NO."
                }, {
                    field: 'orderId',
                    title: '订单编码',
                    width: '11%'
                }, {
                    field: 'userAccount',
                    title: '用户名',
                    width: '9%'
                }, {
                    field: 'payName',
                    title: '支付方式',
                    width: '9%'
                }, {
                    field: 'orderAmount',
                    title: '订单金额',
                    width: '8%'
                }, {
                    field: 'orderTime',
                    title: '订单时间',
                    width: '12%'
                }, {
                    field: 'paymentName',
                    title: '订单来源',
                    width: '9%'
                }, {
                    field: 'orderState',
                    title: '订单状态',
                    width: '10%',
                    templet: function (d) {
                        var retStr = "";
                        switch (d.orderState) {
                            case 10:
                                retStr = "支付处理中";
                                break;
                            case 30:
                                retStr = "支付成功";
                                break;
                            default:
                                retStr = "支付失败";
                        }
                        return retStr;
                    }
                }, {
                    field: 'state',
                    title: '处理状态',
                    width: '8%',
                    templet: function (d) {
                        var retStr = "";
                        switch (d.state) {
                            case 10:
                                retStr = '<span style="color:blue;">待处理</span>';
                                break;
                            case 20:
                                retStr = '<span style="color:red;">已锁定(' + d.updateUser + ')</span>';
                                break;
                            case 30:
                                retStr = '<span style="color:blue;">待确认</span>';
                                break;
                            case 50:
                                retStr = '<span style="color:blue;">已取消</span>';
                                break;
                            default:
                                retStr = '<span style="color:blue;">已确认</span>';
                        }
                        return retStr;
                    }
                }, {
                    field: 'orderDesc',
                    title: '备注',
                    width: '8%',
                    templet: function (d) {
                        var retStr = "";
                        if (d.updateUser) {
                            retStr = retStr + "(" + d.updateUser + ") ";
                        }
                        if (d.orderDesc) {
                            retStr = retStr + d.orderDesc;
                        }
                        return retStr;
                    }
                }, {
                    fixed: 'right',
                    title: '操作',
                    width: '10%',
                    align: 'center',
                    templet: function (row) {
                        //如果订单的状态为支付处理中或者支付成功
                        var rowhtml = '';
                        if (row.orderState == 10 || row.orderState == 30) {
                            if (row.state >= 20) {
                                rowhtml += '<a class="layui-btn layui-btn-xs" lay-event="unlock">解锁</a>' +
                                    '<a class="layui-btn layui-btn-xs update" lay-event="update">更改状态</a>';
                            }
                            if (row.state == 10 || row.state == 50) {
                                rowhtml += '<a class="layui-btn layui-btn-xs" lay-event="lock">锁定</a>';
                            }
                            if (row.state >= 30) {
                                rowhtml += '<a class="layui-btn layui-btn-danger layui-btn-xs del" lay-event="delete" >删除</a>';
                            }
                        }
                        return rowhtml;
                    }
                }]],
            id: 'orderTable'
            , done: function (res, curr, count) {
                var data = table.cache.orderTable;
                //查看是否有查询的权限进行按钮控制
                // if(!checkShiro('select')){
                // 	$("#searchbtn").hide();
                // }
                if (!checkShiro('delete')) {
                    $(".del").hide();
                }
//							if(!checkShiro('update')){
//								$(".update").hide();
//							}
//							var ordersum = res.responseData;
//							$("#tcount").html("");//先清空
//							var trhtml = "总金额：¥&nbsp;&nbsp;<span style='color:red;'>"+ ordersum.allMoney
//										+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>总手续费：&nbsp;&nbsp;¥<span style='color:red;'>&nbsp;"
//									+ ordersum.allPoundage || 0 +"</span>&nbsp;&nbsp;";
//							$("#tcount").append(trhtml);

            }
        };

        function getMonthAgo() {
            var d = new Date;
            d.setMonth(d.getMonth() - 1);
            return d.format("yyyy-MM-dd hh:mm:ss");
        }

        table.render(options);
        table.on('tool(orderInfo)', function (obj) {
            var data = obj.data;
            var layEvent = obj.event;
            var tr = obj.tr;

            if (layEvent === 'lock') {
                $.ajax({
                    type: "post",
                    url: "/config/order/lockOrder",
                    data: data,
                    dataType: 'json',
                    success: function (obj) {
                        layer.msg(obj.message, {time: 1000});
                        // 执行重载
                        table.reload('orderTable', {
                            page: {
                                curr: 1
                            },
                            where: {
                                orderState: $('#orderState').val(),
                                key: $("#moresearch").val(),
                                startTime: $('#start_time').val(),
                                endTime: $('#end_time').val(),
                                paymentCode: $("#paymentCode").val()
                            }
                        });
                    }
                });
            } else if (layEvent === 'unlock') {
                $.ajax({
                    type: "post",
                    url: "/config/order/updateMyOrder",
                    data: {'id': data.id, 'state':10},
                    dataType: 'json',
                    success: function (obj) {
                        layer.msg(obj.message, {time: 1000});
                        // 执行重载
                        table.reload('orderTable', {
                            page: {
                                curr: 1
                            },
                            where: {
                                orderState: $('#orderState').val(),
                                key: $("#moresearch").val(),
                                startTime: $('#start_time').val(),
                                endTime: $('#end_time').val(),
                                paymentCode: $("#paymentCode").val()
                            }
                        });
                    }
                });
            } else if (layEvent === 'update') {
                layer.open({
                    type: 2,
                    content: '/static/view/order/order_edit.html',
                    area: ['721px', '486px'],
                    maxmin: true,
                    success: function (layero, index) {
                        var body = layer.getChildFrame('body', index);
                        var iframeWin = window[layero.find('iframe')[0]['name']];
                        iframeWin.inputDataHandle(data);
                    }
                });
            } else {
                layer.confirm('确认删除？', function (index) {
                    $.ajax({
                        type: "get",
                        url: "/config/order/delOrder/" + data.id,
                        success: function (data) {
                            layer.msg(data.msg, {time: 1000});
                            obj.del();
                        }
                    });
                    layer.close(index);
                });
            }
        });

        active = {
            reload: function () {
                // 执行重载
                table.reload('orderTable', {
                    page: {
                        curr: 1
                    },
                    where: {
                        orderState: $('#orderState').val(),
                        key: $("#moresearch").val(),
                        startTime: $('#start_time').val(),
                        endTime: $('#end_time').val(),
                        paymentCode: $("#paymentCode").val()
                    }
                });

                getSum();

            }
        };

        $('.layui-inline .layui-btn').on('click', function () {
            var type = $(this).data('type');
            //导出excel
            if (type == "exportexcel") {
                var startTime = $('#start_time').val();
                var endTime = $('#end_time').val();
                if (startTime != "" && endTime != "") {
                    var day1 = new Date(startTime);
                    var day2 = new Date(endTime);
                    if ((day2 - day1) / (1000 * 60 * 60 * 24) > 7) {
                        layer.msg("导出事件跨度超过一周，请重新选择时间");
                        return;
                    }
                } else {
                    layer.msg("请先选择时间再导出");
                    return;
                }
                var index = layer.open({
                    content: '服务器正在努力加载数据，请稍后...' //这里content是一个普通的String
                });
                $.ajax({
                    url: '/config/order/generateExcel',
                    async: false,
                    type: "get",
                    timeout: 60000,
                    data: {
                        orderState: $('#orderState').val(),
                        key: $("#moresearch").val(),
                        startTime: $('#start_time').val(),
                        endTime: $('#end_time').val(),
                        paymentCode: $("#paymentCode").val()
                    },
                    success: function (e) {
                        layer.close(index);
                        if (e && e.code==200) {
                            window.location.href = "/config/order/downloadExcel?fileName=" + e.data;
                        } else {
                            layui.layer.msg("系统异常");
                        }
                    }
                });
                return false;
            } else {
                active[type] ? active[type].call(this) : '';
            }
        });

        $.ajax({
            type: 'get',
            url: '/config/payapi/list',
            async: false,
            success: function (data) {
                //动态加载下拉框
                var objSelect = document.getElementById("paymentCode");
                objSelect.options.add(new Option("所有", ""));
                for (var i = 0; i < data.data.length; i++) {
                    objSelect.options.add(new Option(data.data[i].payment_name, data.data[i].payment_code));
                }
                var form = layui.form;
                form.render();
            }
        });


    });

$.ajaxSettings.beforeSend = function (xhr, request) {
    xhr.setRequestHeader('X-CSRF-TOKEN', cookie.get("token"));
};


function getSum() {

    $.ajax({
        url: '/config/order/orderSum',
        async: false,
        type: "get",
        timeout: 60000,
        dataType: 'json',
        data: {
            orderState: $('#orderState').val(),
            key: $("#moresearch").val(),
            startTime: $('#start_time').val(),
            endTime: $('#end_time').val(),
            paymentCode: $("#paymentCode").val()
        },
        success: function (e) {
            var ordersum = e;
            $("#tcount").html("");//先清空
            var trhtml = "总金额：¥&nbsp;&nbsp;<span style='color:red;'>" + ordersum.responseData.allMoney
                + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>总手续费：&nbsp;&nbsp;¥<span style='color:red;'>&nbsp;"
                + ordersum.responseData.allPoundage || 0 + "</span>&nbsp;&nbsp;";
            $("#tcount").append(trhtml);
        }
    });

}
