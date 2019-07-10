#!/bin/bash

# Get environment variables to show up in SSH session
eval $(printenv | sed -n "s/^\([^=]\+\)=\(.*\)$/export \1=\2/p" | sed 's/"/\\\"/g' | sed '/=/s//="/' | sed 's/$/"/' >> /etc/profile)

echo starting sshd process
sed -i "s/SSH_PORT/$SSH_PORT/g" /etc/ssh/sshd_config;
/usr/sbin/sshd

# cron_cmd=$PROJECT_ROOT'/'$PROJECT_NAME'/pakguru_app/shell_scripts/process_show_feeds.sh'
# grep -qxF '0 */4 * * * '$cron_cmd /etc/crontab || echo '0 */4 * * * '$cron_cmd >> /etc/crontab
echo 'running cron '
cron

echo 'setting permissions for sh scripts'
find . -name *.sh | xargs chmod +x

cd $PROJECT_ROOT/$PROJECT_NAME/
echo "Python location: '$(which python)', Python version: '$(python -V)'"
echo "Current directory '$(pwd)' contains $(ls -1q * | wc -l) files"
echo "starting django server on port $SERVER_PORT"

python manage.py runserver 0.0.0.0:$SERVER_PORT
