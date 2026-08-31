'use client';

import React from 'react';
import Link from 'next/link';
import { Satellite, Cpu, Award, Users, Info, Sparkles, BookOpen, Layers, Send } from 'lucide-react';
import { SystemStatus } from '@/types';
import { identityConfig } from '@/lib/identityConfig';

interface HeaderProps {
  systemStatus?: SystemStatus | null;
}

export const Header: React.FC<HeaderProps> = ({ systemStatus }) => {
  const isReady = systemStatus?.status === 'READY';

  const scrollToSection = (e: React.MouseEvent<HTMLAnchorElement>, id: string) => {
    e.preventDefault();
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-slate-800/80 px-4 sm:px-6 py-3 flex items-center justify-between">
      {/* Brand Logo & Title */}
      <div className="flex items-center space-x-3.5">
        <Link href="/" className="flex items-center space-x-3 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 via-blue-600 to-indigo-600 p-0.5 shadow-lg shadow-cyan-500/20 group-hover:scale-105 transition-transform">
            <div className="w-full h-full bg-space-950 rounded-[10px] flex items-center justify-center">
              <Satellite className="w-5 h-5 text-cyan-400 animate-pulse" />
            </div>
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="font-bold tracking-wider text-lg bg-gradient-to-r from-white via-slate-100 to-cyan-400 bg-clip-text text-transparent">
                {identityConfig.PROJECT_NAME}
              </h1>
              <span className="px-2 py-0.5 text-[10px] font-mono uppercase font-bold tracking-widest bg-cyan-950/80 text-cyan-400 border border-cyan-500/30 rounded-full">
                {identityConfig.SIH_PROBLEM_ID}
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block font-medium">
              {identityConfig.TAGLINE}
            </p>
          </div>
        </Link>
      </div>

      {/* Center Navigation Links (Desktop) */}
      <nav className="hidden xl:flex items-center space-x-1 text-xs font-medium text-slate-400">
        <a 
          href="#about"
          onClick={(e) => scrollToSection(e, 'about')}
          className="px-3 py-1.5 rounded-lg hover:text-cyan-300 hover:bg-slate-900/60 transition-all"
        >
          About
        </a>
        <a 
          href="#tech"
          onClick={(e) => scrollToSection(e, 'tech')}
          className="px-3 py-1.5 rounded-lg hover:text-cyan-300 hover:bg-slate-900/60 transition-all"
        >
          Technology
        </a>
        <a 
          href="#team"
          onClick={(e) => scrollToSection(e, 'team')}
          className="px-3 py-1.5 rounded-lg hover:text-cyan-300 hover:bg-slate-900/60 transition-all"
        >
          Team
        </a>
        <a 
          href="#contact"
          onClick={(e) => scrollToSection(e, 'contact')}
          className="px-3 py-1.5 rounded-lg hover:text-cyan-300 hover:bg-slate-900/60 transition-all"
        >
          Contact
        </a>
      </nav>

      {/* Live System Status Badges & Team Section Trigger */}
      <div className="flex items-center space-x-2.5 text-xs">
        {/* Team Section Smooth-Scroll Button */}
        <a
          href="#team"
          onClick={(e) => scrollToSection(e, 'team')}
          className="px-3 py-1.5 rounded-lg bg-cyan-950/70 hover:bg-cyan-900/80 border border-cyan-500/30 text-cyan-300 text-xs font-medium flex items-center space-x-1.5 transition-all shadow-md cursor-pointer group"
          title="Jump to Team Section"
        >
          <Award className="w-3.5 h-3.5 text-cyan-400 group-hover:rotate-12 transition-transform" />
          <span className="hidden sm:inline font-mono">{identityConfig.TEAM_NAME}</span>
          <span className="sm:hidden">Team</span>
        </a>

        {/* Model Mode Indicator */}
        <div className="hidden lg:flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800 text-slate-300">
          <Cpu className="w-3.5 h-3.5 text-cyan-400" />
          <span>{systemStatus?.demo_mode ? 'VLM ACTIVE (Florence-2 / LoRA)' : 'RS-VLM ACTIVE'}</span>
        </div>

        {/* System Health Readiness */}
        <div className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800">
          <span className={`w-2 h-2 rounded-full ${isReady ? 'bg-emerald-400 shadow-[0_0_8px_#10B981]' : 'bg-amber-400'}`}></span>
          <span className="font-semibold tracking-wide text-slate-200 uppercase text-[11px]">
            {isReady ? 'READY' : 'CONNECTING...'}
          </span>
        </div>
      </div>
    </header>
  );
};
