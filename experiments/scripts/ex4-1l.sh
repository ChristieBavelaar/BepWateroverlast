#!/bin/sh
#SBATCH --job-name=ex4-1l
#SBATCH --output=/home/s2155435/ex4-1l.out
#SBATCH --error=/home/s2155435/ex4-1l.err
#SBATCH --mail-user="christie@ziggo.nl"
#SBATCH --mail-type="ALL"
#SBATCH --partition=cpu-long
#SBATCH -c 1
#SBATCH --time=1-00:00:00
#SBATCH --mem-per-cpu=16gb

export PYTHONPATH=/home/s2155435/bep1/
module load Miniconda3/4.7.10
conda init bash
source ~/.bashrc
conda activate bepalice
python3 /home/s2155435/bep1/analyse112/randomForest.py n 