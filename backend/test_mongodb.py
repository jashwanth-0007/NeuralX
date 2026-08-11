from config import client, db


try:
    client.admin.command("ping")

    print("MongoDB connection successful!")

    print("Database:", db.name)

    print("Collections:", db.list_collection_names())

except Exception as e:

    print("MongoDB connection failed!")

    print(e)