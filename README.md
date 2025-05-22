# Search LLM - Ollama Testing Tools

A collection of tools for testing and evaluating Ollama model performance and capabilities.

## Overview

This project provides utilities for testing Ollama language models with various prompts and scenarios to assess their quality, performance, and tool usage capabilities.

## Features

- **Model Quality Testing**: Evaluate different Ollama models across various tasks
- **Tool Usage Testing**: Test models' ability to use and integrate with external tools
- **Performance Benchmarking**: Measure response times and accuracy
- **Automated Reporting**: Generate comprehensive test reports with metrics and analysis

## Files

- `ollama_quality_tester.py` - Main quality testing script
- `ollama_tool_tester.py` - Tool usage testing functionality
- `ollama_report_*.md` - Generated test reports with timestamps

## Requirements

- Python 3.7+
- Ollama installed and running locally
- Access to desired Ollama models

## Usage

1. Ensure Ollama is running on your system
2. Install required Python dependencies
3. Run the testing scripts:
   ```bash
   python ollama_quality_tester.py
   python ollama_tool_tester.py
   ```
4. Check generated reports for analysis results

## Reports

The tool generates timestamped reports showing:
- Model performance metrics
- Response quality assessments
- Tool integration capabilities
- Comparative analysis between models

## Note

This is a research and testing tool designed to help evaluate and compare different Ollama models for various use cases.