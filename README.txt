conda env create -f conda_env.yml

conda activate reg-env

pip install --upgrade numpy

python ./source/main.py ./datasets/UCI.csv -1


