package com.ai.aws.cloudwatch.cloudtrail.aitrigger;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import javax.swing.JOptionPane;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;

public class AITrigger {
	
	public static void runPythonAI() {
		
		try {
			// Run Python AI script
			ProcessBuilder pb = new ProcessBuilder("python", "../backend-python/ai_analysis.py");
			pb.redirectErrorStream(true);
			Process process = pb.start();

			// Wait for completion
			BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
			while (reader.readLine() != null)
				;
			process.waitFor();

			// ✅ Java 8 compatible: Read file content as bytes, then convert to string
			Path aiOutputPath = Paths.get("../backend-python/ai_output.txt");
			byte[] fileBytes = Files.readAllBytes(aiOutputPath);
			String aiResult = new String(fileBytes, "UTF-8");

			// Show AI result in popup
			JTextArea textArea = new JTextArea(aiResult);
			textArea.setEditable(false);
			JScrollPane scrollPane = new JScrollPane(textArea);
			scrollPane.setPreferredSize(new java.awt.Dimension(800, 400));
			JOptionPane.showMessageDialog(null, scrollPane, "AI Analysis Result", JOptionPane.INFORMATION_MESSAGE);

		} catch (Exception e) {
			e.printStackTrace();
			JOptionPane.showMessageDialog(null, "Error running AI analysis: " + e.getMessage(), "Error",
					JOptionPane.ERROR_MESSAGE);
		}
	}
}
