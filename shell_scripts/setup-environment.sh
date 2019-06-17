cd ../
mkdir -p ./.virtualenvs/myproject_env 
python -m venv ./.virtualenvs/myproject_env 
./.virtualenvs/myproject_env/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
