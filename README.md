# Auth REST API
Authentication REST API for a portfolio site

## Install
1 - First clone the repository and enter the project folder.
```bash
  $ git clone https://github.com/CaioSilva23/api-auth
  $ cd api-auth
```
2 - Configure environment variables
```bash
 create .env based on .env-exemple
```
3 - Second start docker compose
```bash
  $ docker compose up
```

## Register a new User

### Example Request

`POST /register/`
```bash
curl --location 'http//127.0.0.1:8000/api/user/register/' \
--data-raw '{
	"email": "email@exemple.com",
	"first_name": "Jhon",
	"last_name": "Snow",
	"password": "Jonsnow@1",
	"password2": "Jonsnow@1"
}'
```
### Example Response
```bash
{
  "token": {
    "refresh": "token refresh",
    "access": "token access"
  },
  "mgs": "Registration Success"
}
```
## Login a User

### Example Request

`POST /login/`
```bash
curl --location 'http//127.0.0.1:8000/api/user/login/' \
--data-raw '{
	"email": "email@exemple.com",
	"password": "Jonsnow@1",
}'
```
### Example Response
```bash
{
  "token": {
    "refresh": "token refresh",
    "access": "token access"
  },
   "msg": "Login success"
}
```
## Profile a User

### Example Request

`GET /profile/`
```bash
curl --location 'http//127.0.0.1:8000/api/user/profile/' \
--header 'Authorization: Bearer token access'
```
### Example Response
```bash
{
  "id": 1,
  "email": "email@exemple.com",
  "first_name": "Jhon",
  "last_name": "Snow"
}
```
## Change Password a User

### Example Request

`PUT /changepassword/`
```bash
curl --location --request PUT 'http//127.0.0.1:8000/api/user/changepassword/' \
--header 'Authorization: Bearer access token' \
--data-raw '{

	"password": "NewPassword@23",
	"password2": "NewPassword@23"

}'
```
### Example Response
```bash
{
  "msg": "Password Changed Successfully"
}
```
## Reset a User password via email

### Example Request

`POST /send-reset-password-email/`
```bash
curl --location 'http//127.0.0.1:8000/api/user/send-reset-password-email/' \
--data-raw '{
  "email": "email@exemple.com"
}'
```
### Example Response
```bash
{
  "msg": "Password Reset link send. Please check your Email"
}
```
## Reset a User password

### Example Request

`PUT /reset-password/UID/TOKEN/`
```bash
curl --location --request PUT 'http//127.0.0.1:8000/api/user/reset-password/UID/TOKEN/' \
--data-raw '{
		"password": "NewPassword@10",
		"password2": "NewPassword@10"
}'
```
### Example Response
```bash
{
  "msg": "Password Reset Successfully"
}
```
