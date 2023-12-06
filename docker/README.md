Building Image
--------------
- Make sure you are in the `./docker` directory of the cloned source tree. 
- Run this command : `docker-compose build`


Running Experiments
-------------------
- Run this command : `docker-compose run --rm fluire_experiments`
- At this point you should be inside the running container
- Run this command :  `cd ./src/bash/expeirments`
- Run the experiments on the Air Quality dataset with this command : `sh run_air_quality.sh`
- Run the experiments on the Concrete dataset with this command : `sh run_concrete.sh`
- Run the experiments on the Protein dataset with this command : `sh run_protein.sh`
- Run the experiments on the Turbine dataset with this command  : `sh run_turbine.sh`
- The results of the experiments will be in the `~/data/usup_reg/work` directory.
