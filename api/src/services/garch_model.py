import numpy as np
from arch import arch_model
from loguru import logger

from src.config import GarchParams


def get_garch_pred(log_return, params: GarchParams) -> float | None:
    try:
        model = arch_model(
            log_return,
            vol="GARCH",
            p=params.p,
            q=params.q,
            dist=params.dist,
            mean="Constant",
        )

        res = model.fit(disp="off", show_warning=False)
        logger.debug(res.summary())

        if res.convergence_flag != 0:
            logger.error(f"Optimization failed with flag: {res.convergence_flag}")
            return None

        forecast = res.forecast(horizon=1)
        var = forecast.variance.iloc[-1]["h.1"]
        pred = np.sqrt(var)

        if np.isnan(pred) or np.isinf(pred):
            logger.error(f"Error in predicted sigma: {pred}")
            return None

        if pred > 500.0:
            logger.warning(
                f"Predicted sigma value exploded (failed estimation): {pred}"
            )
            return None

        if pred < 0.001:
            logger.warning(f"Model degenerated to zero variance: {pred}")
            return None

        logger.info(f"GARCH prediction calculated: {pred:.4f}")
        return pred

    except Exception:
        logger.exception("Error during GARCH training and prediction")
        return None
