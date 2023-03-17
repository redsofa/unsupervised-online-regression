# Building the Package(s)
## Fluire
* Building the fluire package :

### Conda Build
~~~
cd ./src/python/packages/fluire
conda build ./conda.recipe
~~~
** This will create a file in your conda environment under the conda-bld directory



### PIP - (Here for reference.. Use Conda build)
~~~
cd ./src/python/packages/fluire
pip wheel .
~~~
* This will create a file called : `fluire-<version_information>-none-any.whl`
* It can be installed (IN ANOTHER PIP or CONDA ENVIRONMENT!) with this command :
~~~
pip install fluire-<version_information>-none-any.whl
~~~
