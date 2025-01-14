import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useLocation, useNavigate } from 'react-router-dom';
import './CourseEditPage.css';

const CourseEditPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const userType = location.state?.userType || 'hr';
  const [courses, setCourses] = useState([]);
  const [error, setError] = useState('');

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

  const handleEdit = (courseId) => {
    navigate(`/edit-course/${courseId}`, { state: { userType } });
  };

  const handleDelete = async (courseId) => {
    if (window.confirm('Are you sure you want to delete this course?')) {
      try {
        await axios.post('http://127.0.0.1:5000/api/courses/delete-notify', {
          course_id: courseId,
        });

        await axios.delete(`http://127.0.0.1:5000/api/courses/${courseId}`);

        setCourses(courses.filter((course) => course.course_id !== courseId));
        alert('Course deleted and notification sent successfully');
      } catch (err) {
        console.error('Error deleting course:', err);
        setError('Failed to delete the course.');
      }
    }
  };

  const handleBack = () => {
    navigate(userType === 'hr' ? '/hr-dashboard' : '/instructor-dashboard');
  };

  return (
    <div className="course-edit-container">
      <h1 className="page-header">Edit Courses</h1>
      <button className="back-button" onClick={handleBack}>Back</button>

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
              <div className="button-row">
                <button onClick={() => handleEdit(course.course_id)} className="blue-button">Edit Course</button>
                <button onClick={() => handleDelete(course.course_id)} className="blue-button">Delete Course</button>
              </div>
              <div className="button-row">
                <button onClick={() => navigate('/add-modules/', { state: { course_id: course.course_id,userType: 'hr' } })} className="blue-button">Add Modules</button>
                <button onClick={() => navigate('/add-resource', { state: { course_id: course.course_id, module_id: module.module_id,userType: 'hr' } })} className="blue-button">Add Resources</button>
                <button onClick={() => navigate(`/add-quiz/${course.course_id}`, { state: { userType } })} className="blue-button">Add Quiz</button>              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CourseEditPage;