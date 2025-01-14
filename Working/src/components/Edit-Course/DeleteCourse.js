import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {useLocation, useNavigate } from 'react-router-dom';
import './DeleteCourse.css';  // Add styling for the delete course page

const DeleteCourse = () => {
  const [courses, setCourses] = useState([]);
  const [error, setError] = useState('');
  const location = useLocation();
    const navigate = useNavigate();
    const userType = location.state?.userType || "hr"; // Default to "hr" if not provided

  // Fetch courses on component mount
  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/courses');
        setCourses(response.data || []);
      } catch (err) {
        console.error('Error fetching courses:', err);
        setError('Failed to fetch courses.');
      }
    };

    fetchCourses();
  }, []);

  // Handle deleting a course
  const handleDelete = async (courseId) => {
    if (window.confirm('Are you sure you want to delete this course?')) {
      try {
        await axios.post('http://127.0.0.1:5000/api/courses/delete-notify', {
          course_id: courseId,
        });
        
        await axios.delete(`http://127.0.0.1:5000/api/courses/${courseId}`);
        
        setCourses(courses.filter(course => course.course_id !== courseId));  // Update the course list
        alert('Course deleted and notification sent successfully');
      } catch (err) {
        console.error('Error deleting course:', err);
        setError('Failed to delete the course.');
      }
    }
  };

  // Handle Back button
  const handleBack = () => {
    navigate(userType === "hr" ? "/hr-dashboard" : "/instructor-dashboard");
  };

  return (
    <div className="delete-course-container">
      <h1 className="page-header">Delete Courses</h1>
      {/* Back Button */}
      <div className="header-container">
        <button className="back-button" onClick={handleBack}>
          Back
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}
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
              <button onClick={() => handleDelete(course.course_id)} className="delete-button">
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DeleteCourse;
