#!/bin/sh
#SBATCH --job-name=ex4
#SBATCH --output=/home/s2155435/ex4.out
#SBATCH --error=/home/s2155435/ex4.err
#SBATCH --mail-user="christie@ziggo.nl"
#SBATCH --mail-type="ALL"
#SBATCH --partition=cpu-short
#SBATCH -c 2
#SBATCH --time=01:00:00
#SBATCH --mem-per-cpu=32gb

export PYTHONPATH=/home/s2155435/bep1/
module load Miniconda3/4.7.10
conda init bash
source ~/.bashrc
conda activate bepalice
python3 /home/s2155435/bep1/pandafy_data/scriptsSerialized.py n 11 2 10
#python3 /home/s2155435/bep1/analyseData/randomForest.py n 
