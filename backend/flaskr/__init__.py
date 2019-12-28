import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  app.config['DEBUG'] = True
  setup_db(app)
  CORS(app, resources ={r"/*": {"origins":'*'}})
 
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
    start = (page-1)*QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_quest = [quest.format() for quest in questions]
    return formatted_quest[start:end]
  
  def get_questions_sorted_by_category(data):
    ctg_id = data['quiz_category']['id']
    if  data['quiz_category']['id'] == 0:
      return  Question.query.filter().all()
    else:
      return Question.query.filter(Question.category == ctg_id).all()

  def get_queez_question(data):
    previousQuestions = data['previous_questions']
    questions = get_questions_sorted_by_category(data)
    if not previousQuestions:
        rand_quest = random.choice(questions)
        return  rand_quest.format()
    else:
        sorted_questions=[]
        for quest in questions:
          if quest.id not in previousQuestions:
            sorted_questions.append(quest)
        if len(sorted_questions)==0:
          return None
        return  (random.choice(sorted_questions)).format()

  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.all()
    formatted_ctg = [ctg.type for ctg in categories]
    if(len(formatted_ctg)==0):
      abort(404)
    return jsonify({ 
      'categories': formatted_ctg,
    })

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
        
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    try:
      quest = Question.query.filter(Question.id == id).one_or_none()
      quest.delete()
    except:
      abort(404)
    return jsonify({
        'success':True
    })

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

  @app.route('/quizzes', methods=['POST'])
  def play_quizz():
    try:
        data = request.get_json()
        rand_quest = get_queez_question(data)
    except:
       print('This is error output', file=sys.stderr)
       abort(422)
    return jsonify({
        'question': rand_quest,
     })     

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

    