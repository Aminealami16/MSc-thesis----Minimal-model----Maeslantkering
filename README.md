# MSc-thesis----Minimal-model----Maeslantkering
This repository contains the Python code used to develop a minimal model of the Maeslantkering. It contains the model in three operational phases, a set of sensitivity analyses and a finite element model updating optimisation. 

To understand this code, it is of importance to read the thesis report, which contains the underlying assumptions.

Click [here](https://repository.tudelft.nl/record/uuid:e09ade5d-a41f-44e6-b1ab-7c02f42c766b) to find my MSc thesis report, which is publicly available at the TU Delft repository!

# **Structure of the repository**

The repository consists of the following 7 folders:

1. `00models_OP1` $\rightarrow$ Consists of the minimal model in operational phase 1 and a corresponding set of sensitivity analyses.
2. `01models_OP2` $\rightarrow$ Consists of the minimal model in operational phase 2 and a corresponding set of sensitivity analyses.
3. `02models_OP3` $\rightarrow$ Consists of the minimal model in operational phase 3 and a corresponding set of sensitivity analyses.
4. `03model_comparisons` $\rightarrow$ Consists of a comparisons of the baseline models in the three operational phases.
5. `04sensor_layouts` $\rightarrow$ Contains three possible sensor layouts. 
6. `05model_updating` $\rightarrow$ Contains the model updating optimisations.
7. `scripts` $\rightarrow$ Consists of a set of Python files, used for a variety of function in the different notebooks.
8. `text_files` $\rightarrow$ Contains `.txt` files of the geometry of the model and some `.npy` files containing mode shapes. 


# **1. The minimal models and the sensitivity analyses**

`00models_OP1`, `00models_OP2` and `00models_OP3` are structured similarly. Therefore, only `00models_OP1` is elaborated on further. Its file tree is as follows:

```text
00models_OP1/
├── 00minimal_model_baseline.ipynb 
├── 01minimal_model_sensitivity_kr.ipynb
├── 02minimal_model_sensitivity_kf.ipynb
├── 03minimal_model_sensitivity_Iywall.ipynb
├── 04minimal_sensitivity_Iytruss.ipynb
├── 05minimal_model_sensitivity_locomobile.ipynb
```
The first file contains one instance of the model, for which its developement was based on a set of assumptions. The rest of the files are 1D sensitivity analyses in which the influence of the change of one of the model parameters is visualised. 

# **2. The model comparisons**

The file tree of `03model_comparisons` is relatively simple:

```text
03model_comparisons/
├── 00comparisons_modes.ipynb
```

It contains a `.ipynb` file in which both the natural frequencies and the mode shapes of the model in the three operational phases are compared.

# **3. Sensor layout advice (Only OP1)**

In the thesis, I propose three different sensor layouts. In this part of the repository, I test these three layouts on their ability to capture the natural frequencies and mode shapes. The file tree is as follows:

```text
04sensor_layouts/
├── experimental_eigvectors/
│   ├── phi_experiment_2_sensors.npy
│   ├── phi_experiment_12_sensors.npy
│   └── phi_experiment_22_sensors.npy
├── 00sensor_placement.ipynb
└── 01experimental_mode_shapes.ipynb
```

`experimental_eigvectors` contains the mode shapes retrieved in `00sensor_placement.ipynb`. They are visualised in `01experimental_mode_shapes.ipynb`.


# **4. Model updating optimisations (Only OP1)**

TBD.
