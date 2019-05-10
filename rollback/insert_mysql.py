from django.shortcuts import render,HttpResponse,HttpResponseRedirect
import mysql
from rollback import ssh_scp
import datetime,json

#插入项目
def insert_project(request):
    userID = request.session.get('userID')
    if userID == None:
        return HttpResponseRedirect('/')
    username = request.session.get('username')
    project_names = request.session.get('project_names')
    return_data={}
    return_data['pagetags'] = 'insert'
    return_data['userID'] = userID
    return_data['username'] = username
    return_data['project_names'] = project_names
    return_data['pagetag'] = 'insert'
    return render(request,'index.html',return_data)

def judge_server(request):
    if request.method != 'POST':
        return HttpResponse(status=500)
    userID = request.session.get('userID')
    if userID == None:
        return HttpResponseRedirect('/')
    username = request.session.get('username')
    project_names = request.session.get('project_names')
    project_name=request.POST.get('project_name')
    project_server=request.POST.get('project_server')
    project_bakcode=request.POST.get('project_bakcode')
    project_codepath=request.POST.get('project_codepath')
    project_path=request.POST.get('project_path')
    sql=''' insert into t_project_info(project_name,server_ip,back_path,code_path,project_path) value('%s','%s','%s','%s','%s') ''' %(project_name,project_server,project_bakcode,project_codepath,project_path)
    if mysql.mysql_write(sql):
        #重新读取project_names并加入session
        sql = ''' select project_name from t_project_info order by projectID ASC '''
        project_names = mysql.mysql_info(sql, 'all')
        project_list = []
        for name in project_names:
            project_list.append(name[0])
        request.session['project_names'] = project_list
        ######判断服务器是否都在库内
        server_ip=[]
        if ',' in project_server:
            for ip in project_server.split(','):
                if ip != '':
                    server_ip.append(ip)
        else:
            server_ip.append(project_server)
        no_server=[]
        for ip in server_ip:
            sql=''' select * from t_server_info where IP='%s' ''' %ip
            print(ip)
            server_data=mysql.mysql_info(sql,'one')
            print('server_data:',server_data)
            if server_data == None:
                no_server.append(ip)
        print(no_server)
        print(len(no_server))
        if len(no_server) != 0:
            return_data = {}
            return_data['no_server'] = no_server
            return_data['username'] = username
            return_data['project_names'] = project_list
            ########################
            return_data['pagetag'] = 'add_server'
            return_data['userID'] = userID
            return_data['username'] = username
            return_data['server_num']=len(no_server)
            return render(request,'index.html',return_data)
        return HttpResponse('''<script language="javascript"> 
                				alert("插入成功"); 
                				window.location.href="/insert_project.html";
                				</script>''')
    else:
        return HttpResponse('''<script language="javascript"> 
                				alert("插入失败"); 
                				window.location.href="/insert_project.html";
                				</script>''')

def delete_project(request):
    if request.method == 'GET':
        userID = request.session.get('userID')
        if userID == None:
            return HttpResponseRedirect('/')
        username = request.session.get('username')
        project_names = request.session.get('project_names')
        sql=''' select project_name,server_ip from t_project_info '''
        mysql_data=mysql.mysql_info(sql,'all')
        print(mysql_data)
        return_data={}
        return_data['username'] = username
        return_data['project_names'] = project_names
        return_data['projects']=mysql_data
        return_data['pagetag'] = 'del_project'
        return render(request,'index.html',return_data)
    elif request.method == 'POST':
        userID = request.session.get('userID')
        if userID == None:
            return HttpResponseRedirect('/')
        username = request.session.get('username')
        project=request.POST.get('project')
        sql=''' delete from t_project_info where project_name='%s' ''' %project
        print(sql)
        if mysql.mysql_write(sql):
            sql = ''' select project_name from t_project_info order by projectID ASC '''
            project_names = mysql.mysql_info(sql, 'all')
            project_list = []
            for name in project_names:
                project_list.append(name[0])
            request.session['project_names'] = project_list
            DATETIME = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            relute=(username+'\t'+DATETIME+'\t'+project)
            ssh_scp.result_log('del_project.log',relute)
            return_data={}
            return_data['status']='success'
            return HttpResponse(json.dumps(return_data), content_type="application/json")
        else:
            sql = ''' select project_name from t_project_info order by projectID ASC '''
            project_names = mysql.mysql_info(sql, 'all')
            project_list = []
            for name in project_names:
                project_list.append(name[0])
            request.session['project_names'] = project_list
            return_data={}
            return_data['status'] = 'error'
            return HttpResponse(json.dumps(return_data), content_type="application/json")
    else:
        return HttpResponse(status=504)


