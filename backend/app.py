import os

from flask import (
    Flask,
    request,
    jsonify,
    send_from_directory
)

from flask_cors import CORS

from config import (
    client,
    db,
    teams_collection,
    members_collection
)


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

    try:

        # Test connection with MongoDB Atlas
        client.admin.command("ping")

        # Get database information
        database_name = db.name

        # Get collection names
        collections = db.list_collection_names()

        return jsonify({

            "status": "success",

            "message": "MongoDB connection successful.",

            "database": database_name,

            "collections": collections

        })

    except Exception as error:

        print(
            "Database Error:",
            error
        )

        return jsonify({

            "status": "error",

            "message": str(error)

        }), 500


# =========================================================
# GENERATE TEAM CODE
# =========================================================

def generate_team_code(track):

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
    # FIND EXISTING TEAM CODES
    # -----------------------------------------------------

    existing_codes = teams_collection.find(
        {
            "team_code": {
                "$regex": f"^{prefix}[0-9]+$"
            }
        },
        {
            "team_code": 1
        }
    )


    # -----------------------------------------------------
    # FIND HIGHEST NUMBER
    # -----------------------------------------------------

    highest_number = 0

    for team in existing_codes:

        code = team.get(
            "team_code",
            ""
        )

        try:

            number = int(
                code[len(prefix):]
            )

            if number > highest_number:

                highest_number = number

        except (ValueError, TypeError):

            continue


    # -----------------------------------------------------
    # GENERATE NEXT NUMBER
    # -----------------------------------------------------

    next_number = highest_number + 1

    team_code = (
        prefix +
        str(next_number).zfill(2)
    )


    # -----------------------------------------------------
    # SAFETY CHECK
    # -----------------------------------------------------

    while teams_collection.find_one(
        {
            "team_code": team_code
        }
    ):

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

            team_size = int(
                team_size
            )

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


        if not isinstance(
            members,
            list
        ):

            return jsonify({

                "status": "error",

                "message":
                    "Invalid team member data."

            }), 400


        if len(members) != expected_members:

            return jsonify({

                "status": "error",

                "message":
                    f"Team size is {team_size}. "
                    f"Please provide details for "
                    f"{expected_members} team member(s)."

            }), 400


        # =================================================
        # DUPLICATE TEAM NAME
        # =================================================

        existing_team = teams_collection.find_one(
            {
                "team_name": team_name
            }
        )


        if existing_team:

            return jsonify({

                "status": "error",

                "message":
                    "Team name already exists."

            }), 409


        # =================================================
        # DUPLICATE TEAM LEAD EMAIL
        # =================================================

        existing_email = teams_collection.find_one(
            {
                "lead_email": lead_email
            }
        )


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
            track
        )


        # =================================================
        # PREPARE TEAM DOCUMENT
        # =================================================

        team_document = {

            "team_code": team_code,

            "team_name": team_name,

            "team_size": team_size,

            "track": track,

            "lead_name": lead_name,

            "lead_email": lead_email,

            "lead_phone": lead_phone,

            "college": college,

            "lead_reg_no": lead_reg_no,

            "degree": degree

        }


        # =================================================
        # INSERT TEAM
        # =================================================

        team_result = teams_collection.insert_one(
            team_document
        )


        team_id = team_result.inserted_id


        # =================================================
        # INSERT TEAM MEMBERS
        # =================================================

        member_documents = []


        for member_index, member in enumerate(
            members,
            start=2
        ):

            # ---------------------------------------------
            # MEMBER NAME
            # ---------------------------------------------

            member_name = member.get(
                "name",
                ""
            ).strip()


            # ---------------------------------------------
            # MEMBER EMAIL
            # ---------------------------------------------

            member_email = member.get(
                "email",
                ""
            ).strip()


            # ---------------------------------------------
            # MEMBER COLLEGE
            # ---------------------------------------------

            member_college = member.get(
                "college",
                ""
            ).strip()


            # ---------------------------------------------
            # MEMBER REGISTRATION NUMBER
            # ---------------------------------------------

            member_reg_no = member.get(
                "regNo",
                ""
            ).strip()


            # ---------------------------------------------
            # MEMBER COURSE
            # ---------------------------------------------

            member_course = member.get(
                "course",
                ""
            ).strip()


            # ---------------------------------------------
            # VALIDATE MEMBER
            # ---------------------------------------------

            if not all([

                member_name,

                member_email,

                member_college,

                member_reg_no,

                member_course

            ]):

                # Remove the team if member
                # validation fails

                teams_collection.delete_one(
                    {
                        "_id": team_id
                    }
                )

                return jsonify({

                    "status": "error",

                    "message":
                        f"Please fill all details "
                        f"for team member {member_index}."

                }), 400


            # ---------------------------------------------
            # CHECK DUPLICATE MEMBER EMAIL
            # ---------------------------------------------

            existing_member = members_collection.find_one(
                {
                    "member_email": member_email
                }
            )


            if existing_member:

                teams_collection.delete_one(
                    {
                        "_id": team_id
                    }
                )

                return jsonify({

                    "status": "error",

                    "message":
                        f"Email {member_email} "
                        f"is already registered."

                }), 409


            # ---------------------------------------------
            # CREATE MEMBER DOCUMENT
            # ---------------------------------------------

            member_document = {

                "team_id": team_id,

                "team_code": team_code,

                "member_number": member_index,

                "member_name": member_name,

                "member_email": member_email,

                "member_college": member_college,

                "member_reg_no": member_reg_no,

                "member_course": member_course

            }


            member_documents.append(
                member_document
            )


        # =================================================
        # INSERT ALL MEMBERS
        # =================================================

        if member_documents:

            members_collection.insert_many(
                member_documents
            )


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
    # VALUE ERROR
    # =====================================================

    except ValueError as error:

        print(
            "Validation Error:",
            error
        )

        return jsonify({

            "status": "error",

            "message":
                str(error)

        }), 400


    # =====================================================
    # GENERAL ERROR
    # =====================================================

    except Exception as error:

        print(
            "Registration Error:",
            error
        )

        return jsonify({

            "status": "error",

            "message":
                str(error)

        }), 500


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