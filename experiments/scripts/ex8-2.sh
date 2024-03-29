#!/bin/sh
#SBATCH --job-name=ex8-2
#SBATCH --output=/home/s2155435/ex8-2.out
#SBATCH --error=/home/s2155435/ex8-2.err
#SBATCH --mail-user="christie@ziggo.nl"
#SBATCH --mail-type="ALL"
#SBATCH --partition=cpu-long
#SBATCH -c 2
#SBATCH --time=3-00:00:00
#SBATCH --mem-per-cpu=64gb

export PYTHONPATH=/home/s2155435/bep1/
module load Miniconda3/4.7.10
conda init bash
source ~/.bashrc
conda activate bepalice
python3 /home/s2155435/bep1/preprocess112/serialized2.py n 10 8
