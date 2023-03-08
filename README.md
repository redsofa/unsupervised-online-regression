
# Conda environment
Note: These commands were tested on a Mac only. They may need some modifications in order to run on other platforms.


## (1) - Create the working Conda environment on new machine
~~~
cd ./dev_env
conda env create -n <env_name> -f conda_env.yml
~~~
Note that the default environment name in the conda_env.yml file is ```reg-env```


## (2) -  Activate the environment
~~~
cd ../
conda activate <env_name>
~~~


## (3) - Environment Variables inside Conda <env_name> context

- IMPORTTANT !! Make sure you are in the project's root
- Copy/paste the content below in a terminal and hit enter to run them
- This command only needs to be run once


~~~
ROOT_DIR="$(pwd)" && \
cd $CONDA_PREFIX && \
mkdir -p ./etc/conda/activate.d && \
mkdir -p ./etc/conda/deactivate.d && \
rm -f ./etc/conda/activate.d/env_vars.sh && \

touch ./etc/conda/activate.d/env_vars.sh && \
echo '#!/bin/bash' >> ./etc/conda/activate.d/env_vars.sh && \
echo export PYTHONPATH=${PYTHONPATH}:${ROOT_DIR}/src/python/modules >> ./etc/conda/activate.d/env_vars.sh && \

rm -f ./etc/conda/deactivate.d/env_vars.sh && \
touch ./etc/conda/deactivate.d/env_vars.sh && \
echo '#!/bin/bash' >> ./etc/conda/deactivate.d/env_vars.sh && \
echo unset PYTHONPATH >> ./etc/conda/deactivate.d/env_vars.sh && \
cd $ROOT_DIR
~~~

## (4) - Reload Conda environment
~~~
conda deactivate
conda activate <env_name>
~~~


## (5) - Run code
~~~
cd ./src/python
python main.py
~~~

OR

~~~
cd ./src/bash/experiments
sh example.sh
~~~


## (6) - Run Unit Tests
~~~
From the project root :

cd ./src/bash/unit_testing
sh run_unit_tests.sh
~~~

## (7) - Citation
If you use or reference this work in a scientific publication,
we would appreciate that you use the following citations:

```
@INPROCEEDINGS{
... TODO
}
```

<hr>
<br>
<br>
<br>

# (EXTRA REFERENCE) - To export the working Conda environment
~~~
conda activate <env_name>
conda env export > conda_env.yml
~~~


# (EXTRA REFERENCE) - Tmux and Vim development environment

## Start Tmux dev environment
~~~
cd ./dev_env
sh tmux_dev_env.sh
~~~



