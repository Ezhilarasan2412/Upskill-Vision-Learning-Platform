import React, { useState, useEffect } from 'react';
import axios from 'axios'; // If using axios for API calls

const QuizPerformance = ({ userId }) => {
  const [performanceData, setPerformanceData] = useState([]);
  const courseId = 1; // Example: you can dynamically get this if needed

  useEffect(() => {
    const fetchPerformanceData = async () => {
      try {
        const response = await axios.get(`/api/course/${courseId}/quiz-performance?user_id=${userId}`);
        console.log("Quiz Performance Data:", response.data.performance_data);  // Log the API response
        setPerformanceData(response.data.performance_data);
      } catch (error) {
        console.error('Error fetching quiz performance data', error);
      }
    };
  
    fetchPerformanceData();
  }, [userId, courseId]);
  
  
  return (
    <div>
      <h2>Quiz Performance</h2>
      {performanceData.length === 0 ? (
        <p>No performance data available</p>
      ) : (
        performanceData.map((courseData, idx) => (
          <div key={idx}>
            <h3>{courseData.course_name}</h3>
            {courseData.module.quizzes.length === 0 ? (
              <p>No quizzes available for this module.</p>
            ) : (
              courseData.module.quizzes.map((quiz, quizIdx) => (
                <div key={quizIdx} className="quiz-performance">
                  <h4>{quiz.quiz_title}</h4>
                  <p>Correct Answers: {quiz.correct_answers}</p>
                  <p>Incorrect Answers: {quiz.incorrect_answers}</p>
                  <p>Skipped Answers: {quiz.skipped_answers}</p>
                </div>
              ))
            )}
          </div>
        ))
      )}
    </div>
  );
};

export default QuizPerformance;
