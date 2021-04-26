#!/bin/sh
#SBATCH --job-name=ds
#SBATCH --output=/home/s2155435/ds1.out
#SBATCH --error=/home/s2155435/ds1.err
#SBATCH --mail-user="christie@ziggo.nl"
#SBATCH --mail-type="ALL"
#SBATCH --partition=cpu-short
#SBATCH -c 4
#SBATCH --time=02:00:00
#SBATCH --mem-per-cpu=64gb

export PYTHONPATH=/home/s2155435/bep1/
module load Miniconda3/4.7.10
conda init bash
source ~/.bashrc
conda activate bepalice
python3 /home/s2155435/bep1/advancedRF.py