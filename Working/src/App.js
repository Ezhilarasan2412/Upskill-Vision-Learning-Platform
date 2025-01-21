import React from 'react'; 
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login/Login'; 
import ForgotPasswordPage from './components/Forgot-Password/ForgotPassword';
import ResetPasswordPage from './components/Reset-Password/ResetPassword'; 
import SignUp from './components/Signup/SignUp';
import Course from './components/Create-Course/Course';
import HRDashboard from './components/HR-Dashboard/HR-Dashboard';
import ManagerDashboard from './components/Manager-Dashboard/Manager-Dashboard';
import InstructorDashboard from './components/Instructor-Dashboard/Instructor-Dashboard';
import ParticipantDashboard from './components/Participant-Dashboard/Participant-Dashboard';
import CourseList from './components/User-Course-List/Course-List';
import CourseEditPage from './components/Edit-Course/CourseEditPage'; // Updated to match component name
import EditCourse  from './components/Edit-Course/EditCourse';
import DeleteCourse from './components/Edit-Course/DeleteCourse';
import UserCourselist from './components/User-Course-List/UserCourselist';
import Enrolled from './components/User-Course-List/Enrolled';
import Unenrolled from './components/User-Course-List/Unenrolled';
import Completed from './components/User-Course-List/Completed';
import CourseDetails from './components/User-Course-List/CourseDetails';
import AddModules from './components/Edit-Course/AddModules';
import AddResource from './components/Edit-Course/AddResource';
import QuizForm from './components/Quiz/QuizForm';
import QuestionForm from './components/Quiz/QuestionForm';
import QuizDetails from './components/Quiz/QuizDetails';
import PerformanceDashboard from './components/Performance-Dashboard/Performance-Dashboard'
import QuizAttempt from "./components/Quiz/QuizAttempt";
import QuizPerformance from './components/Quiz/QuizPerformance'; 





const App = () => {
  return (
    <Router> 
      <Routes> 
        {/* Route for LoginPage */}
        <Route path="/" element={<Login />} /> 
        
        {/* Route for ForgotPasswordPage */}
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        
        {/* Route for ResetPasswordPage */}
        <Route path="/reset-password" element={<ResetPasswordPage />} />
        
        {/* Route for SignUpPage */}
        <Route path="/signup" element={<SignUp />} /> 

        {/* Route for Course Page */}
        <Route path="/courses" element={<Course />} /> 

        {/* Dashboard Routes */}
        <Route path="/hr-dashboard" element={<HRDashboard />} />
        <Route path="/manager-dashboard" element={<ManagerDashboard />} />
        <Route path="/instructor-dashboard" element={<InstructorDashboard />} />
        <Route path="/participant-dashboard" element={<ParticipantDashboard />} />

        {/* Course List Route */}
        <Route path="/course-list" element={<CourseList />} />

        {/* Course Edit Route */}
        <Route path="/course-edit" element={<CourseEditPage />} />
        <Route path="/course-edit/:courseId" element={<CourseEditPage />} /> {/* For individual course editing */}

        <Route path="/edit-course/:courseId" element={<EditCourse />} />

        <Route path="/delete-course" element={<DeleteCourse />} />

        <Route path="/user-course-list" element={<UserCourselist />} />

        <Route path="/enrolled" element={<Enrolled />} />

        <Route path="/unenrolled" element={<Unenrolled />} />

        <Route path="/completed" element={<Completed />} />

        <Route path="/course-details/:courseId" element={<CourseDetails />} />

        <Route path="/add-modules" element={<AddModules />} />

        <Route path="/add-resource" element={<AddResource />} />

        <Route path="/add-quiz/:courseId" element={<QuizForm />} />

        <Route path="/add-question/:quizId/:totalScore" element={<QuestionForm />} />

        <Route path="/quiz-details/:quizId/:moduleId" element={<QuizDetails />} />


        <Route path="/quiz/:quizId/:totalScore" element={<QuestionForm />} />

        <Route path="/performance-dashboard" element={<PerformanceDashboard />} />

        <Route path="/quiz/:quizId/:moduleId/attempt" element={<QuizAttempt />} />

        <Route path="/quiz-performance" element={<QuizPerformance  />} />


      </Routes>
    </Router>
  );
};

export default App;