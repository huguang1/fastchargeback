layui.use(['table', 'layer', 'form', 'laydate', 'laytpl'],
    function () {
        var $ = layui.jquery, layer = layui.layer, form = layui.form, laydate = layui.laydate, laytpl = layui.laytpl;
        var table = layui.table;

        var nowTime = new Date().valueOf();
        var max = null;

        var start = laydate.render({
            elem: '#start_time',
            type: 'datetime',
            max: nowTime,
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
            url: '/config/order/listOrderHis',
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
                    width: '8%'
                }]],
            id: 'orderTable'
            , done: function (res, curr, count) {
                if (!checkShiro('delete')) {
                    $(".del").hide();
                }
                var ordersum = res.responseData;
                $("#tcount").html("");//先清空
                var trhtml = "总金额：¥&nbsp;&nbsp;<span style='color:red;'>" + ordersum.allMoney
                    + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>总手续费：&nbsp;&nbsp;¥<span style='color:red;'>&nbsp;"
                    + ordersum.allPoundage || 0 + "</span>&nbsp;&nbsp;";
                $("#tcount").append(trhtml);
            }
        };
        table.render(options);
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
                        endTime: $('#end_time').val()
                    }
                });
            }
        };
        $('#searchbtn').on('click', function () {
            active.reload();
        });


    });