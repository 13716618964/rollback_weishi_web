from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from io import BytesIO
from rollback import yanzheng,ssh_scp
import mysql
import json,datetime

# Create your views here.
def roll_login(request):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(request.META['REMOTE_ADDR'])
    print(request.META)
    userID = request.session.get('userID')
    if userID != None:
        username = request.session.get('username')
        email = request.session.get('email')
        project_names=request.session.get('project_names')
        return_data={}
        return_data['userID'] = userID
        return_data['username'] = username
        return_data['email'] = email
        return_data['project_names'] = project_names
        #定义页面标签
        return_data['pagetag'] = 'homepage'
        return render(request, 'index.html', return_data)
    #登陆页面
    USERNAME='账　号：'
    PASSWORD='密　码：'
    data={'USERNAME':USERNAME,'PASSWORD':PASSWORD}
    return render(request,'login.html',data)

def create_code_img(request):
    # 在内存中开辟空间用以生成临时的图片
    f = BytesIO()
    img, code = yanzheng.create_code()
    request.session['check_code'] = code
    img.save(f, 'PNG')
    return HttpResponse(f.getvalue())

def user_verification(request):
    #登陆验证
    if request.method != 'post':
        HttpResponse(status=404)
    username=request.POST.get('username')
    password=request.POST.get('password')
    password=yanzheng.md5_encryption(password)
    sql=''' select userID,password,email from t_user_info where username='%s' ''' %username
    data=mysql.mysql_info(sql,'one')
    if len(data) == 0:
        return HttpResponse('''<script language="javascript"> 
                                alert("账号/密码错误"); 
                                javascript:window.location.href = '/';
                                </script>''')
    if password == data[1]:
        userID=data[0]
        email=data[2]
        #加入session
        request.session['userID']=userID
        request.session['username']=username
        request.session['email']=email
        return HttpResponseRedirect('/index.html')
    else:
        return HttpResponse('''<script language="javascript"> 
                                alert("账号/密码错误"); 
                                javascript:window.location.href = '/';
                                </script>''')

def roll_homepage(request):
    #获取session
    userID=request.session.get('userID')
    if userID == None:
        return HttpResponseRedirect('/')
    username=request.session.get('username')
    email=request.session.get('email')
    #项目名称栏
    sql=''' select project_name from t_project_info order by projectID ASC '''
    project_names=mysql.mysql_info(sql,'all')
    project_list=[]
    for name in project_names:
        project_list.append(name[0])
    request.session['project_names']=project_list
    return_data={}
    return_data['userID']=userID
    return_data['username']=username
    return_data['email']=email
    return_data['project_names']=project_list
    #定义页面标签
    return_data['pagetag']='homepage'
    return render(request,'index.html',return_data)

def project_web(request):
    #定义项目页面
    if request.method != 'GET':
        return HttpResponse(status=500)
    # 获取session
    userID = request.session.get('userID')
    if userID == None:
        return HttpResponseRedirect('/')
    username = request.session.get('username')
    email = request.session.get('email')
    project_names = request.session.get('project_names')
    pagetag=request.GET.get('project')
    #获取项目信息
    sql=''' select server_ip,back_path from t_project_info where project_name='%s' ''' %pagetag
    mysql_data=mysql.mysql_info(sql,'one')
    if mysql_data == None:
        return HttpResponse(status=403)
    server_ip=[]
    back_file_dir={}
    for ip in mysql_data[0].split(','):
        server_ip.append(ip)
        sql=''' select IP,PORT,USERNAME,PASSWORD from t_server_info where IP='%s' ''' %ip
        server_info=mysql.mysql_info(sql,'one')
        cmd=''' cd %s;ls *.gz|sort -rn ''' %mysql_data[1]
        back_file_list = []
    #print(server_info)
        if server_info != None:
            back_file=ssh_scp.ssh_server(server_info[0],server_info[1],server_info[2],server_info[3],cmd)
            #print(back_file)
            if back_file != None:
                back_file_list=[]
                for file in back_file.split('\n'):
                    if file != '':
                        back_file_list.append(file)
        back_file_dir[ip]=back_file_list
    print(back_file_dir)
    ip_num=len(server_ip)
    print(ip_num)
    #传递变量到修改页面，把需要的变量加入session
    '''
    request.session['server_ip']=str_server_ip
    request.session['pagetag']=pagetag
    '''
    #用ajax调用接口
    return_data = {}
    # 定义页面标签
    return_data['pagetag'] =pagetag
    return_data['userID'] = userID
    return_data['username'] = username
    return_data['email'] = email
    return_data['project_names'] = project_names
    return_data['ip_num']=ip_num
    return_data['back_files']=back_file_dir
    return_data['server_ip']=server_ip
    return render(request, 'index.html', return_data)

def rollbackingceshi(request):
    ip_list=request.POST.get('ip')
    project=request.POST.get('project_name')
    reslue=''
    for ip in ip_list.split(','):
        version=request.POST.get(ip)
        sql=''' select s.IP,s.PORT,s.USERNAME,s.PASSWORD,p.back_path,p.code_path,p.project_path from t_server_info s , t_project_info p where p.project_name='%s' and s.IP='%s'  ''' %(project,ip)
        mysql_data=mysql.mysql_info(sql,'one')
        cmd='cd %s\n' %mysql_data[5]
        cmd+='cp %s/%s ./\n' %(mysql_data[4],version)
        cmd+='tar zxf %s\n' %version
        cmd+='kill -9 `cat %s/server.pid`\n' %mysql_data[6]
        cmd+='sleep 1 && %s/bin/startup.sh\n' %mysql_data[6]
        print(cmd)
        ssh_data=ssh_scp.ssh_server(mysql_data[0],mysql_data[1],mysql_data[2],mysql_data[3],cmd)
        print(ssh_data)
        cmd='ls -l %s' %mysql_data[5]
        ssh_data = ssh_scp.ssh_server(mysql_data[0], mysql_data[1], mysql_data[2], mysql_data[3], cmd)
        reslue+=ssh_data
    return HttpResponse(reslue)

