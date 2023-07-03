layui.use([ 'table', 'layer', 'laydate' ], function() {
	var $ = layui.jquery, layer = layui.layer, laydate = layui.laydate;
	var table = layui.table;

	var userinfo = JSON.parse(window.localStorage.getItem('user'));
	var newDate = new Date();
	var nowTime = newDate.valueOf();
	var endstr = newDate.toLocaleDateString().replace(/\//g,"-").concat(" 12:00:00");
	newDate.setDate(newDate.getDate() -1);
	var startstr = newDate.toLocaleDateString().replace(/\//g,"-").concat(" 12:00:00");
	
	var max = null;

	var start = laydate.render({
		elem : '#start_time',
		type : 'datetime',
		format: 'yyyy-MM-dd HH:mm:ss',
		value : startstr,
		isInitValue: true,	
		max : nowTime,
		btns : [ 'clear', 'confirm' ],
		done : function(value, date) {
			endMax = end.config.max;
			end.config.min = date;
			end.config.min.month = date.month - 1;
		}
	});
	var end = laydate.render({
		elem : '#end_time',
		type : 'datetime',
		format: 'yyyy-MM-dd HH:mm:ss',
		value : endstr,
		isInitValue: true,	
		max : nowTime,
		done : function(value, date) {
			if ($.trim(value) == '') {
				var curDate = new Date();
				date = {
					'date' : curDate.getDate(),
					'month' : curDate.getMonth() + 1,
					'year' : curDate.getFullYear()
				};
			}
			start.config.max = date;
			start.config.max.month = date.month - 1;
		}
	});

	var options = {
		elem : '#accountsTable',
		height : 'full-180',
		url : '/config/order/orderAccounts',
		where : {
			startTime : startstr,
			endTime : endstr
		},
		page : false,
		cellMinWidth : 100,
		text : {
			none : '暂无相关数据'
		},
		even : true,
		cols : [ [ // 表头
		{
			type : 'numbers',
			title : "NO."
		}, {
			field : 'pay_name',
			title : '支付平台'
		}, {
			field : 'amount',
			title : '充值金额'
		}, {
			field : 'poundage',
			title : '手续费'
		} ] ],
		id : 'accountsTable',
		done: function(res, curr, count){
			var zongOrder = 0;
			var zongRate = 0;
			//遍历
			var datalist = res.data;
			if(datalist.length == 0) return;
			for(var idex in datalist){
				if(idex >= 0){
					zongOrder  = parseFloat(zongOrder + datalist[idex].amount);
					zongRate =  parseFloat(zongRate + datalist[idex].poundage);
				}else{
					break;
				}
			}
			var trhtml = "<tr><td></td><td>总计</td><td>总充值："+ Math.round(zongOrder *100)/100 +"</td><td>总手续费：" 
						+Math.round(zongRate *100)/100+"</td></tr>";
			$(".layui-table-body tbody").append(trhtml);
		}
	};

	var tableIns = table.render(options);

	active = {
		reload : function() {
			// 执行重载
			tableIns.reload({
				where : {
                    startTime : $('#start_time').val(),
                    endTime : $('#end_time').val()
				}
			});
		}
	};

	$('.layui-inline .layui-btn').on('click', function() {
		var type = $(this).data('type');
		active[type] ? active[type].call(this) : '';
	});
});
