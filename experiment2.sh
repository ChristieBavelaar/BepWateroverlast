#!/bin/sh
#SBATCH --job-name=ex2
#SBATCH --output=/home/s2155435/ex2.out
#SBATCH --error=/home/s2155435/ex2.err
#SBATCH --mail-user="christie@ziggo.nl"
#SBATCH --mail-type="ALL"
#SBATCH --partition=cpu-medium
#SBATCH -c 1
#SBATCH --time=01:00:00
#SBATCH --mem-per-cpu=16gb

export PYTHONPATH=/home/s2155435/bep1/
module load Miniconda3/4.7.10
conda init bash
source ~/.bashrc
conda activate bepalice
python3 /home/s2155435/bep1/analyseData/randomForest.py n > /home/s2155435/terminaloutput4.txt
