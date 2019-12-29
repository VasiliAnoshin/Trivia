import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
           "question": "London is the capital of GB?",
           "answer": "Yes",
           "category": 4,
           "difficulty": 1
        }
        self.empty_question ={
            "question": [],
            "answer": [],
            "category": [],
            "difficulty": []
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resourse not found')    

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data)

    # def test_delete_question(self):
    #     res = self.client().delete('/questions/4')
    #     data = json.loads(res.data)
    #     question = Question.query.filter(Question.id == 4).one_or_none()
    #     self.assertEqual(question, None)
    #     self.assertEqual(res.status_code, 200)    
    #     self.assertEqual(data['success'], True)

    def test_delete_failed(self):
        res = self.client().delete('/questions/4')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_queez_question(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category':{'type': 'Geography', 'id': '3'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data)

    def test_get_queez_question_failed(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category':{'type': 'Geography', 'id': '90'}})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_insert_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post('/questions/45', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
    
    def test_search_by_param(self):
        res = self.client().post('/questions', json={"searchTerm": "title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data)
    
    def test_sort_questions_by_category(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data)
        self.assertEqual(data['current_category'], 3)
        self.assertTrue(data['total_questions'])
    
    def test_insert_new_question_failed(self):
        res = self.client().post('/questions', json=self.empty_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main() 
