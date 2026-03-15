import requests
import sys
import json
from datetime import datetime

class RestaurantAPITester:
    def __init__(self, base_url="https://dine-orders-1.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.admin_token = None
        self.staff_token = None
        self.admin_user = None
        self.staff_user = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                if response.text:
                    try:
                        response_data = response.json()
                        self.test_results.append({
                            "test": name,
                            "status": "PASS",
                            "response": response_data
                        })
                        return success, response_data
                    except:
                        self.test_results.append({
                            "test": name,
                            "status": "PASS",
                            "response": response.text
                        })
                        return success, response.text
                else:
                    self.test_results.append({
                        "test": name,
                        "status": "PASS",
                        "response": None
                    })
                    return success, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"Response: {response.text}")
                self.test_results.append({
                    "test": name,
                    "status": "FAIL",
                    "error": f"Expected {expected_status}, got {response.status_code}",
                    "response": response.text
                })

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.test_results.append({
                "test": name,
                "status": "ERROR",
                "error": str(e)
            })
            return False, {}

        return False, {}

    def get_auth_header(self, user_type="admin"):
        """Get authorization header"""
        token = self.admin_token if user_type == "admin" else self.staff_token
        if token:
            return {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
        return {'Content-Type': 'application/json'}

    def test_auth(self):
        """Test authentication endpoints"""
        print("\n=== TESTING AUTHENTICATION ===")
        
        # Test admin login
        success, response = self.run_test(
            "Admin Login",
            "POST",
            "auth/login",
            200,
            data={"username": "admin", "password": "admin123"}
        )
        if success and 'access_token' in response:
            self.admin_token = response['access_token']
            self.admin_user = response['user']
            print(f"Admin login successful, role: {self.admin_user['role']}")
        else:
            print("❌ Admin login failed")
            return False

        # Test staff login
        success, response = self.run_test(
            "Staff Login",
            "POST",
            "auth/login",
            200,
            data={"username": "staff", "password": "staff123"}
        )
        if success and 'access_token' in response:
            self.staff_token = response['access_token']
            self.staff_user = response['user']
            print(f"Staff login successful, role: {self.staff_user['role']}")
        else:
            print("❌ Staff login failed")
            return False

        # Test invalid login
        self.run_test(
            "Invalid Login",
            "POST",
            "auth/login",
            401,
            data={"username": "invalid", "password": "wrong"}
        )

        return True

    def test_tables(self):
        """Test table management"""
        print("\n=== TESTING TABLE MANAGEMENT ===")
        
        # Get all tables (should work for both admin and staff)
        success, tables = self.run_test(
            "Get Tables (Admin)",
            "GET",
            "tables",
            200,
            headers=self.get_auth_header("admin")
        )
        
        if success:
            print(f"Found {len(tables)} tables")
            for table in tables[:3]:  # Show first 3 tables
                print(f"  - {table['table_number']}: {table['status']} (capacity: {table['capacity']})")
        
        # Staff should also be able to get tables
        self.run_test(
            "Get Tables (Staff)",
            "GET",
            "tables",
            200,
            headers=self.get_auth_header("staff")
        )

        # Only admin can create tables
        test_table_data = {
            "table_number": "TEST-T1",
            "capacity": 4
        }
        
        success, new_table = self.run_test(
            "Create Table (Admin)",
            "POST",
            "tables",
            200,
            data=test_table_data,
            headers=self.get_auth_header("admin")
        )
        
        table_id = None
        if success and 'id' in new_table:
            table_id = new_table['id']
            print(f"Created test table with ID: {table_id}")

        # Staff should not be able to create tables
        self.run_test(
            "Create Table (Staff - Should Fail)",
            "POST",
            "tables",
            403,
            data=test_table_data,
            headers=self.get_auth_header("staff")
        )

        # Test update and delete if table was created
        if table_id:
            # Update table
            self.run_test(
                "Update Table",
                "PUT",
                f"tables/{table_id}",
                200,
                data={"table_number": "TEST-T1-UPDATED", "capacity": 6},
                headers=self.get_auth_header("admin")
            )
            
            # Delete table
            self.run_test(
                "Delete Table",
                "DELETE",
                f"tables/{table_id}",
                204,
                headers=self.get_auth_header("admin")
            )

        return True

    def test_menu(self):
        """Test menu management"""
        print("\n=== TESTING MENU MANAGEMENT ===")
        
        # Get menu items
        success, menu_items = self.run_test(
            "Get Menu Items",
            "GET",
            "menu",
            200,
            headers=self.get_auth_header("staff")
        )
        
        if success:
            print(f"Found {len(menu_items)} menu items")
            # Group by category
            categories = {}
            for item in menu_items:
                category = item['category']
                if category not in categories:
                    categories[category] = []
                categories[category].append(item['name'])
            
            for category, items in categories.items():
                print(f"  {category}: {len(items)} items")

        # Search menu
        if menu_items and len(menu_items) > 0:
            first_item_name = menu_items[0]['name']
            search_query = first_item_name[:3]  # First 3 chars
            self.run_test(
                f"Search Menu ('{search_query}')",
                "GET",
                f"menu/search?q={search_query}",
                200,
                headers=self.get_auth_header("staff")
            )

        # Test create menu item (admin only)
        test_menu_item = {
            "name": "Test Burger",
            "category": "Test Category",
            "price": 15.99,
            "description": "A test burger for testing"
        }
        
        success, new_item = self.run_test(
            "Create Menu Item (Admin)",
            "POST",
            "menu",
            200,
            data=test_menu_item,
            headers=self.get_auth_header("admin")
        )
        
        item_id = None
        if success and 'id' in new_item:
            item_id = new_item['id']
            print(f"Created test menu item with ID: {item_id}")

        # Staff should not be able to create menu items
        self.run_test(
            "Create Menu Item (Staff - Should Fail)",
            "POST",
            "menu",
            403,
            data=test_menu_item,
            headers=self.get_auth_header("staff")
        )

        # Test update and delete if item was created
        if item_id:
            # Update menu item
            self.run_test(
                "Update Menu Item",
                "PUT",
                f"menu/{item_id}",
                200,
                data={
                    "name": "Test Burger Updated",
                    "category": "Test Category",
                    "price": 17.99,
                    "description": "An updated test burger"
                },
                headers=self.get_auth_header("admin")
            )
            
            # Delete menu item
            self.run_test(
                "Delete Menu Item",
                "DELETE",
                f"menu/{item_id}",
                204,
                headers=self.get_auth_header("admin")
            )

        return True

    def test_orders(self):
        """Test order management"""
        print("\n=== TESTING ORDER MANAGEMENT ===")
        
        # Get available tables first
        success, tables = self.run_test(
            "Get Tables for Order Test",
            "GET",
            "tables",
            200,
            headers=self.get_auth_header("staff")
        )
        
        if not success or not tables:
            print("❌ No tables available for order testing")
            return False
            
        # Find an available table
        available_table = None
        for table in tables:
            if table['status'] == 'available':
                available_table = table
                break
        
        if not available_table:
            print("❌ No available tables for order testing")
            return False
        
        print(f"Using table {available_table['table_number']} for order testing")
        
        # Create order
        success, new_order = self.run_test(
            "Create Order",
            "POST",
            "orders",
            200,
            data={"table_id": available_table['id']},
            headers=self.get_auth_header("staff")
        )
        
        if not success or 'id' not in new_order:
            print("❌ Failed to create order")
            return False
            
        order_id = new_order['id']
        print(f"Created order with ID: {order_id}")
        
        # Get menu items for adding to order
        success, menu_items = self.run_test(
            "Get Menu for Order",
            "GET",
            "menu",
            200,
            headers=self.get_auth_header("staff")
        )
        
        if success and menu_items:
            # Add menu items to order
            first_item = menu_items[0]
            order_items = [
                {
                    "menu_item_id": first_item['id'],
                    "item_name": first_item['name'],
                    "quantity": 2,
                    "price": first_item['price'],
                    "is_manual": False
                },
                {
                    "menu_item_id": None,
                    "item_name": "Custom Test Item",
                    "quantity": 1,
                    "price": 12.50,
                    "is_manual": True
                }
            ]
            
            self.run_test(
                "Add Items to Order",
                "POST",
                f"orders/{order_id}/items",
                200,
                data={"items": order_items},
                headers=self.get_auth_header("staff")
            )
        
        # Get order details
        self.run_test(
            "Get Order Details",
            "GET",
            f"orders/{order_id}",
            200,
            headers=self.get_auth_header("staff")
        )
        
        # Get all active orders
        self.run_test(
            "Get Active Orders",
            "GET",
            "orders?status=active",
            200,
            headers=self.get_auth_header("staff")
        )
        
        # Acknowledge order (reception functionality)
        self.run_test(
            "Acknowledge Order",
            "POST",
            f"orders/{order_id}/acknowledge",
            200,
            headers=self.get_auth_header("staff")
        )
        
        # Complete order
        success, completed_order = self.run_test(
            "Complete Order",
            "POST",
            f"orders/{order_id}/complete",
            200,
            headers=self.get_auth_header("staff")
        )
        
        if success:
            print(f"Order completed successfully")
        
        return True

    def test_currency_settings(self):
        """Test currency settings endpoints (NEW FEATURE)"""
        print("\n=== TESTING CURRENCY SETTINGS (NEW FEATURE) ===")
        
        # Test GET /api/settings - should work for both admin and staff
        success, original_settings = self.run_test(
            "Get Currency Settings (Admin)",
            "GET",
            "settings",
            200,
            headers=self.get_auth_header("admin")
        )
        
        if success:
            print(f"Current currency: {original_settings.get('currency_symbol', '$')} ({original_settings.get('currency_code', 'USD')})")
        
        # Test GET /api/settings with staff token
        self.run_test(
            "Get Currency Settings (Staff)",
            "GET", 
            "settings",
            200,
            headers=self.get_auth_header("staff")
        )
        
        # Test PUT /api/settings with admin token (should work)
        success, updated_settings = self.run_test(
            "Update Currency Settings (Admin)",
            "PUT",
            "settings", 
            200,
            data={"currency_symbol": "€", "currency_code": "EUR"},
            headers=self.get_auth_header("admin")
        )
        
        if success:
            print(f"Updated currency: {updated_settings.get('currency_symbol', '?')} ({updated_settings.get('currency_code', '?')})")
        
        # Test PUT /api/settings with staff token (should fail with 403)
        self.run_test(
            "Update Currency Settings (Staff - Should Fail)",
            "PUT",
            "settings", 
            403,
            data={"currency_symbol": "£", "currency_code": "GBP"},
            headers=self.get_auth_header("staff")
        )
        
        # Test another currency update
        self.run_test(
            "Update Currency Settings Again (Admin)",
            "PUT", 
            "settings",
            200,
            data={"currency_symbol": "₹", "currency_code": "INR"},
            headers=self.get_auth_header("admin")
        )
        
        # Restore original settings
        if original_settings:
            self.run_test(
                "Restore Original Currency Settings",
                "PUT",
                "settings",
                200,
                data={
                    "currency_symbol": original_settings.get("currency_symbol", "$"),
                    "currency_code": original_settings.get("currency_code", "USD")
                },
                headers=self.get_auth_header("admin")
            )
            print(f"Restored original settings")
        
        return True

    def test_order_cancellation(self):
        """Test order cancellation endpoint (NEW FEATURE)"""
        print("\n=== TESTING ORDER CANCELLATION (NEW FEATURE) ===")
        
        # Get available tables first
        success, tables = self.run_test(
            "Get Tables for Cancellation Test",
            "GET", 
            "tables",
            200,
            headers=self.get_auth_header("staff")
        )
        
        if not success or not tables:
            print("❌ No tables available for cancellation testing")
            return False
            
        # Find an available table
        available_table = None
        for table in tables:
            if table['status'] == 'available':
                available_table = table
                break
        
        if not available_table:
            print("❌ No available tables for cancellation testing")
            return False
        
        print(f"Using table {available_table['table_number']} for cancellation testing")
        
        # Create order for cancellation
        success, new_order = self.run_test(
            "Create Order for Cancellation",
            "POST",
            "orders",
            200, 
            data={"table_id": available_table['id']},
            headers=self.get_auth_header("staff")
        )
        
        if not success or 'id' not in new_order:
            print("❌ Failed to create order for cancellation test")
            return False
            
        order_id = new_order['id']
        print(f"Created order with ID: {order_id} for cancellation test")
        
        # Verify order is in active orders before cancellation
        success, active_orders_before = self.run_test(
            "Get Active Orders Before Cancellation",
            "GET",
            "orders?status=active", 
            200,
            headers=self.get_auth_header("staff")
        )
        
        order_exists_before = any(order.get('id') == order_id for order in active_orders_before) if success else False
        if order_exists_before:
            print(f"✅ Order {order_id} found in active orders before cancellation")
        else:
            print(f"❌ Order {order_id} not found in active orders before cancellation")
        
        # Test DELETE /api/orders/{order_id} endpoint
        success = self.run_test(
            "Cancel Order (DELETE endpoint)",
            "DELETE",
            f"orders/{order_id}",
            204,
            headers=self.get_auth_header("staff")
        )[0]
        
        if success:
            print(f"✅ Order {order_id} cancelled successfully")
        else:
            print(f"❌ Failed to cancel order {order_id}")
            return False
        
        # Verify order is no longer in active orders
        success, active_orders_after = self.run_test(
            "Get Active Orders After Cancellation",
            "GET", 
            "orders?status=active",
            200,
            headers=self.get_auth_header("staff")
        )
        
        if success:
            order_exists_after = any(order.get('id') == order_id for order in active_orders_after)
            if not order_exists_after:
                print(f"✅ Order {order_id} correctly removed from active orders")
            else:
                print(f"❌ Order {order_id} still appears in active orders after cancellation")
        
        # Verify table status changed back to available
        success, updated_tables = self.run_test(
            "Get Tables After Cancellation",
            "GET",
            "tables", 
            200,
            headers=self.get_auth_header("staff")
        )
        
        if success:
            cancelled_table = next((t for t in updated_tables if t['id'] == available_table['id']), None)
            if cancelled_table and cancelled_table['status'] == 'available':
                print(f"✅ Table {cancelled_table['table_number']} status correctly reset to available")
            else:
                print(f"❌ Table status not properly reset after order cancellation")
        
        # Test cancelling non-existent order (should return 404)
        fake_order_id = "non-existent-order-id"
        self.run_test(
            "Cancel Non-Existent Order (Should Fail)",
            "DELETE",
            f"orders/{fake_order_id}",
            404,
            headers=self.get_auth_header("staff")
        )
        
        return True

    def test_users(self):
        print("\n=== TESTING USER MANAGEMENT ===")
        
        # Get users (admin only)
        success, users = self.run_test(
            "Get Users (Admin)",
            "GET",
            "users",
            200,
            headers=self.get_auth_header("admin")
        )
        
        if success:
            print(f"Found {len(users)} users")
            for user in users:
                print(f"  - {user['username']} ({user['role']})")
        
        # Staff should not be able to get users
        self.run_test(
            "Get Users (Staff - Should Fail)",
            "GET",
            "users",
            403,
            headers=self.get_auth_header("staff")
        )
        
        # Create test user
        test_user = {
            "username": f"test_user_{datetime.now().strftime('%H%M%S')}",
            "password": "testpass123",
            "role": "staff"
        }
        
        success, new_user = self.run_test(
            "Create User",
            "POST",
            "auth/register",
            200,
            data=test_user,
            headers=self.get_auth_header("admin")
        )
        
        user_id = None
        if success and 'id' in new_user:
            user_id = new_user['id']
            print(f"Created test user with ID: {user_id}")
            
            # Delete the test user
            self.run_test(
                "Delete Test User",
                "DELETE",
                f"users/{user_id}",
                204,
                headers=self.get_auth_header("admin")
            )
        
        return True

    def run_all_tests(self):
        """Run complete test suite"""
        print("🚀 Starting Restaurant Order Management API Tests")
        print(f"Testing against: {self.base_url}")
        
        try:
            # Test authentication first
            if not self.test_auth():
                print("\n❌ Authentication tests failed - stopping")
                return False
            
            # Test all other endpoints
            self.test_tables()
            self.test_menu()
            self.test_orders()
            self.test_users()
            
            # Test NEW FEATURES
            self.test_currency_settings()
            self.test_order_cancellation()
            
        except Exception as e:
            print(f"\n💥 Test suite crashed: {str(e)}")
            return False
        
        # Print final results
        print(f"\n📊 Test Results: {self.tests_passed}/{self.tests_run} passed")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        # Save detailed results
        with open('/app/backend_test_results.json', 'w') as f:
            json.dump({
                "summary": {
                    "total_tests": self.tests_run,
                    "passed": self.tests_passed,
                    "failed": self.tests_run - self.tests_passed,
                    "success_rate": (self.tests_passed/self.tests_run)*100
                },
                "details": self.test_results
            }, f, indent=2)
        
        return self.tests_passed == self.tests_run

def main():
    tester = RestaurantAPITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())