package com.ai.aws.cloudwatch.cloudtrail.gui;

import java.awt.BorderLayout;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JSplitPane;
import javax.swing.JTable;

import com.ai.aws.cloudwatch.cloudtrail.aitrigger.AITrigger;
import com.ai.aws.cloudwatch.cloudtrail.repository.CloudTrailRepository;
import com.ai.aws.cloudwatch.cloudtrail.repository.CloudWatchRepository;

public class UnifiedGUI extends JFrame {
	
	private static final long serialVersionUID = 1L;

	public UnifiedGUI() {

		setTitle("AWS Monitoring Dashboard with AI");
		setSize(1200, 600);
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		setLayout(new BorderLayout());

		// Tables
		JTable tableMetrics = new JTable(new CloudWatchRepository().getAllMetrics());
		JTable tableLogs = new JTable(new CloudTrailRepository().getAllLogs());

		// Add tables
		JSplitPane splitPane = new JSplitPane(JSplitPane.VERTICAL_SPLIT, new JScrollPane(tableMetrics),
				new JScrollPane(tableLogs));
		splitPane.setDividerLocation(300);
		add(splitPane, BorderLayout.CENTER);

		// AI Button
		JButton aiButton = new JButton("Run AI Analysis");
		aiButton.addActionListener(e -> AITrigger.runPythonAI());

		JPanel bottomPanel = new JPanel();
		bottomPanel.add(aiButton);
		add(bottomPanel, BorderLayout.SOUTH);

		setVisible(true);
	}

	public static void main(String[] args) {
		new UnifiedGUI();
	}
}
