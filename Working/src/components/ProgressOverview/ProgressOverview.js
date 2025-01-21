import axios from 'axios';
import React, { useEffect, useState } from 'react';

function UserProgress() {
  const [progressData, setProgressData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserProgress = async () => {
      try {
        const userId = localStorage.getItem('user_id'); // Replace with actual user ID retrieval
        const response = await axios.get(`http://localhost:5000/api/progress/user/${userId}`);
        setProgressData(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching user progress:', error);
        setLoading(false);
      }
    };

    fetchUserProgress();
  }, []);

  const displayValue = (value) => {
    if (value === null || value === undefined) return ''; // Blank for unattempted fields
    return value; // Show actual value, including 0
  };

  if (loading) return <p>Loading progress...</p>;

  return (
    <div>
      <h2>Your Progress</h2>
      {progressData.length === 0 ? (
        <p>No progress data available.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Module Title</th>
              <th>Completion Status</th>
              <th>Resources Completed</th>
              <th>Quiz Score</th>
              <th>Pass/Fail Status</th>
              <th>Correct Answers</th>
              <th>Incorrect Answers</th>
              <th>Skipped Answers</th>
            </tr>
          </thead>
          <tbody>
            {progressData.map((item, index) => (
              <tr key={index}>
                <td>{item.module_title}</td>
                <td>{item.completion_status}</td>
                <td>{displayValue(item.resources_completed)}</td>
                <td>{displayValue(item.quiz_score)}</td>
                <td>{item.pass_fail_status}</td>
                <td>{displayValue(item.correct_answers)}</td>
                <td>{displayValue(item.incorrect_answers)}</td>
                <td>{displayValue(item.skipped_answers)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default UserProgress;
