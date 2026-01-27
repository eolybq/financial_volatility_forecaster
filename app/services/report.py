# 4. Report
# Vizualizace


# 4. Generování Reportu (Statistiky)
    mape = df_res['error_rel'].mean()
    mae = df_res['error_abs'].mean()
    bias = (df_res['predicted'] - df_res['realized']).mean()
    
    worst_tickers = df_res.sort_values('error_abs', ascending=False).head(5)

    # HTML Email Body
    html_body = f"""
    <h2>📊 NASDAQ 100 Volatility Model Report</h2>
    <p><b>Datum evaluace:</b> {datetime.now().strftime('%Y-%m-%d')}</p>
    <p><b>Počet tickerů:</b> {len(df_res)}</p>
    <hr>
    <h3>📈 Globální Metriky</h3>
    <ul>
        <li><b>MAE (Průměrná chyba):</b> {mae:.2f}% vol</li>
        <li><b>MAPE (Relativní chyba):</b> {mape:.2f}%</li>
        <li><b>Bias (Odchylka):</b> {bias:.2f}% ({"Nadhodnocuje" if bias > 0 else "Podhodnocuje"})</li>
    </ul>
    <hr>
    <h3>🚨 Největší úlety (Top 5 Error)</h3>
    <table border="1" cellpadding="5" style="border-collapse: collapse;">
        <tr>
            <th>Ticker</th><th>Predikce</th><th>Realita</th><th>Chyba</th>
        </tr>
        {''.join(f"<tr><td>{r.ticker}</td><td>{r.predicted:.2f}</td><td>{r.realized:.2f}</td><td>{r.error_abs:.2f}</td></tr>" for i, r in worst_tickers.iterrows())}
    </table>
    """
    
    send_email("Volatility Model Daily Report", html_body)
