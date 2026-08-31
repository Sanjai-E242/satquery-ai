'use client';

import React, { useState } from 'react';
import { Layers, Eye, EyeOff, Sliders, Maximize2, ZoomIn, ZoomOut, Compass, Sparkles, AlertTriangle, Radio } from 'lucide-react';
import { ImageMetadata, EvidenceItem } from '@/types';

interface SatelliteViewerProps {
  primaryImage: ImageMetadata | null;
  secondaryImage: ImageMetadata | null;
  evidence: EvidenceItem[];
  mode: 'single' | 'bi_temporal' | 'optical_sar';
}

export const SatelliteViewer: React.FC<SatelliteViewerProps> = ({
  primaryImage,
  secondaryImage,
  evidence,
  mode
}) => {
  const [sliderPos, setSliderPos] = useState(50);
  const [showOverlay, setShowOverlay] = useState(true);
  const [opacity, setOpacity] = useState(80);
  const [zoomLevel, setZoomLevel] = useState(100);
  const [activeMultimodalTab, setActiveMultimodalTab] = useState<'fused' | 'optical' | 'sar'>('fused');

  // Find overlay evidence item (mask, change map, fusion map)
  const overlayEvidence = evidence.find(e => ['mask', 'change_map', 'optical_sar_overlay'].includes(e.type));
  const bboxData = overlayEvidence?.metadata?.bounding_box;
  const changePct = overlayEvidence?.metadata?.change_percentage;
  const multimodalSummary = overlayEvidence?.metadata;

  const primaryUrl = primaryImage ? `/storage/uploads/${primaryImage.filename}` : null;
  const secondaryUrl = secondaryImage ? `/storage/uploads/${secondaryImage.filename}` : null;

  if (!primaryUrl) {
    return (
      <div className="w-full h-full min-h-[440px] glass-panel rounded-2xl border border-slate-800 flex flex-col items-center justify-center p-8 text-center radar-sweep">
        <div className="w-16 h-16 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center mb-4 shadow-xl">
          <Compass className="w-8 h-8 text-cyanAccent-500 animate-spin" style={{ animationDuration: '10s' }} />
        </div>
        <h3 className="text-base font-semibold text-slate-200 mb-1">Satellite Analysis Workstation</h3>
        <p className="text-xs text-slate-400 max-w-sm">
          Upload satellite imagery or click <span className="text-cyan-400 font-semibold font-mono">"Load Demo Satellite Sample Pair"</span> to visualize spectral channels, phrase grounding bounding boxes, and cross-modal fusion.
        </p>
      </div>
    );
  }

  return (
    <div className="w-full h-full min-h-[440px] glass-panel rounded-2xl border border-slate-800 flex flex-col overflow-hidden relative group shadow-2xl">
      {/* Top Controls Overlay Toolbar */}
      <div className="absolute top-4 left-4 right-4 z-20 flex items-center justify-between pointer-events-none">
        {/* Layer & Metadata Pills */}
        <div className="flex items-center space-x-2 pointer-events-auto">
          <div className="px-3 py-1.5 rounded-xl bg-space-950/90 backdrop-blur-md border border-slate-800 text-xs font-mono text-cyan-400 flex items-center space-x-2 shadow-lg">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping"></span>
            <span>{primaryImage?.width} × {primaryImage?.height} PX</span>
            <span>|</span>
            <span className="uppercase text-slate-300">{primaryImage?.modality}</span>
          </div>

          {overlayEvidence && (
            <button
              onClick={() => setShowOverlay(!showOverlay)}
              className={`px-3 py-1.5 rounded-xl backdrop-blur-md border text-xs font-medium flex items-center space-x-1.5 transition-all shadow-lg ${
                showOverlay ? 'bg-cyan-950/90 text-cyan-300 border-cyan-500/50' : 'bg-space-950/80 text-slate-400 border-slate-800'
              }`}
            >
              {showOverlay ? <Eye className="w-3.5 h-3.5 text-cyan-400" /> : <EyeOff className="w-3.5 h-3.5" />}
              <span>{overlayEvidence.title}</span>
            </button>
          )}
        </div>

        {/* Zoom Controls */}
        <div className="flex items-center space-x-1 bg-space-950/90 backdrop-blur-md border border-slate-800 rounded-xl p-1 pointer-events-auto shadow-lg">
          <button
            onClick={() => setZoomLevel(Math.max(50, zoomLevel - 20))}
            className="p-1.5 hover:bg-slate-800 rounded-lg text-slate-300 text-xs"
            title="Zoom Out"
          >
            <ZoomOut className="w-4 h-4" />
          </button>
          <span className="text-[11px] font-mono px-2 text-slate-300">{zoomLevel}%</span>
          <button
            onClick={() => setZoomLevel(Math.min(200, zoomLevel + 20))}
            className="p-1.5 hover:bg-slate-800 rounded-lg text-slate-300 text-xs"
            title="Zoom In"
          >
            <ZoomIn className="w-4 h-4" />
          </button>
          <button
            onClick={() => setZoomLevel(100)}
            className="p-1.5 hover:bg-slate-800 rounded-lg text-slate-400 text-xs font-mono"
            title="Reset View"
          >
            Reset
          </button>
        </div>
      </div>

      {/* Multimodal Optical + SAR Tab Toggle Bar */}
      {mode === 'optical_sar' && secondaryUrl && (
        <div className="absolute top-16 left-4 z-20 flex items-center space-x-1 p-1 bg-space-950/90 backdrop-blur-md border border-slate-800 rounded-xl pointer-events-auto shadow-lg">
          <button
            onClick={() => setActiveMultimodalTab('fused')}
            className={`px-2.5 py-1 rounded-lg text-[11px] font-mono font-medium transition-all ${
              activeMultimodalTab === 'fused' ? 'bg-cyan-600 text-white shadow-md' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Fused Map
          </button>
          <button
            onClick={() => setActiveMultimodalTab('optical')}
            className={`px-2.5 py-1 rounded-lg text-[11px] font-mono font-medium transition-all ${
              activeMultimodalTab === 'optical' ? 'bg-cyan-600 text-white shadow-md' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Sentinel-2 Optical
          </button>
          <button
            onClick={() => setActiveMultimodalTab('sar')}
            className={`px-2.5 py-1 rounded-lg text-[11px] font-mono font-medium transition-all ${
              activeMultimodalTab === 'sar' ? 'bg-cyan-600 text-white shadow-md' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Sentinel-1 SAR
          </button>
        </div>
      )}

      {/* Main Imagery Render Canvas Area */}
      <div className="relative flex-1 w-full bg-space-950 flex items-center justify-center overflow-hidden">
        {/* Satellite Scanning Overlay Line */}
        <div className="satellite-scan-line pointer-events-none opacity-40" />

        <div
          className="relative transition-transform duration-200"
          style={{ transform: `scale(${zoomLevel / 100})` }}
        >
          {/* Bi-Temporal Swipe Mode */}
          {mode === 'bi_temporal' && secondaryUrl ? (
            <div className="relative overflow-hidden select-none max-w-[640px] rounded-xl shadow-2xl">
              {/* Primary / Before Image */}
              <img src={primaryUrl} alt="Before T1" className="w-full h-auto block rounded-xl" />

              {/* Secondary / After Image with Swipe Clip Path */}
              <div
                className="absolute inset-0 overflow-hidden"
                style={{ clipPath: `polygon(0 0, ${sliderPos}% 0, ${sliderPos}% 100%, 0 100%)` }}
              >
                <img src={secondaryUrl} alt="After T2" className="w-full h-auto block rounded-xl" />
              </div>

              {/* Spatial Change Overlay Layer */}
              {showOverlay && overlayEvidence && (
                <img
                  src={overlayEvidence.url}
                  alt="Spatial Change Map"
                  className="absolute inset-0 w-full h-full object-contain rounded-xl pointer-events-none transition-opacity"
                  style={{ opacity: opacity / 100 }}
                />
              )}

              {/* Slider Line Divider */}
              <div
                className="absolute top-0 bottom-0 w-0.5 bg-cyan-400 cursor-ew-resize z-10"
                style={{ left: `${sliderPos}%` }}
              >
                <div className="absolute top-1/2 -translate-y-1/2 -left-3.5 w-7 h-7 bg-cyan-400 text-space-950 rounded-full flex items-center justify-center shadow-lg font-bold text-xs">
                  ↔
                </div>
              </div>
            </div>
          ) : mode === 'optical_sar' && secondaryUrl ? (
            /* Optical + SAR Multimodal Display */
            <div className="relative max-w-[640px] rounded-xl shadow-2xl overflow-hidden">
              {activeMultimodalTab === 'optical' && (
                <img src={primaryUrl} alt="Optical RGB" className="max-h-[520px] max-w-full block rounded-xl object-contain" />
              )}

              {activeMultimodalTab === 'sar' && (
                <div className="relative">
                  <img src={secondaryUrl} alt="SAR Radar" className="max-h-[520px] max-w-full block rounded-xl object-contain grayscale" />
                  <div className="absolute bottom-3 left-3 bg-space-950/80 px-2.5 py-1 rounded-lg border border-slate-700 text-[10px] font-mono text-cyan-300">
                    Sentinel-1 Dual Polarized Radar (VV/VH Backscatter)
                  </div>
                </div>
              )}

              {activeMultimodalTab === 'fused' && (
                <div className="relative">
                  <img src={primaryUrl} alt="Base Optical" className="max-h-[520px] max-w-full block rounded-xl object-contain" />
                  {showOverlay && overlayEvidence && (
                    <img
                      src={overlayEvidence.url}
                      alt="PyTorch Multimodal Fused Composite"
                      className="absolute inset-0 w-full h-full object-contain rounded-xl pointer-events-none transition-opacity"
                      style={{ opacity: opacity / 100 }}
                    />
                  )}
                </div>
              )}
            </div>
          ) : (
            /* Single Image Grounding / VQA Mode */
            <div className="relative max-w-[640px] rounded-xl shadow-2xl">
              <img src={primaryUrl} alt="Satellite Primary" className="max-h-[520px] max-w-full block rounded-xl object-contain" />

              {/* Grounding Segmentation Mask Overlay */}
              {showOverlay && overlayEvidence && (
                <img
                  src={overlayEvidence.url}
                  alt="AI Grounding Mask Overlay"
                  className="absolute inset-0 w-full h-full object-contain rounded-xl pointer-events-none transition-opacity bbox-reveal"
                  style={{ opacity: opacity / 100 }}
                />
              )}

              {/* Dynamic Bounding Box Highlight Overlay */}
              {showOverlay && bboxData && Array.isArray(bboxData) && (
                <div
                  className="absolute border-2 border-cyan-400 bg-cyan-500/20 rounded-md pointer-events-none bbox-reveal"
                  style={{
                    left: `${(bboxData[0] / (primaryImage?.width || 120)) * 100}%`,
                    top: `${(bboxData[1] / (primaryImage?.height || 120)) * 100}%`,
                    width: `${((bboxData[2] - bboxData[0]) / (primaryImage?.width || 120)) * 100}%`,
                    height: `${((bboxData[3] - bboxData[1]) / (primaryImage?.height || 120)) * 100}%`,
                  }}
                >
                  <span className="absolute -top-5 left-0 px-1.5 py-0.5 bg-cyan-500 text-space-950 font-mono font-bold text-[9px] rounded">
                    {overlayEvidence?.metadata?.target || 'TARGET REGION'}
                  </span>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Bottom Opacity / Swipe Slider Toolbar */}
      <div className="p-3 bg-space-950 border-t border-slate-800 flex items-center justify-between text-xs z-10">
        {mode === 'bi_temporal' && secondaryUrl ? (
          <div className="flex items-center space-x-3 w-full max-w-md mx-auto">
            <span className="text-slate-400 font-mono text-[11px]">Before (T1)</span>
            <input
              type="range"
              min="0"
              max="100"
              value={sliderPos}
              onChange={(e) => setSliderPos(Number(e.target.value))}
              className="flex-1 accent-cyan-400 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
            />
            <span className="text-slate-400 font-mono text-[11px]">After (T2)</span>
            {changePct !== undefined && (
              <span className="px-2 py-0.5 bg-rose-950 text-rose-400 border border-rose-500/40 rounded font-mono text-[11px] font-bold">
                {changePct.toFixed(1)}% Changed
              </span>
            )}
          </div>
        ) : (
          overlayEvidence && (
            <div className="flex items-center space-x-3 w-full max-w-md mx-auto">
              <Sliders className="w-3.5 h-3.5 text-slate-400" />
              <span className="text-slate-400 font-mono text-[11px]">Evidence Opacity:</span>
              <input
                type="range"
                min="10"
                max="100"
                value={opacity}
                onChange={(e) => setOpacity(Number(e.target.value))}
                className="flex-1 accent-cyan-400 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
              />
              <span className="text-slate-300 font-mono text-[11px] w-8">{opacity}%</span>
            </div>
          )
        )}
      </div>
    </div>
  );
};
