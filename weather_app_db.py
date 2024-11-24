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
            print(err)     
            exit(1)  
        
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
            query = "SELECT id, name, email, theme, temperatureUnit FROM user WHERE id = %s"
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
        return False

    def get_locationID(self, location_name):
        return False
        
    def add_location(self, location_name): 
        return False
