from typing import NoReturn

from pydantic import BaseSettings
from staker.configs.main import numeraiconfig
from staker.data.dataset import NumerAIDataset
from staker.evaluation.metrics import coeff_determination
from staker.models.loss import rmse
from tensorflow.keras.models import load_model


def main(config: BaseSettings) -> NoReturn:
    """Main function for model training

    :param config: Configuration
    :type config: BaseSettings
    """
    # 1. Load model
    model = load_model(
        "./models/",
        custom_objects={"coeff_determination": coeff_determination, "rmse": rmse},
    )
    # 2. Load tournament dataset
    dataset_getter = NumerAIDataset(config)
    dataset, df = dataset_getter(training=False)
    # 3. Predict
    df["prediction"] = model.predict(dataset)
    # 4. Save predictions
    df[["id", "prediction"]].to_csv("./predictions.csv", index=False)


if __name__ == "__main__":
    main(config=numeraiconfig)
