import pandas as pd

def detect_anomalies(df, column='value'):
    if df.empty:
        return pd.DataFrame()
    mean_val = df[column].mean()
    std_val = df[column].std()
    anomalies = df[df[column] > mean_val + 2 * std_val]
    return anomalies

def summarize_cloudtrail(df):
    if df.empty:
        return "No CloudTrail logs available."
    summary = df.groupby('username')['event_name'].count().sort_values(ascending=False)
    return summary
