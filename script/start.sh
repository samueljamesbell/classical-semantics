#! /bin/bash

gcloud compute instances start birch-vm

gcloud compute ssh sam@birch-vm -- -L 8889:localhost:8889

