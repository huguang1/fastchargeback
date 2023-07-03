layui.use(['form', 'layedit', 'laydate'], function () {
    var form = layui.form
        , layer = layui.layer
        , layedit = layui.layedit
        , laydate = layui.laydate;

    var token = getCookie("token");
    //监听提交
    form.on('submit(save)', function (data) {
        $.ajax({
            type: "post",
            url: "/config/dictionary/update",
            data: data.field,
            headers: {'X-CSRF-TOKEN': token},
            success: function (data) {
                layer.msg(data.message);
                if (data.code == 200) {
                    setTimeout(function () {
                        var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
                        parent.layer.close(index); //再执行关闭
                    }, 1000);
                }
            }
        });
        return false;
    });

    function renderForm() {
        layui.use('form', function () {
            var form = layui.form;
            form.render();
        });
    }
});

function inputMemberInfo(data) {
    $('input[name="dicKey"]').val(data.dic_key);
    $('input[name="dicValue"]').val(data.dic_value);
    $('input[name="description"]').val(data.description);
    $("#id").val(data.id);
    layui.form.render('select');
}
