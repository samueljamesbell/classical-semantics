#! /bin/bash

tmux new-session -s "classical-semantics" -d
tmux send-keys -t "classical-semantics" "jupyter lab --no-browser --port=8889" C-m
tmux split-window -v -t "classical-semantics" 
tmux send-keys -t "classical-semantics" "htop" C-m
tmux split-window -h -t "classical-semantics" 
tmux send-keys -t "classical-semantics" "watch nvidia-smi" C-m
tmux attach -t "classical-semantics"
