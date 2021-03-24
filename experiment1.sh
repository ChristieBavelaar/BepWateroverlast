#!/bin/sh
#SBATCH --job-name=experiment1_sample
#SBATCH --partition=cpu-short
#SBATCH -c 1
#SBATCH --time=1:00:00
#SBATCH --mem-per-cpu=16gb

export PYTHONPATH=/home/vanrijn/projects/openml-defaults
source activate openml-defaults
python ~/projects/openml-defaults/examples/vanilla/multiple_defaults_continuous_on_surrogate.py --run_on_surrogates --metadata_files '/home/vanrijn/projects/hypeCNN/data/12param/resnet.arff' --search_space_identifier 'renamed' --override_parameters '{"resnet:epochs": 200}'  --task_id_column 'dataset'
