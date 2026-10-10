#!/usr/bin/env python3
"""
Tests for Server Health Monitor application.
"""

import os
import sys
import json
import unittest
from unittest.mock import patch, MagicMock

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from health_monitor import (
    get_system_info,
    get_cpu_usage,
    get_ram_usage,
    get_disk_usage,
    check_docker,
    format_bytes,
    generate_report,
    print_report,
    save_report
)

class TestHealthMonitor(unittest.TestCase):
    
    def test_get_system_info(self):
        """Test system information retrieval."""
        result = get_system_info()
        self.assertIsNotNone(result)
        self.assertIn('os', result)
        self.assertIn('cpu_model', result)
        self.assertIn('logical_cpu_count', result)
        self.assertIn('total_ram', result)
        self.assertIn('available_ram', result)
    
    def test_get_cpu_usage(self):
        """Test CPU usage retrieval."""
        result = get_cpu_usage()
        self.assertIsInstance(result, (int, float))
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 100)
    
    def test_get_ram_usage(self):
        """Test RAM usage retrieval."""
        result = get_ram_usage()
        self.assertIsInstance(result, (int, float))
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 100)
    
    def test_get_disk_usage(self):
        """Test disk usage retrieval."""
        result = get_disk_usage()
        self.assertIsNotNone(result)
        self.assertIn('total', result)
        self.assertIn('used', result)
        self.assertIn('free', result)
        self.assertIn('percent', result)
    
    def test_format_bytes(self):
        """Test byte formatting function."""
        # Test various byte values
        self.assertEqual(format_bytes(1024), "1.00 KB")
        self.assertEqual(format_bytes(1024 * 1024), "1.00 MB")
        self.assertEqual(format_bytes(1024 * 1024 * 1024), "1.00 GB")
        self.assertEqual(format_bytes(None), "N/A")
    
    def test_check_docker_installed(self):
        """Test Docker installation check."""
        # This should not raise an exception
        result = check_docker()
        self.assertIsInstance(result, bool)
    
    @patch('health_monitor.get_system_info')
    @patch('health_monitor.get_cpu_usage')
    @patch('health_monitor.get_ram_usage')
    @patch('health_monitor.get_disk_usage')
    @patch('health_monitor.check_docker')
    def test_generate_report(self, mock_docker, mock_disk, mock_ram, mock_cpu, mock_system):
        """Test report generation."""
        # Mock the functions to return specific values
        mock_system.return_value = {
            'os': 'Linux',
            'cpu_model': 'Intel Xeon',
            'logical_cpu_count': 4,
            'total_ram': 8589934592,  # 8GB in bytes
            'available_ram': 4294967296  # 4GB in bytes
        }
        mock_cpu.return_value = 45.0
        mock_ram.return_value = 60.0
        mock_disk.return_value = {
            'total': 10737418240,  # 10GB
            'used': 5368709120,    # 5GB
            'free': 5368709120,    # 5GB
            'percent': 50.0
        }
        mock_docker.return_value = True
        
        report = generate_report()
        
        self.assertIsNotNone(report)
        self.assertIn('timestamp', report)
        self.assertIn('system_info', report)
        self.assertIn('cpu_usage', report)
        self.assertIn('ram_usage', report)
        self.assertIn('disk_usage', report)
        self.assertIn('docker_installed', report)
        self.assertIn('warnings', report)
        
    def test_save_report(self):
        """Test saving report to JSON file."""
        # Create a mock report
        report = {
            'test': 'data',
            'timestamp': '2023-01-01T00:00:00'
        }
        
        # Test saving the report
        save_report(report, 'test-report.json')
        
        # Check if file was created
        self.assertTrue(os.path.exists('test-report.json'))
        
        # Read and verify content
        with open('test-report.json', 'r') as f:
            saved_data = json.load(f)
            self.assertEqual(saved_data['test'], 'data')
        
        # Clean up
        os.remove('test-report.json')

if __name__ == '__main__':
    unittest.main()