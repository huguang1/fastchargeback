layui.config({
    base: window.parent.baseUrl + '/layui/' //静态资源所在路径
}).use(['table','laydate'],function(){
    var token = getCookie('token');
    var table = layui.table;
    var tableIns = table.render({
        elem: '#userData'
        ,url: window.parent.baseUrl +'/blackWhite/whiteList'
        ,method:'get'
        ,cols: [[
            {type:'checkbox'}
            ,{field:'id', title: '编号', width:'10%',sort: true}
            ,{field:'user_name', title: '会员名称'}
            ,{field:'ip', title: 'IP地址'}
            ,{field:'createTimeStr', title: '创建时间'}
            ,{field:'remarks', title: '备注'}
            ,{title: '操作',width:250, align:'center', fixed: 'right', toolbar: '#userOpert'}
        ]]
        ,page: true //是否显示分页
        ,limit:10
        ,limits: [5, 10, 100]
        //添加权限控制
        ,done:function(){
            //查看是否有查询的权限进行按钮控制

        }
    });

    //监听工具条
    table.on('tool(userFilter)', function(obj){
        var data = obj.data;
        if(obj.event === 'deleteUser'){
            //删除
            layer.confirm('确认删除该条数据吗？', function(index){
                $.ajax({
                    type: 'post',
                    url: window.parent.baseUrl + '/blackWhite/delete',
                    data: {id:data.id},
                    headers: {'X-CSRF-TOKEN': token},
                    success: function(result) {
                        if(result.code == 200){
                            layer.alert(result.message,{
                                icon:6,
                                title:"提示"
                            },function(index){
                                layer.close(index);
                                tableIns.reload({
                                    page:{
                                        curr:1 //重新从第 1 页开始
                                    }
                                });
                            });
                        }else{
                            layer.alert(result.message,{
                                icon:5,
                                title:"提示"
                            });
                        }
                    }
                });
            })
        }
    });
    var $ = layui.$, active = {
        getCheckData: function(){ //获取选中数据
            var checkStatus = table.checkStatus('userData'),
                data = checkStatus.data;
        },
        reload: function(){
            var load = $('#searchname');
            //执行重载
            table.reload('userData', {
                page:{
                    cur :1
                },where:{
                    key : load.val()
                }
            });
        },add: function() {
            var index = layer.open({
                title: '新增用户',
                type: 2,
                content: '/static/view/user/addwhite.html',
                area: ['600px', '450px'],
                maxmin: true,
                success: function(layero, index){
                    var body = layer.getChildFrame('body',index);//确定页面间的父子关系，没有这句话数据传递不了
                    var iframeWin = window[layero.find('iframe')[0]['name']];
                }
            });
        },batchdel:function(){
            var checkStatus = table.checkStatus('userData'),
                data = checkStatus.data;
            if(data.length==0){
                layer.alert("没有要删除的数据！");
                return false;
            }
            var str = '';
            for(var i=0;i < data.length;i++){
                if(str==''){
                    str += data[i].id;
                }else {
                    str += ',' + data[i].id;
                }
            }
            layer.confirm('确定删除所选计划吗？', function(index){
                $.ajax({
                    type:'post',
                    url:window.parent.baseUrl + '/blackWhite/batchDelete',
                    data:{ids:str},
                    dataType:'json',
                    headers: {'X-CSRF-TOKEN': token},
                    success: function(result) {
                        if(result.code == 200){
                            layer.alert(result.message,{
                                icon:6,
                                title:"提示"
                            },function(index){
                                layer.close(index);
                                tableIns.reload({
                                    page:{
                                        curr:1 //重新从第 1 页开始
                                    }
                                });
                            });
                        }else{
                            layer.alert(result.message,{
                                icon:5,
                                title:"提示"
                            });
                        }
                    }
                });
            });
        }
    };

    $('.demoTable .layui-btn').on('click', function(){
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
    });
});
