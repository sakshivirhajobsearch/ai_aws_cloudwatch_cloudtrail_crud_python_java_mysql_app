CREATE DATABASE IF NOT EXISTS ai_aws_monitoring;

USE ai_aws_monitoring;

CREATE TABLE IF NOT EXISTS cloudwatch_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    metric_name VARCHAR(255),
    namespace VARCHAR(255),
    timestamp DATETIME,
    value DOUBLE
);

CREATE TABLE IF NOT EXISTS cloudtrail_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(255),
    username VARCHAR(255),
    event_time DATETIME,
    aws_region VARCHAR(100),
    source_ip VARCHAR(100)
);
