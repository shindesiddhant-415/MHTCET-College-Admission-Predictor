import React, { useState, useEffect } from 'react';
import { Scale, Users, Award } from 'lucide-react';
import { fetchComparison } from '../services/api';

export default function CollegeComparisonTab({ filters }) {
  const [selectedColleges, setSelectedColleges] = useState([
    'COEP Technological University, Pune',
    'Veermata Jijabai Technological Institute (VJTI), Mumbai'
  ]);
  const [selectedBranch, setSelectedBranch] = useState('Computer Engineering');
  const [selectedCategory, setSelectedCategory] = useState('GOPENS');
  const [compData, setCompData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (selectedColleges.length >= 2) {
      loadComparison();
    }
  }, [selectedColleges, selectedBranch, selectedCategory]);

  const loadComparison = async () => {
    setLoading(true);
    try {
      const data = await fetchComparison(selectedColleges, selectedBranch, selectedCategory);
      setCompData(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const toggleCollege = (colName) => {
    if (selectedColleges.includes(colName)) {
      if (selectedColleges.length > 2) {
        setSelectedColleges(selectedColleges.filter(c => c !== colName));
      }
    } else {
      setSelectedColleges([...selectedColleges, colName]);
    }
  };

  return (
    <div>
      <div className="card">
        <h3 className="card-title">
          <Scale size={20} color="#00509d" />
          Head-to-Head College & Seat Matrix Comparison
        </h3>
        <p className="card-subtitle">
          Compare closing cutoffs and sanctioned intake across multiple institutions side by side
        </p>

        {/* Filter Selection */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
          <div>
            <label className="form-label">Branch / Discipline</label>
            <select
              className="form-select"
              value={selectedBranch}
              onChange={e => setSelectedBranch(e.target.value)}
            >
              {filters?.branches?.map(b => (
                <option key={b} value={b}>{b}</option>
              ))}
            </select>
          </div>

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
            <label className="form-label">Select Colleges to Compare ({selectedColleges.length} active)</label>
            <div className="chip-container" style={{ maxHeight: '100px', overflowY: 'auto' }}>
              {filters?.colleges?.map(c => (
                <button
                  key={c.institute_code}
                  className={`chip ${selectedColleges.includes(c.institute_name) ? 'selected' : ''}`}
                  onClick={() => toggleCollege(c.institute_name)}
                >
                  {c.institute_name.split(',')[0]}
                </button>
              ))}
            </div>
          </div>
        </div>

        {loading ? (
          <div>Loading comparison matrix...</div>
        ) : (
          <div>
            {/* Cutoff Comparison Matrix */}
            <h4 style={{ color: '#00296b', marginBottom: '0.75rem', fontWeight: 700 }}>
              1. Historical Closing Cutoffs ({selectedBranch} - {selectedCategory} - CAP Round 1)
            </h4>
            <div className="table-responsive" style={{ marginBottom: '2rem' }}>
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Academic Year</th>
                    <th>Institute</th>
                    <th>Closing Percentile</th>
                  </tr>
                </thead>
                <tbody>
                  {compData?.cutoffs?.map((row, idx) => (
                    <tr key={idx}>
                      <td style={{ fontWeight: 600 }}>{row.academic_year}</td>
                      <td>{row.institute_name}</td>
                      <td style={{ fontWeight: 700, color: '#00509d' }}>{row.cutoff_percentile.toFixed(4)}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Seat Intake Breakdown */}
            <h4 style={{ color: '#00296b', marginBottom: '0.75rem', fontWeight: 700 }}>
              2. Approved Seat Matrix & Intake Distribution (2026–27)
            </h4>
            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Institute</th>
                    <th>Total Intake</th>
                    <th>Maharashtra CAP Seats</th>
                    <th>Minority Seats</th>
                    <th>All India (JEE) Seats</th>
                    <th>Institute Quota</th>
                  </tr>
                </thead>
                <tbody>
                  {compData?.intake?.map((row, idx) => (
                    <tr key={idx}>
                      <td style={{ fontWeight: 600 }}>{row.institute_name}</td>
                      <td style={{ fontWeight: 700 }}>{row.total_intake}</td>
                      <td style={{ color: '#10b981', fontWeight: 600 }}>{row.state_seats}</td>
                      <td>{row.minority_seats}</td>
                      <td style={{ color: '#00509d' }}>{row.all_india_seats}</td>
                      <td>{row.institute_seats}</td>
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

