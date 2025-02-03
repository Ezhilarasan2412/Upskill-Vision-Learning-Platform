import React, { useState } from "react";
import {useNavigate} from 'react-router-dom'; // For navigation
import "./HRFilterPerformance.css";

const FilterPerformancePage = () => {
  const [courseName, setCourseName] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [performanceData, setPerformanceData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // Use React Router's navigate

  const fetchPerformanceData = async () => {
    setLoading(true);
    setError(null);
    let queryParams = new URLSearchParams();

    if (courseName) queryParams.append("course", courseName.trim());
    if (startDate) queryParams.append("start_date", new Date(startDate).toISOString().split("T")[0]);
    if (endDate) queryParams.append("end_date", new Date(endDate).toISOString().split("T")[0]);

    const apiUrl = `http://localhost:5000/api/hr/performance?${queryParams.toString()}`;

    try {
      const response = await fetch(apiUrl);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setPerformanceData(Array.isArray(data) ? data : []);
    } catch (error) {
      setError(`Failed to fetch data. Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleBackButtonClick = () => {
    navigate("/hr-dashboard");
  };

  return (
    <div className="filter-performance-page">
      <h1>Filter Performance</h1>
      
      <button className="user-role-management-back-button" onClick={handleBackButtonClick}>
          Back
        </button>

      <div className="filter-section">
        <input type="text" placeholder="Course Name" value={courseName} onChange={(e) => setCourseName(e.target.value)} />
        <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
        <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
        <button onClick={fetchPerformanceData}>Apply Filter</button>
      </div>
      {loading && <p>Loading performance data...</p>}
      {error && <p className="error">{error}</p>}
      {performanceData.length > 0 ? (
        <table className="performance-table">
          <thead>
            <tr>
              <th>Course Name</th>
              <th>Description</th>
              <th>Start Date</th>
              <th>End Date</th>
              <th>Enrollment Count</th>
            </tr>
          </thead>
          <tbody>
            {performanceData.map((course, index) => (
              <tr key={index}>
                <td>{course.course_name || "N/A"}</td>
                <td>{course.description || "N/A"}</td>
                <td>{course.start_date || "N/A"}</td>
                <td>{course.end_date || "N/A"}</td>
                <td>{course.enrollment_count || 0}</td>
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

export default FilterPerformancePage;