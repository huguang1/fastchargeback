//下拉多选
var formSelects = layui.formSelects;
//重新渲染表单
function renderForm() {
    layui.use('form', function () {
        var form = layui.form;//高版本建议把括号去掉，有的低版本，需要加()
        form.render();
    });
};

function initRole(data, res) {
    $("#id").val(res.id);
    $("#userName").val(res.user_name);
    $("#nickname").val(res.nick_name);
    $("#password").val(res.password);
    $("#repassword").val(res.password);
    //动态加载下拉框
    var roleArray = new Array();
    for (var i = 0; i < data.length; i++) {
        var role = {
            "name": data[i].role_desc,
            "value": data[i].id,
            "selected": checkRole(res.roleList, data[i].id),
            "disabled": ""
        }
        roleArray.push(role);
    }
    formSelects.data('roleSelect', 'local', {
        arr: roleArray,
        linkage: false
    });
};

layui.config({
    base: window.parent.baseUrl + '/layui/' //静态资源所在路径
}).use(['form', 'laydate'], function () {
    var token = getCookie('token');
    layer = layui.layer,
        form = layui.form,
        index = parent.layer.getFrameIndex(window.name); //获取窗口索引;
    /* 自定义验证规则 */
    form.verify({
        userName: function (value) {
            if (value.length < 3) {
                return '名称至少得3个字';
            }
        },
        pwd: [/(.+){6,12}$/, '密码必须6到12位'],
        content: function (value) {
            layedit.sync(editIndex);
        }
    });

    /* 监听提交 */
    form.on('submit(editUserSubmit)', function (data) {
        if (data.field.password != data.field.repassword) {
            layer.alert('两次输入的密码不一致，请确认！');
            return false;
        }

        var paramsData = data.field;
        var userRoleStr = getUserRoleStr();
        if (userRoleStr != '') {
            paramsData.roleListStr = userRoleStr;
        }

        $.ajax({
            type: 'post',
            url: window.parent.parent.baseUrl + '/sys/user/updateUser',
            data: paramsData,
            headers: {'X-CSRF-TOKEN': token},
            success: function (result) {
                if (result.code == 200) {
                    layer.alert(result.message, {
                        icon: 6,
                        title: "提示"
                    }, function (index) {
                        layer.close(index);
                        var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
                        parent.layer.close(index); //再执行关闭
                        window.parent.location.reload();
                    });
                } else {
                    layer.alert(result.message, {
                        icon: 5,
                        title: "提示"
                    }, function (index) {
                        layer.close(index);
                        var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
                        parent.layer.close(index); //再执行关闭
                        window.parent.location.reload();
                    });
                }
            }
        })
        return false;
    });

    var active = {
        cancel: function (set) {
            parent.layer.close(index);
        }
    }
    $('.layui-btn').on('click', function () {
        var othis = $(this),
            type = othis.data('type');
        active[type] && active[type].call(this);
    });
});

//判断是否要把角色列表选择的方法
function checkRole(arr, roleId) {
    for (var i = 0; i < arr.length; i++) {
        if (roleId === arr[i].id) {
            return true;
        }
    }
    return false;
}

// 返回用户选了什么角色，用","号隔开
function getUserRoleStr() {
    var roleArr = formSelects.value('roleSelect');
    var roleArrStr = "";
    if (roleArr != null && roleArr != '') {
        for (var i = 0; i < roleArr.length; i++) {
            roleArrStr += roleArr[i].value;
            if (i != roleArr.length - 1) {
                roleArrStr += ",";
            }
        }
    }
    return roleArrStr;
}
