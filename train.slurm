#!/bin/sh
#SBATCH --account=share-ie-idi
#SBATCH --job-name="sport-tracking"
#SBATCH --time=10:00:00
#SBATCH --partition=GPUQ
#SBATCH --mem=80GB
#SBATCH --constraint="(a100|h100|h200)&(gpu40g|gpu80g)"
#SBATCH --output=slurm_outputs/output_sport-tracking.txt
#SBATCH --error=slurm_outputs/output_sport-tracking.err
#SBATCH --mail-user=sverrnys@stud.ntnu.no
#SBATCH --mail-type=ALL


WORKDIR=${SLURM_SUBMIT_DIR}
cd ${WORKDIR}
echo "Running from this directory: $SLURM_SUBMIT_DIR"
echo "Name of job: $SLURM_JOB_NAME"
echo "ID of job: $SLURM_JOB_ID"
echo "The job was run on these nodes: $SLURM_JOB_NODELIST"


module purge
module load Python/3.13.5-GCCcore-14.3.0

pip install uv --user

uv sync

# Enable W&B logging for Ultralytics
uv run yolo settings wandb=True


# Run the Python script
uv run python train-obb.py

echo "Job finished"