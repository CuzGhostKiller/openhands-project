#!/bin/bash

# Health Monitor Installation Script
# This script installs and runs a simple health monitor on port 6767

echo "Installing Health Monitor..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Python3 is required but not installed."
    echo "Please install Python3 and try again."
    exit 1
fi

# Create a directory for the health monitor if it doesn't exist
mkdir -p /opt/health-monitor

# Copy the health monitor script to the installation directory
cp health_monitor.py /opt/health-monitor/
chmod +x /opt/health-monitor/health_monitor.py

# Create a systemd service file (if on a system that supports systemd)
cat > /etc/systemd/system/health-monitor.service << EOF
[Unit]
Description=Health Monitor Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/health-monitor
ExecStart=/usr/bin/python3 /opt/health-monitor/health_monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
systemctl daemon-reload
systemctl enable health-monitor.service
systemctl start health-monitor.service

echo "Health Monitor installed and started on port 6767"
echo "You can check the status with: systemctl status health-monitor.service"
echo ""
echo "Test the health monitor:"
echo "curl http://localhost:6767/health"
echo ""
echo "Main page:"
echo "curl http://localhost:6767/"