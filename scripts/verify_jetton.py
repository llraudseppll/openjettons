import json
import requests
import yaml
import sys
import os
from urllib.parse import quote

# Tonscan API endpoint
TONSCAN_API = "https://tonscan.org/api/v1"

def get_jetton_data(address):
    """Fetch jetton data from tonscan API."""
    try:
        encoded_address = quote(address)
        url = f"{TONSCAN_API}/jetton/{encoded_address}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "ok" and data.get("data"):
            return data["data"]
        else:
            print(f"Error: No valid jetton data for address {address}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching data for {address}: {e}")
        return None

def validate_jetton(jetton_yaml, jetton_data):
    """Validate jetton YAML against tonscan data."""
    if not jetton_data:
        return False
    
    if jetton_yaml["address"] != jetton_data.get("address"):
        print("Error: Address mismatch")
        return False
    
    if not jetton_data.get("isJetton"):
        print("Error: Contract is not a jetton")
        return False
    
    if jetton_yaml["name"] != jetton_data.get("name"):
        print("Error: Name mismatch")
        return False
    if jetton_yaml["symbol"] != jetton_data.get("symbol"):
        print("Error: Symbol mismatch")
        return False
    if jetton_yaml["decimals"] != jetton_data.get("decimals"):
        print("Error: Decimals mismatch")
        return False
    
    print(f"Jetton {jetton_yaml['name']} validated successfully!")
    return True

def verify_files(files):
    """Verify specified jetton YAML files."""
    all_valid = True
    for file in files:
        if not file.startswith("jettons/") or not file.endswith(".yaml"):
            print(f"Skipping non-jetton file: {file}")
            continue
        if not os.path.exists(file):
            print(f"Error: File {file} does not exist")
            all_valid = False
            continue
        with open(file, "r") as f:
            try:
                jetton_yaml = yaml.safe_load(f)
                if not jetton_yaml or not isinstance(jetton_yaml, dict):
                    print(f"Error: Invalid YAML in {file}")
                    all_valid = False
                    continue
                jetton_data = get_jetton_data(jetton_yaml["address"])
                if not validate_jetton(jetton_yaml, jetton_data):
                    print(f"Error: Validation failed for {file}")
                    all_valid = False
            except yaml.YAMLError as e:
                print(f"Error: Failed to parse {file}: {e}")
                all_valid = False
    return all_valid

def generate_jettons_json():
    """Generate jettons.json from all valid jettons."""
    jettons = []
    for file in os.listdir("jettons"):
        if file.endswith(".yaml"):
            with open(f"jettons/{file}", "r") as f:
                try:
                    jetton_yaml = yaml.safe_load(f)
                    jetton_data = get_jetton_data(jetton_yaml["address"])
                    if validate_jetton(jetton_yaml, jetton_data):
                        jettons.append(jetton_yaml)
                except yaml.YAMLError as e:
                    print(f"Error: Failed to parse {file}: {e}")
    with open("jettons.json", "w") as f:
        json.dump(jettons, f, indent=2)
    print("Generated jettons.json")

if __name__ == "__main__":
    # Get files from command-line arguments (e.g., from GitHub Actions)
    files = sys.argv[1:] if len(sys.argv) > 1 else []
    if not files:
        print("No files specified, checking all jettons")
        all_valid = verify_files([f"jettons/{f}" for f in os.listdir("jettons") if f.endswith(".yaml")])
    else:
        all_valid = verify_files(files)
    
    if all_valid:
        generate_jettons_json()
        print("All jettons validated successfully")
        sys.exit(0)
    else:
        print("Validation failed for one or more jettons")
        sys.exit(1)
