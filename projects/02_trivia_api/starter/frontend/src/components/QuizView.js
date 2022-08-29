import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/QuizView.css';

const questionsPerPlay = 5;

class QuizView extends Component {
  constructor(props) {
    super(props);
    this.state = {
      quizCategory: null,
      previousQuestions: [],
      showAnswer: false,
      categories: {},
      numCorrect: 0,
      currentQuestion: {},
      username: '',
      user_id: 0,
      guess: '',
      forceEnd: false
    }
  }

  componentDidMount() {
    // this.setDisabled()
    $.ajax({
      url: `/categories`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.categories })
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again')
      }
    })
  }

  setDisabled = () => {
    document.getElementById("guess_input").disabled = true;
    document.getElementById("guess_btn").disabled = true;
  }

  removeDisabled = () => {
    document.getElementById("guess_input").disabled = false;
    document.getElementById("guess_btn").disabled = false;
  }

  getUsername = (e) => {
    e.preventDefault()
    $.ajax({
      url: `/users`, //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        user_name: this.state.username,
        categoryType: this.state.quizCategory
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        if (result.newUser) {
          alert('Created successfully! Go ahead and enjoy your play.')
        } else {
          let msg = this.state.username !== undefined ? `You are welcome back ${this.state.username}.` : "Please, enter a valid name."
          alert(msg)
        }
        this.setState({
          user_id: result.user_id
        });
        document.querySelector(".user-btn").disabled = true
        document.querySelector(".input-username").disabled = true
      },
      error: (error) => {
        alert('Unable to save your name. Please try again')
        document.querySelector(".user-btn").disabled = false
        document.querySelector(".input-username").disabled = false
      }
    })
  }

  selectCategory = ({ type, id = 0 }) => {
    this.setState({ quizCategory: { type, id } }, this.getNextQuestion)
  }

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value })
  }

  getNextQuestion = () => {
    const previousQuestions = [...this.state.previousQuestions]
    if (this.state.currentQuestion.id) { previousQuestions.push(this.state.currentQuestion.id) }

    $.ajax({
      url: '/quizzes', //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        previous_questions: previousQuestions,
        quiz_category: this.state.quizCategory
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          showAnswer: false,
          previousQuestions: previousQuestions,
          currentQuestion: result.question,
          guess: '',
          forceEnd: result.question ? false : true
        });
        this.updateUserScore(this.state.user_id)
      },
      error: (error) => {
        alert('Unable to load question. Please try your request again')
      }
    })
  }

  updateUserScore = (user_id) => {

    $.ajax({
      url: `/scores/${user_id}`, //TODO: update request URL
      type: "PATCH",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        score: this.state.numCorrect
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        // alert('Score successfully updated.')
        this.setState({
          username: result.user_name
        })
      },
      error: (error) => {
        if (this.state.previousQuestions.length !== 0) { alert('Unable to update user\'s score.') }
      }
    })
  }


  submitGuess = (event) => {
    event.preventDefault();
    const formatGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "").toLowerCase()
    const evaluate = this.evaluateAnswer()
    this.setState({
      numCorrect: !evaluate ? this.state.numCorrect : this.state.numCorrect + 1,
      showAnswer: true
    })
  }

  restartGame = () => {
    this.setState({
      quizCategory: null,
      previousQuestions: [],
      showAnswer: false,
      numCorrect: 0,
      currentQuestion: {},
      guess: '',
      username: "",
      user_id: 0,
      forceEnd: false
    })
  }

  renderPrePlay() {
    return (
      <div className="quiz-play-holder">
        <div className="choose-header">Choose Category</div>
        <div className="category-holder">
          <div className="play-category" onClick={this.selectCategory}>ALL</div>
          {Object.keys(this.state.categories).map(id => {
            return (
              <div
                key={id}
                value={id}
                className="play-category"
                onClick={() => this.selectCategory({ type: this.state.categories[id], id })}>
                {this.state.categories[id]}
              </div>
            )
          })}
        </div>
      </div>
    )
  }

  renderFinalScore() {
    return (
      <div className="quiz-play-holder">
        <div className="final-header"> {`${this.state.username ? this.state.username.toLocaleUpperCase() + ', ' : ""}`}Your Final Score is {this.state.numCorrect}</div>
        <div className="play-again button" onClick={this.restartGame}> Play Again? </div>
      </div>
    )
  }

  evaluateAnswer = () => {
    const formatGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "").toLowerCase()
    const answerArray = this.state.currentQuestion.answer.toLowerCase().split(' ');
    return answerArray.every(el => formatGuess.includes(el));
  }

  renderCorrectAnswer() {
    const formatGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "").toLowerCase()
    const evaluate = this.evaluateAnswer()
    return (
      <div className="quiz-play-holder">
        <div className="quiz-question">{this.state.currentQuestion.question}</div>
        <div className={`${evaluate ? 'correct' : 'wrong'}`}>{evaluate ? "You were correct!" : "You were incorrect"}</div>
        <div className="quiz-answer">{this.state.currentQuestion.answer}</div>
        <div className="next-question button" onClick={this.getNextQuestion}> Next Question </div>
      </div>
    )
  }

  renderPlay() {
    return this.state.previousQuestions.length === questionsPerPlay || this.state.forceEnd
      ? this.renderFinalScore()
      : this.state.showAnswer
        ? this.renderCorrectAnswer()
        : (
          <div className="quiz-play-holder">
            <div id="user-info">
              <form className="form-view" id="add-username-form" onSubmit={this.getUsername}>
                <label>
                  <input type="text" name="username" className='input-username' placeholder='Please, enter your name here.' onChange={this.handleChange} />
                </label>
                <input type="submit" className="button user-btn" value="OK" />
              </form>
            </div>
            <div className="question-block">
              <div className="quiz-question">{this.state.currentQuestion.question}</div>
              <form onSubmit={this.submitGuess} className="guess-form">
                <input type="text" name="guess" className="guess-input" id='guess_input' onChange={this.handleChange} />
                <input className="submit-guess button" id='guess_btn' type="submit" value="Submit Answer" />
              </form>
            </div>
          </div>
        )
  }


  render() {
    return this.state.quizCategory
      ? this.renderPlay()
      : this.renderPrePlay()
  }
}

export default QuizView;
