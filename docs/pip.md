# Python Virtual Environment
Note: These commands were tested on a Mac only. They may need some modifications in order to run on other platforms.

# Commands
Make sure you are in the project's root directory
~~~
python -m venv my_env
source ./my_env/bin/activate
ROOT_DIR="$(pwd)"
export PYTHONPATH=$PYTHONPATH:${ROOT_DIR}/src/python/packages/fluire
pip install -r requirements.txt
cd ./src/bash
sh example.sh
~~~
