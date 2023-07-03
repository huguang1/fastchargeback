layui.use(['form', 'layer'], function () {
    var form = layui.form
        , layer = layui.layer;
    var token = getCookie('token');
    //监听提交
    form.on('submit(save)', function (data) {
        $.ajax({
            type: "post",
            url: "/config/dictionary/save",
            data: data.field,
            headers: {'X-CSRF-TOKEN': token},
            success: function (data) {
                layer.msg(data.message);
                if (data.code == 200) {
                    setTimeout(function () {
                        var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
                        window.parent.location.reload();
                        parent.layer.close(index); //再执行关闭
                    }, 1000);
                }
            }
        });
        return false;
    });
});
