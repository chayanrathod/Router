# router_project/router_app/views.py
from django.shortcuts import render
import paramiko
from paramiko.ssh_exception import SSHException, AuthenticationException

def index(request):
    return render(request, 'router_app/index.html')

def router_info(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        ip_address = request.POST.get('ip_address')
        command = 'show version'

        try:
            # SSH Connection
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip_address, username=username, password=password, timeout=10)

            # Run the selected command
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode('utf-8')

            # Close the SSH connection
            ssh.close()

            return render(request, 'router_app/result.html', {'output': output})
        except AuthenticationException as e:
            error_message = "Authentication failed. Please check your username and password."
            return render(request, 'router_app/error.html', {'error_message': error_message})
        except SSHException as e:
            error_message = f"SSH connection failed: {str(e)}"
            return render(request, 'router_app/error.html', {'error_message': error_message})
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render(request, 'router_app/error.html', {'error_message': error_message})
    return render(request, 'router_app/index.html')
