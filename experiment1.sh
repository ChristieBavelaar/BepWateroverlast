#!/bin/sh
#SBATCH --job-name=experiment1_sample
#SBATCH --partition=cpu-short
#SBATCH -c 1
#SBATCH --time=0:30:00
#SBATCH --mem-per-cpu=16gb

export PYTHONPATH=/home/s2155435/bep1/
module load Miniconda3/4.7.10
conda init bash
source ~/.bashrc
conda activate bepalice
python3 /home/s2155435/bep1/pandafy_data/scriptsSerialized.py y 0 >> /home/s2155435/terminaloutput1.txt
