function exit() {
    if(window.confirm('你确定要退出吗？')){
                    $.ajax  ({
                        type: "GET",
                        url: "/exit",
                        dataType: "json",
                        success: function(info) {
                            var result = info.status;
                            if (result=='OK') {
                                alert('退出成功');
                                javascript:window.location.href = '/';
                            }
                        }
                    })
              }else{
                 return false;
             }
}

function axaj_rollback(ths) {
    if(window.confirm('你确定要退出吗？')){
    /*    获取参数   */
    var back_file_name=document.getElementsByName('version')[0].value;    //回滚文件名称
    var project=document.getElementsByName('project')[0].id;              //项目名称
    var ips=document.getElementById('ip').name;                            //服务器ip
    /*     把ip改变成数组   */
    var ip_list=ips.split(',');
    var ip_num=ip_list.length;
    /*   for循环回滚每个IP   */
    var for_num;
    for(for_num in ip_list){
        var ip=ip_list[for_num];
        /* test
        console.log(ip);
        console.log('-----------------');
        */
        $.ajax({
        type:"POST",
        url:"/rollbacking",
        dataType: "json",
        data:{file_name:back_file_name,project:project,server_ip:ip},
        success: function(info) {
                            console.log(info);
                            //console.log(info.status);
                            var result = info.status;
                            console.log(result);
                            if (result=='success') {
                                console.log(ip+'成功');
                            }else{
                                console.log(ip+'未成功');
                            }

                            }
    })
  }}else{
        return false;
    }
}


function delete_project(ths) {
    var res = confirm("确定要删除吗？");
    if(res==true) {
        var project = ths.id;
        $.ajax({
            type: "POST",
            url: "/api_del_project",
            dataType: "json",
            data: {project: project},
            success: function (info) {
                var result = info.status;
                if (result == 'success') {
                    alert('删除成功');
                    //window.location.reload();
                    parent.document.location.reload();
                } else {
                    alert('删除失败')
                    //window.location.href="/index.html";
                    parent.document.location.reload();
                }
            }
        })
    }
}

function password_judge() {
    var password=document.getElementById('pass').value;
    var pass_num=password.length;
    var new_password=document.getElementById('new_pass').value;
    var new_pass_num=new_password.length;
    /* 密码位数 */
    if(pass_num<6){
        alert('密码位数不能小于6');
        return false;
    }
    /* 特殊字符*/
    var regEn = /[`~!@#$%^&*()_+<>?:"{},.\/;'[\]]/im,
         regCn = /[·！#￥（——）：；“”‘、，|《。》？、【】[\]]/im;
    if(regEn.test(password) || regCn.test(password)) {
        alert("名称不能包含特殊字符.");
        return false;
	    }
    /*两次密码是否相同*/
    if(password!=new_password) {
        alert('两次密码不一致');
        return false;
    }
    return true;
}

function user_judge() {
    var username=document.getElementsByName('username')[0].value;
    var password=document.getElementsByName('password')[0].value;
    var user_num=username.length;
    var pass_num=password.length;
    if(user_num<5 || pass_num<6){
        alert('用户名不能小于5位且密码不能小于6位');
        return false;
    }else{
        return true;
    }
}

function xxx() {
    var num=document.getElementById('server_num').value;
    var ip=document.getElementById('ip').value;
    console.log(num);
    console.log(ip);
    return false;
}