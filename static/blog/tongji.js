//UUID
// var uuid = " "
// const UUIDGeneratorBrowser = () =>
// ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
// (c ^ (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))).toString(16)
// );
// uuid = UUIDGeneratorBrowser();

// 获取浏览器版本
function getBrowserVersion(){
    var agent = navigator.userAgent.toLowerCase();
    var arr={};
    var Browser="";
    var Bversion="";
    var verinNum="";

    //IE
    if(agent.indexOf("msie") > 0){
        var regStr_ie = /msie [\d.]+;/gi ;
        Browser="IE";
        Bversion=""+agent.match(regStr_ie)
    }
    //firefox
    else if(agent.indexOf("firefox") > 0){
        var regStr_ff = /firefox\/[\d.]+/gi;
        Browser="firefox";
        Bversion=""+agent.match(regStr_ff);
    }
    //Chrome
    else if(agent.indexOf("chrome") > 0){
        var regStr_chrome = /chrome\/[\d.]+/gi ;
        Browser="chrome";
        Bversion=""+agent.match(regStr_chrome);
    }
    //Safari
    else if(agent.indexOf("safari") > 0 && agent.indexOf("chrome") < 0){
        var regStr_saf = /version\/[\d.]+/gi ;
        Browser="safari";
        Bversion=""+agent.match(regStr_saf);
    }
    //Opera
    else if(agent.indexOf("opera")>=0){
        var regStr_opera = /version\/[\d.]+/gi ;
        Browser="opera";
        Bversion=""+agent.match(regStr_opera);
    }else{
        var browser=navigator.appName;
        if(browser=="Netscape"){
            var version=agent.split(";");
            var trim_Version=version[7].replace(/[ ]/g,"");
            var rvStr=trim_Version.match(/[\d\.]/g).toString();
            var rv=rvStr.replace(/[,]/g,"");
            Bversion=rv;
            Browser="IE"
        }
    }
    verinNum=(Bversion+"").replace(/[^0-9.]/ig,"");
    arr["Browser"] = Browser;
    arr["Verin"] = verinNum;
    arr["Agent"] = agent;
    arr["Reffer_url"] = document.referrer;
    arr["Local_url"] = window.location.href;
    // arr["UUID"] = uuid;
    console.log(arr);
    return arr
};

// 浏览器版本信息传递
$(document).ready(function(){
    $("button[id^=browser]").on('click', function(){
    // $('#browser').on('click', function(){
        console.log("点击了");
        var x = new getBrowserVersion();
        console.log(x);
        $.ajax({
            cache: false,
            type: "POST",
            url:"/version/",
            data:JSON.stringify(x),
            dateType:"application/json",
            async: true,
            beforeSend:function(xhr, settings){
                xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
            },
            success: function(data) {
                if(data.status == 'success'){
                    console.log("提交成功");
                    // alert("提交成功");
                }
                else if(data.status == 'false'){
                    alert(data.message);
                }
            },
        });
    });
});