import sys
import yfinance as yf
from datetime import date
from sqlalchemy import create_engine, text
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




def get_nasdaq_100() -> list | None:
   # 1. Získání seznamu tickerů z Wikipedie
   # Pandas umí přečíst HTML tabulky přímo z URL
   url = "https://en.wikipedia.org/wiki/Nasdaq-100"

   try:
       # read_html vrací list všech tabulek na stránce
       tables = pd.read_html(url)

       # Obvykle je tabulka s firmami ta s indexem 4 (nebo 3), ale lepší je najít ji podle sloupce 'Ticker'
       # Hledáme tabulku, která obsahuje sloupec "Ticker"
       nasdaq_table = next(t for t in tables if "Ticker" in t.columns)

       # Převedeme na list
       tickers = nasdaq_table["Ticker"].tolist()
       print(f"Nalezeno {len(tickers)} tickerů.")

   except Exception as e:
       print(f"Chyba při stahování seznamu tickerů: {e}")
       return
   data = yf.download(tickers, period="1y", group_by="ticker", auto_adjust=True)
   return data




def get_realized_volatility(date: str) -> None:
    real_data = yf.download(..., date=date)


def run_evaluation() -> None:
    today = date.today()

    sql_extract = text("""
       SELECT *
       FROM garch_preds 
       WHERE target_date = :today
    """)

    with engine.connect() as conn:
        preds = conn.execute(sql_extract, {"today": today}).fetchall()

    real_vol = get_realized_volatility(today)


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
