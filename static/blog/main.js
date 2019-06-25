//网站时间
setInterval(getlocaltime, 1000);
function getlocaltime() {
    var localtime = new Date();
    var yy = localtime.getFullYear();
    var mo = localtime.getMonth() + 1;
    var dd = localtime.getDate();
    var hh = localtime.getHours();
    var mm = localtime.getMinutes();
    var ss = localtime.getSeconds();
    mm = extra(mm);
    ss = extra(ss);
    document.getElementById("navbar_time").innerHTML = "NowTime：" + yy + "年" + mo + "月" + dd + "日" + " " + hh + ":" + mm + ":" + ss;
}

function extra(x) {
    if (x < 10) {
        return "0" + x;
    } else {
        return x;
    }
}

function show_runtime() {
    window.setTimeout("show_runtime()",1000);
    X=new
    Date("9/26/2018 10:00:00");
    Y=new Date();T=(Y.getTime()-X.getTime());M=24*60*60*1000;
    a=T/M;A=Math.floor(a);b=(a-A)*24;B=Math.floor(b);c=(b-B)*60;C=Math.floor((b-B)*60);D=Math.floor((c-C)*60);
    document.getElementById("runtime_span").innerHTML = "Running: "+A+"天"+B+"小时"+C+"分"+D+"秒";
}
show_runtime();


//时间控件显示格式#}
$(function () {
    $('#datetimepicker').datetimepicker({
        format: 'YYYY-MM-DD',
        locale: moment.locale('zh-cn'),
        timeZone:'Asia/Shanghai'

    });
    $('#datetimepicker1').datetimepicker({
        format: 'YYYY-MM-DD',
        locale: moment.locale('zh-cn')
    });

});


// 回到顶部
function toTopHide(){
    $(document).scrollTop()>400?
        $("#toTop").show()
        :$("#toTop").hide();
}
$(window).scroll(function(){toTopHide()});


// 导航栏鼠标滑动展开

$(function () {
    $(".dropdown").mouseover(function () {
        $(this).addClass("open");
    });
    $(".dropdown").mouseleave(function(){
        $(this).removeClass("open");
    })
})


//定时弹出模态框
function tip()  {
    $('#myModal1').modal('show');
}
window.setInterval("tip()",600000);
console.log("弹出啦");

// Collapse折叠插件生效
$('.collapse').collapse('toggle');

//代码高亮
SyntaxHighlighter.all();
