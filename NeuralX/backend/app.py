import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
# EMAIL CONFIGURATION
# =========================================================

SMTP_HOST = os.environ.get(
    "SMTP_HOST",
    "smtp.gmail.com"
)

SMTP_PORT = int(
    os.environ.get(
        "SMTP_PORT",
        587
    )
)

SMTP_EMAIL = os.environ.get(
    "SMTP_EMAIL",
    ""
)

SMTP_PASSWORD = os.environ.get(
    "SMTP_PASSWORD",
    ""
)

WHATSAPP_GROUP_LINK = os.environ.get(
    "WHATSAPP_GROUP_LINK",
    "https://chat.whatsapp.com/YOUR_GROUP_LINK"
)


# =========================================================
# EVENT DETAILS
# =========================================================

EVENT_DATE = "24 August 2026"
EVENT_TIME = "8:00 AM"
EVENT_VENUE = "SIMATS ENGINEERING"


# =========================================================
# SEND REGISTRATION EMAIL
# =========================================================

def send_registration_email(
    lead_email,
    lead_name,
    team_name,
    team_code,
    track
):

    if not SMTP_EMAIL or not SMTP_PASSWORD:

        print(
            "Email configuration missing. "
            "Registration saved, but confirmation email was not sent."
        )

        return False

    try:

        message = MIMEMultipart(
            "alternative"
        )

        message["Subject"] = (
            f"NeuralX 2026 - Registration Successful | "
            f"Team {team_code}"
        )

        message["From"] = SMTP_EMAIL

        message["To"] = lead_email


        # -------------------------------------------------
        # PLAIN TEXT EMAIL
        # -------------------------------------------------

        plain_text = f"""
Dear {lead_name},

Congratulations!

Your team has been successfully registered for NeuralX 2026.

TEAM DETAILS
--------------------------------
Team Name : {team_name}
Team Code : {team_code}
Track     : {track}

EVENT DETAILS
--------------------------------
Date      : {EVENT_DATE}
Time      : {EVENT_TIME}
Venue     : {EVENT_VENUE}

IMPORTANT
--------------------------------
Please report to the venue by {EVENT_TIME}
on {EVENT_DATE}.

Please keep your Team Code safe.
Your Team Code will be used for team identification
and event-related communication.

WHATSAPP GROUP
--------------------------------
Join the official NeuralX 2026 WhatsApp group
using the invitation link below:

{WHATSAPP_GROUP_LINK}

We look forward to welcoming your team to
NeuralX 2026.

Regards,

NeuralX 2026 Organizing Team
Department of Medical Electronics
SIMATS ENGINEERING
"""


        # -------------------------------------------------
        # HTML EMAIL
        # -------------------------------------------------

        html_content = f"""
<!DOCTYPE html>

<html>

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>
        NeuralX 2026 Registration
    </title>

</head>

<body style="
    margin: 0;
    padding: 0;
    background-color: #08090d;
    font-family: Arial, Helvetica, sans-serif;
">

    <div style="
        max-width: 650px;
        margin: 30px auto;
        background: #101217;
        border: 1px solid #1f2a32;
        color: #ffffff;
    ">

        <!-- HEADER -->

        <div style="
            padding: 30px;
            text-align: center;
            border-bottom: 1px solid #1f2a32;
        ">

            <h1 style="
                margin: 0;
                font-size: 32px;
                letter-spacing: 4px;
                color: #ffffff;
            ">
                NEURAL<span style="color: #00e5ff;">X</span>
            </h1>

            <p style="
                margin: 10px 0 0;
                color: #00e5ff;
                font-size: 12px;
                letter-spacing: 2px;
                text-transform: uppercase;
            ">
                National Level Hackathon
            </p>

        </div>


        <!-- SUCCESS MESSAGE -->

        <div style="
            padding: 30px;
        ">

            <h2 style="
                margin-top: 0;
                color: #00e5ff;
            ">
                Registration Successful!
            </h2>

            <p style="
                color: #cccccc;
                font-size: 15px;
                line-height: 1.7;
            ">
                Dear {lead_name},
            </p>

            <p style="
                color: #cccccc;
                font-size: 15px;
                line-height: 1.7;
            ">
                Congratulations! Your team has been
                successfully registered for
                <strong style="color: #ffffff;">
                    NeuralX 2026
                </strong>.
            </p>


            <!-- TEAM DETAILS -->

            <div style="
                margin-top: 25px;
                padding: 20px;
                border: 1px solid #24313a;
                background: #0b0e13;
            ">

                <h3 style="
                    margin-top: 0;
                    color: #00e5ff;
                    font-size: 15px;
                    letter-spacing: 1px;
                ">
                    TEAM DETAILS
                </h3>

                <p style="
                    margin: 10px 0;
                    color: #cccccc;
                ">
                    <strong style="color: #ffffff;">
                        Team Name:
                    </strong>
                    {team_name}
                </p>

                <p style="
                    margin: 10px 0;
                    color: #cccccc;
                ">
                    <strong style="color: #ffffff;">
                        Team Code:
                    </strong>

                    <span style="
                        color: #00e5ff;
                        font-size: 20px;
                        font-weight: bold;
                    ">
                        {team_code}
                    </span>
                </p>

                <p style="
                    margin: 10px 0;
                    color: #cccccc;
                ">
                    <strong style="color: #ffffff;">
                        Track:
                    </strong>
                    {track}
                </p>

            </div>


            <!-- EVENT DETAILS -->

            <div style="
                margin-top: 20px;
                padding: 20px;
                border: 1px solid #24313a;
                background: #0b0e13;
            ">

                <h3 style="
                    margin-top: 0;
                    color: #00e5ff;
                    font-size: 15px;
                    letter-spacing: 1px;
                ">
                    EVENT DETAILS
                </h3>

                <p style="
                    margin: 10px 0;
                    color: #cccccc;
                ">
                    <strong style="color: #ffffff;">
                        Date:
                    </strong>
                    24 August 2026
                </p>

                <p style="
                    margin: 10px 0;
                    color: #cccccc;
                ">
                    <strong style="color: #ffffff;">
                        Time:
                    </strong>
                    8:00 AM
                </p>

                <p style="
                    margin: 10px 0;
                    color: #cccccc;
                ">
                    <strong style="color: #ffffff;">
                        Venue:
                    </strong>
                    SIMATS ENGINEERING
                </p>

            </div>


            <!-- IMPORTANT -->

            <div style="
                margin-top: 20px;
                padding: 20px;
                border-left: 3px solid #00e5ff;
                background: #0b0e13;
            ">

                <h3 style="
                    margin-top: 0;
                    color: #ffffff;
                    font-size: 15px;
                ">
                    Important
                </h3>

                <p style="
                    margin-bottom: 0;
                    color: #cccccc;
                    line-height: 1.6;
                ">
                    Please report to the venue by
                    <strong style="color: #ffffff;">
                        8:00 AM
                    </strong>
                    on
                    <strong style="color: #ffffff;">
                        24 August 2026
                    </strong>.
                    Please keep your Team Code
                    <strong style="color: #00e5ff;">
                        {team_code}
                    </strong>
                    safe.
                </p>

            </div>


            <!-- WHATSAPP -->

            <div style="
                margin-top: 25px;
                text-align: center;
                padding: 25px;
                background: #0b0e13;
                border: 1px solid #24313a;
            ">

                <h3 style="
                    margin-top: 0;
                    color: #ffffff;
                ">
                    Join the NeuralX 2026 WhatsApp Group
                </h3>

                <p style="
                    color: #aaaaaa;
                    line-height: 1.6;
                ">
                    Join the official WhatsApp group
                    for important announcements,
                    updates and event communication.
                </p>

                <a href="{WHATSAPP_GROUP_LINK}"
                   style="
                    display: inline-block;
                    margin-top: 10px;
                    padding: 13px 25px;
                    background: #00e5ff;
                    color: #000000;
                    text-decoration: none;
                    font-weight: bold;
                    border-radius: 3px;
                ">
                    JOIN WHATSAPP GROUP
                </a>

            </div>


            <!-- FOOTER MESSAGE -->

            <p style="
                margin-top: 30px;
                color: #aaaaaa;
                line-height: 1.7;
            ">
                We look forward to welcoming your team
                to NeuralX 2026.
            </p>

            <p style="
                color: #ffffff;
                line-height: 1.7;
            ">
                Regards,<br>

                <strong>
                    NeuralX 2026 Organizing Team
                </strong>
                <br>

                <span style="color: #00e5ff;">
                    Department of Medical Electronics
                </span>
                <br>

                SIMATS ENGINEERING
            </p>

        </div>

    </div>

</body>

</html>
"""


        # -------------------------------------------------
        # ATTACH EMAIL CONTENT
        # -------------------------------------------------

        message.attach(
            MIMEText(
                plain_text,
                "plain"
            )
        )

        message.attach(
            MIMEText(
                html_content,
                "html"
            )
        )


        # -------------------------------------------------
        # CONNECT TO SMTP SERVER
        # -------------------------------------------------

        with smtplib.SMTP(
            SMTP_HOST,
            SMTP_PORT
        ) as server:

            server.starttls()

            server.login(
                SMTP_EMAIL,
                SMTP_PASSWORD
            )

            server.sendmail(
                SMTP_EMAIL,
                lead_email,
                message.as_string()
            )


        print(
            f"Registration email sent successfully "
            f"to {lead_email}"
        )

        return True


    except Exception as error:

        print(
            "Email sending error:",
            error
        )

        return False


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
        # COMMIT DATABASE
        # =================================================

        connection.commit()


        # =================================================
        # SEND SUCCESS EMAIL
        # =================================================

        email_sent = send_registration_email(

            lead_email=lead_email,

            lead_name=lead_name,

            team_name=team_name,

            team_code=team_code,

            track=track

        )


        # =================================================
        # SUCCESS RESPONSE
        # =================================================

        if email_sent:

            message = (
                "NeuralX registration successful. "
                "Confirmation email sent successfully."
            )

        else:

            message = (
                "NeuralX registration successful, "
                "but the confirmation email could not be sent. "
                "Please contact the organizers."
            )


        return jsonify({

            "status": "success",

            "message": message,

            "team_id": team_code,

            "team_name": team_name,

            "team_size": team_size,

            "track": track,

            "email_sent": email_sent

        }), 201


    # =====================================================
    # VALUE ERROR
    # =====================================================

    except ValueError as error:

        if connection:

            connection.rollback()


        return jsonify({

            "status": "error",

            "message":
                str(error)

        }), 400


    # =====================================================
    # GENERAL ERROR
    # =====================================================

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