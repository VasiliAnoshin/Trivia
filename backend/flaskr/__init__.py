import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources ={r"/*": {"origins":'*'}})
  #cors = CORS(app, resources={r"/*": {"origins": "*"}})
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  # CORS Headers 
  @app.after_request
  def after_request(response):
     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
     response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
     return response
  
  def get_formatted_categories():
    categories = Category.query.all()
    return [ctg.type for ctg in categories]

  def get_formatted_questions(questions):
    page = request.args.get('page', 1, type=int)
    start = (page-1)*QUESTIONS_PER_PAGE #Page can be 0 ?
    end = start + QUESTIONS_PER_PAGE
    formatted_quest = [quest.format() for quest in questions]
    return formatted_quest[start:end]
  
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  #@cross_origin()
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.all()
    formatted_ctg = [ctg.type for ctg in categories]
    print(formatted_ctg)
    if(len(formatted_ctg)==0):
      abort(404)
    return jsonify({ 
      'categories': formatted_ctg,
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def questions():
    questions = Question.query.all()
    cur_quest = get_formatted_questions(questions)
    if not cur_quest:
          abort(404) 
    return jsonify({
      'success': True,
      'questions':cur_quest,
      'total_questions':len(Question.query.all()),
      'current_category': '',
      'categories': get_formatted_categories(),
    })
        
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    try:
      quest = Question.query.filter(Question.id == id).one_or_none()
      if quest is None:
        abort(404)
      quest.delete()
    except:
      abort(422)
    return jsonify({
      'success':True
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def post_new_question():
    try:
      data = request.get_json()
      if 'searchTerm' in data:
        questions = Question.query.filter(Question.question.ilike(f"%{data['searchTerm']}%")).all()
        return jsonify({
          'success': True,
          'questions': get_formatted_questions(questions),
          'current_category': '',
          'total_questions':len(questions),
        })
      else:
        question=Question(question=data['question'],
                          answer=data['answer'],
                          category=data['category'],
                          difficulty=data['difficulty'])
        question.insert()
        return jsonify({
            'success': True
        })
    except:
      abort(422)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category.
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_question_by_category(id):
     try:
        questions = Question.query.filter(Question.category == id).all()
        cur_quest = get_formatted_questions(questions)
     except:
        abort(422)
     return jsonify({
      'success': True,
      'questions':cur_quest,
      'total_questions':len( Question.query.filter(Question.category == id).all()),
      'current_category': id,
      'categories': get_formatted_categories(),   
    })
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quizz():
    try:
      data = request.get_json()
      previousQuestions = data['previous_questions']
      ctg_id = data['quiz_category']
      questions = Question.query.filter(Question.category == ctg_id).all()
    except:
       abort(422)

    return jsonify({
        'previousQuestions': previousQuestions,
        'currentQuestion': get_formatted_questions(questions),
     })     
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message":"resourse not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message":"unprocessable"
  }), 422

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'code': 405,
      'success': False,
      'message': 'method not allowed'
  }), 405

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      'code': 500,
      'success': False,
      'message': 'server error'
    }), 500  
  return app

    