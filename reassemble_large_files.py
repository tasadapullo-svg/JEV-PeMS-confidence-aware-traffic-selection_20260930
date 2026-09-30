from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parent
FILES = [
  {
    "output_relative_path": "01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS.zip",
    "original_sha256": "d9cb5887bcac793478281a368e7d35a0bd14b1ace76ebcd04aa701542fb4d7bd",
    "parts": [
      "01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS.zip.part001",
      "01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS.zip.part002",
      "01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS.zip.part003",
      "01_raw_data/01_caltrans_pems/Caltrans PeMS/00_DATA_AUDIT/13_PERCENT_OBSERVED_SEMANTICS.zip.part004"
    ]
  },
  {
    "output_relative_path": "02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/test__01_H30.parquet",
    "original_sha256": "c278ab9ebccbf6410610cf5bbdfc59f21956febcd7fcf192a8ba49b989b569fd",
    "parts": [
      "02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/test__01_H30.parquet.part001",
      "02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/test__01_H30.parquet.part002",
      "02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/test__01_H30.parquet.part003",
      "02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/test__01_H30.parquet.part004"
    ]
  },
  {
    "output_relative_path": "02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/train__01_H30.parquet",
    "original_sha256": "2e1d326db471bbc6281e6c8e9e174453e60e9941316c7120433555814260a186",
    "parts": [
      "02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/train__01_H30.parquet.part001",
      "02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/train__01_H30.parquet.part002",
      "02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/train__01_H30.parquet.part003",
      "02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/train__01_H30.parquet.part004",
      "02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/train__01_H30.parquet.part005",
      "02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/train__01_H30.parquet.part006",
      "02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/train__01_H30.parquet.part007",
      "02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/train__01_H30.parquet.part008",
      "02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/train__01_H30.parquet.part009"
    ]
  },
  {
    "output_relative_path": "02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/validation__01_H30.parquet",
    "original_sha256": "d35d02c143e1379fbc45505d3a605ea595d779782c9ab08d2ef0fb2e916c9799",
    "parts": [
      "02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/validation__01_H30.parquet.part001",
      "02_training_data/01_H30/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/01_H30/validation__01_H30.parquet.part002"
    ]
  },
  {
    "output_relative_path": "02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/test__02_H60.parquet",
    "original_sha256": "9f4f8e3641bb699c4bb9a6aa37f715153bc0a0173497dc408559d0d1cf497bb7",
    "parts": [
      "02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/test__02_H60.parquet.part001",
      "02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/test__02_H60.parquet.part002",
      "02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/test__02_H60.parquet.part003",
      "02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/test__02_H60.parquet.part004"
    ]
  },
  {
    "output_relative_path": "02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/train__02_H60.parquet",
    "original_sha256": "929c0c79809bcf0907e982e648dc519ecdb794c7a72ea16d62d49bc47fdc97c7",
    "parts": [
      "02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/train__02_H60.parquet.part001",
      "02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/train__02_H60.parquet.part002",
      "02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/train__02_H60.parquet.part003",
      "02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/train__02_H60.parquet.part004",
      "02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/train__02_H60.parquet.part005",
      "02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/train__02_H60.parquet.part006",
      "02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/train__02_H60.parquet.part007",
      "02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/train__02_H60.parquet.part008",
      "02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/train__02_H60.parquet.part009"
    ]
  },
  {
    "output_relative_path": "02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/validation__02_H60.parquet",
    "original_sha256": "5129dec5ee48a96889df401d9fb2c2e22ceb786ba32f4c789cf0d650ddcd345b",
    "parts": [
      "02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/validation__02_H60.parquet.part001",
      "02_training_data/02_H60/Caltrans PeMS/02_FORECASTING_DATASET_FREEZE/02_H60/validation__02_H60.parquet.part002"
    ]
  },
  {
    "output_relative_path": "07_figures/PNG/fig/\u6b63\u5f0f\u56fe/JEV_Fig1-Fig5_FINAL_SCI_Multiformat_16x9_20260927.zip",
    "original_sha256": "d0369f660fa01c68af67020ef2e09062a4b3e3472e43f1d742e182ebcf2d894d",
    "parts": [
      "07_figures/PNG/fig/\u6b63\u5f0f\u56fe/JEV_Fig1-Fig5_FINAL_SCI_Multiformat_16x9_20260927.zip.part001",
      "07_figures/PNG/fig/\u6b63\u5f0f\u56fe/JEV_Fig1-Fig5_FINAL_SCI_Multiformat_16x9_20260927.zip.part002",
      "07_figures/PNG/fig/\u6b63\u5f0f\u56fe/JEV_Fig1-Fig5_FINAL_SCI_Multiformat_16x9_20260927.zip.part003"
    ]
  },
  {
    "output_relative_path": "02_training_data/03_train_split/training_data.zip",
    "original_sha256": "8b1b9a1516049bb6961d65e5009f6069f577fc664b4a280cd6ea2a609017f8a1",
    "parts": [
      "02_training_data/03_train_split/training_data.zip.part001",
      "02_training_data/03_train_split/training_data.zip.part002",
      "02_training_data/03_train_split/training_data.zip.part003",
      "02_training_data/03_train_split/training_data.zip.part004",
      "02_training_data/03_train_split/training_data.zip.part005"
    ]
  },
  {
    "output_relative_path": "09_model_outputs/predictions/training_data/01_STEP1B_FULL_H30/06_PREDICTIONS/test_predictions_H30__06_PREDICTIONS.parquet",
    "original_sha256": "772fcfa1996058cd66e95e31b20cb7e428306441d00b85d0c1e140fd8332e60c",
    "parts": [
      "09_model_outputs/predictions/training_data/01_STEP1B_FULL_H30/06_PREDICTIONS/test_predictions_H30__06_PREDICTIONS.parquet.part001",
      "09_model_outputs/predictions/training_data/01_STEP1B_FULL_H30/06_PREDICTIONS/test_predictions_H30__06_PREDICTIONS.parquet.part002",
      "09_model_outputs/predictions/training_data/01_STEP1B_FULL_H30/06_PREDICTIONS/test_predictions_H30__06_PREDICTIONS.parquet.part003"
    ]
  },
  {
    "output_relative_path": "09_model_outputs/predictions/training_data/01_STEP1B_FULL_H30/06_PREDICTIONS/validation_predictions_H30__06_PREDICTIONS.parquet",
    "original_sha256": "c320b1eb8603d4c10e7a353a57318c5fd6410da084e1c501f6c132996fe46355",
    "parts": [
      "09_model_outputs/predictions/training_data/01_STEP1B_FULL_H30/06_PREDICTIONS/validation_predictions_H30__06_PREDICTIONS.parquet.part001",
      "09_model_outputs/predictions/training_data/01_STEP1B_FULL_H30/06_PREDICTIONS/validation_predictions_H30__06_PREDICTIONS.parquet.part002"
    ]
  }
]

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

for item in FILES:
    out = ROOT / item["output_relative_path"]
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as w:
        for part_rel in item["parts"]:
            with (ROOT / part_rel).open("rb") as r:
                for chunk in iter(lambda: r.read(1024 * 1024), b""):
                    w.write(chunk)
    digest = sha256(out)
    if digest != item["original_sha256"]:
        raise SystemExit(f"SHA256 mismatch for {item['output_relative_path']}: {digest}")
    print(f"Reassembled and verified: {item['output_relative_path']}")
