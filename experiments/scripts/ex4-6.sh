#!/bin/sh
#SBATCH --job-name=ex4-6
#SBATCH --output=/home/s2155435/ex4-6.out
#SBATCH --error=/home/s2155435/ex4-6.err
#SBATCH --mail-user="christie@ziggo.nl"
#SBATCH --mail-type="ALL"
#SBATCH --partition=cpu-long
#SBATCH -c 1
#SBATCH --time=7-00:00:00
#SBATCH --mem-per-cpu=64gb

export PYTHONPATH=/home/s2155435/bep1/
module load Miniconda3/4.7.10
conda init bash
source ~/.bashrc
conda activate bepalice
python3 /home/s2155435/bep1/analyse112/rfDepSamp3.py n 