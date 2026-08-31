'use client';

import React from 'react';
import { CheckCircle2, Clock, GitBranch, Cpu, ShieldCheck } from 'lucide-react';
import { ExecutionStep } from '@/types';

interface ExecutionTraceProps {
  steps: ExecutionStep[];
  modelsUsed?: string[];
  toolsUsed?: string[];
  totalDurationMs?: number;
  executionId?: string;
}

export const ExecutionTrace: React.FC<ExecutionTraceProps> = ({
  steps,
  modelsUsed = [],
  toolsUsed = [],
  totalDurationMs = 0,
  executionId
}) => {
  if (!steps || steps.length === 0) return null;

  return (
    <div className="glass-panel rounded-2xl p-5 border border-slate-800 space-y-4">
      {/* Title Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2.5">
          <GitBranch className="w-4 h-4 text-cyan-400" />
          <h3 className="text-sm font-semibold text-slate-200">Observable Agent Execution Trace</h3>
          {executionId && (
            <span className="px-2 py-0.5 rounded bg-space-950 border border-slate-800 text-[10px] font-mono text-cyan-400">
              {executionId}
            </span>
          )}
        </div>
        <div className="flex items-center space-x-2 text-xs font-mono text-slate-400">
          <Clock className="w-3.5 h-3.5 text-cyan-400" />
          <span>{totalDurationMs} ms</span>
        </div>
      </div>

      {/* Step Nodes Tree */}
      <div className="space-y-3 relative before:absolute before:left-3.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-800">
        {steps.map((step, idx) => (
          <div key={idx} className="relative flex items-start space-x-3.5 z-10">
            {/* Step Icon */}
            <div className="w-7 h-7 rounded-full bg-space-950 border border-cyan-500/40 flex items-center justify-center flex-shrink-0 shadow-md">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            </div>

            {/* Step Content Card */}
            <div className="flex-1 p-3 rounded-xl bg-space-950/70 border border-slate-800/80 text-xs space-y-1">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-slate-200">{step.name}</span>
                <span className="text-[10px] font-mono text-emerald-400 bg-emerald-950/50 px-2 py-0.5 rounded border border-emerald-500/20">
                  {step.status.toUpperCase()} ({step.duration_ms}ms)
                </span>
              </div>
              {step.detail && (
                <p className="text-[11px] text-slate-400 font-mono">{step.detail}</p>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Summary Footer Badges */}
      {(modelsUsed.length > 0 || toolsUsed.length > 0) && (
        <div className="pt-2 border-t border-slate-800 flex flex-wrap items-center gap-2 text-[11px] font-mono">
          <span className="text-slate-400">Selected Tools:</span>
          {modelsUsed.concat(toolsUsed).map((item, i) => (
            <span key={i} className="px-2.5 py-1 rounded-md bg-slate-900 border border-slate-700/80 text-cyan-300">
              {item}
            </span>
          ))}
        </div>
      )}
    </div>
  );
};
