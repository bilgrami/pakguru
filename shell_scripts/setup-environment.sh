mkdir -p ./.virtualenvs/myproject_env 
python -m venv ./.virtualenvs/myproject_env 

if [ "$(uname)" == "Darwin" ]; then
    echo "You are under Mac OS X platform"        
    ./.virtualenvs/myproject_env/bin/activate
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    echo "You are under GNU/Linux platform"
    ./.virtualenvs/myproject_env/bin/activate
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    echo "You are under 32 bits Windows NT platform" && \
    ./.virtualenvs/myproject_env/Scripts/activate.bat
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    echo "You are under 64 bits Windows NT platform" && \
    ./.virtualenvs/myproject_env/Scripts/activate.bat
fi
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
