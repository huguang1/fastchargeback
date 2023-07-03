layui.config({
    base: window.parent.baseUrl + '/layui/' //静态资源所在路径
}).use(['table', 'laydate'], function () {
    var token = getCookie('token');
    var table = layui.table;
    var laydate = layui.laydate;
    laydate.render({
        elem: '#loginTime'
        , type: 'datetime'
    });

    var tableIns = table.render({
        elem: '#userData'
        , url: window.parent.baseUrl + '/sys/user/list'
        , method: 'get'
        , cols: [
            [
                {type: 'checkbox'}
                , {field: 'id', title: '编号', width: '10%', sort: true}
                , {field: 'user_name', title: '用户名'}
                , {field: 'nick_name', title: '昵称'}
                , {field: 'lastLoginTimeStr', title: '上次登录时间'}
                , {field: 'login_ip', title: '登录IP'}
                , {title: '操作', width: 250, align: 'center', fixed: 'right', toolbar: '#userOpert'}
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

    //监听工具条
    table.on('tool(userFilter)', function (obj) {
        var data = obj.data;

        if (obj.event === 'editUser') {
            //编辑
            var index = layer.open({
                title: '修改用户',
                type: 2,
                content: '/static/view/user/editUser.html',
                area: ['600px', '500px'],
                maxmin: true,
                success: function (layero, index) {
                    var body = layer.getChildFrame('body', index);//确定页面间的父子关系，没有这句话数据传递不了
                    var iframeWin = window[layero.find('iframe')[0]['name']];
                    $.ajax({
                        type: 'get',
                        url: window.parent.baseUrl + '/sys/role/list',
                        success: function (result) {
                            if (result.code == 0) {
                                iframeWin.initRole(result.data, data);
                            } else {
                                layer.alert(result.msg);
                            }
                        }
                    })
                }
            });

        } else if (obj.event === 'deleteUser') {
            //删除
            layer.confirm('确认删除该条数据吗？', function (index) {
                $.ajax({
                    type: 'post',
                    url: window.parent.baseUrl + '/sys/user/delete',
                    data: {userId: data.id},
                    headers: {'X-CSRF-TOKEN': token},
                    success: function (result) {
                        if (result.code == 200) {
                            layer.alert(result.message, {
                                icon: 6,
                                title: "提示"
                            }, function (index) {
                                layer.close(index);
                                tableIns.reload({
                                    page: {
                                        curr: 1 //重新从第 1 页开始
                                    }
                                });
                            });
                        } else {
                            layer.alert(result.message, {
                                icon: 5,
                                title: "提示"
                            });
                        }
                    }
                });
            })
        }
    });
    var $ = layui.$,
        active = {
            reload: function () {
                var load = $('#searchname');
                //执行重载
                table.reload('userData', {
                    page: {
                        cur: 1
                    }, where: {
                        keyWord: load.val()
                    }
                });
            }, add: function () {
                var index = layer.open({
                    title: '新增用户',
                    type: 2,
                    content: '/static/view/user/addUser.html',
                    area: ['600px', '500px'],
                    maxmin: true,
                    success: function (layero, index) {
                        $.ajax({
                            type: 'get',
                            url: window.parent.baseUrl + '/sys/role/list',
                            success: function (result) {
                                var body = layer.getChildFrame('body', index);//确定页面间的父子关系，没有这句话数据传递不了
                                var iframeWin = window[layero.find('iframe')[0]['name']];
                                iframeWin.initRole(result.data);
                            }
                        })
                    }
                });
            }
        };

    $('.demoTable .layui-btn').on('click', function () {
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
    });
});