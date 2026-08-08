import os

import mysql.connector


def get_db_connection():

    connection = mysql.connector.connect(

        host=os.environ.get(
            "MYSQLHOST",
            "localhost"
        ),

        port=int(
            os.environ.get(
                "MYSQLPORT",
                4306
            )
        ),

        user=os.environ.get(
            "MYSQLUSER",
            "root"
        ),

        password=os.environ.get(
            "MYSQLPASSWORD",
            ""
        ),

        database=os.environ.get(
            "MYSQLDATABASE",
            "neuralx"
        )

    )

    return connection