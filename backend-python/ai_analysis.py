import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from ai_utils import detect_anomalies, summarize_cloudtrail

# ✅ Load environment variables
load_dotenv(dotenv_path="config.env")

# ✅ Get MySQL credentials from env
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

# ✅ Check all required environment variables
if None in [MYSQL_HOST, MYSQL_PORT, MYSQL_DB, MYSQL_USER, MYSQL_PASSWORD]:
    raise EnvironmentError("❌ Missing required MySQL environment variables in config.env")

# ✅ Create SQLAlchemy engine
engine = create_engine(
    f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

# ✅ Analyze CloudWatch Metrics
def analyze_cloudwatch():
    df = pd.read_sql("SELECT * FROM cloudwatch_metrics", engine)
    anomalies = detect_anomalies(df)
    with open("ai_output.txt", "w", encoding="utf-8") as f:
        f.write("=== CloudWatch Analysis ===\n")
        if anomalies.empty:
            f.write("✅ No anomalies detected in CloudWatch metrics.\n")
        else:
            f.write("🚨 CloudWatch Anomalies Detected:\n")
            f.write(anomalies.to_string(index=False))
            f.write("\n")

# ✅ Analyze CloudTrail Logs
def analyze_cloudtrail():
    df = pd.read_sql("SELECT * FROM cloudtrail_logs", engine)
    summary = summarize_cloudtrail(df)  # ✅ This is already a string
    with open("ai_output.txt", "a", encoding="utf-8") as f:
        f.write("\n=== CloudTrail User Activity Summary ===\n")
        f.write(summary)  # ✅ FIXED: No .to_string() used on a string

# ✅ Main
if __name__ == "__main__":
    analyze_cloudwatch()
    analyze_cloudtrail()
