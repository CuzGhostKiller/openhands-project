# Server Health Monitor Test Environment

This repository contains a test environment for OpenHands and local Qwen3-Coder development.

## Project: Server Health Monitor

A Python application that monitors system resources and Docker status with the following features:

1. **System Information**: Detects operating system, CPU model, logical CPU count, total RAM, and available RAM
2. **Resource Usage**: Displays CPU utilization and RAM usage percentages
3. **Disk Usage**: Reports disk usage for the root filesystem
4. **Docker Detection**: Checks whether Docker is installed without requiring root access
5. **Warning System**: Displays warnings when RAM, CPU, or disk usage exceeds 85%
6. **Clean Output**: Provides a readable terminal report
7. **JSON Export**: Saves the report to `health-report.json`
8. **Error Handling**: Gracefully handles missing dependencies and unsupported environments

## Requirements

- Python 3.x
- psutil library (automatically installed via requirements.txt)

## Installation

```bash
cd server-health-test
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python health_monitor.py
```

Or run the demo script:

```bash
python demo.py
```

## Tests

Run the automated tests with:

```bash
python test_health_monitor.py
```

## Files in this Repository

- `health_monitor.py`: Main application code
- `demo.py`: Demo script to run the application
- `test_health_monitor.py`: Automated tests (5 tests)
- `requirements.txt`: Dependencies
- `health-report.json`: Sample output file