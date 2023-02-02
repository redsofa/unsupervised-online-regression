# Conda environment

## 1 - Create the working Conda environment on new machine
~~~
cd ./dev_env
conda env create -n <env_name> -f conda_env.yml
~~~
Note that the default environment name in the conda_env.yml file is ```reg-env```


## 2 -  Activate the environment
~~~
conda activate <env_name>
~~~


## 3 - Environment Variables inside Conda <env_name> context
- Copy/paste the content below run in a terminal

~~~
export REPOSITORY_ROOT="/Users/richardr/dev/git/unsupervised-online-regression"
cd $CONDA_PREFIX && \
mkdir -p ./etc/conda/activate.d && \
mkdir -p ./etc/conda/deactivate.d && \
rm -f ./etc/conda/activate.d/env_vars.sh && \

touch ./etc/conda/activate.d/env_vars.sh && \
echo '#!/bin/bash' >> ./etc/conda/activate.d/env_vars.sh && \
echo 'export PYTHONPATH="$PYTHON_PATH":"${REPOSITORY_ROOOT}"/src/python/modules' >> ./etc/conda/activate.d/env_vars.sh && \

rm -f ./etc/conda/deactivate.d/env_vars.sh && \
touch ./etc/conda/deactivate.d/env_vars.sh && \
echo '#!/bin/bash' >> ./etc/conda/deactivate.d/env_vars.sh && \
echo 'unset PYTHONPATH' >> ./etc/conda/deactivate.d/env_vars.sh
~~~

## 4 - Reload Conda environment
~~~
conda deactivate
conda activate <env_name>
~~~


## 5 - Run code
~~~
python ./src/python/main.py
~~~



# (EXTRA REFERENCE) - To export the working Conda environment
~~~
conda activate <env_name>
conda env export > conda_env.yml
~~~


# (EXTRA REFERENCE ) - Tmux and Vim development environment

## Start Tmux dev environment
~~~
cd ./dev_env
sh tmux_dev_env.sh
~~~

