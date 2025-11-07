import subprocess

# Install wget
subprocess.run(["apt", "install", "wget", "-y"])

# Install webdriver_manager
subprocess.run(["pip", "install", "webdriver_manager"])

# Upgrade webdriver_manager
subprocess.run(["pip", "install", "--upgrade", "webdriver_manager"])

# Update package list
subprocess.run(["apt-get", "update"])

# Install Firefox
subprocess.run(["apt-get", "install", "firefox", "-y"])

# Install wget (if not installed)
subprocess.run(["apt-get", "install", "wget", "-y"])

# Download and install the latest version of GeckoDriver
subprocess.run(["wget", "https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz"])
subprocess.run(["tar", "-xvzf", "geckodriver-v0.30.0-linux64.tar.gz"])
subprocess.run(["chmod", "+x", "geckodriver"])
subprocess.run(["mv", "geckodriver", "/usr/local/bin/"])
