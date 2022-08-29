from ast import Constant
import collections
import json
from math import ceil
import os
from traceback import print_tb
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, User, db

QUESTIONS_PER_PAGE = 10
ROUND = 5


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    '''
  @TODO: Set up CORS. Allow '*' for origins.
  Delete the sample route after completing the TODOs
  '''
    CORS(app, resources={r'/api/*': {'origins': '*'}})
    # resources={r"*/api/*": {"origins":"*"}}

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def afterRequest(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    def pagination(request, selection):
        '''
        This function takes two parameters and return slided seletion

          Parameters:
            @request
            @selection => list of questions

          Returns:
            10 questions at a time
        '''
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        selection = [item.format() for item in selection]

        return selection[start:end]

    def randomizeQuiz(previous_ids, selection):
        size = len(selection)
        randomIndex = random.randint(0, size)

        if randomIndex >= size:
            return -1

        if len(previous_ids) != 0:
            if len(previous_ids) == ROUND:
                return False
            s = selection[randomIndex]
            while s['id'] in previous_ids:
                randomIndex = random.randint(0, size)

        return randomIndex

    @app.route('/users', methods=['POST'])
    def create_user():
        try:
            # get value from the frontend
            body = request.get_json()
            new_user = body.get('user_name', None)
            if new_user is None or len(new_user) == 0:
                return jsonify({'success': True})
            user = User.query.filter(User.name == new_user).first()
            if user:
                user_id = user.uid()['id']
                return jsonify({
                    'success': True,
                    'user_id': user_id
                })
            new_entry = User(new_user)
            new_entry.insert()
            userInfo = User.query.order_by(User.id.desc()).first()
            user_id = userInfo.uid()['id']
            # return true
            return jsonify({
                'success': True,
                'user_id': user_id,
                'newUser': True
            })
        except:
            abort(422)

    @app.route('/categories', methods=['GET', 'POST'])
    def retrieve_categories():
        '''
        This function makes a get request to fetch all
        the possible categories in the db order the list by ID

        Returns:
          -success: True
          -all categories (types without id)
          -total categories
          else: abort with error 400 (bad request)
        '''
        try:

            if request.method == 'POST':
                body = request.get_json()
                new_category = body.get('categoryType', None)
                if new_category is None:
                    abort(400)
                # print("New Cat:::", new_category)
                newCategory = Category(new_category)
                newCategory.insert()

            selection = Category.query.order_by(Category.id).all()

            if len(selection) == 0:
                abort(404)

            categories = [item.ctype() for item in selection]
            data = {
                'success': True,
                'categories': categories,
                'total_categories': len(categories)
            }
            return jsonify(data)
        except:
            abort(400)

    @app.route('/questions', methods=['GET', 'POST'])
    def retrieve_or_create_questions():
        '''
        Questions endpoint does three types of operations
        Get questions
        order by category their belong
        Get return
        json data which comprises of success, questions,
        categories, current_category, total questions

        Insert a new question by Post method
        Create a new entry trivia's question and does return success

        Search for questions with search substring term
        Search all the possible questions with the search term entered

        Check if action method is post
        '''
        try:

            if request.method == 'POST':
                body = request.get_json()
                # Gets the json's body members
                new_question = body.get('question', None)
                new_answer = body.get('answer', None)
                new_difficulty = body.get('difficulty', None)
                new_category = body.get('category', None)
                new_rating = body.get('rating', None)
                search_term = body.get('searchTerm', None)

                if search_term:
                    questions = Question.query.filter(Question.question.ilike(
                        f'%{search_term}%')).order_by(Question.id).all()

                    if questions is None:
                        return jsonify({
                            'success': True
                        })

                    current_questions = pagination(request, questions)
                    current_category = Category.query.filter(
                        Category.id == current_questions[0]['category'])\
                        .one_or_none().ctype() if questions else ''
                    data = {
                        'success': True,
                        'questions': current_questions,
                        'total_questions': len(questions),
                        'current_category': current_category
                    }
                    return jsonify(data)
                else:
                    new_entry = Question(
                        new_question, new_answer, new_category,
                        new_difficulty, new_rating)
                    try:
                        new_entry.insert()
                    except:
                        abort(400)
                    #nprint("Saved successfully:: ", new_entry)
                    return jsonify({
                        'success': True
                    })
            else:
                # Here is the third operation that get all avialable questions
                # performs join on the two models Question and Category
                selection = db.session.query(
                    Question, Category).join(
                    Category, Category.id == Question.category).order_by(
                    Category.id).all()
                # If no seletion, abort with error 404 (resource not found)
                if len(selection) == 0:
                    abort(404)
                # Create a empty dictionary template for questions
                questions = {'questions': [], 'categories': []}
                # Loop through the return of the database query
                for question in selection:
                    # add to the element of questions dictionary template
                    questions['questions'].append(question[0])
                    questions['categories'].append(question[1].ctype())
                # get category type alone
                categories = [category.ctype() for category in Category
                              .query.order_by(Category.id).all()]
                # structuring the return data
                data = {
                    'success': True,
                    'questions': pagination(request, questions['questions']),
                    'total_questions': len(selection),
                    'current_category': questions['categories'][0],
                    'categories': categories
                }
                return jsonify(data)
        except:
            abort(400)

    @app.route('/categories/<int:category_id>/questions')
    def getCategoryQuestions(category_id):
        '''
        # Get Categorical Questions By Category ID
        '''
        try:
            # Join on Question and Category Models to
            # Get all Questions Belonging to a particular category
            questions = db.session.query(Question).join(
                Category, Category.id == Question.category).filter(
                Category.id == category_id).order_by(Question.id).all()
            # json data return
            return jsonify({
                'success': True,
                'questions': pagination(request, questions),
                'total_questions': len(Question.query.all()),
                'current_category': Category.query.filter(
                    Category.id == category_id).first().ctype()
            })
        except:
            # abort with error code 404
            abort(404)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def deleteQuestion(question_id):
        '''
        # deleteQuestion as the name implies,
        # deletes a specific question that the its ID is known
        '''
        try:

            question = Question.query.filter(
                Question.id == question_id).first()
            # If there is no such question, abort
            # with an error code 404 (resource not found)
            if question is None:
                abort(404)
            question.delete()
            # This is to confirm the deletion of the question
            questions = Question.query.order_by(Question.id).all()
            current_questions = pagination(request, questions)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })
        except:
            # else unprocessable
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def play():
        # Post a unique quiz that is not part of the previous questions queue
        body = request.get_json()
        try:
            # json body values
            quiz_category = body.get('quiz_category', None)['type']
            previous_questions = body.get('previous_questions')
            # print("Quiz category::: >> ", quiz_category)
            questions = []
            if quiz_category == 'click' or quiz_category is None:
                # print("===Yes===")
                questions = Question.query.order_by(Question.id).all()
                # print(questions)
                # print("===***===")
            else:
                collection = Category.query.order_by(Category.id).all()
                categories = [category.format() for category in collection]
                # print("===No===", quiz_category)
                # print("===No===", categories)
                for category in categories:
                    if (category['type'] == quiz_category):
                        # print("Match:: ", category['type'])
                        category_id = category['id']
                # print("Match ID: ", category_id)
                # print(f"Categories:::  {categories}, type::: {quiz_category}")
                questions = Question.query.filter(
                    Question.category == category_id)\
                    .order_by(Question.id).all()

                if len(questions) == False:
                    data = {
                        'success': True,
                        'question': False
                    }
                # print("Question ::: ", questions)
            questions = [question.format() for question in questions]
            quiz_no = randomizeQuiz(previous_questions, questions)
            # print(f'>>> {quiz_no} => {questions[quiz_no]}=======\n')
            if quiz_no != -1:
                q = questions[quiz_no]
                quiz_id = q['id']
                previous_questions.append(quiz_id)
                question = questions[quiz_no]
            else:
                question = False
            data = {
                'success': True,
                'quiz_category': quiz_category,
                'previous_questions': previous_questions,
                'question': question
            }
            try:
                return jsonify(data)
            except TypeError:
                abort(500)
        except:
            abort(400)

    @app.route('/scores/<int:user_id>', methods=['PATCH'])
    def update_score(user_id):
        try:
            if user_id != 0:
                body = request.get_json()
                user = User.query.filter(User.id == user_id).first()

                if 'score' in body:
                    user.score = int(body.get('score'))

                user.update()
            return jsonify({'success': True})
        except:
            abort(400)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    return app
