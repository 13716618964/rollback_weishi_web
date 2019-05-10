import paramiko

def result_log(files,result):
    f=open(files,'a')
    f.write(result)
    f.close()

def ssh_server(hostIP,Port,Username,Password,cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostIP, port=Port, username=Username, password=Password)
    except:
        result=(hostIP+'无法连接')
        result_log('error.log',result)
        return ''
        #return False
    else:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result_stdout = stdout.read()
        result = result_stdout.decode()
        result_stderr = stderr.read()
        stderr_result = result_stderr.decode()
        if stderr_result != '':
            result_log('error.log',stderr_result)
        ssh.close()
        return result