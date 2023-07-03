var $ = layui.$;
function initRole(res){
    var token = getCookie('token');
    $("#roleId").val(res.id);
    $("#roleName").val(res.role_name);
    $("#roleDesc").val(res.role_desc);
    //把用户拥有的权限选中
    $.ajax({
        type: 'get',
        url:  window.parent.parent.baseUrl + '/sys/role/queryPermisson',
        data: {roleId:res.id},
        headers: {'X-CSRF-TOKEN': token},
        success: function(result) {
            d.setDefaultCheck(result.data)
        }
    });

};

$(function () {
    $("#btnEditRoleSubmit").click(function () {
        var token = getCookie('token');
        var roleName = $("#roleName").val();
        var roleDesc = $("#roleDesc").val();
        if (!roleName || !roleDesc) {
            layer.alert("角色名字或者描述不能为空");
            return;
        }

        var data = $("#myForm").serialize();
        $.ajax({
            type: 'post',
            url: window.parent.parent.baseUrl + '/sys/role/update',
            data: data,
            dataType: 'json',
            headers: {'X-CSRF-TOKEN': token},
            success: function(result) {
                if(result.code==200){
                    layer.alert("新增成功",{
                        icon:6,
                        title:"提示"
                    },function(index){
                        layer.close(index);
                        var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
                        parent.layer.close(index); //再执行关闭
                        window.parent.location.reload();
                    });
                }else{
                    layer.alert("新增失败",{
                        icon:5,
                        title:"提示"
                    },function(index){
                        layer.close(index);
                        var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
                        parent.layer.close(index); //再执行关闭
                        window.parent.location.reload();
                    });
                }
            }
        });
    })

    $("#btnCancel").click(function () {
        parent.layer.close(index);
    });
})

layui.config({
    base: window.parent.baseUrl + '/layui/' //静态资源所在路径
}).use(['form', 'laydate'], function() {
        layer = layui.layer,
        form = layui.form,
        index = parent.layer.getFrameIndex(window.name); //获取窗口索引;
        /* 自定义验证规则 */
        form.verify({
            userName: function(value) {
                if(value.length < 5) {
                    return '名称至少得5个字';
                }
            }
        });
        var active = {
            cancel: function(set) {
                parent.layer.close(index);
            }
        }
        $('.layui-btn').on('click', function() {
            var othis = $(this),
                type = othis.data('type');
            active[type] && active[type].call(this);
        });

});