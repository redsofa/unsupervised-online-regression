#!/bin/bash

source ./settings.sh

tmux -2 new-session -d -s ${TMUX_SESSION}

# First window (DEV))
tmux rename-window "(DEV)"
tmux send-keys "cd ${REPOSITORY_ROOT}/src; vim" C-m

# Split panes
tmux split-window -v
tmux resize-pane -D 10
tmux select-pane -t 1
tmux send-keys "cd ${REPOSITORY_ROOT}/src; clear " C-m
#tmux split-window -h
#tmux send-keys "cd $REPOSITORY_ROOT; clear" C-m

# Second window (UTIL)
tmux new-window -n "(UTIL)"
tmux send-keys "cd ${REPOSITORY_ROOT}/src; clear " C-m

# Split UTIL window
#tmux split-window -h
#tmux send-keys "cd $REPOSITORY_ROOT; clear " C-m
#tmux select-pane -t 0

# Select the control window and first pane
tmux select-window -t "(DEV)"
tmux select-pane -t 0

# Reattach
tmux -2 attach-session -t $TMUX_SESSION
