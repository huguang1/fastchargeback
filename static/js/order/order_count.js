$(function($) {
	pageInit();
});

function pageInit() {
	queryPageData();
}

function queryPageData() {
	$.get("/config/order/queryIndexData", function(data) {
		// 今日订单数
		$("#todayOrder").html(data.todayNum);
		// 今日订单金额
		$("#todayAmount").html(data.todayAmount);
		// 总订单数
		$("#countOrder").html(data.allNum);
		// 总订单金额
		$("#countAmount").html(data.allAmount);
	});

	//柱状图和折线图的js
    function getChartDay() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('chartDay'));
        $.get('/config/order/queryDaySumOrder?days=7&startDate='+getTime(-1)).done(function(data) {
            var keys=new Array();
            var success=new Array();
            var fail=new Array();
            for(var i=0;i<data.length;i++){
                keys.push(data[i].key);
                success.push(data[i].amountSuccess);
                fail.push(data[i].amountFail);
            }
            myChart.setOption({
                title : {
                    text: '日订单金额',
                    subtext: '日金额变化'
                },
                legend:{
                    data:['成功金额','待支付金额']
                },
                tooltip : {
                    align:'left',
                    trigger: 'axis',
                    formatter: function(datas) {
                        var res="";
                        res +=  '成功金额：' + (datas[0].value) + '元' + '<br/>';
                        res +=  '待支付金额：' + (datas[1].value) + '元' + '<br/>';
                        return res;
                    }
                },
                toolbox: {
                    show : true,
                    feature : {
                        mark : {show: true},
                        dataView : {show: true, readOnly: false},
                        magicType : {show: true, type: ['line', 'bar']},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                xAxis : [
                    {
                        type : 'category',
                        name:"日期",
                        data :keys
                    }
                ],
                yAxis : [
                    {
                        type : 'value',
                        name:"元"
                    }
                ],
                series : [
                    {
                        name:'成功金额',
                        type:'bar',
                        data:success,
                        barWidth:20,
                        barCateGoryGap:20,
                        stack: 'sum'
                    },
                    {
                        name:'待支付金额',
                        type:'bar',
                        data:fail,
                        barWidth:20,   //改变柱状图宽度
                        barCateGoryGap:20,
                        stack: 'sum'
                    }
                ]
            });
        });

    }
    getChartDay();
    function getChartWeek() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('chartWeek'));
        $.get('/config/order/queryWeekSumOrder?weeks=6&startDate='+getMonDate()).done(function(data) {
            var keys=new Array();
            var success=new Array();
            var fail=new Array();
            for(var i=0;i<data.length;i++){
                keys.push(data[i].key);
                success.push(data[i].amountSuccess);
                fail.push(data[i].amountFail);
            }
            myChart.setOption({
                title : {
                    text: '周订单金额',
                    subtext: '周金额变化'
                },
                legend:{
                    data:['成功金额','待支付金额']
                },
                tooltip : {
                    align:'left',
                    trigger: 'axis',
                    formatter: function(datas) {
                        var res="";
                            res +=  '成功金额：' + (datas[0].value) + '元' + '<br/>';
                            res +=  '待支付金额：' + (datas[1].value) + '元' + '<br/>';
                        return res;
                    }
                },
                toolbox: {
                    show : true,
                    feature : {
                        mark : {show: true},
                        dataView : {show: true, readOnly: false},
                        magicType : {show: true, type: ['bar', 'line']},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                xAxis : [
                    {
                        type : 'category',
                        name:"日期",
                        data :keys
                    }
                ],
                yAxis : [
                    {
                        type : 'value',
                        name:"元"
                    }
                ],
                series : [
                    {
                        name:'成功金额',
                        type:'line',
                        data:success,
                        barWidth:20,
                        barCateGoryGap:20,
                        stack: 'sum'
                    },
                    {
                        name:'待支付金额',
                        type:'line',
                        data:fail,
                        barWidth:20,   //改变柱状图宽度
                        barCateGoryGap:20,
                        stack: 'sum'
                    }
                ]
            });
        });

    }
    getChartWeek();
}
function getTime(diff){
    var time = new Date(new Date().getTime() + diff*43200000);
    return time.format("yyyy-MM-dd");
}
function getMonDate() {
        var d=new Date(),
            day=d.getDay(),
            date=d.getDate();
        if(day==1){
             d.setDate(date-7);
        }else if(day==0){
            d.setDate(date-6);
        }else{
            d.setDate(date-day+1);
        }
        return d.format("yyyy-MM-dd");
    }