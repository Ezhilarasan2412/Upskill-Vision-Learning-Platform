import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import './HR-Dashboard.css';
import Logout from '../Logout/Logout';

const HRdashboard = () => {
  const navigate = useNavigate();
  const [pendingUsers, setPendingUsers] = useState([]);
  const [error, setError] = useState('');
  const [showApprovalSection, setShowApprovalSection] = useState(false);

  useEffect(() => {
    const fetchPendingUsers = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/users/pending');
        setPendingUsers(response.data.pending_users || []);
      } catch (err) {
        console.error('Error fetching pending users:', err);
        setError('Failed to fetch pending users.');
      }
    };

    fetchPendingUsers();
  }, []);

  const handleApprove = async (userId) => {
    try {
      await axios.put(`http://127.0.0.1:5000/api/users/approve/${userId}`);
      alert('User approved successfully');
      setPendingUsers(pendingUsers.filter(user => user.id !== userId));
    } catch (err) {
      console.error('Error approving user:', err);
      setError('Failed to approve user.');
    }
  };

  return (
    <div className="dashboard-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <h2>HR Dashboard</h2>
        <ul className="sidebar-menu">
          <li onClick={() => setShowApprovalSection(!showApprovalSection)}>
            {showApprovalSection ? 'Hide User Approvals' : 'Approve Users'}
          </li>

          <li onClick={() => navigate('/performance-dashboard', { state: { userType: 'hr' } })}>
            User Performance
          </li>

          <li onClick={() => navigate('/course-list', { state: { userType: 'hr' } })}>
            View Courses List
          </li>

          <li>
            <Link to="/Courses" state={{ userType: "hr" }}>
              Create Course
            </Link>
          </li>
          
          <li onClick={() => navigate('/course-edit', { state: { userType: 'hr' } })}>
            Edit Course
          </li>


          {/*<li onClick={() => navigate('/delete-course', { state: { userType: 'hr' } })}>
            Delete Course
          </li>*/}

          {/* <li onClick={() => navigate('/delete-course', { state: { userType: 'hr' } })}> */}
          
        </ul>
        <Logout />
      </aside>

      {/* Main Content */}
      <div className="main-content">
        <header className="main-header">
          <h1>Welcome, HR!</h1>
        </header>

        {/* User Approval Section */}
        {showApprovalSection && (
          <section className="pending-users-section">
            <h2>Users Awaiting Approval</h2>
            {error && <div className="error-message">{error}</div>}

            {pendingUsers.length === 0 ? (
              <p>No users awaiting approval.</p>
            ) : (
              <ul className="user-list">
                {pendingUsers.map(user => (
                  <li key={user.id} className="user-item">
                    <div>
                      <strong>{user.first_name} {user.last_name}</strong>
                      <p>{user.username} - {user.email}</p>
                      <button className="approve-button" onClick={() => handleApprove(user.id)}>
                        Approve
                      </button>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </section>
        )}
      </div>
    </div>
  );
};

export default HRdashboard;