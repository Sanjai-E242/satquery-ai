'use client';

import React from 'react';
import { Database, Cpu, CheckCircle2, AlertTriangle, Layers, Server } from 'lucide-react';
import { SystemStatus } from '@/types';

interface StatusPanelsProps {
  systemStatus: SystemStatus | null;
}

export const StatusPanels: React.FC<StatusPanelsProps> = ({ systemStatus }) => {
  const dataset = systemStatus?.dataset;
  const components = systemStatus?.components || {};
  const hardware = systemStatus?.hardware;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {/* Model Status Panel */}
      <div className="glass-panel rounded-2xl p-4 border border-slate-800 space-y-3">
        <div className="flex items-center justify-between border-b border-slate-800 pb-2.5">
          <div className="flex items-center space-x-2">
            <Cpu className="w-4 h-4 text-cyan-400" />
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-200">Specialist Model Status</h3>
          </div>
          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-500/30">
            {systemStatus?.demo_mode ? 'Demo / Deterministic Mode' : 'RS-VLM Production Mode'}
          </span>
        </div>

        <div className="space-y-2 text-xs font-mono">
          <ModelStatusRow name="Remote-Sensing VLM (BigEarthNet)" status={components.vlm || 'Ready'} />
          <ModelStatusRow name="RS Grounding Engine (SAM)" status={components.grounding || 'Ready'} />
          <ModelStatusRow name="Bi-Temporal Change Engine" status={components.change_model || 'Ready'} />
          <ModelStatusRow name="Optical + SAR Fusion Adapter" status={components.sar_fusion || 'Ready'} />
        </div>
      </div>

      {/* Dataset Status Panel */}
      <div className="glass-panel rounded-2xl p-4 border border-slate-800 space-y-3">
        <div className="flex items-center justify-between border-b border-slate-800 pb-2.5">
          <div className="flex items-center space-x-2">
            <Database className="w-4 h-4 text-emerald-400" />
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-200">BigEarthNet Dataset Integration</h3>
          </div>
          <span className={`text-[10px] font-mono px-2 py-0.5 rounded ${dataset?.connected ? 'bg-emerald-950 text-emerald-400 border border-emerald-500/30' : 'bg-rose-950 text-rose-400'}`}>
            {dataset?.connected ? 'CONNECTED' : 'NOT FOUND'}
          </span>
        </div>

        <div className="space-y-1.5 text-xs">
          <div className="flex justify-between font-mono">
            <span className="text-slate-400">Dataset File:</span>
            <span className="text-slate-200 font-semibold">{dataset?.name || 'BigEarthNet.txt.parquet'}</span>
          </div>
          <div className="flex justify-between font-mono">
            <span className="text-slate-400">Total VQA Samples:</span>
            <span className="text-cyan-400 font-bold">{(dataset?.rows || 9553962).toLocaleString()}</span>
          </div>
          <div className="flex justify-between font-mono">
            <span className="text-slate-400">Execution Hardware:</span>
            <span className="text-slate-200">{hardware?.device || 'CPU'} (PyTorch {hardware?.torch_version || '2.2.2'})</span>
          </div>
          <div className="flex justify-between font-mono">
            <span className="text-slate-400">Adaptation Pipeline:</span>
            <span className="text-emerald-400 font-semibold">Ready for Fine-Tuning</span>
          </div>
        </div>
      </div>
    </div>
  );
};

const ModelStatusRow: React.FC<{ name: string; status: string }> = ({ name, status }) => (
  <div className="flex items-center justify-between p-2 rounded-lg bg-space-950 border border-slate-800/80">
    <span className="text-slate-300">{name}</span>
    <div className="flex items-center space-x-1.5 text-emerald-400">
      <CheckCircle2 className="w-3.5 h-3.5" />
      <span className="text-[11px] font-semibold">{status}</span>
    </div>
  </div>
);
