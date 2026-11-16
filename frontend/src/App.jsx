import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import OverviewTab from './components/OverviewTab';
import RecommendationsTab from './components/RecommendationsTab';
import CutoffTrendsTab from './components/CutoffTrendsTab';
import ModelPerformanceTab from './components/ModelPerformanceTab';
import CollegeComparisonTab from './components/CollegeComparisonTab';
import DatasetInfoTab from './components/DatasetInfoTab';
import { fetchOverview, fetchFilters } from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [overview, setOverview] = useState(null);
  const [filters, setFilters] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function initData() {
      try {
        const [ovData, fltData] = await Promise.all([
          fetchOverview(),
          fetchFilters()
        ]);
        setOverview(ovData);
        setFilters(fltData);
      } catch (err) {
        console.error('API Init Error:', err);
      } finally {
        setLoading(false);
      }
    }
    initData();
  }, []);

  return (
    <div className="app-container">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="main-content">
        {activeTab === 'overview' && (
          <OverviewTab overview={overview} setActiveTab={setActiveTab} />
        )}
        {activeTab === 'recommend' && (
          <RecommendationsTab filters={filters} />
        )}
        {activeTab === 'trends' && (
          <CutoffTrendsTab filters={filters} />
        )}
        {activeTab === 'performance' && (
          <ModelPerformanceTab />
        )}
        {activeTab === 'compare' && (
          <CollegeComparisonTab filters={filters} />
        )}
        {activeTab === 'dataset' && (
          <DatasetInfoTab />
        )}
      </main>

      <footer className="footer">
        <p>
          🎓 <strong>MHT-CET College Admission Predictor & Recommender</strong> | Practical No. 07 Mini-Project
        </p>
        <p style={{ marginTop: '0.25rem', fontSize: '0.75rem' }}>
          Third Year B.Tech – Artificial Intelligence & Machine Learning Lab (`2311331L`) | MIT Academy of Engineering, Pune
        </p>
      </footer>
    </div>
  );
}
