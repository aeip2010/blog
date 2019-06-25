// 时间线筛选
$(document).ready(function() {
    $("#search-text1").keyup(function () {
        // 遍历值
        var q = $("#search-text1").val();
        $.get("/timesearch/", {'q': q}, function (data) {
            if (data.message == "false") {
                /* 显示评论信息*/
                var data1 = JSON.parse(data.weibos), //返回的result为json格式的数据
                    con1 = "";
                console.log(data1);
                con1+='<div style="padding: 0px 100px; background-color: #fff;">'
                con1+='<table class="table table-hover"><thead><tr class="form-list-font">'
                con1+= '<th>时间</th> <th>内容</th> <th>地标</th> <th>地点</th> <th>关键字</th> <th>类型</th>'
                con1+='</thead> <tbody> <tr class="form-list-font">'
                $.each(data1, function (index, item) {
                    con1+='<td>'+ item.fields.year+'-'+ item.fields.month+ '</td><td>'+item.fields.content+'</td>'
                    con1+= '<td>'+item.fields.landmark+'</td> <td>'+item.fields.city+'</td>'
                    con1+='<td>'+item.fields.keyword+'</td><td>'+item.fields.type+ '</td>'
                    con1+= '</tr> </tbody> '
                });
                con1+='</table> </div>'

                $("#timeline_type").html(con1); //把内容入到这个div中即完成
                if (q!=""){
                    qs =q;
                }
                else {
                    qs="全部内容"
                }
                var seartitle = "";
                seartitle += '<span style="color: blue">['+qs+']</span> '+'搜索结果 (共 ' + data.weibos_count + ' 大事件)';
                $("#title").html(seartitle);
            }
            else {
                $("#timeline_type").html("暂无搜索结果,请更换搜索词！"); //把内容入到这个div中即完成
                $("#title").html("暂无搜索结果");
            }

            $('#search-text1').keydown(function () {
                $('#search-result1').empty();

            });
        });
    });
});

// 微博搜索

$(document).ready(function() {
    $("#search-text1").keyup(function () {
        // 遍历值
        var q = $("#search-text1").val();
        $.get("/weibosearch/", {'q': q}, function (data) {
            if (data.message == "false") {
                /* 显示评论信息*/
                var data1 = JSON.parse(data.weibos), //返回的result为json格式的数据
                    con1 = "";
                console.log(data1);
                $.each(data1, function (index, item) {
                    time1 = item.fields.create_time.split("T")[0];
                    time2 = item.fields.create_time.split("T")[1]
                    time3 = time2.split(".")[0]

                    con1 += "<p>";
                    con1 += '第  <a class="post-id" href="#">【<strong style="color: blue">' + item.pk + '</strong>】</a>条  ' + "<span class=\"glyphicon glyphicon-time\">：" + time1  + " " + time3 +" ";
                    con1 += '<span class="glyphicon glyphicon-user">：' + item.fields.createuser + "  ";
                    con1 += '<span class="glyphicon glyphicon-map-marker">：' + item.fields.ip + '</a></p> ';
                    con1 += "<p>" + item.fields.content + "</p>";
                    con1 += "<hr class=\"the-line\"  />"
                });
                $("#weibopost").html(con1); //把内容入到这个div中即完成
                if (q!=""){
                    qs =q;
                }
                else {
                    qs="全部内容"
                }
                var seartitle = "";
                seartitle += '<span style="color: blue">['+qs+']</span> '+'搜索结果 (共 ' + data.weibos_count + ' 句叨叨)';
                $("#title").html(seartitle);
            }
            else {
                $("#weibopost").html("暂无搜索结果,请更换搜索词！"); //把内容入到这个div中即完成
                $("#title").html("暂无搜索结果");
            }


            $('#search-text1').keydown(function () {
                $('#search-result1').empty();

            });
        });
    });
});

// 评论提交
$(document).ready(function(){
    $('#jsStayBtn').on('click', function(){
        $.ajax({
            cache: false,
            type: "POST",
            url:"/add_comment/",
            data:$('#jsStayForm').serialize(),
            dateType:"json",
            async: true,
            beforeSend:function(xhr, settings){
                xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
            },
            success: function(data) {
                if(data.status == 'success'){
                    alert("提交成功");
                    window.location.reload();//刷新当前页面
                    console.log("更新评论内容");
                    var data1 = JSON.parse(data.comments), //返回的result为json格式的数据
                        con1 = "";
                    console.log(data1);
                    /* 打印出评论内容 索引用index、评论总数可以传过来*/
                    $.each(data1, function(index, item){
                        time1 = item.fields.create_time.split("T")[0];
                        time2 = item.fields.create_time.split("T")[1]
                        time3 = time2.split(".")[0]

                        index+=1
                        con1+='<li class="comment-item"> <hr class="the-line" /> <p class="floor">['+index +'楼]  '
                        con1+='<span class="nickname">'+item.fields.name + '</span> -'
                        con1+='<time class="comment-submit-date" >'+ time1 + " " +time3+ " " + '</time> </p>'
                        con1+='<div style="word-wrap: break-word">'+item.fields.content+ '</div></li>'
                    });
                    console.log(con1);    //可以在控制台打印一下看看，这是拼起来的标签和数据
                    $("#all_comment").html('评论 [共'+ data.comments_count+ '条]')
                    $("#comment_type").html(con1); //把内容入到这个div中即完成
                }
                else if(data.status == 'false'){
                    alert("评论错误，请重新评论");
                    alert(data.message);
                }
            },
        });
    });
});

