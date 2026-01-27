#!/usr/bin/env python3
"""
Backend API Testing for J2Systems Landing Page
Tests all contact message endpoints with comprehensive validation
"""

import requests
import json
import uuid
from datetime import datetime
import sys
import os

# Backend URL from frontend .env
BACKEND_URL = "https://solucionesintegra.preview.emergentagent.com/api"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_test_header(test_name):
    print(f"\n{Colors.BLUE}{Colors.BOLD}=== {test_name} ==={Colors.ENDC}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.ENDC}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.ENDC}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.ENDC}")

class ContactAPITester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.created_messages = []  # Track created messages for cleanup
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }

    def log_result(self, test_name, success, message=""):
        if success:
            self.test_results['passed'] += 1
            print_success(f"{test_name}: {message}")
        else:
            self.test_results['failed'] += 1
            self.test_results['errors'].append(f"{test_name}: {message}")
            print_error(f"{test_name}: {message}")

    def test_create_contact_valid_data(self):
        """Test POST /api/contact with valid data including company"""
        print_test_header("Test 1: Create Contact Message - Valid Data with Company")
        
        test_data = {
            "name": "Juan Carlos Pérez",
            "email": "juan.perez@empresa.com",
            "company": "Empresa Tech Solutions",
            "message": "Necesito integración de sistemas para mi empresa. Tenemos un ERP legacy que necesita conectarse con nuevas APIs."
        }
        
        try:
            response = requests.post(f"{self.base_url}/contact", json=test_data)
            
            if response.status_code == 201:
                data = response.json()
                
                # Validate response structure
                required_fields = ['id', 'name', 'email', 'company', 'message', 'created_at', 'read', 'replied']
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_result("Create Contact Valid", False, f"Missing fields in response: {missing_fields}")
                    return None
                
                # Validate data integrity
                if (data['name'] == test_data['name'] and 
                    data['email'] == test_data['email'] and
                    data['company'] == test_data['company'] and
                    data['message'] == test_data['message'] and
                    data['read'] == False and
                    data['replied'] == False):
                    
                    self.created_messages.append(data['id'])
                    self.log_result("Create Contact Valid", True, f"Message created successfully with ID: {data['id']}")
                    return data['id']
                else:
                    self.log_result("Create Contact Valid", False, "Response data doesn't match input data")
                    return None
            else:
                self.log_result("Create Contact Valid", False, f"Expected 201, got {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            self.log_result("Create Contact Valid", False, f"Request failed: {str(e)}")
            return None

    def test_create_contact_without_company(self):
        """Test POST /api/contact without optional company field"""
        print_test_header("Test 2: Create Contact Message - Without Company (Optional Field)")
        
        test_data = {
            "name": "María González",
            "email": "maria.gonzalez@gmail.com",
            "message": "Hola, soy desarrolladora freelance y me interesa conocer más sobre sus servicios de integración."
        }
        
        try:
            response = requests.post(f"{self.base_url}/contact", json=test_data)
            
            if response.status_code == 201:
                data = response.json()
                
                if (data['name'] == test_data['name'] and 
                    data['email'] == test_data['email'] and
                    data['company'] is None and
                    data['message'] == test_data['message']):
                    
                    self.created_messages.append(data['id'])
                    self.log_result("Create Contact No Company", True, f"Message created without company field: {data['id']}")
                    return data['id']
                else:
                    self.log_result("Create Contact No Company", False, "Response data validation failed")
                    return None
            else:
                self.log_result("Create Contact No Company", False, f"Expected 201, got {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            self.log_result("Create Contact No Company", False, f"Request failed: {str(e)}")
            return None

    def test_create_contact_invalid_email(self):
        """Test POST /api/contact with invalid email"""
        print_test_header("Test 3: Create Contact Message - Invalid Email Validation")
        
        test_data = {
            "name": "Test User",
            "email": "invalid-email-format",
            "message": "This should fail due to invalid email"
        }
        
        try:
            response = requests.post(f"{self.base_url}/contact", json=test_data)
            
            if response.status_code == 422:  # Pydantic validation error
                self.log_result("Invalid Email Validation", True, "Correctly rejected invalid email format")
            else:
                self.log_result("Invalid Email Validation", False, f"Expected 422, got {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Invalid Email Validation", False, f"Request failed: {str(e)}")

    def test_create_contact_missing_required_fields(self):
        """Test POST /api/contact with missing required fields"""
        print_test_header("Test 4: Create Contact Message - Missing Required Fields")
        
        # Test missing name
        test_cases = [
            {"email": "test@example.com", "message": "Missing name"},
            {"name": "Test User", "message": "Missing email"},
            {"name": "Test User", "email": "test@example.com"},  # Missing message
            {}  # Missing all fields
        ]
        
        for i, test_data in enumerate(test_cases, 1):
            try:
                response = requests.post(f"{self.base_url}/contact", json=test_data)
                
                if response.status_code == 422:
                    self.log_result(f"Missing Fields Test {i}", True, f"Correctly rejected incomplete data: {list(test_data.keys())}")
                else:
                    self.log_result(f"Missing Fields Test {i}", False, f"Expected 422, got {response.status_code}")
                    
            except Exception as e:
                self.log_result(f"Missing Fields Test {i}", False, f"Request failed: {str(e)}")

    def test_get_all_contacts(self):
        """Test GET /api/contact - List all messages"""
        print_test_header("Test 5: Get All Contact Messages")
        
        try:
            response = requests.get(f"{self.base_url}/contact")
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list):
                    # Check if our created messages are in the list
                    found_messages = 0
                    for message_id in self.created_messages:
                        if any(msg['id'] == message_id for msg in data):
                            found_messages += 1
                    
                    # Verify sorting (should be by created_at descending)
                    if len(data) > 1:
                        dates = [datetime.fromisoformat(msg['created_at'].replace('Z', '+00:00')) for msg in data]
                        is_sorted = all(dates[i] >= dates[i+1] for i in range(len(dates)-1))
                        
                        if is_sorted:
                            self.log_result("Get All Contacts", True, f"Retrieved {len(data)} messages, correctly sorted by date desc, found {found_messages}/{len(self.created_messages)} created messages")
                        else:
                            self.log_result("Get All Contacts", False, "Messages not sorted by created_at descending")
                    else:
                        self.log_result("Get All Contacts", True, f"Retrieved {len(data)} messages, found {found_messages}/{len(self.created_messages)} created messages")
                else:
                    self.log_result("Get All Contacts", False, "Response is not a list")
            else:
                self.log_result("Get All Contacts", False, f"Expected 200, got {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Get All Contacts", False, f"Request failed: {str(e)}")

    def test_get_contact_by_id(self):
        """Test GET /api/contact/{id} - Get specific message"""
        print_test_header("Test 6: Get Contact Message by ID")
        
        if not self.created_messages:
            self.log_result("Get Contact By ID", False, "No created messages to test with")
            return
        
        message_id = self.created_messages[0]
        
        try:
            response = requests.get(f"{self.base_url}/contact/{message_id}")
            
            if response.status_code == 200:
                data = response.json()
                
                if data['id'] == message_id:
                    self.log_result("Get Contact By ID", True, f"Successfully retrieved message: {message_id}")
                else:
                    self.log_result("Get Contact By ID", False, f"ID mismatch: expected {message_id}, got {data['id']}")
            else:
                self.log_result("Get Contact By ID", False, f"Expected 200, got {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Get Contact By ID", False, f"Request failed: {str(e)}")

    def test_get_contact_nonexistent_id(self):
        """Test GET /api/contact/{id} with non-existent ID"""
        print_test_header("Test 7: Get Contact Message - Non-existent ID")
        
        fake_id = str(uuid.uuid4())
        
        try:
            response = requests.get(f"{self.base_url}/contact/{fake_id}")
            
            if response.status_code == 404:
                self.log_result("Get Nonexistent Contact", True, "Correctly returned 404 for non-existent ID")
            else:
                self.log_result("Get Nonexistent Contact", False, f"Expected 404, got {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Get Nonexistent Contact", False, f"Request failed: {str(e)}")

    def test_update_contact_status(self):
        """Test PATCH /api/contact/{id} - Update message status"""
        print_test_header("Test 8: Update Contact Message Status")
        
        if not self.created_messages:
            self.log_result("Update Contact Status", False, "No created messages to test with")
            return
        
        message_id = self.created_messages[0]
        
        # Test updating read status
        try:
            update_data = {"read": True}
            response = requests.patch(f"{self.base_url}/contact/{message_id}", json=update_data)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['read'] == True and data['id'] == message_id:
                    self.log_result("Update Read Status", True, f"Successfully updated read status to True")
                    
                    # Test updating replied status
                    update_data = {"replied": True}
                    response = requests.patch(f"{self.base_url}/contact/{message_id}", json=update_data)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data['replied'] == True and data['read'] == True:
                            self.log_result("Update Replied Status", True, "Successfully updated replied status to True")
                        else:
                            self.log_result("Update Replied Status", False, f"Status update failed: read={data['read']}, replied={data['replied']}")
                    else:
                        self.log_result("Update Replied Status", False, f"Expected 200, got {response.status_code}")
                else:
                    self.log_result("Update Read Status", False, f"Read status update failed: {data}")
            else:
                self.log_result("Update Read Status", False, f"Expected 200, got {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Update Contact Status", False, f"Request failed: {str(e)}")

    def test_update_contact_nonexistent_id(self):
        """Test PATCH /api/contact/{id} with non-existent ID"""
        print_test_header("Test 9: Update Contact Message - Non-existent ID")
        
        fake_id = str(uuid.uuid4())
        update_data = {"read": True}
        
        try:
            response = requests.patch(f"{self.base_url}/contact/{fake_id}", json=update_data)
            
            if response.status_code == 404:
                self.log_result("Update Nonexistent Contact", True, "Correctly returned 404 for non-existent ID")
            else:
                self.log_result("Update Nonexistent Contact", False, f"Expected 404, got {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Update Nonexistent Contact", False, f"Request failed: {str(e)}")

    def test_mongodb_persistence(self):
        """Verify data persistence in MongoDB by checking if created messages persist"""
        print_test_header("Test 10: MongoDB Data Persistence")
        
        if not self.created_messages:
            self.log_result("MongoDB Persistence", False, "No created messages to verify persistence")
            return
        
        # Wait a moment and then fetch all messages to verify persistence
        import time
        time.sleep(1)
        
        try:
            response = requests.get(f"{self.base_url}/contact")
            
            if response.status_code == 200:
                all_messages = response.json()
                persisted_count = 0
                
                for message_id in self.created_messages:
                    if any(msg['id'] == message_id for msg in all_messages):
                        persisted_count += 1
                
                if persisted_count == len(self.created_messages):
                    self.log_result("MongoDB Persistence", True, f"All {persisted_count} created messages persisted in MongoDB")
                else:
                    self.log_result("MongoDB Persistence", False, f"Only {persisted_count}/{len(self.created_messages)} messages persisted")
            else:
                self.log_result("MongoDB Persistence", False, f"Failed to fetch messages for persistence check: {response.status_code}")
                
        except Exception as e:
            self.log_result("MongoDB Persistence", False, f"Persistence check failed: {str(e)}")

    def run_all_tests(self):
        """Run all contact API tests"""
        print(f"{Colors.BOLD}{Colors.BLUE}")
        print("=" * 60)
        print("  J2SYSTEMS BACKEND API TESTING")
        print("  Contact Message Endpoints")
        print("=" * 60)
        print(f"{Colors.ENDC}")
        
        print_info(f"Testing backend at: {self.base_url}")
        
        # Run all tests in sequence
        self.test_create_contact_valid_data()
        self.test_create_contact_without_company()
        self.test_create_contact_invalid_email()
        self.test_create_contact_missing_required_fields()
        self.test_get_all_contacts()
        self.test_get_contact_by_id()
        self.test_get_contact_nonexistent_id()
        self.test_update_contact_status()
        self.test_update_contact_nonexistent_id()
        self.test_mongodb_persistence()
        
        # Print final results
        self.print_final_results()

    def print_final_results(self):
        """Print comprehensive test results"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}")
        print("=" * 60)
        print("  FINAL TEST RESULTS")
        print("=" * 60)
        print(f"{Colors.ENDC}")
        
        total_tests = self.test_results['passed'] + self.test_results['failed']
        success_rate = (self.test_results['passed'] / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print_success(f"Passed: {self.test_results['passed']}")
        
        if self.test_results['failed'] > 0:
            print_error(f"Failed: {self.test_results['failed']}")
            print(f"\n{Colors.RED}{Colors.BOLD}FAILED TESTS:{Colors.ENDC}")
            for error in self.test_results['errors']:
                print_error(f"  • {error}")
        
        print(f"\n{Colors.BOLD}Success Rate: {success_rate:.1f}%{Colors.ENDC}")
        
        if self.test_results['failed'] == 0:
            print_success("🎉 ALL TESTS PASSED! Backend API is working correctly.")
        else:
            print_error("❌ Some tests failed. Please check the errors above.")
        
        print(f"\n{Colors.BLUE}Created Messages for Testing: {len(self.created_messages)}{Colors.ENDC}")
        for msg_id in self.created_messages:
            print(f"  • {msg_id}")

if __name__ == "__main__":
    tester = ContactAPITester()
    tester.run_all_tests()