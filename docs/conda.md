# Conda Environment
Note: These commands were tested on a Mac only. They may need some modifications in order to run on other platforms.


# Setup
For reproducibility, the core packages (and their versions) used for building and running
the scripts can be found in `environment.yaml`. To reproduce this environment, use
Conda with the following command:


## (1) - Create the Conda Environment - (Do This Once)
!!! IMPORTTANT !!! Make sure you are in the project's root prior to running these commands.

~~~
conda env create -n <env_name> -f environment.yaml
~~~
Note that the default environment name in the `environment.yaml` file is `reg-env`.
In the command example above, replace `<env_name>` with your desired Conda environment name.
If no `-n <env_name>` parameter is supplied, the default name of `reg-env` will be used.


## (2) -  Activate the Environment  - (Do this Once)
~~~
conda activate <env_name>
~~~


## (3) - Environment Variables Inside Conda <env_name> Context  - (Do this once)

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
echo export PYTHONPATH=${PYTHONPATH}:${ROOT_DIR}/src/python/packages/fluire >> ./etc/conda/activate.d/env_vars.sh && \

rm -f ./etc/conda/deactivate.d/env_vars.sh && \
touch ./etc/conda/deactivate.d/env_vars.sh && \
echo '#!/bin/bash' >> ./etc/conda/deactivate.d/env_vars.sh && \
echo unset PYTHONPATH >> ./etc/conda/deactivate.d/env_vars.sh && \
cd $ROOT_DIR
~~~

## (4) - Reload Conda Environment  - (Do this Whenever You Use the Package)
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
From the project root :
~~~
cd ./src/bash/unit_testing
sh run_unit_tests.sh
~~~
