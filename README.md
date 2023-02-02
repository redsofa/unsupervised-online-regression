# Conda environment

## To export the working Conda environment - (For reference purposes only)
~~~
conda env export > conda_env.yml
~~~

## To create the working Conda environment on new machine
~~~
conda env create -n <env_name> -f conda_env.yml
~~~
Note that the default environment name in the conda_env.yml file is ```my_conda_env```


## Activate the environment
conda activate <env_name>



## Environment Variables inside Conda <env_name> context
Copy/paste the content below run in a terminal

~~~
cd $CONDA_PREFIX && \
mkdir -p ./etc/conda/activate.d && \
mkdir -p ./etc/conda/deactivate.d && \
rm -f ./etc/conda/activate.d/env_vars.sh && \

touch ./etc/conda/activate.d/env_vars.sh && \
echo '#!/bin/bash' >> ./etc/conda/activate.d/env_vars.sh && \
echo 'export SPARK_HOME="${CONDA_PREFIX}"/lib/python3.9/site-packages/pyspark' >> ./etc/conda/activate.d/env_vars.sh && \
echo 'export PYTHONPATH="${SPARK_HOME}"/python:"${HOME}"/dev/git/mcgill_new_dat_trans/src/python/modules' >> ./etc/conda/activate.d/env_vars.sh && \
echo 'export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")' >> ./etc/conda/activate.d/env_vars.sh && \
echo 'export PATH="${PATH}":"${JAVA_HOME}"' >> ./etc/conda/activate.d/env_vars.sh && \

rm -f ./etc/conda/deactivate.d/env_vars.sh && \
touch ./etc/conda/deactivate.d/env_vars.sh && \
echo '#!/bin/bash' >> ./etc/conda/deactivate.d/env_vars.sh && \
echo 'unset PYTHONPATH' >> ./etc/conda/deactivate.d/env_vars.sh
~~~

## Reload Conda environment
~~~
conda deactivate
conda activate <env_name>
~~~



# Tmux and Vim development environment

## Setup environment
- Copy `settings.template.sh` to `settings.sh`
- Edit the `settings.sh` file to suit your context
- Start up the Tmux and Vim development environment by launching the `tmux_dev_env.sh` script


# Running the pipeline
- Make sure that `./src/python/modules/job_utils/settings_py` file is edited to suit your context.
- There is a `job` dictionary that probably needs editing
- The rest of the file is probably OK to leave as is.

