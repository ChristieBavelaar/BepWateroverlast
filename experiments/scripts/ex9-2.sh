#!/bin/sh
#SBATCH --job-name=ex9-2
#SBATCH --output=/home/s2155435/ex9-2.out
#SBATCH --error=/home/s2155435/ex9-2.err
#SBATCH --mail-user="christie@ziggo.nl"
#SBATCH --mail-type="ALL"
#SBATCH --partition=cpu-long
#SBATCH -c 1
#SBATCH --time=1-00:00:00
#SBATCH --mem-per-cpu=32gb

export PYTHONPATH=/home/s2155435/bep1/
module load Miniconda3/4.7.10
conda init bash
source ~/.bashrc
conda activate bepalice
python3 /home/s2155435/bep1/pandafy_data/unfilteredRain.py
