layui.use(['table', 'layer'], function () {
    var $ = layui.jquery, layer = layui.layer;
    var table = layui.table;
    var token = getCookie('token');
    var tableIns = table.render({
        elem: '#dictionaryList',
        url: window.parent.baseUrl + '/dictionary/list',
        method: 'get',
        cols: [[{
            field: 'id',
            title: 'ID',
            sort: true,
            align: 'center'
        }, {
            field: 'dic_key',
            title: '字典key',
            align: 'center'
        }, {
            field: 'dic_value',
            title: '字典值',
            align: 'center'
        }, {
            field: 'description',
            title: '字典描述',
            align: 'center'
        }, {
            title: '操作',
            width: 250,
            align: 'center',
            fixed: 'right',
            toolbar: '#barDemo'
        }]],
        page: true //是否显示分页
        ,
        limit: 10,
        limits: [5, 10, 100]
        //添加权限控制
    });

    $('#selectbtn').on('click', function () {
        active.reload();
    });
    //监听工具条
    table.on('tool(demo)', function (obj) {
        var data = obj.data;
        if (obj.event === 'del') {
            layer.confirm('真的删除行么', function (index) {
                $.ajax({
                    type: "post",
                    url: "/config/dictionary/del/" + data.id,
                    data: {},
                    dataType: "json",
                    headers: {'X-CSRF-TOKEN': token},
                    success: function (data) {
                        layer.msg(data.message);
                        setTimeout(function () {
                            active.reload();
                        }, 1000);
                    }
                });
                layer.close(index);
            });
        } else if (obj.event === 'edit') {
            var index = layer.open({
                type: 2,
                content: '/static/view/dictionary/editDictionary.html?id=' + data.id,
                area: ['45%', '50%'],
                maxmin: true,
                success: function (layero, index) {
                    var body = layer.getChildFrame('body', index);//确定页面间的父子关系，没有这句话数据传递不了
                    var iframeWin = window[layero.find('iframe')[0]['name']];
                    iframeWin.inputMemberInfo(data);
                },
                end: function () {
                    active.reload();
                }
            });
        }
    });
    active = {
        reload: function () {
            var searchKey = $('#searchKey');
            var searchValue = $('#searchValue');
            // 执行重载
            table.reload('dictionaryList', {
                page: {
                    curr: 1
                },
                where: {
                    searchValue: searchValue.val(),
                    searchKey: searchKey.val()
                }
            });
        }
    };
    // 添加
    $('#addbtn').on('click', function () {
        layer.open({
            type: 2,
            title: false,
            content: '/static/view/dictionary/addDictionary.html',
            area: ['45%', '45%']
        });
    });


});
