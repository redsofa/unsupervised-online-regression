Building Image
--------------
- Open a terminal window
- Make sure you are in the `./docker` directory of the cloned source tree. 
- Run this command : `docker-compose build`


Running Experiments
-------------------
- Run this command : `docker-compose run --name fluire --rm fluire_experiments`
- At this point you should be inside the running container
- Run this command :  `cd ./src/bash/expeirments`
- Run the experiments on the Air Quality dataset with this command : `sh run_air_quality.sh`
- Run the experiments on the Concrete dataset with this command : `sh run_concrete.sh`
- Run the experiments on the Protein dataset with this command : `sh run_protein.sh`
- Run the experiments on the Turbine dataset with this command  : `sh run_turbine.sh`
- The results of the experiments will be in the `~/data/usup_reg/work` directory.


Copying Results to Host System
------------------------------
- In another terminal, on the host system, type :  `docker cp fluire:/home/exp_user/data <destination directory>`
- Replace the `<destination directory>` above with a directory of your choosing.
- Once the copy is done, you should have a directory named `usup_reg` in the `<destination directory>`
- There will be two sub-directories, `work` contains all experiment results and `raw` contains the raw data.


Note
----
- These instructions were run and tested successfully on OSX and Ubuntu Linux systems.
