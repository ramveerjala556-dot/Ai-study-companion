import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Calendar, Bell, AlertTriangle, List, CheckCircle } from 'lucide-react';

const Dashboard = () => {
  const [reminders, setReminders] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const resReminders = await axios.get('http://localhost:8000/ai/reminders/');
        const resSubjects = await axios.get('http://localhost:8000/subjects/');
        setReminders(resReminders.data);
        setSubjects(resSubjects.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const getMasteryColor = (mastery) => {
    if (mastery < 0.3) return 'bg-red-500';
    if (mastery < 0.6) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  return (
    <div className="p-6 bg-gray-50 min-h-screen text-gray-900">
      <div className="max-w-6xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Study Dashboard</h1>

        {/* Smart Reminders Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-xl shadow-md border-l-4 border-yellow-500">
            <h2 className="text-xl font-bold flex items-center mb-4 text-yellow-700">
              <Bell className="mr-2" /> Smart Reminders
            </h2>
            <div className="space-y-4">
              {reminders.filter(r => r.type === 'exam_reminder').map((r, i) => (
                <div key={i} className="flex items-start p-3 bg-yellow-50 rounded-lg">
                  <AlertTriangle className="text-yellow-600 mr-3 mt-1" size={20} />
                  <p className="text-yellow-800">{r.message}</p>
                </div>
              ))}
              {reminders.length === 0 && <p className="text-gray-500 italic">No urgent reminders. Keep it up!</p>}
            </div>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md border-l-4 border-blue-500">
            <h2 className="text-xl font-bold flex items-center mb-4 text-blue-700">
              <List className="mr-2" /> AI Study Suggestions
            </h2>
            <div className="space-y-4">
              {reminders.filter(r => r.type === 'study_suggestion').map((r, i) => (
                <div key={i} className="p-3 bg-blue-50 rounded-lg whitespace-pre-line text-blue-900">
                  {r.message}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Forgetting Risk Heatmap */}
        <div className="bg-white p-6 rounded-xl shadow-md">
          <h2 className="text-xl font-bold flex items-center mb-6 text-red-700">
            <AlertTriangle className="mr-2" /> Retention & Forgetting Risk
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
            {subjects.flatMap(s => s.topics).map((t, i) => {
              // Mastery is simulated here as backend doesn't return it per topic yet
              // but in a real app, the API would return srs_score.
              const mastery = Math.random(); // Mocking for visualization
              return (
                <div key={i} className="flex flex-col items-center p-2 border rounded shadow-sm">
                  <div className={`w-12 h-12 rounded-lg mb-2 ${getMasteryColor(mastery)} opacity-80 flex items-center justify-center text-white font-bold`}>
                    {Math.round(mastery * 100)}%
                  </div>
                  <span className="text-xs text-center font-medium truncate w-full">{t.name}</span>
                </div>
              );
            })}
          </div>
          <div className="mt-4 flex justify-end space-x-4 text-xs font-bold uppercase tracking-wider text-gray-500">
              <span className="flex items-center"><span className="w-3 h-3 bg-red-500 rounded-full mr-1"></span> Critical</span>
              <span className="flex items-center"><span className="w-3 h-3 bg-yellow-500 rounded-full mr-1"></span> Review</span>
              <span className="flex items-center"><span className="w-3 h-3 bg-green-500 rounded-full mr-1"></span> Mastered</span>
          </div>
        </div>

        {/* Subjects & Progress Section */}
        <div className="bg-white p-6 rounded-xl shadow-md">
          <h2 className="text-xl font-bold flex items-center mb-6 text-gray-800">
            <CheckCircle className="mr-2 text-green-600" /> My Subjects
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {subjects.map((s, i) => (
              <div key={i} className="p-4 border rounded-lg hover:border-blue-400 hover:shadow-sm transition-all bg-white group">
                <h3 className="font-bold text-lg mb-2 group-hover:text-blue-600">{s.name}</h3>
                <p className="text-gray-500 text-sm">{s.topics.length} topics enrolled</p>
                <div className="mt-4 w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-blue-600 h-2 rounded-full w-[45%]"></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
