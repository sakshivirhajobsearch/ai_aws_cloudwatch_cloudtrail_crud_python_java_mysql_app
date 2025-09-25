package com.ai.aws.cloudwatch.cloudtrail.repository;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import javax.swing.table.DefaultTableModel;

public class CloudWatchRepository {
	private Connection conn;

	public CloudWatchRepository() {
		try {
			conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/ai_aws_monitoring", "root", "yourpassword");
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}

	public DefaultTableModel getAllMetrics() {
		DefaultTableModel model = new DefaultTableModel();
		model.addColumn("ID");
		model.addColumn("Metric Name");
		model.addColumn("Namespace");
		model.addColumn("Timestamp");
		model.addColumn("Value");

		try {
			Statement stmt = conn.createStatement();
			ResultSet rs = stmt.executeQuery("SELECT * FROM cloudwatch_metrics");
			while (rs.next()) {
				model.addRow(new Object[] { rs.getInt("id"), rs.getString("metric_name"), rs.getString("namespace"),
						rs.getTimestamp("timestamp"), rs.getDouble("value") });
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return model;
	}
}
