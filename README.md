How to run the project :

Prerequisites
Make sure the following are installed on your system:

Python 3.10+

pip (Python package manager)

MongoDB (running locally on default port 27017)

Clone the Repository
git clone https://github.com/Rohanwagh5/BackendInternAssignment-The-Wedding-Company

Create Virtual Environment
python -m venv venv

Activate it:

Windows:
venv\Scripts\activate

macOS / Linux:
source venv/bin/activate

Install Dependencies
pip install -r requirements.txt

Configure Environment Variables
Create a .env file in the project root and add:

MONGO_URI=MONGO_URI=mongodb+srv://rohanwagh52005:6iIDo7fC20778zWL@cluster0.c70xh.mongodb.net/Organisation_DB

MASTER_DB=Organisation_DB
JWT_SECRET_KEY=secret123
JWT_EXPIRES_SECONDS=3600

(Sharing ENV only because assignment requires database testing access.)

Run the Application
python run.py

After running, the backend will be available at:
http://localhost:5000

API Reference :

Create Organization
POST /org/create
Request Headers: Content-Type: application/json
Request Body Example:
{
"organization_name": "Google",
"email": "google@email.com
",
"password": "Admin123"
}

Admin Login (Get JWT Access Token)
POST /admin/login
Request Body:
{
"email": "google@email.com
",
"password": "Admin123"
}
Response returns: access_token
This token is required for protected endpoints (e.g., delete organization).

Get Organization Metadata
GET /org/get?organization_name=<name>
Example:
http://localhost:5000/org/get?organization_name=Google

Update Organization (Rename and/or Update Admin Details)
PUT /org/update
Required: organization_name (current org name)
Optional: new_organization_name (rename), email (admin update), password (admin update)

Request Body Example (rename):
{
"organization_name": "Google",
"new_organization_name": "Google India"
}

Delete Organization (Admin Only - JWT Protected)
DELETE /org/delete
Headers Required:
Content-Type: application/json
Authorization: Bearer <access_token>

Request Body:
{
"organization_name": "Google India"
}

Testing the APIs

You can test the APIs using:

1.Postman

2. Swagger UI (recommended) :
Swagger UI URL:
http://localhost:5000/docs

Swagger UI Usage Steps:

Start the backend locally.

Open http://localhost:5000/docs
 in your browser.

Expand any API endpoint to test it.

For protected (JWT) endpoints:
a. First call POST /admin/login
b. Copy the returned access_token
c. Click the "Authorize" button in Swagger UI
d. Paste the token in Bearer format
e. Now you can execute DELETE /org/delete and other protected routes successfully.

Note:
All organization-related data, including dynamic collections (org_<slug>), can be viewed in the MongoDB database configured through the .env file.
