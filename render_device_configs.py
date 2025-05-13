import os
import yaml
import logging
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Base directory of this script
base_dir = os.path.dirname(__file__)
# Directory containing Jinja2 templates
template_dir = os.path.join(base_dir, "templates")
# Directory for rendered output files
output_dir = os.path.join(base_dir, "output")
# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Initialize the Jinja2 environment
env = Environment(
    loader=FileSystemLoader(template_dir),
    trim_blocks=True,
    lstrip_blocks=True
)

def render_device_configs(devices_file):
    try:
        # Load the devices YAML file
        with open(devices_file, 'r') as f:
            devices_data = yaml.safe_load(f)

        # Validate structure
        if 'devices' not in devices_data:
            logging.error("Invalid YAML structure: 'devices' key not found.")
            return

        for device in devices_data['devices']:
            device_name = device.get('name')
            if not device_name:
                logging.warning("Device entry missing 'name'. Skipping...")
                continue

            # Determine template file (explicit or fallback to type)
            template_file = device.get('template') or f"{device.get('type', 'default')}_template.j2"

            # Load template
            try:
                template = env.get_template(template_file)
            except TemplateNotFound:
                logging.warning(f"Template {template_file} not found for {device_name}. Skipping...")
                continue

            # Render template
            try:
                rendered_config = template.render(device)
            except Exception as e:
                logging.error(f"Error rendering {device_name}: {e}")
                continue

            # Write output file to output directory
            output_path = os.path.join(output_dir, f"{device_name}_config.txt")
            try:
                with open(output_path, 'w') as out_f:
                    out_f.write(rendered_config)
                logging.info(f"Configuration for {device_name} saved to {output_path}")
            except Exception as e:
                logging.error(f"Error writing {device_name} config: {e}")

    except FileNotFoundError:
        logging.error(f"Devices file {devices_file} not found.")
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    devices_file = os.path.join(base_dir, "devices.yaml")
    render_device_configs(devices_file)
