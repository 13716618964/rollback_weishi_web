    function refresh_check_code(ths) {
        ths.src += '?';
        //src后面加问号会自动刷新验证码img的srclogin
    }
    function jiance() {
    var newName=document.getElementsByName('username')[0].value;
    var regEn = /[`~!@#$%^&*()_+<>?:"{},.\/;'[\]]/im,
         regCn = /[·！#￥（——）：；“”‘、，|《。》？、【】[\]]/im;
    if(regEn.test(newName) || regCn.test(newName)) {
        alert("名称不能包含特殊字符.");
        return false;
	    }
    }


    function login() {
    var name=document.getElementsByName('username')[0].value;
        if (name.length == 0) {
            alert("用户名不能为空");
            return false;
        }
        var regEn = /[`~!@#$%^&*()_+<>?:"{},.\/;'[\]]/im,
             regCn = /[·！#￥（——）：；“”‘、，|《。》？、【】[\]]/im;
        if(regEn.test(name) || regCn.test(name)) {
        alert("名称不能包含特殊字符.");
        return false;
	    }

        var pass = document.getElementById("pass");
        if (pass.value.length == 0) {
            alert("密码不能为空");
            return false;
        }
        var code = document.getElementById("code");
        if (code.value.length != 4) {
            alert("请按照图片输入验证码");
            return false;
        }
        return true;
    }

