#! /bin/bash

gcloud compute ssh sam@birch-vm \
    --command "tmux attach -t classical-semantics" \
    -- -t -L 8889:localhost:8889
