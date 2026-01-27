import sys
import yfinance as yf
from datetime import date
from sqlalchemy import create_engine
from dotenv import load_dotenv
from loguru import logger

from app.config import DB_URL


load_dotenv()


if DB_URL:
    try:
        engine = create_engine(DB_URL)
    except Exception:
        logger.error("Failed to initialize DB engine. Check credentials and connectivity.")
        sys.exit(1)
else:
    logger.error("Environment variable DB_URL is missing.")
    sys.exit(1)



def get_realized_volatility():
    real_data = yfinance.download(..., date="2026-01-27")
    pass


def run_evaluation():
    today = date.today()

    # 1. Extract
    preds = db.fetch("SELECT * FROM garch_preds WHERE target_date = '2026-01-27'")
    preds = 

    # 2. Transform
    # Výpočet chyb
    # mape
    # rmse = np.sqrt(mean_squared_error(results['Actual_Abs_Return'], results['Predicted_Volatility']))
    # mae = mean_absolute_error(results['Actual_Abs_Return'], results['Predicted_Volatility'])
    results = []
    for p in preds:
        real_vol = calculate_real_vol(
            real_data, p.ticker
        )  # Např. z High-Low nebo Close-Close
        error = abs(p.prediction - real_vol)
        results.append((p.ticker, p.prediction, real_vol, error))

    # 3. Load
    db.insert_many("model_performance", results)



if __name__ == "__main__":
    run_evaluation()
