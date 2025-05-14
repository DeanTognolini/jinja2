# Device Configuration Renderer

This project is a Python-based tool that uses Jinja2 templates to generate device configurations from a YAML file. It is designed to simplify the process of creating consistent and reusable configurations for network devices.

## Features

- Parses device details from a YAML file (`devices.yaml`).
- Renders device configurations using Jinja2 templates stored in `templates` directory.
- Supports multiple device types with customizable templates.
- Logs errors and warnings for missing templates or invalid YAML structures.

## Prerequisites

- Python 3.7 or higher
- `pip` (Python package manager)
- `pyenv`

## Installation

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Create new Python venv: `python -m venv venv`.
4. Activate venv:
    * Powershell: `.\venv\Scripts\Activate.ps1`.
4. Install the required Python packages: `pip install -r requirements.txt`

## Usage
1. Prepare the YAML File:
    * Add device details to the devices.yaml file. Ensure the structure matches the expected format.
2. Create Templates:
    * Add Jinja2 templates for each device type in the templates/ directory. For example:
        * router_template.j2 for routers
        * switch_template.j2 for switches
3. Run the Script:
    * Execute the script to generate configurations: `python render_device_configs.py`.
4. Output:
    * The rendered configurations will be saved as <device_name>_config.txt in the output directory.

## Examples
* Sample YAML definitions: `devices.yaml`.
* Sample Template `router_template.j2`.
* Sample output `router1_config.txt`.

## Logging
The script logs important events, such as:

* Missing templates
* Invalid YAML structure
* Errors during rendering or file writing
* Logs are displayed in the console.

## License
This project is licensed under the MIT License. See the LICENSE file for details.