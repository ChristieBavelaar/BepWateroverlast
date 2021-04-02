#!/bin/sh
#SBATCH --job-name=ex1-4
#SBATCH --output=/home/s2155435/ex1-4.out
#SBATCH --error=/home/s2155435/ex1-4.err
#SBATCH --mail-user="christie@ziggo.nl"
#SBATCH --mail-type="ALL"
#SBATCH --partition=cpu-medium
#SBATCH -c 2
#SBATCH --time=05:00:00
#SBATCH --mem-per-cpu=30gb

export PYTHONPATH=/home/s2155435/bep1/
module load Miniconda3/4.7.10
conda init bash
source ~/.bashrc
conda activate bepalice
python3 /home/s2155435/bep1/pandafy_data/scriptsSerialized.py n 8 > /home/s2155435/terminaloutput3.txt
