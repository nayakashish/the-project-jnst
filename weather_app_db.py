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


print(f"STARTUP...")
appDB = app_DB()
appDB.connect()
appDB.close()