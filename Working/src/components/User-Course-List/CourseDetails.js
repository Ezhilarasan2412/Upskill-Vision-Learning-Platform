import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom"; // Import Link for navigation
import "./CourseDetails.css";

const CourseDetails = () => {
  const { courseId } = useParams();
  const [courseDetails, setCourseDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCourseDetails = async () => {
      const userId = parseInt(localStorage.getItem("user_id"));
      if (!userId) {
        setError("User is not logged in");
        setLoading(false);
        return;
      }

      try {
        const response = await fetch(
          `http://localhost:5000/api/course-details/${courseId}?user_id=${userId}`
        );
        if (!response.ok) {
          throw new Error("Failed to fetch course details");
        }
        const data = await response.json();

        // Calculate overall progress if not provided by the backend
        const completedModules = data.modules.filter(
          (module) => module.completion_status === "completed"
        ).length;

        const totalModules = data.modules.length;
        const overallProgress = totalModules > 0 ? (completedModules / totalModules) * 100 : 0;

        setCourseDetails({
          ...data,
          overallProgress: overallProgress,
        });
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchCourseDetails();
  }, [courseId]);

  const handleResourceCompletion = async (resourceId, moduleId) => {
    const userId = parseInt(localStorage.getItem("user_id"));
    if (!userId) {
      alert("User is not logged in");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/api/complete-resource", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, resource_id: resourceId }),
      });

      if (!response.ok) {
        throw new Error("Failed to mark resource as completed");
      }

      setCourseDetails((prevDetails) => {
        const updatedModules = prevDetails.modules.map((module) => {
          if (module.module_id === moduleId) {
            const updatedResources = module.resources.map((resource) => {
              if (resource.resource_id === resourceId) {
                return { ...resource, completed: true };
              }
              return resource;
            });

            const allCompleted = updatedResources.every((res) => res.completed);
            return {
              ...module,
              resources: updatedResources,
              completion_status: allCompleted ? "completed" : module.completion_status,
            };
          }
          return module;
        });

        const completedModules = updatedModules.filter(
          (module) => module.completion_status === "completed"
        ).length;

        const totalModules = updatedModules.length;

        return {
          ...prevDetails,
          modules: updatedModules,
          overallProgress: (completedModules / totalModules) * 100,
        };
      });
    } catch (err) {
      alert(err.message);
    }
  };

  if (loading) return <div>Loading course details...</div>;
  if (error)
    return (
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
          background: "linear-gradient(to right,rgb(81, 102, 208), #2575fc)",
        }}
      >
        <div
          style={{
            backgroundColor: "#fff",
            padding: "20px 40px",
            borderRadius: "10px",
            boxShadow: "0 4px 12px rgba(0, 0, 0, 0.1)",
            textAlign: "center",
            color: "#333",
            fontSize: "24px",
            fontWeight: "bold",
            width: "300px",
          }}
        >
          Material is not added
        </div>
      </div>
    );

  if (!courseDetails) return <div>No course details found.</div>;

  return (
    <div className="course-details-container">
      <h1>{courseDetails.course_name}</h1>
      <p>{courseDetails.description}</p>

      <h3>Modules:</h3>
      {courseDetails.modules.map((module) => (
        <div key={module.module_id} className="module-item">
          <div className="module-header">
            <strong>{module.module_title}</strong>
            <span> ({module.completion_status})</span>
          </div>

          <div className="module-resources">
            <details>
              <summary>View Resources</summary>
              <ul>
                {module.resources.map((resource) => (
                  <li key={resource.resource_id} className="resource-item">
                    <input
                      type="checkbox"
                      checked={resource.completed || false}
                      onChange={() => handleResourceCompletion(resource.resource_id, module.module_id)}
                      disabled={resource.completed}
                    />
                    <span>{resource.resource_title}</span>
                    {resource.resource_type === "link" && (
                      <a href={resource.resource_content} target="_blank" rel="noopener noreferrer">
                           Open Link
                      </a>
                    )}
                    {resource.resource_type === "file" && (
                      <a href={resource.resource_content} target="_blank" rel="noopener noreferrer">
                           Open File
                      </a>
                    )}
                    {resource.resource_type === "text" && (
                      <div>{resource.resource_content}</div>
                    )}
                  </li>
                ))}
              </ul>
            </details>
          </div>

          {/* Add Quiz Link */}
          <div className="quiz-link">
            <Link to={`/quiz/${module.quiz_id}/${module.module_id}/attempt`} className="quiz-button">
              Take Quiz for {module.module_title}
            </Link>
          </div>
        </div>
      ))}

      <h3>Overall Progress:</h3>
      <progress value={courseDetails.overallProgress} max={100} />
      <div>{Math.round(courseDetails.overallProgress)}%</div>
    </div>
  );
};

export default CourseDetails;
