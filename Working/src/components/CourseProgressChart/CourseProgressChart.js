import React, { useState, useEffect } from 'react';
import { Pie } from 'react-chartjs-2';
import axios from 'axios';

const CourseProgressChart = () => {
  const [completed, setCompleted] = useState(0);
  const [inProgress, setInProgress] = useState(0);

  useEffect(() => {
    const fetchCourseData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/course-status');
        setCompleted(response.data.completed);
        setInProgress(response.data.inProgress);
      } catch (error) {
        console.error('Failed to fetch course data:', error);
      }
    };

    fetchCourseData();
  }, []);

  const data = {
    labels: ['Completed', 'In Progress'],
    datasets: [
      {
        label: 'Courses',
        data: [completed, inProgress],
        backgroundColor: ['#4CAF50', '#FF9800'],
        hoverOffset: 4,
      },
    ],
  };

  const options = {
    plugins: {
      legend: { position: 'top' },
    },
    responsive: true,
    maintainAspectRatio: false,
  };

  return (
    <div style={{ width: '400px', height: '400px', margin: '0 auto' }}>
      <Pie data={data} options={options} />
    </div>
  );
};

export default CourseProgressChart;
