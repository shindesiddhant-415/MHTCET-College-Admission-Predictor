import React, { useState } from 'react';
import { 
  Target, 
  Download, 
  Sparkles, 
  ShieldCheck, 
  AlertCircle, 
  CheckCircle2, 
  Filter,
  Info
} from 'lucide-react';
import { fetchRecommendations } from '../services/api';

export default function RecommendationsTab({ filters }) {
  // Input form state
  const [percentile, setPercentile] = useState(92.50);
  const [category, setCategory] = useState('GOPENS');
  const [pool, setPool] = useState('State Level');
  const [capRound, setCapRound] = useState(1);
  const [selectedBranches, setSelectedBranches] = useState([
    'Computer Engineering',
    'Information Technology',
    'Artificial Intelligence and Data Science'
  ]);
  const [selectedRegions, setSelectedRegions] = useState([]);
  const [topN, setTopN] = useState(20);

  // Result state
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);
  const [groupFilter, setGroupFilter] = useState('ALL');

  // Handle branch chip toggle
  const toggleBranch = (b) => {
    if (selectedBranches.includes(b)) {
      setSelectedBranches(selectedBranches.filter(x => x !== b));
    } else {
      setSelectedBranches([...selectedBranches, b]);
    }
  };

  // Handle region chip toggle
  const toggleRegion = (r) => {
    if (selectedRegions.includes(r)) {
      setSelectedRegions(selectedRegions.filter(x => x !== r));
    } else {
      setSelectedRegions([...selectedRegions, r]);
    }
  };

  // Execute recommendation
  const handleRecommend = async (e) => {
    if (e) e.preventDefault();
    if (percentile < 0 || percentile > 100) {
      setError('MHT-CET percentile must be between 0.00 and 100.00');
      return;
    }
    setError(null);
    setLoading(true);

    try {
      const data = await fetchRecommendations({
        student_percentile: parseFloat(percentile),
        seat_category: category,
        seat_pool: pool,
        preferred_branches: selectedBranches.length > 0 ? selectedBranches : null,
        preferred_regions: selectedRegions.length > 0 ? selectedRegions : null,
        cap_round: parseInt(capRound),
        top_n: parseInt(topN)
      });
      setResults(data);
    } catch (err) {
      setError(err.message || 'Failed to generate recommendations');
    } finally {
      setLoading(false);
    }
  };

  // Download Shortlist as CSV
  const downloadCSV = () => {
    if (!results || !results.recommendations) return;
    const recs = results.recommendations;
    const headers = [
      'Suitability Group',
      'Institute Name',
      'Branch Name',
      'City/Region',
      'Predicted Cutoff 2027',
      'Student Percentile',
      'Percentile Gap',
      '2026 Cutoff',
      'Recommendation Explanation'
    ];
    const rows = recs.map(r => [
      r.suitability_group,
      `"${r.institute_name}"`,
      `"${r.branch_name}"`,
      r.region,
      r.predicted_cutoff,
      r.student_percentile,
      r.percentile_gap > 0 ? `+${r.percentile_gap}` : r.percentile_gap,
      r.history_2026,
      `"${r.explanation}"`
    ]);
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `mht_cet_shortlist_${percentile}_${category}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Filter recommendations by selected group
  const filteredRecs = results?.recommendations ? results.recommendations.filter(r => {
    if (groupFilter === 'ALL') return true;
    return r.suitability_group === groupFilter;
  }) : [];

  const saferCount = results?.recommendations?.filter(r => r.suitability_group === 'Safer').length || 0;
  const modCount = results?.recommendations?.filter(r => r.suitability_group === 'Moderate').length || 0;
  const reachCount = results?.recommendations?.filter(r => r.suitability_group === 'Reach').length || 0;

  return (
    <div>
      <div className="grid-2">
        {/* Left Column: Form Controls */}
        <div className="card">
          <h3 className="card-title">
            <Target size={20} color="#00509d" />
            Candidate Admission Profile
          </h3>
          <p className="card-subtitle">
            Input your score and admission preferences for AI-driven option list generation
          </p>

          <form onSubmit={handleRecommend}>
            <div className="form-group">
              <label className="form-label">
                MHT-CET PCM Percentile (0.00 – 100.00)
              </label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="100"
                className="form-input"
                value={percentile}
                onChange={e => setPercentile(e.target.value)}
                required
              />
            </div>

            <div className="grid-2" style={{ gap: '1rem', marginBottom: '1rem' }}>
              <div>
                <label className="form-label">Seat Category Code</label>
                <select 
                  className="form-select"
                  value={category}
                  onChange={e => setCategory(e.target.value)}
                >
                  {filters?.categories?.map(c => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="form-label">Seat Reservation Pool</label>
                <select
                  className="form-select"
                  value={pool}
                  onChange={e => setPool(e.target.value)}
                >
                  {filters?.pools?.map(p => (
                    <option key={p} value={p}>{p}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Target CAP Round</label>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                {[1, 2, 3, 4].map(r => (
                  <button
                    key={r}
                    type="button"
                    className={`btn ${capRound === r ? 'btn-primary' : 'btn-outline'}`}
                    style={{ flex: 1, padding: '0.45rem' }}
                    onClick={() => setCapRound(r)}
                  >
                    Round {r}
                  </button>
                ))}
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">
                Preferred Engineering Branches ({selectedBranches.length} selected)
              </label>
              <div className="chip-container">
                {filters?.branches?.map(b => (
                  <button
                    key={b}
                    type="button"
                    className={`chip ${selectedBranches.includes(b) ? 'selected' : ''}`}
                    onClick={() => toggleBranch(b)}
                  >
                    {b}
                  </button>
                ))}
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">
                Preferred Region / City (Optional)
              </label>
              <div className="chip-container">
                {filters?.regions?.map(r => (
                  <button
                    key={r}
                    type="button"
                    className={`chip ${selectedRegions.includes(r) ? 'selected' : ''}`}
                    onClick={() => toggleRegion(r)}
                  >
                    {r}
                  </button>
                ))}
              </div>
            </div>

            <div className="form-group">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <label className="form-label">Maximum Recommendations: {topN}</label>
              </div>
              <input 
                type="range"
                min="5"
                max="50"
                step="5"
                value={topN}
                onChange={e => setTopN(e.target.value)}
                style={{ width: '100%' }}
              />
            </div>

            <button 
              type="submit" 
              className="btn btn-primary"
              style={{ width: '100%', padding: '0.75rem' }}
              disabled={loading}
            >
              <Sparkles size={18} />
              {loading ? 'Evaluating Cutoffs...' : 'Generate Personalized Recommendations'}
            </button>
          </form>
        </div>

        {/* Right Column: Grouping Rules & Explanations */}
        <div>
          <div className="card">
            <h3 className="card-title">
              <ShieldCheck size={20} color="#10b981" />
              Transparent Suitability Grouping Logic
            </h3>
            <p className="card-subtitle">
              Calculated using the model validation error margin (M = 1.5 &times; MAE ≈ 0.17%)
            </p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', fontSize: '0.9rem' }}>
              <div style={{ padding: '0.75rem', background: '#ecfdf5', borderRadius: '8px', border: '1px solid #a7f3d0' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: '#065f46', fontWeight: 700, marginBottom: '0.2rem' }}>
                  <span className="badge badge-safer">🛡️ SAFER OPTIONS</span>
                  <span>Gap &gt; +M</span>
                </div>
                <p style={{ color: '#047857', fontSize: '0.825rem' }}>
                  Your percentile is comfortably above the estimated closing cutoff by more than the model error margin. 
                  High probability buffer.
                </p>
              </div>

              <div style={{ padding: '0.75rem', background: '#fffbeb', borderRadius: '8px', border: '1px solid #fde68a' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: '#92400e', fontWeight: 700, marginBottom: '0.2rem' }}>
                  <span className="badge badge-moderate">⚖️ MODERATE OPTIONS</span>
                  <span>-M &le; Gap &le; +M</span>
                </div>
                <p style={{ color: '#b45309', fontSize: '0.825rem' }}>
                  Your score is within the competitive error margin of the predicted cutoff. Realistic, highly competitive target.
                </p>
              </div>

              <div style={{ padding: '0.75rem', background: '#fef2f2', borderRadius: '8px', border: '1px solid #fecaca' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: '#991b1b', fontWeight: 700, marginBottom: '0.2rem' }}>
                  <span className="badge badge-reach">🚀 REACH OPTIONS</span>
                  <span>Gap &lt; -M</span>
                </div>
                <p style={{ color: '#b91c1c', fontSize: '0.825rem' }}>
                  The predicted cutoff exceeds your score. Ambitious / Dream option to include at the top of your CAP preference form.
                </p>
              </div>
            </div>
          </div>

          {error && (
            <div className="alert alert-error">
              <AlertCircle size={20} />
              <div>{error}</div>
            </div>
          )}
        </div>
      </div>

      {/* Results View */}
      {results && results.status === 'success' && (
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', marginBottom: '1rem' }}>
            <div>
              <h3 className="card-title">
                <CheckCircle2 size={20} color="#10b981" />
                Personalized Shortlist ({filteredRecs.length} Options)
              </h3>
              <p className="card-subtitle" style={{ marginBottom: 0 }}>
                Target: CAP Round {results.cap_round} | Category: <strong>{results.seat_category}</strong> | Pool: <strong>{results.seat_pool}</strong>
              </p>
            </div>

            <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
              <button 
                className="btn btn-outline"
                onClick={downloadCSV}
              >
                <Download size={16} />
                Export Shortlist (CSV)
              </button>
            </div>
          </div>

          {/* Group Count Badges & Filter Tabs */}
          <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.25rem', flexWrap: 'wrap' }}>
            <button 
              className={`chip ${groupFilter === 'ALL' ? 'selected' : ''}`}
              onClick={() => setGroupFilter('ALL')}
            >
              All Options ({results.recommendations.length})
            </button>
            <button 
              className={`chip ${groupFilter === 'Safer' ? 'selected' : ''}`}
              onClick={() => setGroupFilter('Safer')}
            >
              🛡️ Safer Only ({saferCount})
            </button>
            <button 
              className={`chip ${groupFilter === 'Moderate' ? 'selected' : ''}`}
              onClick={() => setGroupFilter('Moderate')}
            >
              ⚖️ Moderate Only ({modCount})
            </button>
            <button 
              className={`chip ${groupFilter === 'Reach' ? 'selected' : ''}`}
              onClick={() => setGroupFilter('Reach')}
            >
              🚀 Reach Only ({reachCount})
            </button>
          </div>

          {/* Results Table */}
          <div className="table-responsive">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Suitability</th>
                  <th>Engineering College</th>
                  <th>Branch / Discipline</th>
                  <th>Region</th>
                  <th>Predicted Cutoff (2027)</th>
                  <th>Percentile Gap</th>
                  <th>2026 Cutoff</th>
                  <th>Recommendation Rationale</th>
                </tr>
              </thead>
              <tbody>
                {filteredRecs.map((r, idx) => {
                  const badgeClass = r.suitability_group === 'Safer' 
                    ? 'badge-safer' 
                    : r.suitability_group === 'Moderate' 
                    ? 'badge-moderate' 
                    : 'badge-reach';
                  const gapFormatted = r.percentile_gap > 0 ? `+${r.percentile_gap.toFixed(2)}%` : `${r.percentile_gap.toFixed(2)}%`;
                  const gapColor = r.percentile_gap > 0 ? '#10b981' : r.percentile_gap === 0 ? '#64748b' : '#ef4444';

                  return (
                    <tr key={idx}>
                      <td>
                        <span className={`badge ${badgeClass}`}>
                          {r.suitability_group === 'Safer' ? '🛡️ SAFER' : r.suitability_group === 'Moderate' ? '⚖️ MODERATE' : '🚀 REACH'}
                        </span>
                      </td>
                      <td style={{ fontWeight: 600 }}>{r.institute_name}</td>
                      <td>{r.branch_name}</td>
                      <td>{r.region}</td>
                      <td style={{ fontWeight: 700, color: '#00296b' }}>
                        {r.predicted_cutoff.toFixed(2)}%
                      </td>
                      <td style={{ fontWeight: 700, color: gapColor }}>
                        {gapFormatted}
                      </td>
                      <td style={{ color: '#64748b' }}>
                        {r.history_2026?.toFixed(2)}%
                      </td>
                      <td style={{ fontSize: '0.8rem', color: '#475569' }}>
                        {r.explanation}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
