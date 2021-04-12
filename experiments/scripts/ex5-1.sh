#!/bin/sh
#SBATCH --job-name=ex5
#SBATCH --output=/home/s2155435/ex5.out
#SBATCH --error=/home/s2155435/ex5.err
#SBATCH --mail-user="christie@ziggo.nl"
#SBATCH --mail-type="ALL"
#SBATCH --partition=cpu-short
#SBATCH -c 1
#SBATCH --time=01:00:00
#SBATCH --mem-per-cpu=16gb

export PYTHONPATH=/home/s2155435/bep1/
module load Miniconda3/4.7.10
conda init bash
source ~/.bashrc
conda activate bepalice
python3 /home/s2155435/bep1/analyseData/rfDepSamp.py n 
