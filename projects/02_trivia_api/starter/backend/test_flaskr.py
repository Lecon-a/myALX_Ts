import os
from sre_constants import SUCCESS
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flaskr import create_app
from models import setup_db, Question, Category, User
import secret as s


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{0}@{1}/{2}".format(
            s.credentials, s.address, self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": 'What is physics?',
            "answer": 'Study of phenomenon',
            "category": 'Science',
            "difficulty": 4,
            "rating": 3
        }

        self.new_user = {
            "user_name": "Mr. Daniel",
            "score": 0
        }

        self.new_quiz = {
            "quiz_category": {
                "type": "Science",
                "id": "0"
            },
            "previous_questions": []
        }

        self.search_term = "What"

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_categories'])

    def test_404_categories(self):
        res = self.client().get('/categories/23')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_retrieve_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['current_category']))
        self.assertTrue(len(data['categories']))

    def test_405_bad_req_during_questions_retrieval(self):
        res = self.client().get('/questions/13')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_create_question(self):
        res = self.client().post(
            '/questions', json={'new_question': self.new_question})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_create_question_not_allowed(self):
        res = self.client().post('/questions/24', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_search_question_with_result(self):
        res = self.client().post(
            '/questions', json={'searchTerm': self.search_term})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['current_category']))

    def test_search_question_without_result(self):
        res = self.client().post(
            '/questions', json={'searchTerm': 'eternal glory'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)

    def test_retrieve_questions_by_category(self):
        item_id = 5
        res = self.client().get(f'/categories/{item_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['current_category']))

    def test_404_retrieve_questions_by_category(self):
        item_id = 500
        res = self.client().get(f'/categories/{item_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question_endpoint(self):
        question_id = 7
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        question = Question.query.filter(
            Question.id == question_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], question_id)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertEqual(question, None)

    def test_422_if_question_does_not_exit_for_deletion(self):
        question_id = 236
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_400_quizzes(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_quizzes(self):
        res = self.client().post('/quizzes', json=self.new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['previous_questions'], [])
        self.assertTrue(len(data['quiz_category']))
        self.assertFalse(data['question'])

    def test_405_quizzes(self):
        res = self.client().get('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_404_posting_quizzes_with_item(self):
        res = self.client().post('/quizzes/12')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_user(self):
        res = self.client().post('/users', json=self.new_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_create_user_unprocessable(self):
        res = self.client().post('/users')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_405_unprocessable_request_to_user(self):
        res = self.client().get('/users')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_score_update(self):
        res = self.client().patch('/scores/1', json={'score': 2})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_score_update(self):
        res = self.client().patch('/scores/10000', json={'score': 2})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
