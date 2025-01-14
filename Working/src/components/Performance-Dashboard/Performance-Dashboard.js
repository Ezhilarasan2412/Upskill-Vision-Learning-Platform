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
            <th>Quiz Score</th>
            <th>Resources Completed</th>
            <th>Pass/Fail Status</th>
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
                <td>{item.quiz_score}</td>
                <td>{item.resources_completed}</td>
                <td>{item.pass_fail_status}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default UserProgress;