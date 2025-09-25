import boto3
import mysql.connector
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import botocore.exceptions

# ✅ Load environment variables from config.env
load_dotenv(dotenv_path="config.env")

# ✅ Fetch MySQL environment variables
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")

# ✅ Fetch AWS environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

# ✅ Check for missing MySQL variables
if None in [MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB]:
    raise EnvironmentError("❌ Missing one or more MySQL environment variables in config.env")

# ✅ Check for missing AWS variables
if None in [AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION]:
    raise EnvironmentError("❌ Missing one or more AWS credentials in config.env")

# ✅ Connect to MySQL
conn = mysql.connector.connect(
    host=MYSQL_HOST,
    port=int(MYSQL_PORT),
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB
)
cursor = conn.cursor()

# ✅ Set up CloudWatch client
cloudwatch = boto3.client(
    'cloudwatch',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# ✅ Test AWS Credentials before fetching metrics
try:
    # ✅ Valid credential test using real CloudWatch namespace/metric
    cloudwatch.list_metrics(Namespace='AWS/EC2', MetricName='CPUUtilization')
except botocore.exceptions.ClientError as e:
    print("❌ AWS credentials error:", e)
    exit(1)

# ✅ Fetch and save CloudWatch metrics
def fetch_cloudwatch_metrics():
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=60)

    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': 'i-1234567890abcdef0'}],  # Replace with your actual instance ID
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average']
    )

    for data_point in response['Datapoints']:
        cursor.execute(
            """
            INSERT INTO cloudwatch_metrics (metric_name, timestamp, value, unit)
            VALUES (%s, %s, %s, %s)
            """,
            (
                'CPUUtilization',
                data_point['Timestamp'],
                data_point['Average'],
                data_point['Unit']
            )
        )
    conn.commit()
    print("✅ CloudWatch metrics saved to MySQL")

# ✅ Main
if __name__ == "__main__":
    fetch_cloudwatch_metrics()
