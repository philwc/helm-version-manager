# Helm Version Manager

This is a tool to manage and use multiple helm versions on the same machine.

## Requirements

- Python 3
- PIP

## Usage

### Installation

This will clone the repo somewhere convenient and create a symlink to the script

```bash
git clone https://github.com/philwc/helm-version-manager.git
cd helm-version-manager
pip3 install -r requirements.txt
sudo ./install.py
```

### Retrieving Versions of Helm

```bash
hvm get 3.0.2
```

### Using a specified version

```bash
hvm switch 3.0.2
```

### Deleting a speciefied version

```bash
hvm delete 3.0.2
```
