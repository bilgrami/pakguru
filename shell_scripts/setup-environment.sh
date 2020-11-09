mkdir -p ./.virtualenvs/myproject_env 
python -m virtualenv ./.virtualenvs/myproject_env

if [ "$(uname)" == "Darwin" ]; then
    echo "You are under Mac OS X platform"        
    source ./.virtualenvs/myproject_env/bin/activate
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    echo "You are under GNU/Linux platform"
    source ./.virtualenvs/myproject_env/bin/activate
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    echo "You are under 32 bits Windows NT platform" && \
    ./.virtualenvs/myproject_env/Scripts/activate.bat
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    echo "You are under 64 bits Windows NT platform" && \
    ./.virtualenvs/myproject_env/Scripts/activate.bat
fi
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo 'Bringing web container up in detached mode (pointing to dev db)';
docker-compose up -d;
echo 'Running any pending migrations';
docker-compose exec web bash -c 'cd /usr/local/project/pakguru_project && python manage.py migrate';
echo 'Flushing local db';
docker-compose exec web bash -c 'cd /usr/local/project/pakguru_project && python manage.py flush --no-input';
echo 'Running init script';
docker-compose exec web bash -c 'cd /usr/local/project/pakguru_project && chmod +x ./shell_scripts/init_script.sh && ./shell_scripts//init_script.sh';
echo 'Running load script on local container';
docker-compose exec web bash -c 'cd /usr/local/project/pakguru_project && ./shell_scripts/load_data.sh';
echo 'Bringing local container down';
docker-compose down;
echo done;
