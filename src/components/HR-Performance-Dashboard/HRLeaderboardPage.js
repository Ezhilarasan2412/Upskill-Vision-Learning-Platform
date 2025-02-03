import React, { useState, useEffect } from "react";
import {useNavigate} from 'react-router-dom'; // For navigation
import "./HRLeaderboardPage.css"; // Add your styles here

const HRLeaderboardPage = () => {
  const [leaderboardData, setLeaderboardData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // Use React Router's navigate

  useEffect(() => {
    const fetchLeaderboardData = async () => {
      setLoading(true);
      setError(null);

      const apiUrl = `http://localhost:5000/api/hr/course-leaderboard`;

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
  }, []);

  const handleBackButtonClick = () => {
    navigate("/hr-dashboard");
  };

  return (
    <div className="hr-leaderboard-page">
      <h1>HR Course Leaderboard</h1>

      <button className="user-role-management-back-button" onClick={handleBackButtonClick}>
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
        !loading && <p>No results found</p>
      )}
    </div>
  );
};

export default HRLeaderboardPage;
