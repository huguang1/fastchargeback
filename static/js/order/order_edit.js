var form;
layui.use(['form', 'layedit', 'jquery'],

    function () {
        form = layui.form, layer = layui.layer;
        var $ = layui.jquery;
        var token = getCookie('token');
        form.on('submit(mainSub)', function (data) {
            var orderState = $("#status").val();
            if (!orderState) {
                orderState = "";
            }
            var formdata = {
                id: data.field.id,
                state: $("#state").val(),
                orderState: orderState,
                orderDesc: $("#orderDesc").val()
            };

            var canUpdateAmount = $("#orderAmount").attr("readonly");
            if (!canUpdateAmount) {
                if (!isMoney($("#orderAmount").val())) {
                    layer.msg("请正确输入订单金额");
                    return false;
                }
                formdata.orderAmount = $("#orderAmount").val();
            }
            // postAjax("/config/order/updateMyOrder", formdata, function (obj) {
            //     layer.msg(obj.msg);
            //     setTimeout(function () {
            //         var index = parent.layer.getFrameIndex(window.name);
            //         parent.layer.close(index);
            //
            //         parent.layui.table.reload('orderTable', {
            //             where: {
            //                 key: parent.$("#moresearch").val(),
            //                 startTime: parent.$('#start_time').val(),
            //                 endTime: parent.$('#end_time').val()
            //             }
            //         });
            //     }, 1000);
            // });
            $.ajax({
                type: "post",
                url: "/config/order/updateMyOrder",
                data: formdata,
                dataType: "json",
                headers: {'X-CSRF-TOKEN': token},
                success: function (obj) {
                    layer.msg(obj.message);
                    setTimeout(function () {
                    var index = parent.layer.getFrameIndex(window.name);
                    parent.layer.close(index);
                    parent.layui.table.reload('orderTable', {
                        where: {
                            key: parent.$("#moresearch").val(),
                            startTime: parent.$('#start_time').val(),
                            endTime: parent.$('#end_time').val()
                        }
                    });
                }, 1000);
                }
            });
            return false;
        });
    });

function isMoney(s) {
    var regu = /^([1-9][\d]{0,7}|0)(\.[\d]{1,2})?$/;
    var re = new RegExp(regu);
    if (re.test(s)) {
        return true;
    } else {
        return false;
    }
}

/**
 *
 */
function inputDataHandle(data) {

    var payMentCode = data.paymentCode;
    if (payMentCode && payMentCode == 'erweima') {
        $("#orderAmount").removeAttr("readonly");
    }

    $("#orderId").val(data.orderId);
    $("#userAccount").val(data.userAccount);
    $("#orderAmount").val(data.orderAmount);
    if (data.orderState == 10) {
        $("#orderState").val("支付处理中");
    } else if (data.orderState == 30) {
        $("#orderState").val("支付成功");
    } else {
        $("#orderState").val("支付失败");
    }
    $("#orderDesc").val(data.orderDesc);
    $("#id").val(data.id);
    if (data.paymentCode == "erweima") {
        if (data.orderState == '10') {
            $("#orderStatus").html('<select name="status" id="status"><option value="10" selected="selected">支付处理中</option><option value="30">支付成功</option><option value="20">支付失败</option></select>');
        } else if (data.orderState == '30') {
            $("#orderStatus").html('<select name="status" id="status"><option value="10" >支付处理中</option><option selected="selected" value="30">支付成功</option><option value="20">支付失败</option></select>');
        } else {
            $("#orderStatus").html('<select name="status" id="status"><option value="10" >支付处理中</option><option  value="30">支付成功</option><option value="20" selected="selected">支付失败</option></select>');
        }
    }
    layui.use(['form'], function () {
        var form = layui.form
        form.render();
    })
}
$.ajaxSettings.beforeSend = function (xhr, request) {
    xhr.setRequestHeader('X-CSRF-TOKEN', cookie.get("token"));
};