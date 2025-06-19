import json
import requests
import yaml
import sys
import os
import base64
from urllib.parse import quote
from tonsdk.utils import b64_to_bytes, bytes_to_dict  # Для парсинга Cell

# TON Center API endpoint
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

        # Парсинг результата get_jetton_data
        # Результат: [total_supply, mintable, admin_address, jetton_content, jetton_wallet_code]
        result = data["result"]["stack"]
        if len(result) < 4:
            print(f"Error: Invalid jetton data structure for {address}")
            return None

        # Извлечение jetton_content (метаданные)
        jetton_content = result[3]
        if jetton_content["type"] != "slice":
            print(f"Error: Jetton content is not a slice for {address}")
            return None

        # Парсинг метаданных из Cell
        content_bytes = b64_to_bytes(jetton_content["value"])
        try:
            content_dict = bytes_to_dict(content_bytes)
        except Exception as e:
            print(f"Error parsing jetton content for {address}: {e}")
            return None

        # Извлечение name, symbol, decimals
        metadata = content_dict.get("content", {})
        name = metadata.get("name", "")
        symbol = metadata.get("symbol", "")
        decimals = int(metadata.get("decimals", 0)) if metadata.get("decimals") else 0

        if not name or not symbol:
            print(f"Error: Missing name or symbol in metadata for {address}")
            return None

        # Формируем данные в формате, совместимом с валидацией
        jetton_data = {
            "address": address,
            "name": name,
            "symbol": symbol,
            "decimals": decimals,
            "isJetton": True  # Предполагаем, что контракт jetton, если метод успешен
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
