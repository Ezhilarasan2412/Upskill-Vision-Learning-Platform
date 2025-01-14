import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './QuizForm.css';

function QuizForm() {
  const [moduleId, setModuleId] = useState('');
  const [quizTitle, setQuizTitle] = useState('');
  const [totalScore, setTotalScore] = useState('');
  const [passingScore, setPassingScore] = useState('');
  const navigate = useNavigate();

  const handleBackButtonClick = () => {
    window.history.back(); // Go to the previous page
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/api/quizzes', {
        module_id: moduleId,
        quiz_title: quizTitle,
        total_score: totalScore,
        passing_score: passingScore,
      });

      console.log('API Response:', response.data);  // Log the response to verify quiz_id

      alert(response.data.message);

      // Check if the quiz ID is available in the response data
      if (response.data.quiz_id) {
        // Navigate to QuestionForm with quizId and totalScore (number of questions to add)
        navigate(`/add-question/${response.data.quiz_id}/${totalScore}`);
      } else {
        alert('Quiz ID is missing.');
      }
    } catch (err) {
      console.error('Error adding quiz:', err);
      alert('Failed to add quiz.');
    }
  };

  return (
    <div className="quiz-form-container">
      <h2>Add Quiz</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Module ID:</label>
          <input
            type="text"
            value={moduleId}
            onChange={(e) => setModuleId(e.target.value)}
            required
          />
        </div>

        <button className="back-button" onClick={handleBackButtonClick}>
          Back
        </button>

        <div className="form-group">
          <label>Quiz Title:</label>
          <input
            type="text"
            value={quizTitle}
            onChange={(e) => setQuizTitle(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Total Score (Number of Questions):</label>
          <input
            type="number"
            value={totalScore}
            onChange={(e) => setTotalScore(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Passing Score (Number of Questions Correct):</label>
          <input
            type="number"
            value={passingScore}
            onChange={(e) => setPassingScore(e.target.value)}
            required
          />
        </div>
        <button type="submit">Add Quiz</button>
      </form>
    </div>
  );
}

export default QuizForm;
