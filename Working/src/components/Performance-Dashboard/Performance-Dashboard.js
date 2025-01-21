import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Performance-Dashboard.css';

function UserProgress() {
  const [progressData, setProgressData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProgressData = async () => {
      try {
        const url = 'http://localhost:5000/api/progress'; // API endpoint

        const response = await axios.get(url);
        setProgressData(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching user progress data:', error);
        setLoading(false);
      }
    };

    fetchProgressData();
  }, []);

  const displayValue = (value) => {
    if (value === null || value === undefined) return ''; // Blank for unattempted fields
    return value; // Show actual value, including 0
  };


  if (loading) {
    return <p>Loading progress...</p>;
  }

  return (
    <div className="progress-container">
      <h3>User Progress Overview</h3>

      <table>
        <thead>
          <tr>
            <th>User ID</th>
            <th>Username</th>
            <th>Module Title</th>
            <th>Completion Status</th>
            <th>Resources Completed</th>
            <th>Quiz Score</th>
            <th>Quiz Status</th>
            <th>Correct Answers</th> 
            <th>Incorrect Answers</th> 
            <th>Skipped Answers</th> 
          </tr>
        </thead>
        <tbody>
          {progressData.length === 0 ? (
            <tr>
              <td colSpan="7">No progress data available.</td>
            </tr>
          ) : (
            progressData.map((item, index) => (
              <tr key={index}>
                <td>{item.user_id}</td>
                <td>{item.username}</td>
                <td>{item.module_title}</td>
                <td>{item.completion_status}</td>
                <td>{displayValue(item.resources_completed)}</td>
                <td>{displayValue(item.quiz_score)}</td>
                <td>{item.pass_fail_status}</td>
                <td>{displayValue(item.correct_answers)}</td>
                <td>{displayValue(item.incorrect_answers)}</td>
                <td>{displayValue(item.skipped_answers)}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default UserProgress;