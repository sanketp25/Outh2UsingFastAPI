Steps to run:
  1. Create a Folder.
  2. Execute the command `pip3 install -r requirements.txt` to install all dependencies.
  3. Generate your Secret Key using `openssl rand -hex 32`
  4. Execute the command `python3 -m uvicorn main:app --reload`

----------------------------------------------------------
In case you get an error while installing dependencies throught `requirements.txt` file, execute the commands using the following syntax:
`pip3 install 'python-jose[cryptography]' ` i.e. by adding single quotes before each dependency.

--------------------------
Explanation of dependencies:
1. Uvicorn: Creates a webserver for the fastapi
2. python-multipart: This decodes json data, internally used by fastapi.
3. python-jose[cryptography] : Generating JWT tokens
4. passlib[bcrypt] : Used for Password Hashing 

