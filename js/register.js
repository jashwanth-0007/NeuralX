const registrationForm =
    document.getElementById("registrationForm");

const teamSizeSelect =
    document.getElementById("teamSize");

const membersContainer =
    document.getElementById("membersContainer");

const formMessage =
    document.getElementById("formMessage");


/* =========================================================
   TEAM SIZE CHANGE
   ========================================================= */

teamSizeSelect.addEventListener(
    "change",
    generateMemberFields
);


/* =========================================================
   GENERATE MEMBER FIELDS
   ========================================================= */

function generateMemberFields() {

    const teamSize =
        parseInt(teamSizeSelect.value);

    membersContainer.innerHTML = "";

    if (!teamSize) {
        return;
    }

    /*
        Team lead is already counted.

        Team size 2
        = Lead + Member 2

        Team size 3
        = Lead + Member 2 + Member 3

        Team size 4
        = Lead + Member 2 + Member 3 + Member 4
    */

    const numberOfMembers =
        teamSize - 1;

    for (
        let i = 2;
        i <= teamSize;
        i++
    ) {

        createMemberCard(i);

    }

}


/* =========================================================
   CREATE MEMBER CARD
   ========================================================= */

function createMemberCard(memberNumber) {

    const memberCard =
        document.createElement("div");

    memberCard.className =
        "member-card";

    memberCard.innerHTML = `

        <div class="member-header">

            <div class="member-number">
                MEMBER ${String(memberNumber).padStart(2, "0")}
            </div>

            <span>
                TEAM MEMBER
            </span>

        </div>


        <div class="form-grid">


            <!-- NAME -->

            <div class="form-group">

                <label>
                    Full Name
                </label>

                <input
                    type="text"
                    name="memberName[]"
                    placeholder="Enter full name"
                    required
                >

            </div>


            <!-- REGISTRATION NUMBER -->

            <div class="form-group">

                <label>
                    Registration Number
                </label>

                <input
                    type="text"
                    name="memberRegNo[]"
                    placeholder="Enter registration number"
                    required
                >

            </div>


            <!-- EMAIL -->

            <div class="form-group">

                <label>
                    Email Address
                </label>

                <input
                    type="email"
                    name="memberEmail[]"
                    placeholder="Enter email address"
                    required
                >

            </div>


            <!-- COLLEGE -->

            <div class="form-group">

                <label>
                    College / Institution
                </label>

                <input
                    type="text"
                    name="memberCollege[]"
                    placeholder="Enter college or institution"
                    required
                >

            </div>


            <!-- COURSE -->

            <div class="form-group full-width">

                <label>
                    Degree / Course
                </label>

                <input
                    type="text"
                    name="memberCourse[]"
                    placeholder="Example: B.Tech CSE"
                    required
                >

            </div>


        </div>

    `;

    membersContainer.appendChild(
        memberCard
    );

}


/* =========================================================
   FORM SUBMISSION
   ========================================================= */

registrationForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        showMessage(
            "Submitting your registration...",
            "loading"
        );


        try {


            /* =================================================
               TEAM INFORMATION
               ================================================= */

            const teamName =
                document
                    .getElementById("teamName")
                    .value
                    .trim();


            const teamSize =
                document
                    .getElementById("teamSize")
                    .value;


            const track =
                document
                    .getElementById("track")
                    .value;


            /* =================================================
               TEAM LEAD
               ================================================= */

            const leadName =
                document
                    .getElementById("leadName")
                    .value
                    .trim();


            const leadEmail =
                document
                    .getElementById("leadEmail")
                    .value
                    .trim();


            const leadPhone =
                document
                    .getElementById("leadPhone")
                    .value
                    .trim();


            const college =
                document
                    .getElementById("college")
                    .value
                    .trim();


            const regNo =
                document
                    .getElementById("regNo")
                    .value
                    .trim();


            const degree =
                document
                    .getElementById("degree")
                    .value
                    .trim();


            /* =================================================
               TEAM MEMBERS
               ================================================= */

            const memberCards =
                document.querySelectorAll(
                    ".member-card"
                );


            const members = [];


            memberCards.forEach(
                function (card) {

                    const name =
                        card
                            .querySelector(
                                'input[name="memberName[]"]'
                            )
                            .value
                            .trim();


                    const email =
                        card
                            .querySelector(
                                'input[name="memberEmail[]"]'
                            )
                            .value
                            .trim();


                    const memberRegNo =
                        card
                            .querySelector(
                                'input[name="memberRegNo[]"]'
                            )
                            .value
                            .trim();


                    const memberCollege =
                        card
                            .querySelector(
                                'input[name="memberCollege[]"]'
                            )
                            .value
                            .trim();


                    const course =
                        card
                            .querySelector(
                                'input[name="memberCourse[]"]'
                            )
                            .value
                            .trim();


                    members.push({

                        name: name,

                        email: email,

                        regNo: memberRegNo,

                        college: memberCollege,

                        course: course

                    });

                }
            );


            /* =================================================
               VALIDATE MEMBER COUNT
               ================================================= */

            const expectedMembers =
                parseInt(teamSize) - 1;


            if (
                members.length !==
                expectedMembers
            ) {

                showMessage(
                    "Please enter details for all team members.",
                    "error"
                );

                return;

            }


            /* =================================================
               DATA
               ================================================= */

            const registrationData = {

                teamName: teamName,

                teamSize: teamSize,

                track: track,

                leadName: leadName,

                leadEmail: leadEmail,

                leadPhone: leadPhone,

                college: college,

                regNo: regNo,

                degree: degree,

                members: members

            };


            console.log(
                "Registration Data:",
                registrationData
            );


            /* =================================================
               SEND TO FLASK
               ================================================= */

            const response =
                await fetch(
                    "/register",
                    {

                        method: "POST",

                        headers: {

                            "Content-Type":
                                "application/json"

                        },

                        body:
                            JSON.stringify(
                                registrationData
                            )

                    }
                );


            const result =
                await response.json();


            /* =================================================
               SUCCESS
               ================================================= */

            if (response.ok) {

                /*
                    Store registration details temporarily
                    so success.html can display them.
                */

                const successData = {

                    teamName:
                        teamName,

                    teamId:
                        result.team_id,

                    track:
                        track,

                    teamSize:
                        teamSize,

                    leadName:
                        leadName

                };


                sessionStorage.setItem(
                    "neuralXRegistration",
                    JSON.stringify(successData)
                );


                /*
                    Redirect to separate success page.
                */

                window.location.href =
                    "/pages/success.html";


                return;

            }


            /* =================================================
               ERROR
               ================================================= */

            else {

                showMessage(
                    result.message ||
                    "Registration failed.",
                    "error"
                );

            }


        }

        catch (error) {

            console.error(
                "Registration Error:",
                error
            );


            showMessage(
                "Unable to connect to the NeuralX server. Please make sure Flask is running.",
                "error"
            );

        }

    }
);


/* =========================================================
   MESSAGE
   ========================================================= */

function showMessage(
    message,
    type
) {

    formMessage.textContent =
        message;


    formMessage.className =
        "form-message";


    if (type === "success") {

        formMessage.classList.add(
            "success"
        );

    }


    else if (type === "error") {

        formMessage.classList.add(
            "error"
        );

    }


    else {

        formMessage.classList.add(
            "loading"
        );

    }

}