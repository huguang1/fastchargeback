layui.use(['jquery', 'form', 'layer', 'upload'], function () {
    var upload = layui.upload;
    var token = getCookie("token");
    var requests = GetRequest();
    var payType = requests["pay_code"];
    var form = layui.form, layer = layui.layer, upload = layui.upload;
    var $ = layui.jquery;//重点处
    //执行实例
    var uploadInst = upload.render({
        elem: '#test1', //绑定元素
        headers: {
            'X-CSRF-TOKEN': token
        },
        url: '/config/payCode/filesUpload', //上传接口
        auto: false,
        bindAction: "#test2",
        choose: function (obj) {
            //将每次选择的文件追加到文件队列
            var files = obj.pushFile();
            //预读本地文件，如果是多文件，则会遍历。(不支持ie8/9)
            obj.preview(function (index, file, result) {
                $("#pic").attr("src", result);
                $("#pic").attr("style", "height:100px;width:100px");
            });
        },
        before: function (obj) { //obj参数包含的信息，跟 choose回调完全一致，可参见上文。
            if ($("#comment").val()) {
                this.data = {"payType": payType, "comment": $("#comment").val()}//携带额外的数据
                layer.load(); //上传loading
            } else {
                return false;
            }
        },
        done: function (res) {
            var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
            parent.layer.close(index); //再执行关闭
            window.parent.location.reload();
        },
        error: function (er) {
        }
    });
});
function GetRequest() {
    var url = location.search;
    var theRequest = new Object();
    if (url.indexOf("?") != -1) {
        var str = url.substr(1);
        strs = str.split("&");
        for (var i = 0; i < strs.length; i++) {
            theRequest[strs[i].split("=")[0]] = unescape(strs[i].split("=")[1]);
        }
    }
    return theRequest;
}
function getCookie(sName) {
    var aCookie = document.cookie.split("; ");
    for (var i = 0; i < aCookie.length; i++) {
        var aCrumb = aCookie[i].split("=");
        if (sName == aCrumb[0])
            return unescape(aCrumb[1]);
    }
    return null;
}
