#!/bin/sh
#SBATCH --job-name=experiment1_full
#SBATCH --partition=cpu-medium
#SBATCH -c 1
#SBATCH --time=8:00:00
#SBATCH --mem-per-cpu=16gb

export PYTHONPATH=/home/s2155435/bep1/
module load Miniconda3/4.7.10
conda init bash
source ~/.bashrc
conda activate bepalice
python3 /home/s2155435/bep1/pandafy_data/scriptsSerialized.py n 1 &>> /home/s2155435/terminaloutput2.txt
