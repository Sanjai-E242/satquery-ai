'use client';

import React from 'react';
import Link from 'next/link';
import { Satellite, Code, Sparkles, Heart } from 'lucide-react';
import { identityConfig } from '@/lib/identityConfig';

export const Footer: React.FC = () => {
  return (
    <footer className="mt-12 border-t border-slate-800/80 bg-space-950/90 backdrop-blur-xl relative z-10">
      {/* Top Footer Section */}
      <div className="max-w-[1600px] mx-auto px-4 sm:px-6 py-10">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          {/* Brand Info */}
          <div className="flex items-center space-x-3.5 text-center md:text-left">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 via-blue-600 to-indigo-600 p-0.5 shadow-lg shadow-cyan-500/20">
              <div className="w-full h-full bg-space-950 rounded-[10px] flex items-center justify-center">
                <Satellite className="w-5 h-5 text-cyan-400" />
              </div>
            </div>
            <div>
              <div className="flex items-center justify-center md:justify-start space-x-2">
                <h3 className="font-bold text-base tracking-wider text-slate-100">
                  {identityConfig.PROJECT_NAME}
                </h3>
                <span className="px-2 py-0.5 text-[9px] font-mono font-bold uppercase tracking-widest bg-cyan-950/80 text-cyan-400 border border-cyan-500/30 rounded-full">
                  {identityConfig.SIH_PROBLEM_ID}
                </span>
              </div>
              <p className="text-xs text-slate-400 font-medium">
                Intelligent Satellite Image Analysis &bull; {identityConfig.TEAM_NAME}
              </p>
            </div>
          </div>

          {/* Quick Navigation Links */}
          <div className="flex flex-wrap justify-center items-center gap-4 sm:gap-6 text-xs font-mono text-slate-400">
            <a href="#about" className="hover:text-cyan-300 transition-colors">
              #about
            </a>
            <a href="#tech" className="hover:text-cyan-300 transition-colors">
              #technology
            </a>
            <a href="#team" className="hover:text-cyan-300 transition-colors">
              #team
            </a>
            <a href="#contact" className="hover:text-cyan-300 transition-colors">
              #contact
            </a>
          </div>
        </div>

        {/* Divider */}
        <div className="my-8 border-t border-slate-800/80" />

        {/* Developer Credit: Prominent Futuristic Badge */}
        <div className="flex flex-col items-center justify-center text-center space-y-2 py-2">
          <div className="inline-flex items-center space-x-2.5 px-5 py-2.5 rounded-2xl bg-gradient-to-r from-cyan-950/60 via-space-900 to-indigo-950/60 border border-cyan-500/40 shadow-[0_0_25px_rgba(6,182,212,0.2)] hover:border-cyan-400 transition-all group">
            <div className="w-7 h-7 rounded-lg bg-cyan-950 border border-cyan-400/40 flex items-center justify-center shadow-inner">
              <Code className="w-3.5 h-3.5 text-cyan-300" />
            </div>
            <div className="text-left">
              <p className="text-xs font-mono uppercase tracking-wider text-slate-400 text-[10px]">
                Developer Credit
              </p>
              <p className="text-sm font-bold bg-gradient-to-r from-white via-cyan-200 to-cyan-400 bg-clip-text text-transparent">
                Developed by {identityConfig.DEVELOPED_BY} &mdash; {identityConfig.DEVELOPER_ROLE}
              </p>
            </div>
          </div>

          <p className="text-[11px] text-slate-400 pt-1">
            {identityConfig.COLLEGE_NAME} &bull; {identityConfig.DEPARTMENT}
          </p>
        </div>

        {/* Divider */}
        <div className="my-6 border-t border-slate-800/60" />

        {/* Copyright Line */}
        <div className="flex flex-col sm:flex-row items-center justify-between text-center sm:text-left gap-2 text-[11px] text-slate-400 font-mono">
          <p>
            &copy; 2026 {identityConfig.PROJECT_NAME} &bull; {identityConfig.TEAM_NAME}
          </p>
          <p className="text-slate-400">
            Smart India Hackathon {identityConfig.SIH_PROBLEM_ID} &bull; Autonomous Geospatial AI
          </p>
        </div>
      </div>
    </footer>
  );
};
