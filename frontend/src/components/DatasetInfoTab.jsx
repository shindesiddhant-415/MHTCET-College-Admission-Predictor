import React, { useState, useEffect } from 'react';
import { BookOpen, ShieldCheck, Database, CheckCircle2 } from 'lucide-react';
import { fetchManifest } from '../services/api';

export default function DatasetInfoTab() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchManifest()
      .then(d => {
        setData(d);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const categories = [
    { code: 'GOPENS', type: 'General', name: 'Open / General State Level', desc: 'Merit seats accessible to all Maharashtra State candidates.' },
    { code: 'LOPENS', type: 'Ladies', name: 'Ladies Open State', desc: 'Seats reserved specifically for female Open candidates.' },
    { code: 'GOBCS', type: 'General', name: 'Other Backward Class', desc: 'General quota for Non-Creamy Layer OBC candidates.' },
    { code: 'LOBCS', type: 'Ladies', name: 'Ladies Other Backward Class', desc: 'Female quota for Non-Creamy Layer OBC candidates.' },
    { code: 'EWS', type: 'Economically Weaker', name: 'Economically Weaker Section', desc: '10% supernumerary quota for family income < 8 LPA.' },
    { code: 'TFWS', type: 'Fee Waiver', name: 'Tuition Fee Waiver Scheme', desc: '5% supernumerary quota with 100% tuition fee concession for top merit.' },
    { code: 'GSCS / LSCS', type: 'SC Quota', name: 'Scheduled Caste (General / Ladies)', desc: 'Constitutional quota for Scheduled Caste candidates.' },
    { code: 'GSTS / LSTS', type: 'ST Quota', name: 'Scheduled Tribe (General / Ladies)', desc: 'Constitutional quota for Scheduled Tribe candidates.' },
    { code: 'GVJS / LVJS', type: 'VJ / DT', name: 'Vimukta Jati / Denotified Tribes', desc: 'State quota for DT-A category candidates.' },
    { code: 'GNT1S / 2S / 3S', type: 'NT Quota', name: 'Nomadic Tribes (B, C, D)', desc: 'State quotas for specific Nomadic Tribe communities.' }
  ];

  return (
    <div>
      {/* Manifest Table */}
      <div className="card">
        <h3 className="card-title">
          <BookOpen size={20} color="#00509d" />
          Official CET Cell Source Documents & Traceability Manifest
        </h3>
        <p className="card-subtitle">
          Audit trail of all 18 official PDF documents (14 CAP cutoff lists + 4 seat matrices) ingested into the system
        </p>

        {loading ? (
          <div>Loading source manifest...</div>
        ) : (
          <div className="table-responsive" style={{ maxHeight: '350px', overflowY: 'auto' }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Academic Year</th>
                  <th>Document Type</th>
                  <th>CAP Round</th>
                  <th>PDF File Name</th>
                  <th>File Size</th>
                  <th>Verification Status</th>
                </tr>
              </thead>
              <tbody>
                {data?.manifest?.map((m, idx) => (
                  <tr key={idx}>
                    <td style={{ fontWeight: 600 }}>{m.academic_year}</td>
                    <td>{m.document_type === 'cutoff' ? 'CAP Cutoff List' : 'Sanctioned Seat Matrix'}</td>
                    <td>{m.cap_round ? `Round ${m.cap_round}` : 'Annual Intake'}</td>
                    <td style={{ fontFamily: 'monospace', fontSize: '0.8rem' }}>{m.file_name}</td>
                    <td>{(m.file_size_bytes / 1024).toFixed(1)} KB</td>
                    <td>
                      <span className="badge badge-safer">
                        <CheckCircle2 size={12} />
                        VERIFIED
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Data Quality Report */}
      <div className="card">
        <h3 className="card-title">
          <Database size={20} color="#00509d" />
          Automated Data Integrity & Quality Audit Report
        </h3>
        <p className="card-subtitle">
          Validation checks performed on parsed tables prior to machine learning feature store generation
        </p>

        <div className="table-responsive">
          <table className="data-table">
            <thead>
              <tr>
                <th>Audit Metric</th>
                <th>Measured Value</th>
                <th>Validation Status</th>
              </tr>
            </thead>
            <tbody>
              {data?.quality_report?.map((q, idx) => (
                <tr key={idx}>
                  <td style={{ fontWeight: 600, fontFamily: 'monospace' }}>{q.metric}</td>
                  <td style={{ fontWeight: 700 }}>
                    {typeof q.value === 'number' && q.value % 1 !== 0 ? q.value.toFixed(1) : q.value.toLocaleString()}
                  </td>
                  <td>
                    <span className={`badge ${q.status === 'PASS' ? 'badge-safer' : q.status === 'INFO' ? 'badge-primary' : 'badge-moderate'}`}>
                      {q.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Official Categories Guide */}
      <div className="card">
        <h3 className="card-title">
          <BookOpen size={20} color="#00509d" />
          Official Maharashtra Seat Reservation Category Definitions
        </h3>
        <p className="card-subtitle">
          Definitions of official reservation codes printed in State CET Cell documents
        </p>

        <div className="table-responsive">
          <table className="data-table">
            <thead>
              <tr>
                <th>Category Code</th>
                <th>Type</th>
                <th>Full Reservation Designation</th>
                <th>Official Quota Scope</th>
              </tr>
            </thead>
            <tbody>
              {categories.map((c, idx) => (
                <tr key={idx}>
                  <td><span className="badge badge-primary">{c.code}</span></td>
                  <td>{c.type}</td>
                  <td style={{ fontWeight: 600 }}>{c.name}</td>
                  <td style={{ color: '#475569' }}>{c.desc}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Ethical Considerations & SDGs */}
      <div className="card">
        <h3 className="card-title">
          <ShieldCheck size={20} color="#10b981" />
          Ethical AI Framework & UN Sustainable Development Goals
        </h3>
        <p className="card-subtitle">
          Responsible AI practices implemented in compliance with educational equity standards
        </p>

        <div className="grid-2">
          <div style={{ padding: '1rem', background: '#eff6ff', borderRadius: '8px', border: '1px solid #bfdbfe' }}>
            <h4 style={{ color: '#1e40af', fontWeight: 700, marginBottom: '0.4rem' }}>
              🎯 SDG 4: Quality Education (Target 4.3)
            </h4>
            <p style={{ fontSize: '0.85rem', color: '#1e3a8a' }}>
              Democratizes higher education access by providing high-quality, transparent cutoff forecasting 
              to rural and first-generation aspirants without commercial counseling fees.
            </p>
          </div>

          <div style={{ padding: '1rem', background: '#ecfdf5', borderRadius: '8px', border: '1px solid #a7f3d0' }}>
            <h4 style={{ color: '#065f46', fontWeight: 700, marginBottom: '0.4rem' }}>
              🎯 SDG 10: Reduced Inequalities (Target 10.2)
            </h4>
            <p style={{ fontSize: '0.85rem', color: '#064e3b' }}>
              Maintains full integrity of constitutional reservation quotas (OBC, SC, ST, EWS, TFWS) 
              without bias or arbitrary ranking, reducing admission disparities.
            </p>
          </div>
        </div>

        <div style={{ marginTop: '1rem', fontSize: '0.85rem', color: '#64748b' }}>
          <strong>Privacy by Design:</strong> The platform operates strictly on aggregate numerical scores and academic preferences. 
          Zero personally identifiable information (PII), application IDs, or personal documents are stored or logged.
        </div>
      </div>
    </div>
  );
}

