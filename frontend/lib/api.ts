import { SystemStatus, ImageMetadata, ImageValidation, AnalysisResult } from '@/types';

const API_BASE = '/api';

export async function fetchSystemStatus(): Promise<SystemStatus> {
  const res = await fetch(`${API_BASE}/system/status`);
  if (!res.ok) throw new Error('Failed to fetch system status');
  return res.json();
}

export async function fetchSampleDataset(): Promise<{ primary_image: ImageMetadata; secondary_image: ImageMetadata; sample_info: any }> {
  const res = await fetch(`${API_BASE}/system/sample-dataset`);
  if (!res.ok) throw new Error('Failed to load sample dataset from backend');
  return res.json();
}

export async function fetchSEN12MSDataset(sampleId: string = 'sample_001'): Promise<{ primary_image: ImageMetadata; secondary_image: ImageMetadata; sample_info: any }> {
  const res = await fetch(`${API_BASE}/system/sen12ms-dataset?sample_id=${sampleId}`);
  if (!res.ok) throw new Error(`Failed to load SEN12MS-CR dataset sample '${sampleId}' from backend`);
  return res.json();
}

export async function uploadImage(file: File): Promise<ImageMetadata> {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE}/images/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    let msg = 'Image upload failed';
    if (typeof errorData.detail === 'string') {
      msg = errorData.detail;
    } else if (Array.isArray(errorData.detail)) {
      msg = errorData.detail.map((e: any) => e.msg || JSON.stringify(e)).join(', ');
    }
    throw new Error(msg);
  }

  return res.json();
}

export async function validateImages(primaryId: string, secondaryId?: string): Promise<ImageValidation> {
  const params = new URLSearchParams({ primary_id: primaryId });
  if (secondaryId) params.append('secondary_id', secondaryId);

  const res = await fetch(`${API_BASE}/images/validate?${params.toString()}`, {
    method: 'POST',
  });

  if (!res.ok) throw new Error('Image validation failed');
  return res.json();
}

export async function submitQuery(query: string, mode: string, primaryId: string, secondaryId?: string): Promise<AnalysisResult> {
  const res = await fetch(`${API_BASE}/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query,
      analysis_mode: mode,
      primary_image_id: primaryId,
      secondary_image_id: secondaryId || null,
    }),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    let errorMsg = 'Query execution failed';
    if (typeof errorData.detail === 'string') {
      errorMsg = errorData.detail;
    } else if (Array.isArray(errorData.detail)) {
      errorMsg = errorData.detail.map((e: any) => e.msg || JSON.stringify(e)).join(', ');
    } else if (errorData.message) {
      errorMsg = errorData.message;
    }
    throw new Error(errorMsg);
  }

  return res.json();
}

export async function generateReport(executionId: string, format: 'pdf' | 'json' = 'pdf'): Promise<{ download_url: string }> {
  const res = await fetch(`${API_BASE}/reports/generate/${executionId}?format=${format}`, {
    method: 'POST',
  });

  if (!res.ok) throw new Error('Report generation failed');
  return res.json();
}

export function getReportDownloadUrl(executionId: string, format: 'pdf' | 'json' = 'pdf'): string {
  return `${API_BASE}/reports/${executionId}/download?format=${format}`;
}
