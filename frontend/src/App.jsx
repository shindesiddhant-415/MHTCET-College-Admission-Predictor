import React, { useState, useEffect, Component } from 'react';
import Navbar from './components/Navbar';
import OverviewTab from './components/OverviewTab';
import RecommendationsTab from './components/RecommendationsTab';
import CutoffTrendsTab from './components/CutoffTrendsTab';
import ModelPerformanceTab from './components/ModelPerformanceTab';
import CollegeComparisonTab from './components/CollegeComparisonTab';
import DatasetInfoTab from './components/DatasetInfoTab';
import { 
  fetchOverview, 
  fetchFilters, 
  checkBackendHealth,
  FALLBACK_OVERVIEW, 
  FALLBACK_FILTERS 
} from './services/api';
import { Wifi, WifiOff, AlertTriangle, RefreshCw } from 'lucide-react';

// Error Boundary to prevent any blank white screen
class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '3rem', maxWidth: '700px', margin: '4rem auto', fontFamily: 'system-ui, sans-serif' }}>
          <div style={{ background: '#fef2f2', border: '1px solid #fecaca', borderRadius: '12px', padding: '2rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: '#b91c1c', marginBottom: '1rem' }}>
              <AlertTriangle size={28} />
              <h2 style={{ margin: 0, fontSize: '1.4rem' }}>Application Render Notice</h2>
            </div>
            <p style={{ color: '#7f1d1d', marginBottom: '1rem', lineHeight: 1.6 }}>
              A UI component encountered an issue during rendering:
            </p>
            <pre style={{ background: '#ffffff', padding: '1rem', borderRadius: '8px', border: '1px solid #fee2e2', color: '#991b1b', fontSize: '0.85rem', overflowX: 'auto' }}>
              {this.state.error?.message || String(this.state.error)}
            </pre>
            <div style={{ marginTop: '1.5rem', display: 'flex', gap: '1rem' }}>
              <button 
                onClick={() => window.location.reload()} 
                style={{ background: '#00509d', color: '#fff', border: 'none', padding: '0.6rem 1.2rem', borderRadius: '8px', cursor: 'pointer', fontWeight: 600 }}
              >
                Reload Dashboard
              </button>
            </div>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

export default function App() {
  const [activeTab, setActiveTab] = useState(() => {
    try {
      const params = new URLSearchParams(window.location.search);
      return params.get('tab') || 'overview';
    } catch {
      return 'overview';
    }
  });

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    try {
      const url = new URL(window.location);
      url.searchParams.set('tab', tab);
      window.history.replaceState({}, '', url);
    } catch {}
  };
  // Initialize with verified data so UI renders immediately without a blank white screen
  const [overview, setOverview] = useState(FALLBACK_OVERVIEW);
  const [filters, setFilters] = useState(FALLBACK_FILTERS);
  const [backendOnline, setBackendOnline] = useState(null); // null = checking, true = live, false = offline
  const [checking, setChecking] = useState(false);

  const refreshBackendStatus = async () => {
    setChecking(true);
    const health = await checkBackendHealth();
    setBackendOnline(health.online);
    if (health.online) {
      try {
        const [ovData, fltData] = await Promise.all([
          fetchOverview(),
          fetchFilters()
        ]);
        if (ovData) setOverview(ovData);
        if (fltData) setFilters(fltData);
      } catch (err) {
        console.error('Data reload error:', err);
      }
    }
    setChecking(false);
  };

  useEffect(() => {
    refreshBackendStatus();
    // Periodically probe backend health every 15 seconds
    const interval = setInterval(refreshBackendStatus, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <ErrorBoundary>
      <div className="app-container">
        {/* Backend Connection Status Banner */}
        <div style={{
          background: backendOnline ? '#064e3b' : '#1e293b',
          color: '#ffffff',
          padding: '0.4rem 1.5rem',
          fontSize: '0.78rem',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '0.5rem',
          borderBottom: '1px solid rgba(255,255,255,0.1)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            {backendOnline ? (
              <>
                <Wifi size={14} color="#34d399" />
                <span>
                  <strong>FastAPI Backend:</strong> Connected & Serving Production Ridge Regressor (:8000)
                </span>
              </>
            ) : (
              <>
                <WifiOff size={14} color="#f59e0b" />
                <span>
                  <strong>Standalone Demo Mode:</strong> Serving from compiled assets. To connect live Python ML inference, run: <code>python -m uvicorn api.main:app --port 8000</code>
                </span>
              </>
            )}
          </div>
          <button 
            onClick={refreshBackendStatus}
            disabled={checking}
            style={{
              background: 'transparent',
              border: '1px solid rgba(255,255,255,0.3)',
              color: '#ffffff',
              padding: '0.15rem 0.6rem',
              borderRadius: '4px',
              fontSize: '0.72rem',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.3rem'
            }}
          >
            <RefreshCw size={11} className={checking ? 'spin' : ''} />
            {checking ? 'Checking...' : 'Check Backend'}
          </button>
        </div>

        <Navbar activeTab={activeTab} setActiveTab={handleTabChange} />

        <main className="main-content">
          {activeTab === 'overview' && (
            <OverviewTab overview={overview} setActiveTab={handleTabChange} />
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
    </ErrorBoundary>
  );
}
