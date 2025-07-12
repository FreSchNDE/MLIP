# MACE-Based MLIP for Solvent Molecules

This repository contains code, data, models, and results from an Advanced Research Laboratory course. The goal was to develop and evaluate machine learning interatomic potentials (MLIPs) based on the [MACE](https://arxiv.org/abs/2206.07697) framework for simulating small organic solvent molecules and liquids.

## Project Summary

Machine learning potentials offer quantum-level accuracy at a fraction of the computational cost. We trained a MACE model on xTB-labeled solvent clusters and evaluated:

- Accuracy on test data (energies and forces)
- Transferability to molecular dynamics (MD)
- Structural and dynamical analysis of a liquid system
- Fine-tuning of a foundation model for rapid deployment

Both full-scale training and low-cost fine-tuning were tested. The fine-tuned model (trained in ~3.2 minutes) showed reasonable MD performance compared to the larger model trained on 4000 structures (~87 minutes).

## Repository Structure

```
.
├── data/                        						# xTB-labeled training and test structures
├── MACE_models/                 						# Trained MACE models (compiled and raw)
├── benchmark_results/           						# Hyperparameter scan and learning curves
├── moldyn/                      						# MD results, RDFs, MSDs, XYZ trajectories
├── figures/                                            # Tutorial illustrations
├── MSD.py                                              # Script for MSD computation
├── T01-MACE-Practice-I.ipynb							# Tutorial file
├── T02-MACE-Practice-II.ipynb							# Tutorial file
├── Tutorial_Descriptors_MLIP_ResearchLab_2025.ipynb	# Tutorial file
├── 1-MACE-parameters.ipynb								# Report: Hyperparameter sweep
├── 2-MACE-learning-curve.ipynb							# Report: Learning curve creation
├── 3-MACE-evaluation.ipynb								# Report: Static model evaluation
├── 4-MACE-fineTune.ipynb								# Report: Fine-tuned alternative model
├── 5-MACE-MD.ipynb										# Report: Molecular dynamics (isolated molecule and liquid)
├── Advanced Research Laboratory MLIP.pdf               # Final report
```

## Key Results

- Final MACE model (trained on 4000 structures):
  - RMSE Energy: < 3 meV/atom
  - RMSE Force: < 50 meV/Å
  - Stable MD for isolated molecules and periodic liquids

- Fine-tuned model (trained on 400 structures):
  - Training time: ~3.2 minutes
  - Stable liquid MD with reasonable RDFs and MSDs

## Videos

The following molecular dynamics videos are included:

- `xtb_md_molecule.mp4`
- `mace_md_molecule.mp4`
- `mace_md_input2.mp4`
- `mace_finetuned_md.mp4`

## Report

The full report is available as `Advanced Research Laboratory MLIP.pdf` in this repository.
