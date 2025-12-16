# UCOPhyRehab++
---

This repository contains the code used to train and evaluate models for **3D angle prediction** on the **UCOPhyRehab++** dataset.  
The goal is to allow other researchers to **reproduce the experiments** reported in the paper, including:

- Training on **individual camera viewpoints** vs. **all viewpoints jointly**.
- Comparing different **visual modalities**:
  - Silhouettes  
  - Optical Flow (GMFlow, TV-L1)  
  - Semantic Segmentation  
  - (Optionally) RGB / other modalities
- Evaluating performance using **Mean Absolute Error (MAE)** in degrees with a **4-fold cross-validation** scheme.

This project uses [Hydra](https://hydra.cc/) as a baseline. The configuration files used in the paper are provided as an example. You can override every label from the default files in your `exoeriment` folder.

---

## 1. Repository structure


```
.
├── conf/                   # Configuration files
│   ├── data                
│   ├── experiment              # All the experiments are here
│   ├── loss
│   ├── model
|   ├── training
|   └── default.yaml            # Default config file
|
├── data/                    # Configuration files
│   ├── manifests               # Sets of data for train/val/test
|   └── splits                  # Split files
|
├── scripts
│   ├── build_manifest.sh
│   ├── train.sh
│   └── test.sh
|
├── src/
│   ├── cli/
│   ├── data/
│   ├── logging/
│   ├── loss/
│   ├── metric/
│   ├── model/
│   ├── normalization/
│   └── utils/
|
├── requirements.txt        # pip dependencies
└── README.md
```

## 2. Instalation
### 2.1. Clone the repository
```
git clone https://github.com/i62agorr/uncophyrehab_validation_models.git
cd ucophyrehab_validation_models
```
### 2.2. Create the environment
**OPTION A - Conda (recommended)**
```
conda env create -f requirements.yaml
conda activate ucophyrehab2
```
**OPTION B - pip**
```
python -m venv .ucophyrehab2
source .ucophyrehab2/bin/activate
pip install -r requirements.txt
```
## Dataset preparation
### Separate frames
First of all, you need to launch the `prepare_dataset` script to separate the frames from the distributed `.mp4` videos. You just need to launch the provided script specifying the downloaded and uncompressed dataset root, the modality that you want to separate and the output path.

```
bash scripts/prepare_dataset.sh /path_to_your_mp4_dataset_root <modality> /output_path
```

### Build Manifests
Once that you have the frames separated for the desired modality, you will need to build a manifest for the data set of your experiment. Create a new configuration file or use one of the provided ones.

You must specify the path to the UCOPhyRehab++ dataset root, the modality you want to use and the extension of the target files. Also, if you want to change the splits of the data, you must specify the new files in `conf/data/ucophyrehab_base.yaml` or in your `experiment` file.

For example, we're going to prepare the data manifest for `Silhouettes`, exercise `01_05`, `cam0` and `split_1`. Then, we have to modify the file `conf/sils/split_1/ex_01_05_cam0.yaml` modifying the following fields:

```
data:
  modality: "sils"
  channels: "1"
  dataset_loader: "SilsFolderDataset"
  split_path: "data/splits/split_1_80_10_10.json"
  split_name: "split_1"
  include_exercises: ['01', '05']
  include_cameras: ['cam0']
```

This configuration will inherit the rest of the fields from the other files but will override the specified in the `data` section.

Once the configuration is finished, you must run the following script:
```
python -m src.cli.build_manifest experiment=sils/split_1/ex_01_05_cam0
```

You can automatize this process by writing all your configuration files and calling to the `build_manifest` function from a single script, like the examples in the `scripts` folder.

## 4. Running the experiments
### 4.1. Training
To train our example file:
```
python -m src.cli.train experiment=sils/split_1/ex_01_05_cam0
```
### 4.2. Test
Once it finishes, you can launch the test using the same configuration file:
```
python -m src.cli.test experiment=sils/split_1/ex_01_05_cam0
```

## 5. Logs and output
You can find the logs of your experiments in the `output` folder.
