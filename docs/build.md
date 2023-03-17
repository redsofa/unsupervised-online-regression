# Building the Package(s)
## Fluire
* Building the fluire package :
~~~
cd ./src/python/packages/fluire
pip wheel .
~~~
* This will create a file called : `fluire-<version_information>-none-any.whl`
* It can be installed (IN ANOTHER PIP or CONDA ENVIRONMENT!) with this command :
~~~
pip install fluire-<version_information>-none-any.whl
~~~