#删除session(退出登陆)
def delete_session(request):
    del request.session['userID']
    del request.session['username']
    del request.session['email']
    del request.session['project_names']
    return HttpResponse('{"status":"OK"}')

#ajax调用后端rollback接口
def rollback_api(request):
    if request.method != 'POST':
        return HttpResponse(status=500)
    # 获取session
    userID = request.session.get('userID')
    if userID == None:
        return HttpResponseRedirect('/')
    username = request.session.get('username')
    #获取ajax的传参
    file_name=request.POST.get('file_name')
    print(file_name)
    if file_name == '无法回滚':
        #return HttpResponse('{"status":"ERR","info":"没有回滚文件"')
        return HttpResponse(status=404)
    project=request.POST.get('project')
    server_ip=request.POST.get('server_ip')
    sql=''' select PORT,USERNAME,PASSWORD from t_server_info where IP='%s' ''' %server_ip
    PORT, USERNAME, PASSWORD=mysql.mysql_info(sql,'one')
    sql=''' select back_path,code_path,project_path from t_project_info where project_name='%s'  ''' %project
    back_path, code_path, project_path=mysql.mysql_info(sql,'one')
    #//每台服务器上的备份文件的名称不同，所以需要单台回滚
    command=''' sh /automation/shell/rollback.sh %s %s %s %s %s''' %(project_path,back_path,code_path,project,file_name)
    ssh_data=ssh_scp.ssh_server(server_ip,PORT,USERNAME,PASSWORD,command)
    DATETIME=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    info=(username+'\t'+project+' '+server_ip+' '+DATETIME)
    ssh_scp.result_log('rollback.log',info)
    ssh_data=json.loads(ssh_data)
    return HttpResponse(json.dumps(ssh_data), content_type="application/json")

def user_info(request):
    if request.method != 'GET':
        return HttpResponse(status=504)
    # 获取session
    userID = request.session.get('userID')
    if userID == None:
        return HttpResponseRedirect('/')
    username = request.session.get('username')
    email = request.session.get('email')
    project_names = request.session.get('project_names')
    return_data = {}
    # 定义页面标签
    return_data['pagetag'] = 'user_info'
    return_data['userID'] = userID
    return_data['username'] = username
    return_data['email'] = email
    return_data['project_names'] = project_names
    return render(request,'index.html',return_data)

def update_password(request):
    if request.method != 'POST':
        return HttpResponse(status=504)
    # 获取session
    userID = request.session.get('userID')
    if userID == None:
        return HttpResponseRedirect('/')
    #获取新密码
    password=request.POST.get('new_password')
    password=yanzheng.md5_encryption(password)
    sql=""" update t_user_info set password='%s' where userID='%s' """ %(password,userID)
    mysql.mysql_write(sql)
    del request.session['userID']
    del request.session['username']
    del request.session['email']
    del request.session['project_names']
    return HttpResponse('''<script language="javascript"> 
                                        alert("修改成功，请重新登陆。"); 
                                        window.location.href="/";
                                       </script>''')


def add_user(request):
    if request.method != 'GET':
        return HttpResponse(status=504)
    # 获取session
    userID = request.session.get('userID')
    if userID == None:
        return HttpResponseRedirect('/')
    username = request.session.get('username')
    email = request.session.get('email')
    project_names = request.session.get('project_names')
    return_data = {}
    # 定义页面标签
    return_data['pagetag'] = 'add_user'
    return_data['userID'] = userID
    return_data['username'] = username
    return_data['email'] = email
    return_data['project_names'] = project_names
    return render(request, 'index.html', return_data)

def add_user_api(request):
    if request.method != 'POST':
        return HttpResponse(status=504)
    # 获取session
    userID = request.session.get('userID')
    if userID == None:
        return HttpResponseRedirect('/')
    #获取参数
    new_usernaem=request.POST.get('username')
    new_password=request.POST.get('password')
    new_email=request.POST.get('email')
    sql=''' SELECT (CASE username WHEN '%s' THEN 'yes' ELSE  'no' END ) AS exist FROM  t_user_info WHERE username='%s' ''' %(new_usernaem,new_usernaem)
    result=mysql.mysql_info(sql,'one')
    if result == None:
        sql=''' INSERT INTO t_user_info(username,password,email) VALUE('%s','%s','%s')''' %(new_usernaem,new_password,new_email)
        mysql.mysql_write(sql)
        return HttpResponse('''<script language="javascript"> 
                                alert("添加成功"); 
                                window.location.href="/adduser.html";
                                </script>''')
    elif result == 'yes':
        return HttpResponse('''<script language="javascript"> 
                                alert("用户已存在"); 
                                window.location.href="/adduser.html";
                                </script>''')
    else:
        return HttpResponse('ERROR')



def concurrent_test(request):
    mysql.concurrent_test()
    return HttpResponse('123456789')
