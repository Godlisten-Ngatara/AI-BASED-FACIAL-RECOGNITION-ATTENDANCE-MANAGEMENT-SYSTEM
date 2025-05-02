import { useState } from 'react';
import Header from './components/Header';
import TabNavigation from './components/TabsNavigation';
import StudentWiseView from './views/StudentWiseView';
import ClassWiseView from './views/ClassWiseView';
import DetailedReportView from './views/DetailedReportView';

function App() {
  const [activeTab, setActiveTab] = useState('student');

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="container mx-auto px-4 py-6">
        <TabNavigation activeTab={activeTab} setActiveTab={setActiveTab} />
        
        {activeTab === 'student' && <StudentWiseView />}
        {activeTab === 'class' && <ClassWiseView />}
        {activeTab === 'report' && <DetailedReportView />}
      </main>
    </div>
  );
}

export default App;