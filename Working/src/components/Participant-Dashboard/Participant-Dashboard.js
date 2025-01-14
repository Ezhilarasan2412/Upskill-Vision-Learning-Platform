import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Participant-Dashboard.css'; // Separate CSS file for Participant Dashboard
import Logout from '../Logout/Logout';

const ParticipantDashboard = () => {
  const navigate = useNavigate();

  return (
    <div className="dashboard-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <h2>Participant Dashboard</h2>
        <ul className="sidebar-menu">
          <li onClick={() => navigate('/user-course-list')}>Courses List</li>
          <li onClick={() => navigate('/enrolled')}>Enrolled</li>
          <li onClick={() => navigate('/unenrolled')}>Not Enrolled</li>
          <li onClick={() => navigate('/completed')}>Completed</li>
        </ul>
        <Logout />
      </aside>

      {/* Main Content */}
      <div className="main-content">
        <header className="main-header">
          <h1>Welcome, Participant!</h1>
        </header>
      </div>
    </div>
  );
};

export default ParticipantDashboard;