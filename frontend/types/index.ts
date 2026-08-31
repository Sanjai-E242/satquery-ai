export interface ImageMetadata {
  id: string;
  filename: string;
  filepath: string;
  url?: string;
  file_size_bytes: number;
  format: string;
  width: number;
  height: number;
  bands: number;
  dtype: string;
  crs?: string | null;
  bounds?: number[] | null;
  resolution?: number[] | null;
  modality: 'optical' | 'sar' | 'multispectral' | 'unknown';
  has_geospatial: boolean;
}

export interface ValidationCheck {
  format: string;
  dimensions: string;
  crs: string;
  alignment: string;
}

export interface ImageValidation {
  valid: boolean;
  warnings: string[];
  errors: string[];
  checks: ValidationCheck;
  metadata?: ImageMetadata;
}

export interface ExecutionStep {
  name: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  duration_ms?: number;
  detail?: string;
}

export interface ConfidenceInfo {
  value: number;
  type: 'model_derived' | 'estimated' | 'demo';
}

export interface EvidenceItem {
  id: string;
  title: string;
  type: 'image' | 'mask' | 'bounding_box' | 'change_map' | 'optical_sar_overlay';
  url: string;
  metadata?: Record<string, any>;
}

export interface AnalysisResult {
  execution_id: string;
  query: string;
  answer: string;
  confidence: ConfidenceInfo;
  task: string;
  input_type: string;
  models_used: string[];
  tools_used: string[];
  execution_steps: ExecutionStep[];
  evidence: EvidenceItem[];
  duration_ms: number;
  timestamp: string;
}

export interface SystemStatus {
  status: string;
  version: string;
  demo_mode: boolean;
  components: Record<string, string>;
  dataset: {
    name: string;
    connected: boolean;
    path: string;
    rows: number;
    adaptation_ready: boolean;
  };
  hardware: {
    python_version: string;
    torch_version: string;
    cuda_available: boolean;
    device: string;
  };
}
