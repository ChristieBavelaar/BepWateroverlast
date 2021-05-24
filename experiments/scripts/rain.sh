#!/bin/sh
#SBATCH --job-name=rain
#SBATCH --output=/home/s2155435/rain.out
#SBATCH --error=/home/s2155435/rain.err
#SBATCH --mail-user="christie@ziggo.nl"
#SBATCH --mail-type="ALL"
#SBATCH --partition=cpu-long
#SBATCH -c 2
#SBATCH --time=2-00:00:00
#SBATCH --mem-per-cpu=64gb

export PYTHONPATH=/home/s2155435/bep1/
module load Miniconda3/4.7.10
conda init bash
source ~/.bashrc
conda activate bepalice
python3 /home/s2155435/bep1/preprocess112/KNMIRainFull.py