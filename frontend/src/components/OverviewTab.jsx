import React from 'react';
import { Database, Building2, Award, Calendar, CheckCircle2, ShieldCheck, Zap } from 'lucide-react';

export default function OverviewTab({ overview, setActiveTab }) {
  if (!overview) {
    return <div className="card">Loading overview data...</div>;
  }

  return (
    <div>
      {/* KPI Cards */}
      <div className="kpi-grid">
        <div className="kpi-card">
          <div className="kpi-icon-wrap">
            <Database size={24} />
          </div>
          <div>
            <div className="kpi-value">{overview.total_records.toLocaleString()}</div>
            <div className="kpi-label">Normalized CAP Records</div>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-icon-wrap">
            <Building2 size={24} />
          </div>
          <div>
            <div className="kpi-value">{overview.total_colleges}</div>
            <div className="kpi-label">Engineering Colleges</div>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-icon-wrap">
            <Award size={24} />
          </div>
          <div>
            <div className="kpi-value">{overview.validation_mae.toFixed(4)}</div>
            <div className="kpi-label">Best Model MAE ({overview.best_model_name.slice(0, 10)})</div>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-icon-wrap">
            <Calendar size={24} />
          </div>
          <div>
            <div className="kpi-value">{overview.forecast_year}</div>
            <div className="kpi-label">Target Admission Cycle</div>
          </div>
        </div>
      </div>

      <div className="grid-2">
        {/* Left Column: Project Motivation */}
        <div className="card">
          <h3 className="card-title">
            <Zap size={20} color="#00509d" />
            Project Objectives & Real-World Impact
          </h3>
          <p className="card-subtitle">
            AI-based decision-support system for Maharashtra Centralized Admission Process (CAP)
          </p>
          <div style={{ fontSize: '0.9rem', color: '#334155', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <p>
              Students preparing for Maharashtra engineering admissions struggle to compare previous CAP cutoffs spread 
              across hundreds of official PDF pages, 4 academic years, 4 CAP rounds, and 14+ seat categories.
            </p>
            <p>
              This system extracts, validates, and normalizes official CET Cell cutoffs, builds chronological lag features (t-1, t-2) 
              without look-ahead bias, evaluates five regression algorithms, and provides transparent recommendations.
            </p>
            <div className="alert alert-info" style={{ marginTop: '0.5rem' }}>
              <ShieldCheck size={20} />
              <div>
                <strong>Academic Decision-Support Tool:</strong> Provides data-driven estimates and suitability grouping. 
                Final allotments are governed by official Maharashtra State CET Cell procedures.
              </div>
            </div>
            <div style={{ marginTop: '0.75rem' }}>
              <button className="btn btn-primary" onClick={() => setActiveTab('recommend')}>
                🚀 Launch AI Predictor & Recommendation Engine
              </button>
            </div>
          </div>
        </div>

        {/* Right Column: Key Capabilities */}
        <div className="card">
          <h3 className="card-title">
            <CheckCircle2 size={20} color="#10b981" />
            Key System Features
          </h3>
          <p className="card-subtitle">Engineered for academic rigor and practical utility</p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', fontSize: '0.9rem' }}>
            <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
              <span className="badge badge-safer">AUTOREGRESSIVE ML</span>
              <div>
                <strong>Chronological Forecasting:</strong> Evaluated strictly on held-out test year 2026–27 using prior-year lags ($t-1, t-2$).
              </div>
            </div>

            <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
              <span className="badge badge-moderate">GROUPING ENGINE</span>
              <div>
                <strong>Suitability Categorization:</strong> Transparent grouping into 🛡️ Safer, ⚖️ Moderate, and 🚀 Reach based on validation error margin ($M = 1.5 \times \text{MAE}$).
              </div>
            </div>

            <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
              <span className="badge badge-primary">FULL TRACEABILITY</span>
              <div>
                <strong>Audit Trail:</strong> Every cutoff links to its official source PDF and page number, with zero zero-imputation.
              </div>
            </div>

            <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
              <span className="badge badge-primary">SDG 4 & SDG 10</span>
              <div>
                <strong>Inclusive Higher Education:</strong> Reduces information asymmetry for first-generation and rural college aspirants across all reservation quotas.
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Dataset Statistics */}
      <div className="card">
        <h3 className="card-title">
          <Database size={20} color="#00509d" />
          Dataset Records Distribution
        </h3>
        <p className="card-subtitle">Normalized records across four official admission cycles</p>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem' }}>
          {Object.entries(overview.year_distribution || {}).map(([yr, count]) => (
            <div key={yr} style={{ background: '#f8fafc', padding: '1rem', borderRadius: '8px', border: '1px solid #e2e8f0', textAlign: 'center' }}>
              <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 600 }}>{yr}</div>
              <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#00296b' }}>{count.toLocaleString()}</div>
              <div style={{ fontSize: '0.75rem', color: '#10b981', fontWeight: 600 }}>Validated Records</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
