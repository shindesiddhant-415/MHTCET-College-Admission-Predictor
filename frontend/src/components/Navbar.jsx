import React from 'react';
import { 
  LayoutDashboard, 
  Target, 
  TrendingUp, 
  Cpu, 
  Scale, 
  BookOpen 
} from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab }) {
  const tabs = [
    { id: 'overview', label: 'Overview', icon: LayoutDashboard },
    { id: 'recommend', label: 'AI Predictor & Recommender', icon: Target },
    { id: 'trends', label: 'Cutoff Trends', icon: TrendingUp },
    { id: 'performance', label: 'Model Benchmarks', icon: Cpu },
    { id: 'compare', label: 'College Comparison', icon: Scale },
    { id: 'dataset', label: 'Dataset & Ethics', icon: BookOpen },
  ];

  return (
    <header className="navbar">
      <div className="nav-content">
        <div className="brand">
          <span className="brand-icon">🎓</span>
          <div>
            <div className="brand-title">MHT-CET Admission AI</div>
            <div className="brand-subtitle">Prediction & Personalized Recommendation System</div>
          </div>
        </div>

        <nav className="nav-tabs">
          {tabs.map(tab => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                className={`nav-tab ${isActive ? 'active' : ''}`}
                onClick={() => setActiveTab(tab.id)}
              >
                <Icon size={16} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
