import os

from flask import (
    Flask,
    request,
    jsonify,
    send_from_directory
)

from flask_cors import CORS

from config import get_db_connection


# =========================================================
# PATH CONFIGURATION
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)

CORS(app)


# =========================================================
# SERVE NEURALX FRONTEND
# =========================================================

@app.route("/")
def home():

    return send_from_directory(
        BASE_DIR,
        "index.html"
    )


@app.route("/<path:filename>")
def serve_frontend(filename):

    file_path = os.path.join(
        BASE_DIR,
        filename
    )

    if os.path.isfile(file_path):

        directory = os.path.dirname(
            file_path
        )

        file_name = os.path.basename(
            file_path
        )

        return send_from_directory(
            directory,
            file_name
        )

    return jsonify({
        "error": "File not found"
    }), 404


# =========================================================
# DATABASE TEST
# =========================================================

@app.route("/test-db")
def test_database():

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor()

        cursor.execute(
            "SELECT DATABASE()"
        )

        result = cursor.fetchone()

        return jsonify({

            "status": "success",

            "database": result[0]

        })

    except Exception as error:

        return jsonify({

            "status": "error",

            "message": str(error)

        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# =========================================================
# GENERATE TEAM CODE
# =========================================================

def generate_team_code(
    cursor,
    track
):

    # -----------------------------------------------------
    # TRACK PREFIX
    # -----------------------------------------------------

    prefixes = {

        "AI": "AI",

        "Full Stack": "FS",

        "Cybersecurity": "CS"

    }


    prefix = prefixes.get(track)


    if not prefix:

        raise ValueError(
            "Invalid track selected."
        )


    # -----------------------------------------------------
    # FIND LAST TEAM NUMBER
    # -----------------------------------------------------

    cursor.execute(

        """
        SELECT team_code
        FROM teams
        WHERE team_code LIKE %s
        ORDER BY id DESC
        LIMIT 1
        """,

        (prefix + "%",)

    )


    result = cursor.fetchone()


    # -----------------------------------------------------
    # FIRST TEAM IN THIS TRACK
    # -----------------------------------------------------

    if not result:

        next_number = 1


    else:

        last_team_code = result[0]


        try:

            last_number = int(
                last_team_code[len(prefix):]
            )

            next_number = last_number + 1

        except (ValueError, TypeError):

            next_number = 1


    # -----------------------------------------------------
    # CREATE TEAM CODE
    # -----------------------------------------------------

    team_code = (

        prefix +

        str(next_number).zfill(2)

    )


    # -----------------------------------------------------
    # SAFETY CHECK
    # -----------------------------------------------------

    while True:

        cursor.execute(

            """
            SELECT id
            FROM teams
            WHERE team_code = %s
            """,

            (team_code,)

        )


        existing = cursor.fetchone()


        if not existing:

            break


        next_number += 1


        team_code = (

            prefix +

            str(next_number).zfill(2)

        )


    return team_code


# =========================================================
# TEAM REGISTRATION
# =========================================================

@app.route(
    "/register",
    methods=["POST"]
)
def register_team():

    connection = None
    cursor = None

    try:

        # =================================================
        # GET JSON DATA
        # =================================================

        data = request.get_json()


        if not data:

            return jsonify({

                "status": "error",

                "message":
                    "No registration data received."

            }), 400


        # =================================================
        # TEAM INFORMATION
        # =================================================

        team_name = data.get(
            "teamName",
            ""
        ).strip()


        team_size = data.get(
            "teamSize"
        )


        track = data.get(
            "track",
            ""
        ).strip()


        # =================================================
        # TEAM LEAD INFORMATION
        # =================================================

        lead_name = data.get(
            "leadName",
            ""
        ).strip()


        lead_email = data.get(
            "leadEmail",
            ""
        ).strip()


        lead_phone = data.get(
            "leadPhone",
            ""
        ).strip()


        college = data.get(
            "college",
            ""
        ).strip()


        lead_reg_no = data.get(
            "regNo",
            ""
        ).strip()


        degree = data.get(
            "degree",
            ""
        ).strip()


        # =================================================
        # TEAM MEMBERS
        # =================================================

        members = data.get(
            "members",
            []
        )


        # =================================================
        # BASIC VALIDATION
        # =================================================

        required_fields = [

            team_name,
            team_size,
            track,

            lead_name,
            lead_email,
            lead_phone,

            college,
            lead_reg_no,
            degree

        ]


        if not all(required_fields):

            return jsonify({

                "status": "error",

                "message":
                    "Please fill all required fields."

            }), 400


        # =================================================
        # TEAM SIZE
        # =================================================

        try:

            team_size = int(team_size)

        except (TypeError, ValueError):

            return jsonify({

                "status": "error",

                "message":
                    "Invalid team size."

            }), 400


        if team_size not in [2, 3, 4]:

            return jsonify({

                "status": "error",

                "message":
                    "Team size must be 2, 3, or 4."

            }), 400


        # =================================================
        # TRACK VALIDATION
        # =================================================

        allowed_tracks = [

            "AI",

            "Full Stack",

            "Cybersecurity"

        ]


        if track not in allowed_tracks:

            return jsonify({

                "status": "error",

                "message":
                    "Invalid track selected."

            }), 400


        # =================================================
        # MEMBER COUNT
        # =================================================

        expected_members = team_size - 1


        if len(members) != expected_members:

            return jsonify({

                "status": "error",

                "message":
                    f"Team size is {team_size}. "
                    f"Please provide details for "
                    f"{expected_members} team member(s)."

            }), 400


        # =================================================
        # DATABASE CONNECTION
        # =================================================

        connection = get_db_connection()

        cursor = connection.cursor()


        # =================================================
        # DUPLICATE TEAM NAME
        # =================================================

        cursor.execute(

            """
            SELECT id
            FROM teams
            WHERE team_name = %s
            """,

            (team_name,)

        )


        existing_team = cursor.fetchone()


        if existing_team:

            return jsonify({

                "status": "error",

                "message":
                    "Team name already exists."

            }), 409


        # =================================================
        # DUPLICATE TEAM LEAD EMAIL
        # =================================================

        cursor.execute(

            """
            SELECT id
            FROM teams
            WHERE lead_email = %s
            """,

            (lead_email,)

        )


        existing_email = cursor.fetchone()


        if existing_email:

            return jsonify({

                "status": "error",

                "message":
                    "This team lead email is already registered."

            }), 409


        # =================================================
        # GENERATE TEAM CODE
        # =================================================

        team_code = generate_team_code(
            cursor,
            track
        )


        # =================================================
        # INSERT TEAM
        # =================================================

        team_query = """

            INSERT INTO teams
            (
                team_code,
                team_name,
                team_size,
                track,
                lead_name,
                lead_email,
                lead_phone,
                college,
                lead_reg_no,
                degree
            )

            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )

        """


        team_values = (

            team_code,

            team_name,

            team_size,

            track,

            lead_name,

            lead_email,

            lead_phone,

            college,

            lead_reg_no,

            degree

        )


        cursor.execute(

            team_query,

            team_values

        )


        team_id = cursor.lastrowid


        # =================================================
        # INSERT TEAM MEMBERS
        # =================================================

        member_query = """

            INSERT INTO team_members
            (
                team_id,
                member_name,
                member_email,
                member_college,
                member_reg_no,
                member_course
            )

            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )

        """


        for member in members:


            member_name = member.get(
                "name",
                ""
            ).strip()


            member_email = member.get(
                "email",
                ""
            ).strip()


            member_college = member.get(
                "college",
                ""
            ).strip()


            member_reg_no = member.get(
                "regNo",
                ""
            ).strip()


            member_course = member.get(
                "course",
                ""
            ).strip()


            if not all([

                member_name,

                member_email,

                member_college,

                member_reg_no,

                member_course

            ]):

                connection.rollback()

                return jsonify({

                    "status": "error",

                    "message":
                        "Please fill all team member details."

                }), 400


            cursor.execute(

                member_query,

                (

                    team_id,

                    member_name,

                    member_email,

                    member_college,

                    member_reg_no,

                    member_course

                )

            )


        # =================================================
        # COMMIT
        # =================================================

        connection.commit()


        # =================================================
        # SUCCESS
        # =================================================

        return jsonify({

            "status": "success",

            "message":
                "NeuralX registration successful.",

            "team_id":
                team_code,

            "team_name":
                team_name,

            "team_size":
                team_size,

            "track":
                track

        }), 201


    # =====================================================
    # ERROR
    # =====================================================

    except ValueError as error:

        if connection:

            connection.rollback()


        return jsonify({

            "status": "error",

            "message":
                str(error)

        }), 400


    except Exception as error:

        if connection:

            connection.rollback()


        print(
            "Registration Error:",
            error
        )


        return jsonify({

            "status": "error",

            "message":
                str(error)

        }), 500


    finally:

        if cursor:

            cursor.close()


        if connection:

            connection.close()


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )