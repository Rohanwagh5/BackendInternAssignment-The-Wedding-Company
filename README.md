API Reference : 
endpoints 
1.Create Organization
POST /org/create
example request body :
Request headers : Content-Type: application/json

{
  "organization_name": "Google",
  "email": "google@email.com",
  "password": "Admin123"
}

2.Admin login(get jwt) : 
POST /admin/login
Logs admin in and returns access_token (JWT)

Body
{
  "email":"google@email.com",
  "password":"Admin123"
}

3.Get Organization metadata : 
GET /org/get?organization_name=<name>
example
http://localhost:5000/org/get?organization_name=Google

4.Update Organization (rename and/or update admin)
PUT /org/update
Required: organization_name (current name)
Optional: new_organization_name (rename), email, password (admin update)

Request body example (rename)
{
  "organization_name":"Google",
  "new_organization_name":"Google India"
}

5.Delete Organization (admin-only)
DELETE /org/delete — protected with @jwt_required(). Token must belong to admin of the organization being deleted.
Headers :
Content-Type: application/json
Authorization: Bearer <access_token>
Body : 
{
  "organization_name": "Google India"
}

Can use the Postman to test the api-endpoints or can use the /docs endpoint (Swagger UI to test the endpoints) -> http://localhost:5000/docs
