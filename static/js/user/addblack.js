layui.config({
    base: window.parent.baseUrl + '/layui/' //静态资源所在路径
}).use(['form', 'laydate'], function() {
    var token = getCookie('token');
    layer = layui.layer,
    form = layui.form,
    index = parent.layer.getFrameIndex(window.name); //获取窗口索引;
    /* 自定义验证规则 */
    var reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
    form.verify({
        userName: function(value) {
            if(value && value.length < 3) {
                return '名称至少得3个字';
            }
        },
        checkIp: function(value) {
            if(value && !new RegExp(reg).test(value)) {
                return 'IP格式不正确';
            }
        },
        content: function(value) {
            layedit.sync(editIndex);
        }
    });

    /* 监听提交 */
    form.on('submit(paysubmit)', function(data) {
        if(data && data.field && (data.field.ip || data.field.userName)){
            $.ajax({
                type: 'post',
                url: window.parent.parent.baseUrl + '/blackWhite/addBlack',
                data: data.field,
                dataType: 'json',
                headers: {'X-CSRF-TOKEN': token},
                success: function(result) {
                    if(result.code == 200){
                        layer.alert(result.message,{
                            icon:6,
                            title:"提示"
                        },function(index){
                            layer.close(index);
                            var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
                            parent.layer.close(index); //再执行关闭
                            window.parent.location.reload();
                        });
                    }else{
                        layer.alert(result.message,{
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
            })

        }else{
            layer.alert("请输入会员名或者ip",{icon:6,
                title:"提示"
            })
        }
        return false;
    });

    var active = {
        cancel: function(set) {
            parent.layer.close(index);
        }
    }

    $('.layui-footer .layui-btn').on('click', function() {
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
    });
});