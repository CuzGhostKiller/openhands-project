#!/usr/bin/env python3
"""
Server Health Monitor - A tool to monitor system resources and Docker status.
"""

import os
import sys
import json
import platform
import psutil
from datetime import datetime
import subprocess

def get_system_info():
    """Get basic system information."""
    try:
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "cpu_model": platform.processor() or platform.machine(),
            "logical_cpu_count": os.cpu_count(),
            "total_ram": psutil.virtual_memory().total,
            "available_ram": psutil.virtual_memory().available
        }
    except Exception as e:
        print(f"Error getting system info: {e}")
        return None

def get_cpu_usage():
    """Get current CPU usage percentage."""
    try:
        return psutil.cpu_percent(interval=1)
    except Exception as e:
        print(f"Error getting CPU usage: {e}")
        return None

def get_ram_usage():
    """Get current RAM usage percentage."""
    try:
        return psutil.virtual_memory().percent
    except Exception as e:
        print(f"Error getting RAM usage: {e}")
        return None

def get_disk_usage():
    """Get disk usage for root filesystem."""
    try:
        # Get disk usage for root directory
        disk = psutil.disk_usage('/')
        return {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent
        }
    except Exception as e:
        print(f"Error getting disk usage: {e}")
        return None

def check_docker():
    """Check if Docker is installed without requiring root access."""
    try:
        # Try to run docker version command
        result = subprocess.run(['docker', 'version'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE, 
                               text=True)
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        # Docker not found or not accessible
        return False

def format_bytes(bytes_value):
    """Convert bytes to human readable format."""
    if bytes_value is None:
        return "N/A"
    
    if bytes_value < 1024.0:
        return f"{bytes_value:.2f} B"
    
    for unit in ['KB', 'MB', 'GB', 'TB']:
        bytes_value /= 1024.0
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
    
    return f"{bytes_value:.2f} PB"

def generate_report():
    """Generate the complete health report."""
    report = {
        "timestamp": datetime.now().isoformat(),
        "system_info": get_system_info(),
        "cpu_usage": get_cpu_usage(),
        "ram_usage": get_ram_usage(),
        "disk_usage": get_disk_usage(),
        "docker_installed": check_docker(),
        "warnings": []
    }
    
    # Check for warnings
    if report["cpu_usage"] is not None and report["cpu_usage"] > 85:
        report["warnings"].append("CPU usage exceeds 85%")
    
    if report["ram_usage"] is not None and report["ram_usage"] > 85:
        report["warnings"].append("RAM usage exceeds 85%")
        
    if report["disk_usage"] is not None and report["disk_usage"]["percent"] > 85:
        report["warnings"].append("Disk usage exceeds 85%")
    
    return report

def print_report(report):
    """Print a clean, readable terminal report."""
    print("=" * 50)
    print("SERVER HEALTH MONITOR REPORT")
    print("=" * 50)
    print(f"Timestamp: {report['timestamp']}")
    print()
    
    if report["system_info"]:
        print("SYSTEM INFORMATION:")
        print(f"  OS: {report['system_info']['os']} {report['system_info']['os_version']}")
        print(f"  CPU Model: {report['system_info']['cpu_model']}")
        print(f"  Logical CPU Count: {report['system_info']['logical_cpu_count']}")
        print(f"  Total RAM: {format_bytes(report['system_info']['total_ram'])}")
        print(f"  Available RAM: {format_bytes(report['system_info']['available_ram'])}")
    else:
        print("SYSTEM INFORMATION: Error retrieving data")
    
    print()
    print("RESOURCE USAGE:")
    if report["cpu_usage"] is not None:
        print(f"  CPU Usage: {report['cpu_usage']:.2f}%")
    else:
        print("  CPU Usage: Error retrieving data")
        
    if report["ram_usage"] is not None:
        print(f"  RAM Usage: {report['ram_usage']:.2f}%")
    else:
        print("  RAM Usage: Error retrieving data")
        
    if report["disk_usage"]:
        print(f"  Disk Usage: {report['disk_usage']['percent']:.2f}%")
        print(f"  Disk Total: {format_bytes(report['disk_usage']['total'])}")
        print(f"  Disk Used: {format_bytes(report['disk_usage']['used'])}")
        print(f"  Disk Free: {format_bytes(report['disk_usage']['free'])}")
    else:
        print("  Disk Usage: Error retrieving data")
    
    print()
    print("DOCKER STATUS:")
    print(f"  Docker Installed: {'Yes' if report['docker_installed'] else 'No'}")
    
    print()
    if report["warnings"]:
        print("WARNINGS:")
        for warning in report["warnings"]:
            print(f"  ⚠️  {warning}")
    else:
        print("No warnings - all usage levels are within acceptable limits.")

def save_report(report, filename="health-report.json"):
    """Save the report to a JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nReport saved to {filename}")
    except Exception as e:
        print(f"Error saving report: {e}")

def main():
    """Main function to run the health monitor."""
    print("Starting Server Health Monitor...")
    
    # Generate the report
    report = generate_report()
    
    # Print the report
    print_report(report)
    
    # Save the report
    save_report(report)
    
    return report

if __name__ == "__main__":
    main()