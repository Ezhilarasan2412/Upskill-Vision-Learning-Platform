import React, { useState, useEffect } from "react";
import { useNavigate} from 'react-router-dom';
import "./ManagerLeaderboardPage.css";

const CourseLeaderboardPage = () => {
  const [leaderboardData, setLeaderboardData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // Use React Router's navigate

  const managerId = localStorage.getItem("user_id"); // Retrieve manager_id from localStorage

  useEffect(() => {
    if (!managerId) {
      setError("Manager ID is missing. Please log in again.");
      return;
    }

    const fetchLeaderboardData = async () => {
      setLoading(true);
      setError(null);

      const apiUrl = `http://localhost:5000/api/manager/course-leaderboard?manager_id=${managerId}`;

      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        setLeaderboardData(data);
      } catch (error) {
        setError(`Failed to fetch leaderboard data. Error: ${error.message}`);
      } finally {
        setLoading(false);
      }
    };

    fetchLeaderboardData();
  }, [managerId]);

  const handleBackButtonClick = () => {
    navigate('/manager-dashboard');
  };

  return (
    <div className="course-leaderboard-page">
      <h1>Course Leaderboard</h1>
      <button className="user-progress-page-back-button" onClick={handleBackButtonClick}>
          Back
        </button>
      {loading && <p>Loading leaderboard data...</p>}
      {error && <p className="error">{error}</p>}
      {leaderboardData.length > 0 ? (
        <table className="leaderboard-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Name</th>
              <th>Completed Courses</th>
            </tr>
          </thead>
          <tbody>
            {leaderboardData.map((participant, index) => (
              <tr key={participant.user_id}>
                <td>{index + 1}</td> {/* Rank */}
                <td>{participant.name}</td>
                <td>{participant.completed_courses_count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        !loading && <p>No participants found in your department.</p>
      )}
    </div>
  );
};

export default CourseLeaderboardPage;
