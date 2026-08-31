'use client';

import React, { useState } from 'react';
import { Upload, FileCheck, Layers, AlertCircle, RefreshCw, Database } from 'lucide-react';
import { ImageMetadata, ImageValidation } from '@/types';
import { uploadImage, validateImages } from '@/lib/api';

interface InputPanelProps {
  analysisMode: 'single' | 'bi_temporal' | 'optical_sar';
  setAnalysisMode: (mode: 'single' | 'bi_temporal' | 'optical_sar') => void;
  primaryImage: ImageMetadata | null;
  setPrimaryImage: (img: ImageMetadata | null) => void;
  secondaryImage: ImageMetadata | null;
  setSecondaryImage: (img: ImageMetadata | null) => void;
  validation: ImageValidation | null;
  setValidation: (val: ImageValidation | null) => void;
  onLoadDemoDataset: () => void;
  onLoadSEN12MSDataset: (sampleId: string) => void;
}

export const InputPanel: React.FC<InputPanelProps> = ({
  analysisMode,
  setAnalysisMode,
  primaryImage,
  setPrimaryImage,
  secondaryImage,
  setSecondaryImage,
  validation,
  setValidation,
  onLoadDemoDataset,
  onLoadSEN12MSDataset
}) => {
  const [uploadingPrimary, setUploadingPrimary] = useState(false);
  const [uploadingSecondary, setUploadingSecondary] = useState(false);
  const [datasetChoice, setDatasetChoice] = useState<'bigearthnet' | 'sen12ms'>('bigearthnet');
  const [selectedSenSample, setSelectedSenSample] = useState<string>('sample_001');

  const handleUpload = async (file: File, isSecondary = false) => {
    try {
      if (isSecondary) setUploadingSecondary(true);
      else setUploadingPrimary(true);

      const meta = await uploadImage(file);
      if (isSecondary) {
        setSecondaryImage(meta);
        if (primaryImage) {
          const val = await validateImages(primaryImage.id, meta.id);
          setValidation(val);
        }
      } else {
        setPrimaryImage(meta);
        if (secondaryImage && (analysisMode === 'bi_temporal' || analysisMode === 'optical_sar')) {
          const val = await validateImages(meta.id, secondaryImage.id);
          setValidation(val);
        } else {
          const val = await validateImages(meta.id);
          setValidation(val);
        }
      }
    } catch (err: any) {
      alert(err.message || 'File upload failed');
    } finally {
      setUploadingPrimary(false);
      setUploadingSecondary(false);
    }
  };

  return (
    <div className="glass-panel rounded-2xl p-5 border border-slate-800 space-y-5">
      {/* Dataset Selection Tabs */}
      <div>
        <label className="text-xs font-semibold uppercase tracking-wider text-slate-400 block mb-2">
          Satellite Dataset
        </label>
        <div className="grid grid-cols-2 gap-2 p-1 bg-space-950 rounded-xl border border-slate-800 mb-3">
          <button
            onClick={() => setDatasetChoice('bigearthnet')}
            className={`py-1.5 px-2 rounded-lg text-xs font-medium transition-all ${
              datasetChoice === 'bigearthnet'
                ? 'bg-cyan-900/80 text-cyan-300 font-bold border border-cyan-500/40 shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            BigEarthNet
          </button>
          <button
            onClick={() => setDatasetChoice('sen12ms')}
            className={`py-1.5 px-2 rounded-lg text-xs font-medium transition-all ${
              datasetChoice === 'sen12ms'
                ? 'bg-amber-900/80 text-amber-300 font-bold border border-amber-500/40 shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            SEN12MS-CR
          </button>
        </div>

        {/* Dataset Quick-Load Button / Sample Selector */}
        {datasetChoice === 'bigearthnet' ? (
          <button
            onClick={onLoadDemoDataset}
            className="w-full py-2 px-3 rounded-xl bg-slate-900 border border-slate-700/60 hover:border-cyan-500/50 text-cyan-400 text-xs font-medium flex items-center justify-center space-x-2 transition-all hover:bg-slate-850"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Load Demo Satellite Sample Pair</span>
          </button>
        ) : (
          <div className="p-3 rounded-xl bg-space-950 border border-amber-500/30 space-y-2 text-xs">
            <div className="flex items-center justify-between text-amber-400 font-bold">
              <span className="flex items-center space-x-1.5">
                <Database className="w-3.5 h-3.5" />
                <span>SEN12MS-CR sample data</span>
              </span>
              <span className="text-[10px] font-mono bg-amber-950 px-1.5 py-0.5 rounded border border-amber-500/30 text-amber-300">
                3 paired SAR + optical samples
              </span>
            </div>
            <p className="text-[11px] text-slate-400 leading-tight">
              Streaming extraction | 13-band Sentinel-2 Optical + 2-channel Sentinel-1 SAR. Ready.
            </p>
            <div className="grid grid-cols-3 gap-1.5 pt-1">
              {(['sample_001', 'sample_002', 'sample_003'] as const).map((sid, idx) => (
                <button
                  key={sid}
                  onClick={() => {
                    setSelectedSenSample(sid);
                    setAnalysisMode('optical_sar');
                    onLoadSEN12MSDataset(sid);
                  }}
                  className={`py-1 px-2 rounded text-[11px] font-mono font-semibold transition-all ${
                    selectedSenSample === sid && primaryImage?.id.includes(sid)
                      ? 'bg-amber-500 text-slate-950 font-bold shadow-md'
                      : 'bg-slate-900 text-amber-300 hover:bg-slate-800 border border-slate-800'
                  }`}
                >
                  Sample 00{idx + 1}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Analysis Mode Selector */}
      <div>
        <label className="text-xs font-semibold uppercase tracking-wider text-slate-400 block mb-2.5">
          Analysis Mode
        </label>
        <div className="grid grid-cols-3 gap-2 p-1 bg-space-950 rounded-xl border border-slate-800">
          {(['single', 'bi_temporal', 'optical_sar'] as const).map((mode) => (
            <button
              key={mode}
              onClick={() => {
                setAnalysisMode(mode);
                setValidation(null);
              }}
              className={`py-2 px-3 rounded-lg text-xs font-medium capitalize transition-all ${
                analysisMode === mode
                  ? 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white shadow-md shadow-cyan-500/20 font-semibold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
              }`}
            >
              {mode.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Upload Zone(s) */}
      <div className="space-y-3">
        {/* Primary Uploader */}
        <div>
          <span className="text-xs font-medium text-slate-300 block mb-1.5">
            {analysisMode === 'bi_temporal' ? 'Before Image (T1)' : analysisMode === 'optical_sar' ? 'Optical / Multispectral Image' : 'Satellite Input Image'}
          </span>
          <UploadBox
            image={primaryImage}
            uploading={uploadingPrimary}
            onFileSelect={(f) => handleUpload(f, false)}
            onClear={() => { setPrimaryImage(null); setValidation(null); }}
            label="Drop GeoTIFF / PNG / JPEG"
          />
        </div>

        {/* Secondary Uploader (Bi-Temporal or Optical + SAR) */}
        {(analysisMode === 'bi_temporal' || analysisMode === 'optical_sar') && (
          <div>
            <span className="text-xs font-medium text-slate-300 block mb-1.5">
              {analysisMode === 'bi_temporal' ? 'After Image (T2)' : 'SAR (Synthetic Aperture Radar) Image'}
            </span>
            <UploadBox
              image={secondaryImage}
              uploading={uploadingSecondary}
              onFileSelect={(f) => handleUpload(f, true)}
              onClear={() => { setSecondaryImage(null); setValidation(null); }}
              label={analysisMode === 'bi_temporal' ? 'Drop T2 Image' : 'Drop SAR Image (Sentinel-1)'}
            />
          </div>
        )}
      </div>

      {/* Image Validation Feedback Panel */}
      {validation && (
        <div className="p-3.5 rounded-xl bg-space-950 border border-slate-800 space-y-2 text-xs">
          <div className="flex items-center justify-between">
            <span className="font-semibold text-slate-200">Validation Status</span>
            <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase ${validation.valid ? 'bg-emerald-950 text-emerald-400 border border-emerald-500/30' : 'bg-rose-950 text-rose-400 border border-rose-500/30'}`}>
              {validation.valid ? 'Passed' : 'Issues Detected'}
            </span>
          </div>

          <div className="grid grid-cols-2 gap-2 text-[11px] font-mono">
            <div>Format: <span className="text-cyan-400">{validation.checks.format}</span></div>
            <div>Dims: <span className="text-cyan-400">{validation.checks.dimensions}</span></div>
            <div>CRS: <span className="text-cyan-400">{validation.checks.crs}</span></div>
            <div>Align: <span className="text-cyan-400">{validation.checks.alignment}</span></div>
          </div>

          {validation.warnings.length > 0 && (
            <div className="text-[11px] text-amber-400 space-y-1 pt-1 border-t border-slate-800">
              {validation.warnings.map((w, i) => (
                <div key={i} className="flex items-start space-x-1">
                  <AlertCircle className="w-3 h-3 text-amber-400 flex-shrink-0 mt-0.5" />
                  <span>{w}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

interface UploadBoxProps {
  image: ImageMetadata | null;
  uploading: boolean;
  onFileSelect: (file: File) => void;
  onClear: () => void;
  label: string;
}

const UploadBox: React.FC<UploadBoxProps> = ({ image, uploading, onFileSelect, onClear, label }) => {
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onFileSelect(e.dataTransfer.files[0]);
    }
  };

  if (image) {
    return (
      <div className="p-3 rounded-xl bg-space-950 border border-slate-800 flex items-center justify-between">
        <div className="flex items-center space-x-3 overflow-hidden">
          <FileCheck className="w-5 h-5 text-emerald-400 flex-shrink-0" />
          <div className="truncate">
            <p className="text-xs font-semibold text-slate-200 truncate">{image.filename}</p>
            <p className="text-[10px] text-slate-400 font-mono">
              {image.width}x{image.height} px | {image.format} | {image.modality.toUpperCase()}
            </p>
          </div>
        </div>
        <button onClick={onClear} className="text-xs text-rose-400 hover:text-rose-300 p-1">
          ✕
        </button>
      </div>
    );
  }

  return (
    <div
      onDragOver={(e) => e.preventDefault()}
      onDrop={handleDrop}
      className="border-2 border-dashed border-slate-800 hover:border-cyan-500/50 rounded-xl p-4 text-center bg-space-950/50 hover:bg-space-950 transition-all cursor-pointer group"
    >
      <input
        type="file"
        accept=".tif,.tiff,.geotiff,.png,.jpg,.jpeg,.webp"
        onChange={(e) => e.target.files?.[0] && onFileSelect(e.target.files[0])}
        className="hidden"
        id={`file-input-${label}`}
      />
      <label htmlFor={`file-input-${label}`} className="cursor-pointer space-y-1 block">
        <Upload className="w-6 h-6 text-slate-500 group-hover:text-cyan-400 transition-colors mx-auto" />
        <p className="text-xs font-medium text-slate-300 group-hover:text-cyan-300">{uploading ? 'Processing Image...' : label}</p>
        <p className="text-[10px] text-slate-500">GeoTIFF, TIFF, PNG, JPEG, WEBP up to 50MB</p>
      </label>
    </div>
  );
};
