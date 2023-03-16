# File Descriptions

- <b>settings.sh</b> - Bash script that defines environment variables that are used in the `tmux_dev_env.sh`. Entries in the setting.sh
  script must be modified to suit individual context.

- <b>tmux_dev_env.sh</b> - Script that launches Tmux and Vim for development purposes. Use only if these tools are your development
  envionment tools of choice.



# (REFERENCE INFO) - To export the working Conda environment
~~~
conda activate <env_name>
conda env export > environment.yaml
~~~


# (REFERENCE INFO) - Tmux and Vim development environment

## Start Tmux dev environment
~~~
cd .vim
sh tmux_dev_env.sh
~~~
