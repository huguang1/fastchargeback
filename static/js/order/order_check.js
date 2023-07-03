
//定义为全局变量
var table,timer;
//var orderState = $('#orderState');

layui.use([ 'table', 'layer','laypage', 'form' ], function() {
	var $ = layui.jquery, layer = layui.layer, form = layui.form;
	 table = layui.table;
	 
	 
	var options = {
		elem : '#orderInfo_check',
		height : 'full-180',
		url : '/config/order/tobegrid',
		page : false,
		where : {
			orderState : '30',
			key : $("#moresearch").val(),
			// paymentCode:$("#paymentCode").val()
		},
		text : {
			none : '暂无相关数据'
		},
		even : true,
		cols : [ [ // 表头
		{
			type : 'numbers',
			title : "NO."
		}, {
			field : 'orderId',
			title : '订单编码',
			width : '11%'
		}, {
			field : 'userAccount',
			title : '用户名',
			width : '9%'
		}, {
			field : 'payName',
			title : '支付方式',
			width : '9%'
		}, {
			field : 'orderAmount',
			title : '订单金额',
			width : '10%'
		}, {
			field : 'orderTime',
			title : '订单时间',
			width : '15%'
		}, {
			field : 'paymentName',
			title : '订单来源',
			width : '9%'
		}, {
			field : 'orderState',
			title : '订单状态',
			width : '10%',
			templet : function(d) {
				var retStr = "";
				switch (d.orderState) {
				case 10:
					retStr = "支付处理中";
					break;
				case 30:
					retStr = "支付成功";
					break;	
				default:
					retStr = "支付失败";
				}
				return retStr;
			}
		}, {
			field : 'state',
			title : '处理状态',
			width : '8%',
			templet : function(d) {
				var retStr = "";
				switch (d.state) {
				case 10:
					retStr = '<span style="color:blue;">待处理</span>';
					break;
				case 20:
					retStr = '<span style="color:red;">已锁定(' + d.updateUser + ')</span>';
					break;
				case 30:
					retStr = '<span style="color:blue;">待确认</span>';
					break;
				case 50:
					retStr = '<span style="color:blue;">已取消</span>';
					break;		
				default:
					retStr = '<span style="color:blue;">已确认</span>';
				}
				return retStr;
			}
		}, {
			field : 'orderDesc',
			title : '备注',
			width : '8%'
		}, {
			fixed : 'right',
			title : '操作',
			width : '7%',
			align : 'center',
			templet : '#toolbar',
			unresize : true
		} ] ],
		id : 'orderTable'
		,done:function(){
			var data = table.cache.orderTable;
			var countMoney = 0;
			var count = data.length;
            var myAuto = document.getElementById('videoId');
			if(data && data.length > 0){
				$.each(data,function(index,item){
					countMoney += parseFloat(item.orderAmount);
				});
				//添加播放代码
                myAuto.play();
			}else{
                myAuto.pause();
			}
			$("#countnum").text(count);
			$("#countmoney").text(countMoney.toFixed(2));
			
			//查看是否有查询的权限进行按钮控制
			// if(!checkShiro('select')){
			// 	$("#searchbtn").hide();
			// }
		}
	};

	table.render(options);
	
	
	//初始化10s
	timer = setInterval('refreshQuery()',10 * 1000);  

	table.on('tool(orderInfo)', function(obj) {
		var data = obj.data;
		var layEvent = obj.event;
		var tr = obj.tr;
		if (layEvent === 'edit') {
			$.ajax({
				type : "post",
				url : "/config/order/lockOrder",
				data: data,
				dataType: 'json',
				success : function(obj) {
					layer.msg(obj.message,{time:1000});
					// 执行重载
					table.reload('orderTable', {
						page : false,
						where : {
//							orderState : orderState.val(),
							orderState : 30,
							key : $("#moresearch").val(),
							paymentCode:$("#paymentCode").val()
						}
					});
				}
			});
		}
	});

	active = {
		reload : function() {
			// 执行重载
			table.reload('orderTable', {
				page :false,
				where : {
//					orderState : orderState.val(),
					orderState : 30,
					key : $("#moresearch").val(),
					paymentCode:$("#paymentCode").val()
				}
			});
		}
	};
	
	var freshTime = parseInt($("#refresh").val());
	//监听指定开关
	form.on('switch(switchTest)', function(data){
//		layer.msg(this.checked);
		
		if(this.checked){
			timer = setInterval('refreshQuery()',freshTime * 1000);  
		}else{
			 clearInterval(timer);
		}
	});

	
	//更改定时器刷新的时间
	form.on('select(refresh)', function (data) {
		clearInterval(timer);
		timer = setInterval('refreshQuery()',parseInt(data.value) * 1000);  
     });
	
	
	$('.layui-inline .layui-btn').on('click', function() {
		var type = $(this).data('type');
		active[type] ? active[type].call(this) : '';
	});
	
    // $.ajax({
    //     type: 'get',
    //     url: '/config/order/listPayment',
    //     async: false,
    //     success: function(data) {
    //         //动态加载下拉框
    //         var objSelect = document.getElementById("paymentCode");
    //         objSelect.options.add(new Option("所有",""));
    //         for (var i=0;i<data.length;i++){
    //             objSelect.options.add(new Option(data[i].paymentName,data[i].paymentCode));
    //         }
    //         var form = layui.form;
    //         form.render();
    //     }
    // });
});
$.ajaxSettings.beforeSend = function(xhr,request){
    xhr.setRequestHeader('X-CSRF-TOKEN',cookie.get("token"));
};
//定时器刷新方法
function refreshQuery(){
	table.reload('orderTable', {
		page :false,
		where : {
//			orderState : orderState.val(),
			paymentCode:$("#paymentCode").val(),
			orderState : 30,
			key : $("#moresearch").val()
		}
	});
}

