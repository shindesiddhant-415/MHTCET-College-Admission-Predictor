/**
 * API Service for communicating with FastAPI Backend
 */

const BASE_URL = import.meta.env.VITE_API_URL || '';

export async function fetchOverview() {
  const res = await fetch(`${BASE_URL}/api/overview`);
  if (!res.ok) throw new Error('Failed to fetch overview metrics');
  return res.json();
}

export async function fetchFilters() {
  const res = await fetch(`${BASE_URL}/api/filters`);
  if (!res.ok) throw new Error('Failed to fetch filter options');
  return res.json();
}

export async function fetchRecommendations(payload) {
  const res = await fetch(`${BASE_URL}/api/recommend`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Prediction failed');
  }
  return res.json();
}

export async function fetchTrends(institutes, branches, category) {
  const params = new URLSearchParams();
  if (category) params.append('category', category);
  if (institutes) institutes.forEach(i => params.append('institutes', i));
  if (branches) branches.forEach(b => params.append('branches', b));
  
  const res = await fetch(`${BASE_URL}/api/trends?${params.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch cutoff trends');
  return res.json();
}

export async function fetchModelPerformance() {
  const res = await fetch(`${BASE_URL}/api/model-performance`);
  if (!res.ok) throw new Error('Failed to fetch model benchmarks');
  return res.json();
}

export async function fetchComparison(institutes, branch, category) {
  const params = new URLSearchParams();
  if (branch) params.append('branch', branch);
  if (category) params.append('category', category);
  if (institutes) institutes.forEach(i => params.append('institutes', i));
  
  const res = await fetch(`${BASE_URL}/api/compare?${params.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch comparison');
  return res.json();
}

export async function fetchManifest() {
  const res = await fetch(`${BASE_URL}/api/manifest`);
  if (!res.ok) throw new Error('Failed to fetch source manifest');
  return res.json();
}
