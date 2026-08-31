'use client';

import React from 'react';
import { 
  Satellite, 
  MessageSquare, 
  Target, 
  GitCompare, 
  Layers, 
  ShieldCheck, 
  Eye, 
  FileText,
  Sparkles
} from 'lucide-react';
import { identityConfig } from '@/lib/identityConfig';

export const AboutSection: React.FC = () => {
  const capabilities = [
    {
      title: "Satellite Image Visual Question Answering",
      desc: "Ask complex natural-language queries about land cover, vegetation density, and scene context.",
      icon: MessageSquare,
      color: "from-cyan-500/20 to-blue-500/20",
      border: "border-cyan-500/30",
      iconColor: "text-cyan-400"
    },
    {
      title: "Text-Guided Object/Region Grounding",
      desc: "Localize specific physical regions, land features, and structures with dynamic bounding boxes.",
      icon: Target,
      color: "from-indigo-500/20 to-purple-500/20",
      border: "border-indigo-500/30",
      iconColor: "text-indigo-400"
    },
    {
      title: "Bi-Temporal Change Detection",
      desc: "Extract deep Siamese neural spatial distance maps to quantify physical surface modifications between T1 and T2.",
      icon: GitCompare,
      color: "from-emerald-500/20 to-teal-500/20",
      border: "border-emerald-500/30",
      iconColor: "text-emerald-400"
    },
    {
      title: "Sentinel-2 Optical + Sentinel-1 SAR Fusion",
      desc: "Cross-modal attention combining multispectral optical bands with cloud-penetrating radar backscatter.",
      icon: Layers,
      color: "from-amber-500/20 to-orange-500/20",
      border: "border-amber-500/30",
      iconColor: "text-amber-400"
    },
    {
      title: "Confidence-Aware AI Analysis",
      desc: "Dynamically calibrated uncertainty quantification grounded in genuine neural activations and model metrics.",
      icon: ShieldCheck,
      color: "from-blue-500/20 to-cyan-500/20",
      border: "border-blue-500/30",
      iconColor: "text-blue-400"
    },
    {
      title: "Evidence-Based Results",
      desc: "Visual transparent overlays, bounding coordinates, and heatmaps showing exact rationale for every AI answer.",
      icon: Eye,
      color: "from-violet-500/20 to-indigo-500/20",
      border: "border-violet-500/30",
      iconColor: "text-violet-400"
    },
    {
      title: "PDF and JSON Report Generation",
      desc: "Production-ready automated intelligence dossiers and machine-readable JSON exports for mission workflows.",
      icon: FileText,
      color: "from-cyan-500/20 to-emerald-500/20",
      border: "border-cyan-500/30",
      iconColor: "text-cyan-400"
    }
  ];

  return (
    <section id="about" className="pt-12 pb-8 scroll-mt-20">
      <div className="glass-panel rounded-3xl p-6 sm:p-10 border border-cyan-500/20 shadow-2xl relative overflow-hidden">
        {/* Background Ambient Glow */}
        <div className="absolute -top-24 -left-24 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-24 -right-24 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto space-y-3 relative z-10">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-cyan-950/80 border border-cyan-500/30 text-cyan-400 text-xs font-mono font-bold tracking-widest uppercase">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Platform Overview</span>
          </div>
          
          <h2 className="text-2xl sm:text-4xl font-extrabold text-slate-100 tracking-tight">
            About <span className="bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-400 bg-clip-text text-transparent">SatQuery AI</span>
          </h2>

          <p className="text-sm sm:text-base font-medium text-cyan-300/90 max-w-xl mx-auto">
            &ldquo;Ask questions. Analyze satellite imagery. Discover meaningful geospatial insights.&rdquo;
          </p>

          <p className="text-xs sm:text-sm text-slate-400 leading-relaxed pt-2">
            SatQuery AI is an intelligent satellite image analysis platform that enables users to interact with remote-sensing imagery using natural-language queries. It combines computer vision, vision-language AI, geospatial analysis, change detection, and multimodal satellite data processing to provide explainable insights from satellite imagery.
          </p>
        </div>

        {/* Supported Capabilities Grid */}
        <div className="mt-10 pt-8 border-t border-slate-800/80 relative z-10">
          <h3 className="text-xs font-mono uppercase tracking-widest text-slate-400 text-center mb-6">
            Core Supported Capabilities
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {capabilities.map((cap, idx) => {
              const IconComp = cap.icon;
              return (
                <div 
                  key={idx}
                  className={`p-4 rounded-2xl bg-space-950/80 border ${cap.border} bg-gradient-to-br ${cap.color} hover:scale-[1.02] hover:border-cyan-400/50 transition-all duration-200 group flex flex-col justify-between`}
                >
                  <div className="space-y-2.5">
                    <div className="w-9 h-9 rounded-xl bg-space-900/90 border border-slate-700/80 flex items-center justify-center shadow-md group-hover:border-cyan-500/40">
                      <IconComp className={`w-5 h-5 ${cap.iconColor}`} />
                    </div>
                    <h4 className="text-xs sm:text-sm font-bold text-slate-100 group-hover:text-cyan-300 transition-colors">
                      {cap.title}
                    </h4>
                    <p className="text-[11px] sm:text-xs text-slate-400 leading-relaxed">
                      {cap.desc}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
};
