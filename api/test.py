from django.test import TestCase, Client


class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_registration(self):
        response = self.client.post('/api/users/', {
            'username': 'test_user1',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john12@example.com',
            'password': 'testpassword',
            'age': 30,
            'country': 'USA',
            'residence': 'California'
        })
        self.assertEqual(response.status_code, 201)


        response = self.client.post('/api/auth/token/', {
            'username': 'test_user1',
            'password': 'testpassword'
        })
        self.assertTrue('access' in response.json())


    def test_user_registration_invalid_data(self):
        response = self.client.post('/api/users/', {
            'username': 'test_user12',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'testemail.com',
            'password': 'testpassword',
            'age': 30,
            'country': 'USA',
            'residence': 'California'
        })
        self.assertEqual(response.status_code, 400)



class UserLoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/api/users/', {
            'username': 'test_user1',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'tester1@test.com',
            'password': 'testpassword',
            'age': 30,
            'country': 'USA',
            'residence': 'California'
        })

    def test_user_login(self):
        response = self.client.post('/api/auth/token/', {
            'username': 'test_user1',
            'password': 'testpassword'
        })
        self.assertTrue('access' in response.json())

    def test_user_login_invalid_data(self):
        response = self.client.post('/api/auth/token/', {
            'username': 'test_user1',
            'password': 'testpassword1'
        })
        self.assertEqual(response.status_code, 401) 


class SkillsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/api/users/', {
            'username': 'test_user1',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'tester12@tester.com',
            'password': 'testpassword',
            'age': 30,
            'country': 'USA',
            'residence': 'California'
        })
        response = self.client.post('/api/auth/token/', {
            'username': 'test_user1',
            'password': 'testpassword'
        })
        self.access_token = response.json()['access']

    def test_add_skill(self):
        response = self.client.post('/api/skills/', {
            'language': 'Python',
            'level': 'beginner'
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 201)

    def test_add_skill_invalid_data(self):
        response = self.client.post('/api/skills/', {
            'language': 'Python',
            'level': 'not_a_level'
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)

    def test_get_skills(self):
        self.client.post('/api/skills/', {
            'language': 'Python',
            'level': 'beginner'
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get('/api/skills/', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)

    def test_get_skills_unauthenticated(self):
        response = self.client.get('/api/skills/')
        self.assertEqual(response.status_code, 401)



class ProjectsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/api/users/', {
            'username': 'test_user1',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test_projects@test.com',
            'password': 'testpassword',
            'age': 30,
            'country': 'USA',
            'residence': 'California'
        })
        response = self.client.post('/api/auth/token/', {
            'username': 'test_user1',
            'password': 'testpassword'
        })
        self.access_token = response.json()['access']


    def test_add_project(self):
        response = self.client.post('/api/projects/', {
            'project_name': 'Project 1',
            'description': 'Description of project 1',
            'max_collaborators': 5
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 201)

    def test_add_project_invalid_data(self):
        response = self.client.post('/api/projects/', {
            'project_name': 'Project 1',
            'description': 'Description of project 1',
            'max_collaborators': -5
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 400)

    def test_get_projects(self):
        self.client.get('/api/projects/', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get('/api/projects/', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 200)

    

class ApplicationsTestCase(TestCase):
    def setUp(self):
        self.client_project_owner = Client()
        self.client_applicant = Client()
        self.client_project_owner.post('/api/users/', {
            'username': 'test_user1',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test_client@test.com',#
            'password': 'testpassword',
            'age': 30,
            'country': 'USA',
            'residence': 'California'
        })
        response = self.client_project_owner.post('/api/auth/token/', {
            'username': 'test_user1',
            'password': 'testpassword'
        })
        self.access_token_project_owner = response.json()['access']

        self.client_applicant.post('/api/users/', {
            'username': 'test_user2',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'test_owner@test.com',
            'password': 'testpassword',
            'age': 30,
            'country': 'USA',
            'residence': 'California'
        })
        response = self.client_applicant.post('/api/auth/token/', {
            'username': 'test_user2',
            'password': 'testpassword'
        })
        self.access_token_applicant = response.json()['access']


        self.client_project_owner.post('/api/projects/', {
            'project_name': 'Project 1',
            'description': 'Description of project 1',
            'max_collaborators': 5
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token_project_owner}')
        response = self.client_project_owner.get('/api/projects/', HTTP_AUTHORIZATION=f'Bearer {self.access_token_project_owner}')
        self.project_id = response.json()[0]['id']

    def test_apply_project(self):
        response = self.client_applicant.post(f'/api/projects/{self.project_id}/apply/', HTTP_AUTHORIZATION=f'Bearer {self.access_token_applicant}')
        self.assertEqual(response.status_code, 201)

    def test_apply_project_invalid_data(self):
        response = self.client_applicant.post('/api/applications/', {
            'project': 100
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token_applicant}')
        self.assertEqual(response.status_code, 405)


    def test_accept_application(self):
        response = self.client_applicant.post(f'/api/projects/{self.project_id}/apply/', {
            'message': 'I am interested in this project, please consider me.'
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token_applicant}')
        self.assertEqual(response.status_code, 201)








        