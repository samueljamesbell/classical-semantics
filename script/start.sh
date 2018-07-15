#! /bin/bash

gcloud compute instances start birch-vm

gcloud compute ssh sam@birch-vm \
    --command "cd ~/projects/classical-semantics ; ./script/start-jupyter.sh" \
    -- -t -L 8889:localhost:8889

