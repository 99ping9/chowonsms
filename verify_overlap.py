import requests
from datetime import date, timedelta

BASE_URL = "http://127.0.0.1:8000"

def test_double_booking():
    print("Running Double Booking Prevention Test...")

    # 1. Create Base Reservation
    print("\n1. Creating Base Reservation (2025-05-10 to 2025-05-12)...")
    base_res = {
        "guest_name": "Test User 1",
        "phone_number": "010-1111-1111",
        "accommodation_name": "초원고택1",
        "checkin_date": "2025-05-10",
        "checkout_date": "2025-05-12",
        "memo": "Base"
    }
    res = requests.post(f"{BASE_URL}/reservations/", json=base_res)
    if res.status_code == 200:
        print("✅ Base reservation created.")
        base_id = res.json()['id']
    else:
        print(f"❌ Failed to create base reservation: {res.text}")
        return

    try:
        # 2. Test Overlap (Inside)
        print("\n2. Testing Overlap (2025-05-11 to 2025-05-12)...")
        overlap_res = base_res.copy()
        overlap_res["guest_name"] = "Test User 2"
        overlap_res["checkin_date"] = "2025-05-11"
        overlap_res["checkout_date"] = "2025-05-12"
        
        res = requests.post(f"{BASE_URL}/reservations/", json=overlap_res)
        if res.status_code == 400 and "이미 예약된 날짜입니다" in res.text:
            print(f"✅ Correctly rejected: {res.text}")
        else:
            print(f"❌ Unexpected result: {res.status_code} {res.text}")

        # 3. Test Checkout Overlap (Allowed)
        print("\n3. Testing Checkout Overlap (2025-05-12 to 2025-05-14)...")
        allowed_res = base_res.copy()
        allowed_res["guest_name"] = "Test User 3"
        allowed_res["checkin_date"] = "2025-05-12"
        allowed_res["checkout_date"] = "2025-05-14"
        
        res = requests.post(f"{BASE_URL}/reservations/", json=allowed_res)
        if res.status_code == 200:
            print("✅ Checkout overlap allowed.")
            allowed_id = res.json()['id']
            # Cleanup
            requests.delete(f"{BASE_URL}/reservations/{allowed_id}")
        else:
            print(f"❌ Failed allowed overlap: {res.text}")

    finally:
        # Cleanup Base
        print(f"\nCleaning up base reservation {base_id}...")
        requests.delete(f"{BASE_URL}/reservations/{base_id}")

if __name__ == "__main__":
    test_double_booking()
