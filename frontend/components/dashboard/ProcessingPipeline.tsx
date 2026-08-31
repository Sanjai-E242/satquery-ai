'use client';

import React, { useEffect, useState } from 'react';
import { CheckCircle2, Loader2, Sparkles, Cpu, Layers, FileCheck } from 'lucide-react';

interface ProcessingPipelineProps {
  loading: boolean;
  mode: string;
}

export const ProcessingPipeline: React.FC<ProcessingPipelineProps> = ({ loading, mode }) => {
  const [currentStep, setCurrentStep] = useState<number>(0);

  const steps = [
    { id: 1, label: "Upload received & georeference inspected" },
    { id: 2, label: "Understanding natural language query intent" },
    { id: 3, label: `Routing task to ${mode.toUpperCase()} specialist pipeline` },
    { id: 4, label: "Executing PyTorch neural model inference" },
    { id: 5, label: "Generating visual evidence & spatial overlays" },
    { id: 6, label: "Calibrating dynamic confidence & packaging result" }
  ];

  useEffect(() => {
    if (!loading) {
      setCurrentStep(0);
      return;
    }

    setCurrentStep(1);
    const t1 = setTimeout(() => setCurrentStep(2), 600);
    const t2 = setTimeout(() => setCurrentStep(3), 1400);
    const t3 = setTimeout(() => setCurrentStep(4), 2200);
    const t4 = setTimeout(() => setCurrentStep(5), 12000);
    const t5 = setTimeout(() => setCurrentStep(6), 18000);

    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
      clearTimeout(t3);
      clearTimeout(t4);
      clearTimeout(t5);
    };
  }, [loading, mode]);

  if (!loading) return null;

  return (
    <div className="glass-panel rounded-2xl p-4 border border-cyan-500/30 space-y-3 animate-fadeIn shadow-xl">
      <div className="flex items-center justify-between pb-2 border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <Loader2 className="w-4 h-4 text-cyan-400 animate-spin" />
          <span className="text-xs font-semibold text-cyan-300 font-mono uppercase">PyTorch AI Model Execution Pipeline</span>
        </div>
        <span className="text-[10px] font-mono text-cyan-400/70">Stage {currentStep}/06</span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
        {steps.map((step) => {
          const isDone = currentStep > step.id;
          const isCurrent = currentStep === step.id;

          return (
            <div
              key={step.id}
              className={`p-2 rounded-xl border transition-all text-xs flex items-center space-x-2 ${
                isDone
                  ? 'bg-emerald-950/40 border-emerald-500/30 text-emerald-300'
                  : isCurrent
                  ? 'bg-cyan-950/70 border-cyan-500/50 text-cyan-200 animate-pulse'
                  : 'bg-space-950/40 border-slate-850 text-slate-500'
              }`}
            >
              <span className="font-mono text-[10px] font-bold w-5 h-5 rounded-lg bg-space-950 flex items-center justify-center flex-shrink-0">
                0{step.id}
              </span>
              <span className="truncate text-[11px] font-medium">{step.label}</span>
              {isDone && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 ml-auto flex-shrink-0" />}
              {isCurrent && <Loader2 className="w-3.5 h-3.5 text-cyan-400 animate-spin ml-auto flex-shrink-0" />}
            </div>
          );
        })}
      </div>
    </div>
  );
};
