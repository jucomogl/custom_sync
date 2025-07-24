##Usage Examples##
#Add a server:
python deploy_push.py add --name staging --host 192.168.0.10 --user ubuntu --remote /var/www/html/

#List all servers:
python deploy_push.py list

#Push folder to server (e.g., ID 1):
python deploy_push.py push --id 1 --folder ./dist
