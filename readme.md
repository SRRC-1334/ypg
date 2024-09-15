# YAML Parameters Generator

The YAML Parameters Generator is a Python script designed to process YAML files by replacing placeholders with actual values from an input YAML file. It supports handling multiple groups, where each group can have its own set of parameters and overrides. The script processes YAML files with a `.yaml` extension located in a specified directory and its subdirectories, applying common and group-specific values.

## Requirements

- Python 3.x
- `pyyaml`
- `jinja2`

## Installation

To install the required Python packages, create a virtual environment (optional) and run:

```bash
pip install -r requirements.txt
```

## Usage

To run the script, use the following command:

```bash
python ymlParametersGenerator.py <group_name> <input_yaml_file> <parameters_directory>
```

- `<group_name>`: Name of the group to process.
- `<input_yaml_file>`: Path to the YAML file containing common and group-specific parameters.
- `<parameters_directory>`: Path to the directory containing the parameters YAML files.

## Example

Given the following files:

### `group_A_Input.yaml`

```yaml
group_A:
  common:
    namespace: "dev-namespace"
    replicas: 3
    container_port: 8080
    log_level: "DEBUG"
    database_url: "jdbc:mysql://app1-db-url"
    max_connections: 1000
    api_version: 1117
    app_name: "RCGEN"

  rck8sparameters:
    metadata_name: "app1"
    services:
      - "aservice"
      - "auth_service"
      # - "auth_service2"
      - "auth2"

  rajk8sparameters:
    service_port: 80
    service_type: "ClusterIP"
group_B:
  common:
    namespace: "prod-namespace"
    replicas: 5
    container_port: 9090
    log_level: "INFO"

  deploymentparameters:
    metadata_name: "app2"
    app_name: "app2"
    image: "app2-image:v2.0"
    sidecar_name: "sidecar2"
    sidecar_image: "sidecar2-image:v2.0"

  serviceparameters:
    service_port: 443
    service_type: "LoadBalancer"
group_C:
  common:
    namespace: "prod-namespace"
    replicas: 5
    container_port: 9090
    log_level: "INFO"
```

### `rck8sparameters.yaml`

```yaml
services:
  - "aservice"
  - "auth_service"
  # - "auth_service2"
  # - "auth2"
  # - "service2"

api_version: "{{api_version}}"
max_connections: "{{max_connections}}"
database_url: "{{database_url}}"
rck8s_ns: "{{namespace}}"
rck8s_url: "http://{{namespace}}.world.dev.azure.net"
metadata_name: "{{ metadata_name }}"
```

### Running the Script

To process the `rck8sparameters.yaml` file for `group_A`, run:

```bash
python ymlParametersGenerator.py group_A /path/to/input.yaml /path/to/parameters_directory
```

### Expected Output for `rck8sparameters.yaml` (after processing)

```yaml
services:
  - "aservice"
  - "auth_service"
  # - "auth_service2"
  - "auth2"
  # - "service2"

api_version: "1117"
max_connections: 1000
database_url: "jdbc:mysql://app1-db-url"
rck8s_ns: "dev-namespace"
rck8s_url: "http://dev-namespace.world.dev.azure.net"
metadata_name: "app1"
```

## Notes

- The script replaces placeholders in the parameters files with values from the input YAML file.
- If a key is present in both the common section and a specific section, the specific section’s value overrides the common value.
- Only keys present in the input YAML file are replaced. Any extra keys in the parameters YAML file will be ignored.

---
