import mysql.connector

class app_DB:
    def connect(self):
        """Makes a connection to the database and returns connection to caller"""
        try:
            print("Connecting to database.")
            # TODO: Verify your connection information
            self.cnx = None
            self.cnx = mysql.connector.connect(user='testuser', password='jnst', host='localhost', port='3307', database='weather_app_DB')
            print("Connected!")
            return self.cnx
        except mysql.connector.Error as err:  
            return False
        
    def close(self):
        try:
            print("Closing database connection.")
            self.cnx.close()
        except mysql.connector.Error as err:  
            print(err)   

    def get_user_info(self, user_id):
        """Fetches user information from the database based on user_id"""
        try:
            cursor = self.cnx.cursor(dictionary=True)  # To get results as a dictionary
            query = "SELECT id, name, email, theme, temperatureUnit, password FROM user WHERE id = %s"
            cursor.execute(query, (user_id,))  # Use parameterized query to avoid SQL injection
            user_info = cursor.fetchone()  # Fetch a single result since we're querying by ID
            
            if user_info:
                return user_info
            else:
                print(f"No user found with ID {user_id}")
                return None

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def get_userid(self, user_name):
        """Fetches user ID from the database based on user_name"""
        try:
            cursor = self.cnx.cursor(dictionary=True)  # To get results as a dictionary
            query = "SELECT id FROM user WHERE name = %s"
            cursor.execute(query, (user_name,))  # Use parameterized query to avoid SQL injection
            user_info = cursor.fetchone()  # Fetch a single result since we're querying by name
            
            if user_info:
                return user_info['id']
            else:
                print(f"No user found with name {user_name}")
                return False

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def add_user(self, user_info):
        """Adds a new user to the database"""

        required_keys = ['name', 'email', 'theme', 'temperatureUnit', 'password']
    
        # check for required keys
        for key in required_keys:
            if key not in user_info:
                print(f"Missing required key: {key}")
                return False
        
        # check for valid data types and non-empty values
        if not isinstance(user_info['name'], str) or not user_info['name']:
            print("Invalid or missing name")
            return False
        if not isinstance(user_info['email'], str) or not user_info['email']:
            print("Invalid or missing email")
            return False
        if not isinstance(user_info['theme'], int):
            print("Invalid or missing theme")
            return False
        if not isinstance(user_info['temperatureUnit'], str) or not user_info['temperatureUnit']:
            print("Invalid or missing temperature unit")
            return False
        if not isinstance(user_info['password'], str) or not user_info['password']:
            print("Invalid or missing password")
            return False

        try:
            cursor = self.cnx.cursor()
            query = "INSERT INTO user (name, email, theme, temperatureUnit, password) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (user_info['name'], user_info['email'], user_info['theme'], user_info['temperatureUnit'], user_info['password']))
            self.cnx.commit()  # Commit the transaction
            print(f"User {user_info['name']} added successfully.")

            # If the user was added successfully, the user id is returned.
            user_id = cursor.lastrowid  # Get the ID of the newly inserted user
            return user_id

        except mysql.connector.Error as err:
            print(f"Invalid user_info provided. Error: {err}")
            return False 

    def delete_user(self, user_id):
        """Deletes a user from the database based on user_id"""
        try:
            cursor = self.cnx.cursor()
            query = "DELETE FROM user WHERE id = %s"
            cursor.execute(query, (user_id,))
            self.cnx.commit()  # Commit the transaction

            if cursor.rowcount > 0:
                print(f"User with ID {user_id} deleted successfully.")
                return user_id
            else:
                print(f"No user found with ID {user_id}")
                return False

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            print("Invalid")
            return False

    def update_user_info(self, user_id, **kwargs):
        """Updates user information in the database based on user_id and provided keyword arguments"""
        if not kwargs:
            print("No information provided to update.")
            return False

        valid_keys = ['name', 'email', 'theme', 'temperatureUnit', 'password']
        update_fields = []
        update_values = []

        for key, value in kwargs.items():
            if key in valid_keys:
                update_fields.append(f"{key} = %s")
                update_values.append(value)
            else:
                print(f"Invalid key: {key}")
                return False

        update_values.append(user_id)
        update_query = f"UPDATE user SET {', '.join(update_fields)} WHERE id = %s"

        try:
            cursor = self.cnx.cursor()
            cursor.execute(update_query, tuple(update_values))
            self.cnx.commit()  # Commit the transaction

            if cursor.rowcount > 0:
                print(f"User with ID {user_id} updated successfully.")
                return True
            else:
                print(f"No user found with ID {user_id}")
                return False

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        
    def get_locationName(self, location_id):
        """Fetches location name from the database based on location_id"""
        try:
            cursor = self.cnx.cursor() 
            query = "SELECT name FROM location WHERE id = %s"
            cursor.execute(query, (location_id,)) 
            location_info = cursor.fetchone() 
            
            if location_info:
                return location_info[0]  
            else:
                print(f"No location found with ID {location_id}")
                return False

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def get_locationID(self, location_name):
        """Fetches location ID from the database based on location_name"""
        try:
            cursor = self.cnx.cursor()  
            query = "SELECT id FROM location WHERE name = %s"
            cursor.execute(query, (location_name,))  
            location_info = cursor.fetchone()  
            
            if location_info:
                return location_info[0]  
            else:
                print(f"No location found with name {location_name}")
                return False

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        
    def add_location(self, location_name): #singleton pattern found here! :D
        """Adds a new location to the database or returns the ID if it already exists"""
        try:
            # Check if the location already exists
            location_id = self.get_locationID(location_name)
            
            if location_id:
                print(f"Location '{location_name}' already exists with ID {location_id}.")
                return location_id
            else:
                # Add the new location
                cursor = self.cnx.cursor()
                query = "INSERT INTO location (name) VALUES (%s)"
                cursor.execute(query, (location_name,))
                self.cnx.commit()  # Commit the transaction
                location_id = cursor.lastrowid  # Get the ID of the newly inserted location
                print(f"Location '{location_name}' added successfully with ID {location_id}.")
                return location_id

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def add_dashboardLocation(self, user_id, location_id):
        """Adds a location to the user's dashboard in the database or returns True if it already exists"""
        try:
            # Check if the location already exists in the user's dashboard
            dashboard_locations = self.get_dashboardLocations(user_id)
            if dashboard_locations:
                for location in dashboard_locations:
                    if location['id'] == location_id:
                        print(f"Location ID {location_id} already exists in user ID {user_id}'s dashboard.")
                        return True
                
            # Add the new location to the dashboard
            cursor = self.cnx.cursor()
            query = "INSERT INTO dashboard_locations (user_id, location_id) VALUES (%s, %s)"
            cursor.execute(query, (user_id, location_id))
            self.cnx.commit()  # Commit the transaction
            print(f"Location ID {location_id} added to user ID {user_id}'s dashboard successfully.")
            return True

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        
    def get_dashboardLocations(self, user_id):
        """Fetches a list of locations from the user's dashboard based on user_id"""
        try:
            cursor = self.cnx.cursor(dictionary=True)
            query = """
                SELECT location.id, location.name 
                FROM dashboard_locations as dashboard
                JOIN location ON dashboard.location_id = location.id 
                WHERE dashboard.user_id = %s
            """
            cursor.execute(query, (user_id,))
            locations = cursor.fetchall()
            
            if locations:
                return locations
            else:
                print(f"No locations found for user ID {user_id}")
                return False

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        
    def delete_dashboardLocation(self, user_id, location_id):
        """Deletes a location from the user's dashboard based on user_id and location_id"""
        try:
            cursor = self.cnx.cursor()
            query = "DELETE FROM dashboard_locations WHERE user_id = %s AND location_id = %s"
            cursor.execute(query, (user_id, location_id))
            self.cnx.commit()

            if cursor.rowcount > 0:
                print(f"Location ID {location_id} deleted from user ID {user_id}'s dashboard successfully.")
                return True
            else:
                print(f"No entry found for user ID {user_id} with location ID {location_id}")
                return False

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        

# This function is just for our team to test the database functions. 
if __name__ == "__main__":
    db = app_DB()
    connection = db.connect()
    
    if connection:
        # Test adding a user
        user_info = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'theme': 1,
            'temperatureUnit': 'C',
            'password': 'securepassword'
        }
        user_id = db.add_user(user_info)
        
        if user_id:
            print(f"User created with ID: {user_id}")
            
            # Test deleting the user
            if not db.delete_user(user_id):
                print(f"Failed to delete user with ID {user_id}.")
        
        db.close()
    print("Done testing database functions.")