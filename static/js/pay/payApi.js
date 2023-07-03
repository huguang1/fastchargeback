layui.config({
    base: window.parent.baseUrl + '/layui/' //静态资源所在路径
}).use(['table', 'laydate', 'jquery'], function () {
    var token = getCookie('token');
    var table = layui.table;
    var laydate = layui.laydate;
    var $ = jQuery = layui.$;
    laydate.render({
        elem: '#loginTime'
        , type: 'datetime'
    });

    var tableIns = table.render({
        elem: '#payApi'
        , url: window.parent.baseUrl + '/payapi/list'
        , method: 'get'
        , cols: [
            [
                {title: '序号', templet: '#indexTpl', type: 'numbers'}
                , {field: 'payment_code', title: '平台编码'}
                , {field: 'payment_name', title: '平台名称'}
                , {field: 'state', title: '状态', templet: '#switchState', unresize: true}
                , {field: 'memberid', title: '商户ID'}
                , {field: 'api_key', title: 'apikey'}
                , {field: 'http_url', title: '请求地址'}
                , {field: 'http_type', title: '请求方式'}
                , {field: 'notify_type', title: '回调类型'}
                , {field: 'remark', title: '备注'}
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
            // 执行重载
            table.reload('payApi', {
                page: {
                    curr: 1
                },
                where: {
                    paymentCode: searchKey.val(),
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
                content: '/static/view/pay/editPayApi.html?id=' + data.id,
                area: ['70%', '90%'],
                end: function () {
                    active.reload();
                }
            });
        } else if (obj.event === 'delete') {
            layer.confirm('确认删除？', function (index) {
                $.ajax({
                    type: 'post',
                    url: window.parent.baseUrl + '/payapi/deleteById',
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

    $('#addPament').on('click', function () {
        layer.open({
            type: 2,
            title: false,
            content: '/static/view/pay/editPayApi.html',
            area: ['70%', '90%'],
            end: function () {
                active.reload();
            }
        });
    });
});