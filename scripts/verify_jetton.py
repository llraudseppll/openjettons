import json
import requests
import yaml
import sys
import os
from urllib.parse import quote

TONCENTER_API = "https://toncenter.com/api/v2"

def get_jetton_data(address):
    """Fetch jetton data from TON Center API."""
    try:
        url = f"{TONCENTER_API}/runGetMethod"
        payload = {
            "address": address,
            "method": "get_jetton_data",
            "stack": []
        }
        response = requests.post(url, json=payload, timeout=10)
        print(f"HTTP Status Code: {response.status_code}")
        print(f"Response Text: {response.text[:200]}")
        response.raise_for_status()
        data = response.json()
        if not data.get("ok"):
            print(f"Error: API request failed for address {address}: {data.get('error')}")
            return None
        result = data["result"]["stack"]
        if len(result) < 4:
            print(f"Error: Invalid jetton data structure for {address}")
            return None
        jetton_data = {
            "address": address,
            "isJetton": True,
            "name": "",
            "symbol": "",
            "decimals": 0
        }
        return jetton_data
    except requests.HTTPError as e:
        print(f"HTTP Error for {address}: {e}")
        return None
    except requests.RequestException as e:
        print(f"Request Error for {address}: {e}")
        return None
    except ValueError as e:
        print(f"JSON Decode Error for {address}: {e}")
        return None

def validate_jetton(jetton_yaml, jetton_data):
    """Validate jetton YAML against TON Center data."""
    if not jetton_data:
        print("Error: No jetton data received")
        return False
    if jetton_yaml["address"] != jetton_data.get("address"):
        print("Error: Address mismatch")
        return False
    if not jetton_data.get("isJetton"):
        print("Error: Contract is not a jetton")
        return False
    print(f"Jetton at {jetton_yaml['address']} validated successfully!")
    return True

def verify_files(files):
    """Verify specified jetton YAML files."""
    all_valid = True
    valid_jettons = []
    print(f"Processing files: {files}")
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
                if validate_jetton(jetton_yaml, jetton_data):
                    valid_jettons.append(jetton_yaml)
                else:
                    print(f"Error: Validation failed for {file}")
                    all_valid = False
            except yaml.YAMLError as e:
                print(f"Error: Failed to parse {file}: {e}")
                all_valid = False
    return all_valid, valid_jettons

def generate_jettons_json(valid_jettons):
    """Generate jettons.json, appending new valid jettons."""
    # Читаем существующий jettons.json, если он есть
    existing_jettons = []
    jettons_json_path = "jettons.json"
    if os.path.exists(jettons_json_path):
        try:
            with open(jettons_json_path, "r") as f:
                existing_jettons = json.load(f)
                if not isinstance(existing_jettons, list):
                    print("Error: jettons.json is not a valid list, resetting to empty")
                    existing_jettons = []
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse jettons.json: {e}, resetting to empty")
            existing_jettons = []

    # Создаём множество адресов существующих токенов для избежания дубликатов
    existing_addresses = {jetton["address"] for jetton in existing_jettons}
    
    # Добавляем новые токены, если их ещё нет
    for jetton in valid_jettons:
        if jetton["address"] not in existing_addresses:
            existing_jettons.append(jetton)
            existing_addresses.add(jetton["address"])
            print(f"Added jetton {jetton['address']} to jettons.json")
        else:
            print(f"Skipping duplicate jetton {jetton['address']}")

    # Записываем обновлённый список в jettons.json
    with open(jettons_json_path, "w") as f:
        json.dump(existing_jettons, f, indent=2)
    print(f"Generated jettons.json with {len(existing_jettons)} jettons")

if __name__ == "__main__":
    files = sys.argv[1:] if len(sys.argv) > 1 else []
    if not files:
        print("No files specified, checking all jettons")
        files = [f"jettons/{f}" for f in os.listdir("jettons") if f.endswith(".yaml")]
    
    all_valid, valid_jettons = verify_files(files)
    
    if all_valid and valid_jettons:
        generate_jettons_json(valid_jettons)
        print("All jettons validated successfully")
        sys.exit(0)
    else:
        print("Validation failed for one or more jettons")
        sys.exit(1)