def add_server(request):
    if request.method == 'POST':
        userID = request.session.get('userID')
        if userID == None:
            return HttpResponseRedirect('/')
        username = request.session.get('username')
        project_names = request.session.get('project_names')
        server_num=request.POST.get('server_num')
        if server_num != 'add':     #第一种通过添加项目，添加项目中未存在的服务器（不用判断）。
            server_list=request.POST.get('IP_Total')
            print(server_list)
            if server_num == '1':
                server_user= request.POST.get(server_list+'_user')
                server_pass = request.POST.get(server_list + '_pass')
                server_port = int(request.POST.get(server_list + '_port'))
                sql=''' insert into t_server_info value('%s',%s,'%s','%s') ''' %(server_list,server_port,server_user,server_pass)
                if mysql.mysql_write(sql):
                    return HttpResponse('''<script language="javascript"> 
                                                    alert("保存成功"); 
                                                    window.location.href="/";
                                                    </script>''')
                else:
                    return HttpResponse('''<script language="javascript"> 
                                                    alert("保存失败"); 
                                                    window.location.href="/";
                                                    </script>''')
            else:   #多个服务器
                num=0
                for ip in server_list.split(','):
                    server_user = request.POST.get(ip + '_user')
                    server_pass = request.POST.get(ip + '_pass')
                    server_port = int(request.POST.get(ip + '_port'))
                    sql = ''' insert into t_server_info value('%s',%s,'%s','%s') ''' %(ip,server_port,server_user,server_pass)
                    if mysql.mysql_write(sql):
                        num+=1
                if int(server_num) == num:
                    return HttpResponse('''<script language="javascript"> 
                                            alert("保存成功"); 
                                            window.location.href="/";
                                            </script>''')
                else:
                    false_server_num=int(server_num)-num
                    return HttpResponse('''<script language="javascript"> 
                                            alert("有%s个服务器保存失败"); 
                                            window.location.href="/";
                                            </script>''' %false_server_num)
        else:   #直接添加服务器，需要判断服务器是否存在。 server_num == 'add'
            server_ip=request.POST.get('server_ip')
            server_user=request.POST.get('server_user')
            server_pass=request.POST.get('server_pass')
            server_port=int(request.POST.get('server_port'))
            sql=''' insert into t_server_info value('%s',%s,'%s','%s') ''' %(server_ip,server_port,server_user,server_pass)
            if mysql.mysql_write(sql):
                return HttpResponse('''<script language="javascript"> 
                                        alert("保存成功"); 
                                        window.location.href="/";
                                       </script>''')
            else:
                return HttpResponse('''<script language="javascript"> 
                                        alert("保存失败"); 
                                        window.location.href="/";
                                       </script>''')
    elif request.method == 'GET':
        userID = request.session.get('userID')
        if userID == None:
            return HttpResponseRedirect('/')
        username = request.session.get('username')
        project_names = request.session.get('project_names')
        return_data = {}
        return_data['pagetag'] = 'add_server'
        return_data['userID'] = userID
        return_data['username'] = username
        return_data['server_num'] = 'add'
        return_data['project_names'] = project_names
        return_data['ip']='server'
        return render(request, 'index.html', return_data)

