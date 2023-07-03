layui.config({
    base: window.parent.baseUrl + '/layui/' //静态资源所在路径
}).use(['table', 'laydate', 'jquery'], function () {
    var token = getCookie("token");
    var table = layui.table;
    var laydate = layui.laydate;
    var $ = jQuery = layui.$;
    laydate.render({
        elem: '#loginTime'
        , type: 'datetime'
    });

    var tableIns = table.render({
        elem: '#payType'
        , url: window.parent.baseUrl + '/lookupitem/getLookupItemByGroupCodePage?groupCode=PAY_TYPE'
        , method: 'get'
        , cols: [
            [
                {title: '序号', templet: '#indexTpl', type: 'numbers'}
                , {field: 'item_code', title: '类型编码'}
                , {field: 'item_name', title: '类型名称'}
                , {field: 'state', title: '状态', templet: '#switchState', unresize: true}
                , {field: 'sort', title: '排序'}
                , {field: 'attribute_2', title: '最小金额'}
                , {field: 'attribute_3', title: '最大金额'}
                , {field: 'attribute_4', title: '图标'}
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

    active = {
        reload: function () {
            // 执行重载
            table.reload('payType', {
                page: {
                    curr: 1
                }
            });
        }
    };

    //监听工具条
    table.on('tool(payType)', function (obj) {
        var data = obj.data;
        if (obj.event === 'edit') {
            layer.open({
                type: 2,
                title: false,
                content: '/static/view/pay/addPayType.html?id=' + data.id,
                area: ['70%', '90%']
            });
        } else if (obj.event === 'delete') {
            layer.confirm('确认删除？', function (index) {
                $.ajax({
                    type: 'post',
                    url: window.parent.baseUrl + '/lookupitem/deleteById',
                    data: {
                        id: data.id
                    },
                    headers: {'X-CSRF-TOKEN': token},
                    success: function (data) {
                        if (data.code = 200) {
                            layer.msg("删除成功!", {time: 1000});
                        } else {
                            layer.msg("删除失败!", {time: 1000});
                        }
                        active.reload();
                    }
                })
                layer.close(index);
            });
        }
    });

    $('#addPayType').on('click', function () {
        layer.open({
            type: 2,
            title: false,
            content: '/static/view/pay/addPayType.html',
            area: ['70%', '90%']
        });
    });
});