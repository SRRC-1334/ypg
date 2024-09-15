import os
import yaml
import glob
import jinja2
import sys

def load_yaml(file_path):
    """Load YAML file."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def replace_placeholders(content, variables):
    """Replace Jinja2 placeholders in the content with actual values."""
    template = jinja2.Template(content)
    return template.render(variables)

def update_array_values(original_array, new_array):
    """Update the original array with values from the new array, handling comments."""
    updated_array = []
    new_values = set(new_array)
    for item in original_array:
        if isinstance(item, str) and item in new_values:
            updated_array.append(item)
            new_values.remove(item)
        elif isinstance(item, str):
            updated_array.append(item)
        elif isinstance(item, str) and item.startswith("#"):
            updated_array.append(item)
    updated_array.extend(new_values)
    return updated_array

def process_parameters_file(file_path, variables, group_data):
    """Process a single parameters YAML file."""
    with open(file_path, 'r') as file:
        content = file.read()

    updated_content = replace_placeholders(content, variables)

    yaml_data = yaml.safe_load(updated_content)
    
    if group_data:
        for key, value in group_data.items():
            if key in yaml_data:
                if isinstance(yaml_data[key], list) and isinstance(value, list):
                    yaml_data[key] = update_array_values(yaml_data[key], value)
                else:
                    yaml_data[key] = value

    with open(file_path, 'w') as file:
        yaml.dump(yaml_data, file)

def main():
    if len(sys.argv) != 4:
        print("Usage: python ymlParametersGenerator.py <group_name> <input_yaml_file> <parameters_directory>")
        sys.exit(1)

    
    group_name = sys.argv[1]
    input_yaml_file = sys.argv[2]
    parameters_dir = sys.argv[3]

    input_data = load_yaml(input_yaml_file)

    if group_name not in input_data:
        print(f"Group '{group_name}' not found in the input YAML file.")
        sys.exit(1)

    group_data = input_data[group_name]

    common_data = group_data.get('common', {})

    pattern = os.path.join(parameters_dir, '**', '*parameters.yaml')
    for parameters_file in glob.glob(pattern, recursive=True):
        print(f"Processing file: {parameters_file}")

        process_parameters_file(parameters_file, common_data, group_data.get(os.path.basename(parameters_file).split('.')[0], {}))

    print("Processing completed.")

if __name__ == "__main__":
    main()
