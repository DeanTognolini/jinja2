import os
import yaml
import logging
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Directory containing the Jinja2 templates
template_dir = os.path.dirname(__file__)

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
        
        # Validate the structure of the YAML file
        if 'devices' not in devices_data:
            logging.error("Invalid YAML structure: 'devices' key not found.")
            return
        
        devices = devices_data['devices']
        
        for device in devices:
            # Extract device details
            device_name = device.get('name')
            if not device_name:
                logging.warning("Device entry missing 'name'. Skipping...")
                continue
            
            config_file = f"{device_name}_config.txt"
            template_file = f"{device.get('type', 'default')}_template.j2"
            
            # Check if the template file exists
            try:
                template = env.get_template(template_file)
            except TemplateNotFound:
                logging.warning(f"Template file {template_file} not found for device {device_name}. Skipping...")
                continue
            
            # Render the template with device details
            try:
                rendered_config = template.render(device)
            except Exception as render_error:
                logging.error(f"Error rendering template for {device_name}: {render_error}")
                continue
            
            # Write the rendered config to the output file
            output_file = os.path.join(template_dir, config_file)
            try:
                with open(output_file, 'w') as f:
                    f.write(rendered_config)
                logging.info(f"Configuration for {device_name} rendered and saved to {config_file}")
            except Exception as write_error:
                logging.error(f"Error writing configuration for {device_name}: {write_error}")
    except FileNotFoundError:
        logging.error(f"Devices file {devices_file} not found.")
    except yaml.YAMLError as yaml_error:
        logging.error(f"Error parsing YAML file: {yaml_error}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    # Path to the devices YAML file
    devices_file = os.path.join(template_dir, "devices.yaml")
    
    # Render configurations for all devices
    render_device_configs(devices_file)