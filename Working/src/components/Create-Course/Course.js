import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const CreateCourse = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const userType = location.state?.userType || "hr"; // Default to "hr" if not provided

  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [duration, setDuration] = useState("");
  const [courseData, setCourseData] = useState({
    courseTitle: "",
    description: "",
    instructor: "",
  });
  const [instructors, setInstructors] = useState([]); // Stores fetched instructors

  // Fetch instructors when the component mounts
  useEffect(() => {
    const fetchInstructors = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/instructors");
        if (response.ok) {
          const data = await response.json();
          setInstructors(data);
        } else {
          console.error("Failed to fetch instructors.");
        }
      } catch (error) {
        console.error("Error fetching instructors:", error);
      }
    };
    fetchInstructors();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCourseData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleStartDateChange = (e) => {
    const newStartDate = e.target.value;
    setStartDate(newStartDate);

    if (duration > 0) {
      const calculatedEndDate = new Date(newStartDate);
      calculatedEndDate.setDate(calculatedEndDate.getDate() + duration * 7);
      setEndDate(calculatedEndDate.toISOString().split("T")[0]);
    } else {
      setEndDate("");
    }
  };

  const handleDurationChange = (e) => {
    const weeks = parseInt(e.target.value, 10);
    setDuration(weeks);

    if (startDate && weeks > 0) {
      const calculatedEndDate = new Date(startDate);
      calculatedEndDate.setDate(calculatedEndDate.getDate() + weeks * 7);
      setEndDate(calculatedEndDate.toISOString().split("T")[0]);
    } else {
      setEndDate("");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      course_name: courseData.courseTitle,
      description: courseData.description,
      start_date: startDate,
      end_date: endDate,
      instructor_id: courseData.instructor,
    };

    try {
      const response = await fetch("http://127.0.0.1:5000/api/courses", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        const data = await response.json();
        const createdCourseId = data.course_id;

        const notifyResponse = await fetch(
          "http://127.0.0.1:5000/api/courses/notify",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ course_id: createdCourseId }),
          }
        );

        if (notifyResponse.ok) {
          alert("Course created and notification sent successfully!");
        } else {
          const notifyError = await notifyResponse.json();
          alert(`Failed to send notification: ${notifyError.message}`);
        }

        navigate(userType === "hr" ? "/hr-dashboard" : "/instructor-dashboard");
      } else {
        const error = await response.json();
        alert(`Error: ${error.message || "Failed to create course"}`);
      }
    } catch (error) {
      console.error("Error:", error);
      alert(`Error: ${error.message || "Failed to create course. Please try again later."}`);
    }
  };

  const handleCancel = () => {
    navigate(userType === "hr" ? "/hr-dashboard" : "/instructor-dashboard");
  };

  const styles = {
    container: {
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      minHeight: "100vh",
      margin: 0,
      fontFamily: "Arial, sans-serif",
      background: "linear-gradient(to bottom, #89f7fe, #66a6ff)",
    },
    formSection: {
      width: "100%",
      maxWidth: "500px",
      textAlign: "center",
      background: "white",
      padding: "20px",
      borderRadius: "10px",
      boxShadow: "0 4px 6px rgba(0, 0, 0, 0.2)",
    },
    formTitle: {
      fontSize: "24px",
      marginBottom: "20px",
      color: "#333",
    },
    form: {
      display: "flex",
      flexDirection: "column",
      gap: "10px",
    },
    input: {
      width: "100%",
      padding: "8px",
      border: "1px solid #ccc",
      borderRadius: "5px",
      fontSize: "14px",
    },
    buttons: {
      display: "flex",
      gap: "10px",
      marginTop: "20px",
    },
    submitButton: {
      padding: "8px 20px",
      background: "linear-gradient(to right, #ff416c, #ff4b2b)",
      color: "white",
      border: "none",
      borderRadius: "20px",
      fontSize: "14px",
      cursor: "pointer",
    },
    cancelButton: {
      padding: "8px 20px",
      background: "linear-gradient(to right, #6a11cb, #2575fc)",
      color: "white",
      border: "none",
      borderRadius: "20px",
      fontSize: "14px",
      cursor: "pointer",
    },
  };

  return (
    <div style={styles.container}>
      <div style={styles.formSection}>
        <h2 style={styles.formTitle}>CREATE NEW COURSE</h2>
        <form style={styles.form} onSubmit={handleSubmit}>
          <input
            type="text"
            name="courseTitle"
            placeholder="Course Title"
            style={styles.input}
            value={courseData.courseTitle}
            onChange={handleInputChange}
            required
          />
          <textarea
            name="description"
            placeholder="Description"
            style={styles.input}
            value={courseData.description}
            onChange={handleInputChange}
            required
          ></textarea>
          <select
            name="instructor"
            style={styles.input}
            value={courseData.instructor}
            onChange={handleInputChange}
            required
          >
            <option value="">Select Instructor</option>
            {instructors.map((instructor) => (
              <option key={instructor.user_id} value={instructor.user_id}>
                {instructor.first_name} {instructor.last_name}
              </option>
            ))}
          </select>
          <input
            type="date"
            style={styles.input}
            value={startDate}
            onChange={handleStartDateChange}
            required
          />
          <input
            type="number"
            style={styles.input}
            placeholder="Duration (weeks)"
            value={duration}
            onChange={handleDurationChange}
            required
          />
          <input
            type="text"
            style={styles.input}
            placeholder="End Date"
            value={endDate}
            readOnly
          />
          <div style={styles.buttons}>
            <button type="submit" style={styles.submitButton}>
              SUBMIT
            </button>
            <button type="button" style={styles.cancelButton} onClick={handleCancel}>
              CANCEL
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateCourse;