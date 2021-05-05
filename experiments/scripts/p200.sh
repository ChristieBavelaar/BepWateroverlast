#!/bin/sh
#SBATCH --job-name=hourlyRain
#SBATCH --output=/home/s2155435/hourlyRain.out
#SBATCH --error=/home/s2155435/hourlyRain.err
#SBATCH --mail-user="christie@ziggo.nl"
#SBATCH --mail-type="ALL"
#SBATCH --partition=cpu-short
#SBATCH -c 1
#SBATCH --time=03:00:00
#SBATCH --mem-per-cpu=32gb

export PYTHONPATH=/home/s2155435/bep1/
module load Miniconda3/4.7.10
conda init bash
source ~/.bashrc
conda activate bepalice
python3 /home/s2155435/bep1/preprocess112/pandafy112.py
