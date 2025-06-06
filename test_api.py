import requests
import json

BASE_URL = "http://localhost:5000"
API_KEY = "3f5e2f9f8b8e4a6b9cfd9eb56ad21e36b7a85efab6224c9787e118fc0df47c28" 
HEADERS = {"x-api-key": API_KEY}
BAD_HEADERS = {"x-api-key": "wrong-key"}
NO_HEADERS = {}

def print_state(tag):
    print(f"\n=== {tag} ===")
    r = requests.get(f"{BASE_URL}/view_all", headers=HEADERS)
    print("Status:", r.status_code)
    print(json.dumps(r.json(), indent=2))

def test_unauthorized_access():
    print("\n=== Unauthorized Access Tests ===")

    r1 = requests.post(f"{BASE_URL}/add_data", json={}, headers=NO_HEADERS)
    print("No Header:", r1.status_code, r1.json())

    r2 = requests.post(f"{BASE_URL}/add_data", json={}, headers=BAD_HEADERS)
    print("Wrong API Key:", r2.status_code, r2.json())

def test_add_data():
    print("\n=== Test Add Data ===")
    data = {
        "id": "unit001",
        "document": "2BHK in Whitefield, Bangalore for 98L with pool & gym.",
        "metadata": {
            "mode": "customer",
            "type": "unit",
            "project_name": "Whitefield Enclave",
            "developer": "Prestige",
            "location": "Whitefield",
            "property_type": "2BHK",
            "price": 9800000,
            "possession_date": "2025-12-31",
            "features": ["pool", "gym"],
            "floor_plan_url": None,
            "brochure_url": None,
            "source": "scraped_web",
            "timestamp": "2025-06-05T10:00:00"
        }
    }
    r = requests.post(f"{BASE_URL}/add_data", json=data, headers=HEADERS)
    print("Add:", r.status_code, r.json())

def test_add_data2():
    print("\n=== Test Add Data 2 ===")
    data = {
        "id": "unit002",
        "document": "3BHK in Whitefield, Bangalore for 98L with pool & gym.",
        "metadata": {
            "mode": "customer",
            "type": "unit",
            "project_name": "Abi Enclave",
            "developer": "Prestige2",
            "location": "KK Nagar",
            "property_type": "3BHK",
            "price": 9800000,
            "possession_date": "2025-12-31",
            "features": ["pool", "gym"],
            "floor_plan_url": None,
            "brochure_url": None,
            "source": "scraped_web",
            "timestamp": "2025-06-05T10:00:00"
        }
    }
    r = requests.post(f"{BASE_URL}/add_data", json=data, headers=HEADERS)
    print("Add:", r.status_code, r.json())

def test_update_data():
    print("\n=== Test Update Data ===")
    data = {
        "id": "unit001",
        "metadata": {
            "mode": "customer",
            "type": "unit",
            "project_name": "Whitefield Enclave - Updated",
            "developer": "Prestige",
            "location": "Whitefield",
            "property_type": "2BHK",
            "price": 9900000,
            "possession_date": "2025-12-31",
            "features": ["pool", "gym", "garden"],
            "floor_plan_url": None,
            "brochure_url": None,
            "source": "scraped_web",
            "timestamp": "2025-06-05T12:00:00"
        }
    }
    r = requests.post(f"{BASE_URL}/update_data", json=data, headers=HEADERS)
    print("Update:", r.status_code, r.json())

def test_generate_embedding():
    print("\n=== Test Generate Embedding ===")
    text = {"text": "3BHK flat near Electronic City with modern amenities"}
    r = requests.post(f"{BASE_URL}/generate_embedding", json=text, headers=HEADERS)
    print("Embedding:", r.status_code)
    print("Embedding Length:", len(r.json().get("embedding", [])))

def test_query_db():
    print("\n=== Test Query DB ===")
    query = {"query": "2BHK in Whitefield", "n_results": 2}
    r = requests.post(f"{BASE_URL}/query_db", json=query, headers=HEADERS)
    print("Query Results:", r.status_code)
    print(json.dumps(r.json(), indent=2))

def test_delete_data():
    print("\n=== Test Delete Data ===")
    r = requests.delete(f"{BASE_URL}/delete_data/unit001", headers=HEADERS)
    print("Delete:", r.status_code, r.json())

if __name__ == "__main__":
    test_unauthorized_access()
    print_state("Before Add")
    test_add_data()
    print_state("After Add")
    print_state("Before Add2")
    test_add_data2()
    print_state("After Add2")
    test_update_data()
    print_state("After Update")
    test_generate_embedding()
    test_query_db()
    # test_delete_data()
    # print_state("After Delete")
