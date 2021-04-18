#!/bin/sh
#SBATCH --job-name=ex3
#SBATCH --output=/home/s2155435/ex3.out
#SBATCH --error=/home/s2155435/ex3.err
#SBATCH --mail-user="christie@ziggo.nl"
#SBATCH --mail-type="ALL"
#SBATCH --partition=cpu-medium
#SBATCH -c 2
#SBATCH --time=08:00:00
#SBATCH --mem-per-cpu=32gb

export PYTHONPATH=/home/s2155435/bep1/
module load Miniconda3/4.7.10
conda init bash
source ~/.bashrc
conda activate bepalice
python3 /home/s2155435/bep1/pandafy_data/scriptsSerialized.py n 11 3 10