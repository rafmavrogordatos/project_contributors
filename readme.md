# Project Contributors Docs


## How to run
1. Set Up a Virtual Environment
	```bash

	python -m venv venv
	venv\Scripts\activate
	```

2. Install the requirements
	```bash

	pip install -r requirements.txt
	```

3. Migrations
	```bash

	python manage.py makemigrations api 
	python manage.py migrate 
	```

4. Run the server
	```bash

	python manage.py runserver
	```

5. Run the tests
  ```bash

  python manage.py test
  ```

You can check my Postman collection [here](https://www.getpostman.com/collections/7) to test the API.

## Authentication
The API uses JWT for authentication. To authenticate, you need to send a POST request to the `/api/token/` endpoint with the username and password in the request body. The API will return a token that you can use to authenticate subsequent requests.


## API Endpoints

1. User Endpoints

## Table of endpoints

| Method | Endpoint | Description | Auth |
| --- | --- | --- | --- |
| GET | /users/ | List all users | Not Required |
| POST | /users/ | Create a new user | Not Required |
| GET | /users/{id}/ | Retrieve user details | Not Required |
| PUT | /users/{id}/ | Update user details | Required |
| DELETE | /users/{id}/ | Delete user | Required |

### GET /users/
- List all users (Auth: Not Required)

### POST /users/
- Create a new user (Auth: Not Required)
  - `username` (string, required)
  - `email` (string, required)
  - `password` (string, required)
  - `first_name` (string, required)
  - `last_name` (string, required)
  - `age` (integer, optional)
  - `country` (string, required)
  - `residence` (string, required)

### GET /users/{id}/
- Retrieve user details (Auth: Not Required)

### PUT /users/{id}/
- Update user details (Auth: Required)
  - `username` (string)
  - `email` (string)

### DELETE /users/{id}/
- Delete user (Auth: Required)

2. Skill Endpoints (Auth: Required)


## 2. Skills Endpoints 


### Table of endpoints

| Method | Endpoint | Description | Auth |
| --- | --- | --- | --- |
| GET | /skills/ | List user skills | Required |
| POST | /skills/ | Add a skill | Required |
| DELETE | /skills/{id}/ | Delete a skill | Required |
| GET | /skills/options/ | List available languages and levels | Not Required |

### GET /skills/
- List user skills

### POST /skills/
- Add a skill (max 3 skills)
  - `name` (string, required)
  - `level` (string, required)

### DELETE /skills/{id}/
- Delete a skill

### GET /skills/options/
- List available languages and levels (Auth: Not Required)

## 3. Project Endpoints (Auth: Required)

### Table of endpoints

| Method | Endpoint | Description | Auth |
| --- | --- | --- | --- |
| GET | /projects/ | List all projects | Not Required |
| POST | /projects/ | Create a project | Required |
| PUT | /projects/{id}/ | Update project | Required |
| DELETE | /projects/{id}/ | Delete project | Required |
| POST | /projects/{id}/apply/ | Apply for a project | Required |
| GET | /projects/{id}/applications/ | View all applications | Required |
| GET | /projects/{id}/collaborators/ | View all collaborators | Required |
| GET | /projects/open_projects/ | List projects with available slots | Not Required |
| GET | /projects/user_stats/ | View user project statistics | Required |

### GET /projects/
- List all projects

### POST /projects/
- Create a project
  - `project_name` (string, required)
  - `description` (string, required)
  - `max_collaborators` (integer, required)

### PUT /projects/{id}/
- Update project (Only by creator)
  - `project_name` (string)
  - `description` (string)

### DELETE /projects/{id}/
- Delete project (Only by creator)

### POST /projects/{id}/apply/
- Apply for a project
  - `message` (string, optional)

### GET /projects/{id}/applications/
- View all applications (Only by creator)

### GET /projects/{id}/collaborators/
- View all collaborators

### GET /projects/open_projects/
- List projects with available slots (Auth: Not Required)

### GET /projects/user_stats/
- View user project statistics

4. Application Endpoints (Auth: Required)

## 4. Application Endpoints

### Table of endpoints

| Method | Endpoint | Description | Auth |
| --- | --- | --- | --- |
| GET | /applications/ | List user-related applications | Required |
| GET | /applications/{id}/ | View application details | Required |
| POST | /applications/{id}/accept/ | Accept application | Required |
| POST | /applications/{id}/decline/ | Decline application | Required |

### GET /applications/
- List user-related applications

### GET /applications/{id}/
- View application details

### POST /applications/{id}/accept/
- Accept application (Only by project creator)

### POST /applications/{id}/decline/
- Decline application (Only by project creator)

