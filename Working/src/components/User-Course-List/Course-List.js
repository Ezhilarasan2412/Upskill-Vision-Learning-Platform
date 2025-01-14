import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Course-List.css';

const CoursesList = () => {
  const [courses, setCourses] = useState([]);
  const [userRole, setUserRole] = useState('');
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/courses`, {
          params: { user_id: userId },
        });
        if (Array.isArray(response.data)) {
          setCourses(response.data);
        } else {
          setCourses([]);
          setError('No courses found.');
        }
      } catch (err) {
        console.error('Error fetching courses:', err);
        setError('Failed to fetch courses.');
      }
    };

    const fetchUserRole = async () => {
      try {
        const email = localStorage.getItem('user_email'); // Retrieve email from local storage
        if (!email) {
          throw new Error('Email not found in local storage.');
        }
    
        const response = await axios.post(
          'http://127.0.0.1:5000/api/get_user_role',
          { email }, // Send email in the request body
          { withCredentials: false } // No cookies needed
        );
    
        const { role_id, user_id } = response.data;
        setUserRole(role_id);
        setUserId(user_id);
      } catch (err) {
        console.error('Error fetching user role:', err);
        // setError('Failed to fetch user role.');
      }
    };
    

    fetchUserRole();
    fetchCourses();
  }, [userId]);

  const updateCourseStatus = (courseId, newStatus) => {
    setCourses((prevCourses) =>
      prevCourses.map((course) =>
        course.course_id === courseId
          ? { ...course, enrollment_status: newStatus }
          : course
      )
    );
  };

  const handleEnroll = async (courseId) => {
    try {
      const response = await axios.post(`http://127.0.0.1:5000/api/courses/${courseId}/enroll`, {
        user_id: userId,
      });
      setSuccessMessage(response.data.message);
      updateCourseStatus(courseId, 'Enrolled');
    } catch (err) {
      console.error('Error enrolling in course:', err);
      setError('Failed to enroll in course.');
    }
  };

  const handleUnenroll = async (courseId) => {
    try {
      const response = await axios.post(`http://127.0.0.1:5000/api/courses/${courseId}/unenroll`, {
        user_id: userId,
      });
      setSuccessMessage(response.data.message);
      updateCourseStatus(courseId, 'Not Enrolled');
    } catch (err) {
      console.error('Error unenrolling from course:', err);
      setError('Failed to unenroll from course.');
    }
  };

  const handleComplete = async (courseId) => {
    try {
      const response = await axios.post(`http://127.0.0.1:5000/api/courses/${courseId}/complete`, {
        user_id: userId,
      });
      setSuccessMessage(response.data.message);
      updateCourseStatus(courseId, 'Completed');
    } catch (err) {
      console.error('Error marking course as complete:', err);
      setError('Failed to mark course as complete.');
    }
  };

  useEffect(() => {
    if (error || successMessage) {
      const timer = setTimeout(() => {
        setError('');
        setSuccessMessage('');
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [error, successMessage]);

  return (
    <div className="courses-container">
      <h1 className="page-header">Courses List</h1>
      {error && <div className="error-message">{error}</div>}
      {successMessage && <div className="success-message">{successMessage}</div>}
      {courses.length === 0 ? (
        <p>No courses available.</p>
      ) : (
        <div className="courses-grid">
          {courses.map((course) => (
            <div key={course.course_id} className="course-card">
              <h2>{course.course_name}</h2>
              <p><strong>Description:</strong> {course.description}</p>
              <p><strong>Instructor:</strong> {course.instructor_name}</p>
              <p>
                <strong>Start Date:</strong> {course.start_date} <br />
                <strong>End Date:</strong> {course.end_date}
              </p>
              <p><strong>Status:</strong> {course.enrollment_status}</p>
              {userRole === '4' && ( // Participant-specific actions
                <div className="course-actions">
                  {course.enrollment_status === 'Not Enrolled' && (
                    <button onClick={() => handleEnroll(course.course_id)}>Enroll</button>
                  )}
                  {course.enrollment_status === 'Enrolled' && (
                    <>
                      <button onClick={() => handleUnenroll(course.course_id)}>Unenroll</button>
                      <button onClick={() => handleComplete(course.course_id)}>Complete</button>
                    </>
                  )}
                  {course.enrollment_status === 'Completed' && <p>Course Completed</p>}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CoursesList;
