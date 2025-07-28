/usr/bin/env python3
"""
JWT API Testing Script
This script demonstrates how to interact with the JWT authentication API endpoints.
Run this script to test various API operations.
"""

import requests
import json
import sys

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

class JWTAPITester:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.user_data = None

    def register_user(self, username, email, password, first_name="", last_name=""):
        """Register a new user"""
        url = f"{BASE_URL}/api/register/"
        data = {
            "username": username,
            "email": email,
            "password": password,
            "password2": password,
            "first_name": first_name,
            "last_name": last_name
        }
        
        print(f"🔐 Registering user: {username}")
        response = requests.post(url, json=data)
        
        if response.status_code == 201:
            result = response.json()
            self.access_token = result['tokens']['access']
            self.refresh_token = result['tokens']['refresh']
            self.user_data = result['user']
            print("✅ Registration successful!")
            print(f"   User ID: {result['user']['id']}")
            print(f"   Username: {result['user']['username']}")
            print(f"   Email: {result['user']['email']}")
            return True
        else:
            print(f"❌ Registration failed: {response.json()}")
            return False

    def login_user(self, username, password):
        """Login user and get tokens"""
        url = f"{BASE_URL}/api/token/"
        data = {
            "username": username,
            "password": password
        }
        
        print(f"🔑 Logging in user: {username}")
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            self.access_token = result['access']
            self.refresh_token = result['refresh']
            if 'user' in result:
                self.user_data = result['user']
            print("✅ Login successful!")
            print(f"   Access Token: {self.access_token[:50]}...")
            print(f"   Refresh Token: {self.refresh_token[:50]}...")
            return True
        else:
            print(f"❌ Login failed: {response.json()}")
            return False

    def get_user_profile(self):
        """Get user profile using access token"""
        if not self.access_token:
            print("❌ No access token available. Please login first.")
            return False
            
        url = f"{BASE_URL}/api/profile/"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        print("👤 Getting user profile...")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Profile retrieved successfully!")
            print(f"   ID: {result['user']['id']}")
            print(f"   Username: {result['user']['username']}")
            print(f"   Email: {result['user']['email']}")
            print(f"   First Name: {result['user']['first_name']}")
            print(f"   Last Name: {result['user']['last_name']}")
            print(f"   Date Joined: {result['user']['date_joined']}")
            return True
        else:
            print(f"❌ Failed to get profile: {response.json()}")
            return False

    def update_profile(self, email=None, first_name=None, last_name=None):
        """Update user profile"""
        if not self.access_token:
            print("❌ No access token available. Please login first.")
            return False
            
        url = f"{BASE_URL}/api/profile/update/"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        data = {}
        if email:
            data['email'] = email
        if first_name:
            data['first_name'] = first_name
        if last_name:
            data['last_name'] = last_name
            
        if not data:
            print("❌ No data to update")
            return False
        
        print(f"✏️ Updating profile with: {data}")
        response = requests.put(url, json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Profile updated successfully!")
            print(f"   Updated user: {result['user']}")
            return True
        else:
            print(f"❌ Failed to update profile: {response.json()}")
            return False

    def refresh_access_token(self):
        """Refresh the access token using refresh token"""
        if not self.refresh_token:
            print("❌ No refresh token available.")
            return False
            
        url = f"{BASE_URL}/api/token/refresh/"
        data = {
            "refresh": self.refresh_token
        }
        
        print("🔄 Refreshing access token...")
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            old_token = self.access_token[:50] if self.access_token else "None"
            self.access_token = result['access']
            print("✅ Token refreshed successfully!")
            print(f"   Old Token: {old_token}...")
            print(f"   New Token: {self.access_token[:50]}...")
            return True
        else:
            print(f"❌ Failed to refresh token: {response.json()}")
            return False

    def verify_token(self):
        """Verify the current access token"""
        if not self.access_token:
            print("❌ No access token to verify.")
            return False
            
        url = f"{BASE_URL}/api/token/verify/"
        data = {
            "token": self.access_token
        }
        
        print("🔍 Verifying access token...")
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            print("✅ Token is valid!")
            return True
        else:
            print(f"❌ Token verification failed: {response.json()}")
            return False

    def logout_user(self):
        """Logout user and blacklist refresh token"""
        if not self.access_token or not self.refresh_token:
            print("❌ No tokens available for logout.")
            return False
            
        url = f"{BASE_URL}/api/logout/"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "refresh_token": self.refresh_token
        }
        
        print("🚪 Logging out user...")
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            print("✅ Logout successful!")
            self.access_token = None
            self.refresh_token = None
            self.user_data = None
            return True
        else:
            print(f"❌ Logout failed: {response.json()}")
            return False


def main():
    """Main testing function"""
    print("🚀 JWT API Testing Script")
    print("=" * 50)
    
    tester = JWTAPITester()
    
    # Test data
    test_username = "testuser_jwt"
    test_email = "testuser@example.com"
    test_password = "SecurePassword123!"
    
    print("\n1️⃣ Testing User Registration")
    print("-" * 30)
    if tester.register_user(test_username, test_email, test_password, "Test", "User"):
        
        print("\n2️⃣ Testing Get Profile (after registration)")
        print("-" * 30)
        tester.get_user_profile()
        
        print("\n3️⃣ Testing Profile Update")
        print("-" * 30)
        tester.update_profile(email="updated@example.com", first_name="Updated")
        
        print("\n4️⃣ Testing Token Verification")
        print("-" * 30)
        tester.verify_token()
        
        print("\n5️⃣ Testing Token Refresh")
        print("-" * 30)
        tester.refresh_access_token()
        
        print("\n6️⃣ Testing Profile Access with New Token")
        print("-" * 30)
        tester.get_user_profile()
        
        print("\n7️⃣ Testing Logout")
        print("-" * 30)
        tester.logout_user()
        
        print("\n8️⃣ Testing Login with Existing User")
        print("-" * 30)
        if tester.login_user(test_username, test_password):
            print("\n9️⃣ Testing Profile Access After Login")
            print("-" * 30)
            tester.get_user_profile()
    
    print("\n🎉 Testing completed!")
    print("=" * 50)
    print("\n💡 Tip: You can also test the API using the web interface at:")
    print(f"   {BASE_URL}/jwt-demo")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
