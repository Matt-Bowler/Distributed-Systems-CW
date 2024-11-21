# Basic social media workflow

## Requirements

### For local development
- Azure storage account or azurite vscode extension
- Azure functions vscode extension

### For Deployment
- Azure account eligible to create function apps and storage accounts

# Usage
1. Clone this repository
2. Setup a python virtual environment
```bash
python -m venv .venv
```
3. Activate virtual environment and install dependencies
```bash
pip install -r requirements.txt
```
4. Make a copy of sample-local-settings.json called local-settings.json and populate `AZURE_STORAGE_CONNECTION_STRING` with your azure storage account connection string
5. If using azurite activate azurite
6. Press `F5` to run the function app
