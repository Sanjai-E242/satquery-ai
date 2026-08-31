'use client';

import React from 'react';
import { Users, Award, Shield, Terminal, Palette, Cpu, Sparkles, Code2 } from 'lucide-react';
import { identityConfig } from '@/lib/identityConfig';

export const TeamSection: React.FC = () => {
  const memberIcons: { [key: string]: React.ElementType } = {
    "Sanjai": Code2,
    "Sanjay Kumar": Cpu,
    "Sanjay": Cpu,
    "Saqlain": Terminal,
    "Prathesha": Palette,
    "Sujit": Shield,
    "Saravana": Award
  };

  const renderCard = (member: typeof identityConfig.TEAM_MEMBERS[0], idx: number) => {
    const IconComp = memberIcons[member.name] || Users;
    const initials = member.name
      .split(' ')
      .map(part => part[0])
      .join('')
      .slice(0, 2)
      .toUpperCase();

    return (
      <div 
        key={member.name}
        className="glass-panel p-6 rounded-2xl border border-slate-800 hover:border-cyan-500/50 hover:shadow-[0_0_20px_rgba(6,182,212,0.15)] transition-all duration-300 group flex flex-col items-center text-center space-y-4 bg-gradient-to-b from-space-900/90 to-space-950/90 relative overflow-hidden"
      >
        {/* Subtle Ambient Light */}
        <div className="absolute -top-12 left-1/2 -translate-x-1/2 w-32 h-32 bg-cyan-500/10 rounded-full blur-2xl group-hover:bg-cyan-500/20 transition-all pointer-events-none" />

        {/* Member Avatar */}
        <div className="relative">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-cyan-600 via-blue-600 to-indigo-600 p-0.5 shadow-lg group-hover:scale-105 transition-transform duration-300">
            <div className="w-full h-full bg-space-950 rounded-[14px] flex items-center justify-center">
              <span className="font-bold text-lg text-cyan-300 font-mono">
                {initials}
              </span>
            </div>
          </div>
          <div className="absolute -bottom-1 -right-1 p-1 rounded-full bg-space-900 border border-slate-700 text-cyan-400">
            <IconComp className="w-3.5 h-3.5" />
          </div>
        </div>

        {/* Member Info */}
        <div className="space-y-1 w-full">
          <h3 className="font-bold text-base text-slate-100 group-hover:text-cyan-300 transition-colors">
            {member.name}
          </h3>
          <p className="text-xs font-semibold text-cyan-400/90 leading-tight">
            {member.role}
          </p>
        </div>

        {/* Skills / Specialization Tags */}
        {member.skills && member.skills.length > 0 && (
          <div className="flex flex-wrap justify-center gap-1.5 pt-2 border-t border-slate-800/80 w-full">
            {member.skills.map((skill, sIdx) => (
              <span 
                key={sIdx}
                className="px-2 py-0.5 rounded-md text-[10px] font-mono bg-cyan-950/40 border border-cyan-500/20 text-slate-300"
              >
                {skill}
              </span>
            ))}
          </div>
        )}
      </div>
    );
  };

  return (
    <section id="team" className="py-8 scroll-mt-20">
      <div className="glass-panel rounded-3xl p-6 sm:p-10 border border-slate-800 shadow-2xl relative overflow-hidden">
        {/* Section Header */}
        <div className="text-center max-w-2xl mx-auto space-y-3">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-cyan-950/80 border border-cyan-500/30 text-cyan-400 text-xs font-mono font-bold tracking-widest uppercase">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Core Engineering Team</span>
          </div>

          <h2 className="text-2xl sm:text-4xl font-extrabold text-slate-100 tracking-tight">
            Meet the Team
          </h2>

          <p className="text-xs sm:text-sm text-slate-400 font-medium">
            Team 404 Coders — Building SatQuery AI
          </p>
        </div>

        {/* Team Grid: 6 Members in 3-Col Desktop Grid, 2-Col Tablet, 1-Col Mobile */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mt-10">
          {identityConfig.TEAM_MEMBERS.map((member, idx) => renderCard(member, idx))}
        </div>
      </div>
    </section>
  );
};
