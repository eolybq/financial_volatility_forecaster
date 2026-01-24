import yfinance as yf

# Připojení k té stejné vzdálené DB
engine = create_engine(DATABASE_URL)

def evaluate_predictions():
    with Session(engine) as session:
        # 1. Najdi predikce, které jsou starší než dnešek a nemají vyplněnou realitu
        for log in logs:
            # 2. Stáhni data pro ten konkrétní den
            df = yf.download(log.ticker, start=log.target_date, end=log.target_date + timedelta(days=1))
            
            if not df.empty:
                # 3. Spočítej "skutečnou" volatilitu (zjednodušeně Absolutní Return)
                # Otevírací vs Uzavírací cena ten den, nebo High-Low range
                open_price = df['Open'].iloc[0]
                close_price = df['Adj Close'].iloc[0]
                
                # Realized Volatility proxy: |(Close - Open) / Open| * 100
                actual_vol = abs((close_price - open_price) / open_price) * 100
                
                # 4. Update v DB
                log.actual_volatility = actual_vol
                session.add(log)
                print(f"Updated {log.ticker}: Pred={log.predicted_volatility:.2f}, Act={actual_vol:.2f}")
        
        session.commit()

if __name__ == "__main__":
    evaluate_predictions()
