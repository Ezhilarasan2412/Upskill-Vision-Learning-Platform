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
          <li onClick={() => navigate('/course-list')}>Courses List</li>
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