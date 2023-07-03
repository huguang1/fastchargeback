// 获取url参数
function g_getQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null)
        return unescape(r[2]);
    return null;
};

/**13位时间戳转换成 年月日 上午 时间  2018-05-23 10:41:08 */
function timeFormat(v, sdformat) {
    return new Date(parseInt(v)).format(sdformat);
}
/**重写toLocaleString方法*/
Date.prototype.format = function (format) {
    var date = {
        "M+": this.getMonth() + 1,
        "d+": this.getDate(),
        "h+": this.getHours(),
        "m+": this.getMinutes(),
        "s+": this.getSeconds(),
        "q+": Math.floor((this.getMonth() + 3) / 3),
        "S+": this.getMilliseconds()
    };
    if (/(y+)/i.test(format)) {
        format = format.replace(RegExp.$1, (this.getFullYear() + '').substr(4 - RegExp.$1.length));
    }
    for (var k in date) {
        if (new RegExp("(" + k + ")").test(format)) {
            format = format.replace(RegExp.$1, RegExp.$1.length == 1
                ? date[k] : ("00" + date[k]).substr(("" + date[k]).length));
        }
    }
    return format;
};

/**
 * 将登录的信息存入cookie中
 * @param value
 */
function setTokenToCookie(value) {
    var Days = 1; //此 cookie 将被保存 30 天  
    var exp = new Date();
    exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
    document.cookie = "my_token =" + escape(value) + ";expires=" + exp.toGMTString();
}


/**
 * 获取存储的token信息
 * @param name
 * @returns
 */
function getCookie(name) {
    var cookieValue;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                //注意这里的编码,存储的时候用的escape 16编码
                cookieValue = unescape(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    //如果cookie获取不到值，则跳转到登录页面
    if (cookieValue) {
        return cookieValue;
    } else {
        window.location.href = "/static/templates/login.html";
    }
}


/**
 * 基本通用JS方法.
 */

/**
 * AJAX post方式提交保存数据.
 *
 * @param url
 *            提交到的URL
 * @param data
 *            要提交的数据，JSON或serialize的表单数据
 * @param callback       需要调用的回调函数
 */
function postAjax(url, data, callback) {
    $.ajax({
        url: url,
        type: "post",
        async: false,
        // headers: {
        // 	my_token: getCookie('my_token') ? getCookie('my_token').split("&")[1] : ''
        // },
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function (e) {
            if (callback) {
                callback.call(this, e);
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            var exceptionMessage = "";
            var responseJson = StringToJson(jqXHR.responseText);
            if (responseJson && responseJson.exception) {
                exceptionMessage = responseJson.exception;
            } else {
                exceptionMessage = jqXHR.responseText;
            }
            if (callback) {
                var backData = {
                    success: false,
                    msg: exceptionMessage
                };
                callback.call(this, backData);
            }
        }
    });
}


/**
 * 将传入字符串转化为JSON对象，如果无法转化，则返回原字符串.
 *
 * @param jsonStr 传入的JSON格式字符串
 * @returns 返回JSON对象，出错返回原字符串
 */
function StringToJson(jsonStr) {
    try {
        var jsonObj = $.parseJSON(jsonStr);
        return jsonObj;
    } catch (ex) {
        return jsonStr;
    }
}

/**
 * AJAX get方式请求
 *
 * @param 请求的URL
 * @param 同步还是一步
 * @param callback       需要调用的回调函数
 */
function getAjax(url, type, callback) {
    $.ajax({
        url: url,
        type: "get",
        async: false,
        headers: {
            my_token: getCookie('my_token') ? getCookie('my_token').split("&")[1] : ''
        },
        success: function (e) {
            if (callback) {
                callback.call(this, e);
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            var exceptionMessage = "";
            var responseJson = StringToJson(jqXHR.responseText);
            if (responseJson && responseJson.exception) {
                exceptionMessage = responseJson.exception;
            } else {
                exceptionMessage = jqXHR.responseText;
            }
            if (callback) {
                var backData = {
                    success: false,
                    msg: exceptionMessage
                };
                callback.call(this, backData);
            }
        }
    });
}


/**
 * 根据传入的参数判断是否有权限.
 *
 * @param jsonStr 传入的JSON格式字符串
 * @returns 返回JSON对象，出错返回原字符串
 */
function checkShiro(value) {
    try {
        var cookie = window.parent.cookieValue;
        if (cookie) {
            var shiro = cookie[2].split("-");
            if (shiro && shiro.length > 0) {
                var index = $.inArray(value, shiro);
                if (index >= 0) {
                    return true;
                } else {
                    return false;
                }
            }
        } else {
            return false;
        }
    } catch (ex) {
        return false;
    }
}

/**
 * 重新更新cookie中的权限字串
 */
function addShiroValue(value) {
    if (value) {
        var oldCookieShiro = parent.cookieValue[2];
        if (oldCookieShiro) {
            parent.cookieValue[2] = oldCookieShiro + '-' + value;
            var arr = oldCookieShiro.split("-");
            arr.push(value);
            parent.cookieValue[2] = arr.join("-");
        } else {
            parent.cookieValue[2] = value;
        }
    }
}

/*
 *　方法:Array.remove(dx)
 *　功能:删除数组元素.
 *　参数:dx删除元素的下标.
 *　返回:在原数组上修改数组
 */
//经常用的是通过遍历,重构数组.
Array.prototype.remove = function (dx) {
    if (isNaN(dx) || dx > this.length) {
        return false;
    }
    for (var i = 0, n = 0; i < this.length; i++) {
        if (this[i] != this[dx]) {
            this[n++] = this[i];
        }
    }
    this.length -= 1;
}


/**
 * 重新更新cookie中的权限字串
 */
function deleteShiroValue(value) {
    if (value) {
        var oldCookieShiro = parent.cookieValue[2];
        if (oldCookieShiro) {
            parent.cookieValue[2] = oldCookieShiro + '-' + value;
            var arr = oldCookieShiro.split("-");
            var index = $.inArray(value, arr);
            arr.remove(index);
            parent.cookieValue[2] = arr.join("-");
        } else {
            parent.cookieValue[2] = value;
        }
    }
}
var setAjax, noJquery;

//  统一处理session过期问题
if (typeof $ === 'undefined') {
    var script = document.createElement("script");
    script.src = "/static/js/common/jquery.js";
    document.body.appendChild(script);
    noJquery = true;
    setAjax = setInterval('ajaxSetup()', '100');

} else {
    ajaxSetup();
}

function ajaxSetup() {
    if (typeof $ === 'undefined') {
        return;
    }
    $.ajaxSetup({
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        complete: function (XMLHttpRequest, textStatus) {
            var response = XMLHttpRequest.responseText;
            var status = XMLHttpRequest.status;
            if (status === 403) {
                return;
            }
            if (response && response.toString().indexOf("<!DOCTYPE html>") > -1) {
                window.location.href = "/config/login";
            }
        }
    });
    if (noJquery) {
        clearInterval(setAjax);
    }

    if (layui && layui.jquery) {
        layui.jquery.ajaxSetup({
            contentType: "application/x-www-form-urlencoded;charset=utf-8",
            complete: function (XMLHttpRequest, textStatus) {
                var response = XMLHttpRequest.responseText;
                var status = XMLHttpRequest.status;
                if (status === 403) {
                    return;
                }
                if (response && response.toString().indexOf("<!DOCTYPE html>") > -1) {
                    window.location.href = "/config/login";
                }
            }
        });
    }
}

