Steps to run:
  1. Create a Folder.
  2. Execute the command `pip3 install -r requirements.txt` to install all dependencies.
  3. Generate your Secret Key using `openssl rand -hex 32`
  4. Execute the command `python3 -m uvicorn main:app --reload`

----------------------------------------------------------
In case you get an error while installing dependencies throught `requirements.txt` file, execute the commands using the following syntax:
`pip3 install 'python-jose[cryptography]' ` i.e. by adding single quotes before each dependency.

--------------------------

System Design:

Overview:

The Lead Management Application is a back-end system built with FastAPI that allows prospects to submit their information through a public form. The system then processes the submission by storing the data in a database and sending confirmation emails to both the prospect and an internal attorney. The application also includes an internal API for authenticated users to manage leads, including changing their state from PENDING to REACHED_OUT.

Features:

  1. Public Lead Submission Form
    1. Allows prospects to submit their details, including first name, last name, email, and resume.
    2. Allows registered users to manually update state for prospects

  2. Authentication and Authorization
    1. Provides token-based authentication using JWT for internal users.
    2. Ensures that internal UI access is restricted to authenticated users.

Technology Stack:
  1. Backend: FastAPI
  2. Database: SQLAlchemy with SQLite
  3. Authentication: OAuth2 with JWT
  3. Email: FastAPI-Mail 

Files:
  1. Models - Consists of the Lead class and LeadClass state. 
  2. Database - Consists of database name and the connection string to connect to Database. 
  3. Auth - Consists the router, token generation logic and P.OST method
  4. main - Entry Point, consists the GET, PUT end points.

Security Considerations

  1. Environment Variables: Use a .env file to store sensitive information and ensure it is included in .gitignore.
  2. Authentication: Protect internal endpoints using OAuth2 with JWT.
  3. Password Storage: Store passwords securely using hashing (e.g., bcrypt).  

Future Enhancements:
  1. Create UI based on JS framework
  2. Implement the send Mail functionality.
   
