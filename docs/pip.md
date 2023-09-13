# Python Virtual Environment
Note: Python version 3.9.16. These commands were tested on a Mac only. They may need some modifications in order to run on other platforms.


# Commands

* Make sure you are in the project's root directory.

* Find out where Python 3 is located. This is the version of Python the virtual environment will be using.
~~~
whereis python3

As an example : The location of Python 3 is /usr/bin/python3. This is what we are using in these instructions.
The full version number of the Python installation on the system these instructions were authored with is 3.9.6.
~~~

* Create virtual enviroment (in this case the environment name is `my_venv`).
~~~
python3 -m venv my_venv
source ./my_env/bin/activate
~~~

* Create a file with a `.pth` extension in the `venv/lib/python3.9/site-packages` directory that will modify the Python search path to include the fluire package.
* As an example, a file `fluire.pth` was created (you can choose the name you want to use) with the following contents :
~~~
/Users/richardr/dev/git/unsupervised-online-regression/src/python/packages/fluire
~~~

* To check the search path has the new entry, you can type this command :
~~~
python -c 'import sys; print(sys.path)'
~~~

* As an example, the command's output on the system where these instructions are authored is (Note the last entry in the collection is the line we added in the `fluire.pth` file above) :
~~~
['', '/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python39.zip', '/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9', '/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/lib-dynload', '/Users/richardr/dev/git/unsupervised-online-regression/my_venv/lib/python3.9/site-packages', '/Users/richardr/dev/git/unsupervised-online-regression/src/python/packages/fluire']
~~~

* Install the project's Python dependencies
~~~
pip install -r requirements.txt
~~~

* The virtual environment for the project is now setup properly.

* In order to test the configuration via the command line, run the project's unit tests.
~~~
python -m unittest discover -s ./src/python/packages/fluire/tests  -p 'test_*.py'
~~~
