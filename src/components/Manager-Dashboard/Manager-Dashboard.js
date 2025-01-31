import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Manager-Dashboard.css'; // Updated file name
import Logout from '../Logout/Logout';


const ManagerDashboard = () => {
  const navigate = useNavigate();

  return (
    <div className="dashboard-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <h2>Manager Dashboard</h2>
        <ul className="sidebar-menu">
        <li onClick={() => navigate('/course-list', { state: { userType: 'manager' } })}>
            View Courses List
          </li>   
          
          <li onClick={() => navigate('/department-management', { state: { userType: 'manager' } })}>
            View Department
          </li>

          <li onClick={() => navigate('/performance-dashboard-manager', { state: { userType: 'manager' } })}>
            Performance Dashboard
          </li>

          <li onClick={() => navigate('/participant-pie-chart', { state: { userType: 'manager' } })}>
            ParticipantPieChart
          </li>

          <li onClick={() => navigate('/filter-performance', { state: { userType: 'manager' } })}>
            FilterPerformance
          </li>
          </ul>
        <Logout />
      </aside>

      {/* Main Content */}
      <div className="main-content">
        <header className="main-header">
          <h1>Welcome, Manager!</h1>
        </header>
      </div>
    </div>
  );
};

export default ManagerDashboard;