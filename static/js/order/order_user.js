layui.use(['table', 'layer', 'form', 'laydate'],
    function () {
        var $ = layui.jquery, layer = layui.layer, form = layui.form, laydate = layui.laydate;
        var table = layui.table;

        var nowTime = new Date().valueOf();
        var max = null;

        var start = laydate.render({
            elem: '#start_time',
            type: 'datetime',
            max: nowTime,
            value: getTime(-1),
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
            value: getTime(1),
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
            elem: '#orderInfo_check',
            height: 'full-180',
            url: '/config/order/myOrder',
            page: true,
            where: {
                startTime: start.config.value,
                endTime: end.config.value
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
                    title: '订单编码'
                }, {
                    field: 'userAccount',
                    title: '用户名'
                }, {
                    field: 'payName',
                    title: '支付方式'
                }, {
                    field: 'orderAmount',
                    title: '订单金额',
                    width: '6%'
                }, {
                    field: 'orderTime',
                    title: '订单时间'
                }, {
                    field: 'paymentName',
                    title: '订单来源'
                }, {
                    field: 'orderState',
                    title: '订单状态',
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
                    templet: function (d) {
                        var retStr = '';
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
                    fixed: 'right',
                    title: '快速确认',
                    align: 'center',
                    templet: '#affirmbar',
                    unresize: true
                }, {
                    fixed: 'right',
                    field: 'orderDesc',
                    title: '备注'
                }, {
                    fixed: 'right',
                    title: '操作',
                    align: 'center',
                    templet: '#operatebar',
                    width: "12%",
                    unresize: true
                }]],
            id: 'orderTable',
            done: function () {
                var data = table.cache.orderTable;
                //查看是否有查询的权限进行按钮控制
                // if(!checkShiro('select')){
                // 	$("#searchbtn").hide();
                // }
//				if(!checkShiro('update')){
//					$(".update").hide();
//				}
            }
        };

        table.render(options);
        function getTime(diff) {
            var day = new Date(new Date().getTime() + diff * 86400000);
            return day.format("yyyy-MM-dd") + " 12:00:00"
        }

        table.on('tool(orderInfo)', function (obj) {
            var data = obj.data;
            var layEvent = obj.event;
            var tr = obj.tr;

            if (layEvent === 'update') {
                layer.open({
                    type: 2,
                    content: '/static/view/order/order_edit.html',
                    area: ['721px', '486px'],
                    maxmin: true,
                    success: function (layero, index) {
                        var body = layer.getChildFrame('body', index);//确定页面间的父子关系，没有这句话数据传递不了
                        var iframeWin = window[layero.find('iframe')[0]['name']];
                        iframeWin.inputDataHandle(data);
                    }
                });
            } else {
                var stateVal = 0;
                if (layEvent === 'affirm') {
                    stateVal = 40;
                } else if (layEvent === 'edit') {
                    //点击的解锁
                    stateVal = 10;
                }
                $.ajax({
                    type: "post",
                    url: "/config/order/updateMyOrder",
                    data: {
                        'id': data.id,
                        'state': stateVal
                    },
                    dataType: 'json',
                    success: function (obj) {
                        layer.msg(obj.message, {time: 1000});
                        // 执行重载
                        table.reload('orderTable', {
                            page: {
                                curr: 1
                            },
                            where: {
                                orderState: "",
                                key: $("#moresearch").val(),
                                startTime: $('#start_time').val(),
                                endTime: $('#end_time').val()
                            }
                        });
                    }
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
//						orderState : $('#orderState').val(),
                        orderState: "",
                        key: $("#moresearch").val(),
                        startTime: $('#start_time').val(),
                        endTime: $('#end_time').val()
                    }
                });
            }
        };

        $('.layui-inline .layui-btn').on('click', function () {
            var type = $(this).data('type');
            active[type] ? active[type].call(this) : '';
        });
        $.ajaxSettings.beforeSend = function (xhr, request) {
            xhr.setRequestHeader('X-CSRF-TOKEN', cookie.get("token"));
        };
    });
$(function () {

})