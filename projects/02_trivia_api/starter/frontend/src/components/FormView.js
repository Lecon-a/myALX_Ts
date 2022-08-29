import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/FormView.css';

class FormView extends Component {
  constructor(props){
    super(props);
    this.state = {
      question: "",
      answer: "",
      difficulty: 1,
      category: 1,
      categories: {},
      rating: 1,
      categoryType: ""
    }
  }

  componentDidMount(){
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


  submitQuestion = (event) => {
    event.preventDefault();
    $.ajax({
      url: '/questions', //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        question: this.state.question,
        answer: this.state.answer,
        difficulty: this.state.difficulty,
        category: this.state.category,
        rating: this.state.rating
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById("add-question-form").reset();
      },
      error: (error) => {
        alert('Unable to add question. Please try your request again')
      }
    })
  }

  submitCategory = (event) => {
    event.preventDefault();
    $.ajax({
      url: '/categories', //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        categoryType: this.state.category
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById("add-category-form").reset();
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
      },
      error: (error) => {
        alert('Unable to add category. Please try your request again')
      }
    })
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})  
  }

  render() {
    return (
      <div id="group_add_forms">
        <div id="add-category">
        <h2>Add a New Category</h2>
        <form className="form-view" id="add-category-form" onSubmit={this.submitCategory}>
          <label>
            <input type="text" name="category" className='form-input-cat' placeholder='Category type' onChange={this.handleChange}/>
          </label>
          <input type="submit" className="button" value="Add" />
        </form>
      </div>

      <div id="add-form">
        <h2>Add a New Trivia Question</h2>
        <form className="form-view" id="add-question-form" onSubmit={this.submitQuestion}>
          <label>
            Question
            <input type="text" name="question" onChange={this.handleChange}/>
          </label>
          <label>
            Answer
            <input type="text" name="answer" onChange={this.handleChange}/>
          </label>
          <label>
            Difficulty
            <select name="difficulty" onChange={this.handleChange}>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
            </select>
          </label>
          <label>
            Rating
            <select name="rating" onChange={this.handleChange}>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
            </select>
          </label>
          <label>
            Category
            <select name="category" onChange={this.handleChange}>
              {Object.keys(this.state.categories).map(id => {
                  return (
                    <option key={id} value={parseInt(id)+1}>{this.state.categories[id]}</option>
                  )
                })}
            </select>
          </label>
          <input type="submit" className="button" value="Submit" />
        </form>
      </div>
      
      </div>
    );
  }
}

export default FormView;
