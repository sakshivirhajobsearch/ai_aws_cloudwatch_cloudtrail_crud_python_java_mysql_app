import boto3
import mysql.connector
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import botocore.exceptions

# ✅ Load environment variables
load_dotenv(dotenv_path="config.env")

# ✅ Get MySQL env variables
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")

# ✅ Get AWS env variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

# ✅ Check MySQL env vars
if None in [MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB]:
    raise EnvironmentError("❌ Missing MySQL environment variables in config.env")

# ✅ Check AWS env vars
if None in [AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION]:
    raise EnvironmentError("❌ Missing AWS credentials in config.env")

# ✅ Connect to MySQL
conn = mysql.connector.connect(
    host=MYSQL_HOST,
    port=int(MYSQL_PORT),
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB
)
cursor = conn.cursor()

# ✅ Set up CloudTrail client
cloudtrail = boto3.client(
    'cloudtrail',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# ✅ Test AWS credentials
try:
    cloudtrail.lookup_events(MaxResults=1)
except botocore.exceptions.ClientError as e:
    print("❌ AWS credentials error:", e)
    exit(1)

# ✅ Fetch and save CloudTrail logs
def fetch_cloudtrail_logs():
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=1)

    response = cloudtrail.lookup_events(
        StartTime=start_time,
        EndTime=end_time,
        MaxResults=50
    )

    for event in response['Events']:
        cursor.execute(
            """
            INSERT INTO cloudtrail_logs (
                event_name,
                username,
                event_time,
                aws_region,
                source_ip
            ) VALUES (%s, %s, %s, %s, %s)
            """,
            (
                event.get('EventName'),
                event.get('Username'),
                event.get('EventTime'),
                event.get('Resources', [{}])[0].get('Region', AWS_REGION),
                event.get('SourceIpAddress')
            )
        )
    conn.commit()
    print("✅ CloudTrail logs saved to MySQL")

# ✅ Main
if __name__ == "__main__":
    fetch_cloudtrail_logs()
