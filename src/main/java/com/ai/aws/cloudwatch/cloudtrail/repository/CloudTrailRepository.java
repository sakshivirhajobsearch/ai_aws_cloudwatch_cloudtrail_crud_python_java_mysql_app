package com.ai.aws.cloudwatch.cloudtrail.repository;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import javax.swing.table.DefaultTableModel;

public class CloudTrailRepository {
	private Connection conn;

	public CloudTrailRepository() {
		try {
			conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/ai_aws_monitoring", "root", "yourpassword");
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}

	public DefaultTableModel getAllLogs() {
		DefaultTableModel model = new DefaultTableModel();
		model.addColumn("ID");
		model.addColumn("Event Name");
		model.addColumn("Username");
		model.addColumn("Event Time");
		model.addColumn("Region");
		model.addColumn("Source IP");

		try {
			Statement stmt = conn.createStatement();
			ResultSet rs = stmt.executeQuery("SELECT * FROM cloudtrail_logs");
			while (rs.next()) {
				model.addRow(new Object[] { rs.getInt("id"), rs.getString("event_name"), rs.getString("username"),
						rs.getTimestamp("event_time"), rs.getString("aws_region"), rs.getString("source_ip") });
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return model;
	}
}
