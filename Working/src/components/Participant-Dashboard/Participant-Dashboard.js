import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Participant-Dashboard.css'; // Separate CSS file for Participant Dashboard
import Logout from '../Logout/Logout';
import ProgressOverview from '../ProgressOverview/ProgressOverview'; // Import ProgressOverview
import QuizPerformance from '../Quiz/QuizPerformance'; // Import QuizPerformance


const ParticipantDashboard = () => {
  const navigate = useNavigate();
  const [showProgress, setShowProgress] = useState(false); // State to toggle progress visibility
  const userId = 5; // Replace with dynamic user ID if needed
  const [showQuizPerformance, setShowQuizPerformance] = useState(false); 


  const handleShowProgress = () => {
    setShowProgress((prev) => !prev); // Toggle progress overview
  };


  const handleShowQuizPerformance = () => {
    setShowQuizPerformance((prev) => !prev); // Toggle quiz performance
  };

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
          <li onClick={handleShowProgress}>Progress Overview</li> {/* Add link to toggle ProgressOverview */}
          <li onClick={handleShowQuizPerformance}>Quiz Performance</li> 
        </ul>
        <Logout />
      </aside>

      {/* Main Content */}
      <div className="main-content">
        <header className="main-header">
          <h1>Welcome, Participant!</h1>
        </header>
        {showProgress && <ProgressOverview userId={userId} />} {/* Render ProgressOverview conditionally */}
        {showQuizPerformance && <QuizPerformance userId={userId}/>} {/* Conditional rendering of QuizPerformance */}


      </div>
    </div>
  );
};

export default ParticipantDashboard;


// import React from 'react';
// import { useNavigate } from 'react-router-dom';
// import './Participant-Dashboard.css'; // Separate CSS file for Participant Dashboard
// import Logout from '../Logout/Logout';

// const ParticipantDashboard = () => {
//   const navigate = useNavigate();

//   return (
//     <div className="dashboard-container">
//       {/* Sidebar */}
//       <aside className="sidebar">
//         <h2>Participant Dashboard</h2>
//         <ul className="sidebar-menu">
//           <li onClick={() => navigate('/user-course-list')}>Courses List</li>
//           <li onClick={() => navigate('/enrolled')}>Enrolled</li>
//           <li onClick={() => navigate('/unenrolled')}>Not Enrolled</li>
//           <li onClick={() => navigate('/completed')}>Completed</li>
//         </ul>
//         <Logout />
//       </aside>

//       {/* Main Content */}
//       <div className="main-content">
//         <header className="main-header">
//           <h1>Welcome, Participant!</h1>
//         </header>
//       </div>
//     </div>
//   );
// };

// export default ParticipantDashboard;