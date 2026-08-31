'use client';

import React from 'react';
import { 
  Layout, 
  Server, 
  BrainCircuit, 
  ScanSearch, 
  Globe, 
  GitBranch, 
  Layers, 
  FileCheck, 
  Terminal,
  Code2,
  Sparkles
} from 'lucide-react';

interface TechCategory {
  category: string;
  items: string[];
  description: string;
  icon: React.ElementType;
  badgeColor: string;
}

export const TechnologySection: React.FC = () => {
  const techStack: TechCategory[] = [
    {
      category: "Frontend Architecture",
      items: ["Next.js", "React", "TypeScript", "Tailwind CSS"],
      description: "Modern responsive web interface for interacting with satellite AI workflows.",
      icon: Layout,
      badgeColor: "bg-cyan-950/70 border-cyan-500/30 text-cyan-300"
    },
    {
      category: "Backend & API Systems",
      items: ["Python 3.9+", "FastAPI", "Uvicorn"],
      description: "High-performance API layer powering the satellite analysis pipeline.",
      icon: Server,
      badgeColor: "bg-blue-950/70 border-blue-500/30 text-blue-300"
    },
    {
      category: "AI & Deep Learning",
      items: ["PyTorch", "Hugging Face Transformers", "Florence-2"],
      description: "Vision-language and deep-learning components for satellite image understanding, VQA and grounding.",
      icon: BrainCircuit,
      badgeColor: "bg-indigo-950/70 border-indigo-500/30 text-indigo-300"
    },
    {
      category: "Computer Vision & Spatial Engine",
      items: ["Computer Vision", "Image Processing", "Spatial Grounding", "Segmentation"],
      description: "Extracts visual and spatial information from satellite imagery and supports text-guided localization.",
      icon: ScanSearch,
      badgeColor: "bg-violet-950/70 border-violet-500/30 text-violet-300"
    },
    {
      category: "Remote Sensing & Geospatial",
      items: ["Sentinel-1", "Sentinel-2", "BigEarthNet"],
      description: "Multispectral optical and SAR satellite data used for remote-sensing analysis and model adaptation.",
      icon: Globe,
      badgeColor: "bg-emerald-950/70 border-emerald-500/30 text-emerald-300"
    },
    {
      category: "Change Detection",
      items: ["Neural Change Detection", "Classical Change Detection"],
      description: "Combines learned and classical approaches to identify differences between temporal satellite observations.",
      icon: GitBranch,
      badgeColor: "bg-teal-950/70 border-teal-500/30 text-teal-300"
    },
    {
      category: "Multimodal AI & Fusion",
      items: ["Optical + SAR Fusion", "Feature Alignment", "Dynamic Channel Attention"],
      description: "Combines complementary optical and radar information for richer satellite scene understanding.",
      icon: Layers,
      badgeColor: "bg-amber-950/70 border-amber-500/30 text-amber-300"
    },
    {
      category: "Report Generation",
      items: ["PDF Reports", "JSON Reports"],
      description: "Export analysis results, evidence and confidence information for further use.",
      icon: FileCheck,
      badgeColor: "bg-sky-950/70 border-sky-500/30 text-sky-300"
    },
    {
      category: "Development / Version Control",
      items: ["Git", "GitHub", "Antigravity IDE", "Visual Studio Code (VS Code)"],
      description: "Used as the primary code editor and development environment for building, debugging, and managing the SatQuery AI project.",
      icon: Terminal,
      badgeColor: "bg-slate-900 border-slate-700 text-slate-300"
    },
    {
      category: "AI Research & Development",
      items: ["ChatGPT", "Claude", "Google Gemini"],
      description: "Used for research, technical exploration, problem solving, documentation, ideation, and AI-assisted development throughout the project.",
      icon: Sparkles,
      badgeColor: "bg-fuchsia-950/70 border-fuchsia-500/30 text-fuchsia-300"
    }
  ];

  return (
    <section id="tech" className="py-8 scroll-mt-20">
      <div className="glass-panel rounded-3xl p-6 sm:p-10 border border-slate-800 shadow-2xl relative overflow-hidden">
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto space-y-3">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-blue-950/80 border border-blue-500/30 text-blue-400 text-xs font-mono font-bold tracking-widest uppercase">
            <Code2 className="w-3.5 h-3.5" />
            <span>Architecture &amp; Stack</span>
          </div>

          <h2 className="text-2xl sm:text-4xl font-extrabold text-slate-100 tracking-tight">
            Technology &amp; Tools
          </h2>

          <p className="text-xs sm:text-sm text-slate-400 max-w-xl mx-auto">
            Built with modern AI, computer vision, geospatial and full-stack technologies.
          </p>
        </div>

        {/* Tech Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5 mt-10">
          {techStack.map((tech, idx) => {
            const IconComponent = tech.icon;
            return (
              <div
                key={idx}
                className="p-5 rounded-2xl bg-space-950/70 border border-slate-800/80 hover:border-cyan-500/40 hover:bg-space-900/60 transition-all duration-200 group flex flex-col justify-between"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="w-10 h-10 rounded-xl bg-space-900 border border-slate-800 flex items-center justify-center group-hover:border-cyan-500/40 group-hover:scale-105 transition-all">
                      <IconComponent className="w-5 h-5 text-cyan-400" />
                    </div>
                    <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">
                      Module {String(idx + 1).padStart(2, '0')}
                    </span>
                  </div>

                  <div>
                    <h3 className="text-sm font-bold text-slate-100 group-hover:text-cyan-300 transition-colors">
                      {tech.category}
                    </h3>
                    <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                      {tech.description}
                    </p>
                  </div>
                </div>

                <div className="flex flex-wrap gap-1.5 pt-4 mt-3 border-t border-slate-800/60">
                  {tech.items.map((item, i) => (
                    <span
                      key={i}
                      className={`px-2 py-0.5 rounded-md text-[11px] font-mono font-medium border ${tech.badgeColor}`}
                    >
                      {item}
                    </span>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
