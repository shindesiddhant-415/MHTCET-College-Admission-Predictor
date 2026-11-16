import React, { useState, useEffect } from 'react';
import { TrendingUp, Filter } from 'lucide-react';
import { fetchTrends } from '../services/api';

export default function CutoffTrendsTab({ filters }) {
  const [selectedCategory, setSelectedCategory] = useState('GOPENS');
  const [selectedColleges, setSelectedColleges] = useState([
    'COEP Technological University, Pune',
    'Veermata Jijabai Technological Institute (VJTI), Mumbai',
    'Pune Institute of Computer Technology (PICT), Pune'
  ]);
  const [selectedBranches, setSelectedBranches] = useState([
    'Computer Engineering',
    'Information Technology'
  ]);
  const [trends, setTrends] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadTrends();
  }, [selectedCategory, selectedColleges, selectedBranches]);

  const loadTrends = async () => {
    setLoading(true);
    try {
      const data = await fetchTrends(selectedColleges, selectedBranches, selectedCategory);
      setTrends(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const toggleCollege = (c) => {
    if (selectedColleges.includes(c)) {
      if (selectedColleges.length > 1) {
        setSelectedColleges(selectedColleges.filter(x => x !== c));
      }
    } else {
      setSelectedColleges([...selectedColleges, c]);
    }
  };

  const toggleBranch = (b) => {
    if (selectedBranches.includes(b)) {
      if (selectedBranches.length > 1) {
        setSelectedBranches(selectedBranches.filter(x => x !== b));
      }
    } else {
      setSelectedBranches([...selectedBranches, b]);
    }
  };

  return (
    <div>
      <div className="card">
        <h3 className="card-title">
          <TrendingUp size={20} color="#00509d" />
          Cutoff Analytics & Historical Progression
        </h3>
        <p className="card-subtitle">
          Observe how cutoffs move across academic years and relax across successive CAP rounds
        </p>

        {/* Filter Controls */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
          <div>
            <label className="form-label">Seat Category</label>
            <select
              className="form-select"
              value={selectedCategory}
              onChange={e => setSelectedCategory(e.target.value)}
            >
              {filters?.categories?.map(c => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="form-label">Institutes ({selectedColleges.length} active)</label>
            <div className="chip-container" style={{ maxHeight: '100px', overflowY: 'auto' }}>
              {filters?.colleges?.slice(0, 10).map(col => (
                <button
                  key={col.institute_code}
                  className={`chip ${selectedColleges.includes(col.institute_name) ? 'selected' : ''}`}
                  onClick={() => toggleCollege(col.institute_name)}
                >
                  {col.institute_name.split(',')[0]}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="form-label">Branches ({selectedBranches.length} active)</label>
            <div className="chip-container">
              {filters?.branches?.slice(0, 4).map(b => (
                <button
                  key={b}
                  className={`chip ${selectedBranches.includes(b) ? 'selected' : ''}`}
                  onClick={() => toggleBranch(b)}
                >
                  {b}
                </button>
              ))}
            </div>
          </div>
        </div>

        {loading ? (
          <div>Loading trend analytics...</div>
        ) : (
          <div>
            <h4 style={{ color: '#00296b', marginBottom: '0.75rem', fontWeight: 700 }}>
              1. Year-over-Year Cutoff Trajectory (CAP Round I - {selectedCategory})
            </h4>
            <div className="table-responsive" style={{ marginBottom: '2rem' }}>
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Academic Year</th>
                    <th>Institute</th>
                    <th>Branch</th>
                    <th>Closing Percentile</th>
                  </tr>
                </thead>
                <tbody>
                  {trends?.yearly_trends?.map((t, idx) => (
                    <tr key={idx}>
                      <td style={{ fontWeight: 600 }}>{t.academic_year}</td>
                      <td>{t.institute_name}</td>
                      <td>{t.branch_name}</td>
                      <td style={{ fontWeight: 700, color: '#00509d' }}>{t.cutoff_percentile.toFixed(4)}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <h4 style={{ color: '#00296b', marginBottom: '0.75rem', fontWeight: 700 }}>
              2. Round Relaxation Pattern (Progression from Round 1 to Round 4)
            </h4>
            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>CAP Round</th>
                    <th>Institute</th>
                    <th>Mean Cutoff Percentile</th>
                  </tr>
                </thead>
                <tbody>
                  {trends?.round_progression?.map((r, idx) => (
                    <tr key={idx}>
                      <td><span className="badge badge-primary">Round {r.cap_round}</span></td>
                      <td style={{ fontWeight: 600 }}>{r.institute_name}</td>
                      <td style={{ fontWeight: 700, color: '#10b981' }}>{r.cutoff_percentile.toFixed(4)}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
