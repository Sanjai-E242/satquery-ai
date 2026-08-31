'use client';

import React from 'react';
import { Mail, Phone, Building2, GraduationCap, Users, Sparkles, Send } from 'lucide-react';
import { identityConfig } from '@/lib/identityConfig';

export const ContactSection: React.FC = () => {
  return (
    <section id="contact" className="py-8 scroll-mt-20">
      <div className="glass-panel rounded-3xl p-6 sm:p-10 border border-slate-800 shadow-2xl relative overflow-hidden">
        {/* Section Header */}
        <div className="text-center max-w-2xl mx-auto space-y-3">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-cyan-950/80 border border-cyan-500/30 text-cyan-400 text-xs font-mono font-bold tracking-widest uppercase">
            <Send className="w-3.5 h-3.5" />
            <span>Get in Touch</span>
          </div>

          <h2 className="text-2xl sm:text-4xl font-extrabold text-slate-100 tracking-tight">
            Contact &amp; Institution
          </h2>

          <p className="text-xs sm:text-sm text-slate-400">
            For academic inquiries, collaboration, and deployment details.
          </p>
        </div>

        {/* Contact Info Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mt-10 max-w-5xl mx-auto">
          {/* Card 1: Team & Project Info */}
          <div className="p-5 rounded-2xl bg-space-950/80 border border-slate-800 flex items-start space-x-4">
            <div className="w-10 h-10 rounded-xl bg-cyan-950 border border-cyan-500/30 flex items-center justify-center shrink-0">
              <Users className="w-5 h-5 text-cyan-400" />
            </div>
            <div className="space-y-1">
              <span className="text-[11px] font-mono uppercase text-slate-400">Team Name</span>
              <p className="text-sm font-bold text-slate-100">{identityConfig.TEAM_NAME}</p>
              <p className="text-xs text-cyan-400 font-mono">SIH Problem: {identityConfig.SIH_PROBLEM_ID}</p>
            </div>
          </div>

          {/* Card 2: Email & Phone */}
          <div className="p-5 rounded-2xl bg-space-950/80 border border-slate-800 flex items-start space-x-4">
            <div className="w-10 h-10 rounded-xl bg-indigo-950 border border-indigo-500/30 flex items-center justify-center shrink-0">
              <Mail className="w-5 h-5 text-indigo-400" />
            </div>
            <div className="space-y-1 overflow-hidden">
              <span className="text-[11px] font-mono uppercase text-slate-400">Direct Contact</span>
              <a 
                href={`mailto:${identityConfig.CONTACT_EMAIL}`}
                className="text-xs font-semibold text-cyan-300 hover:underline block truncate"
              >
                {identityConfig.CONTACT_EMAIL}
              </a>
              <div className="flex items-center space-x-1.5 pt-0.5 text-xs text-slate-300">
                <Phone className="w-3 h-3 text-cyan-400" />
                <span className="font-mono">{identityConfig.MOBILE}</span>
              </div>
            </div>
          </div>

          {/* Card 3: Institution & Department */}
          <div className="p-5 rounded-2xl bg-space-950/80 border border-slate-800 flex items-start space-x-4 md:col-span-2 lg:col-span-1">
            <div className="w-10 h-10 rounded-xl bg-emerald-950 border border-emerald-500/30 flex items-center justify-center shrink-0">
              <GraduationCap className="w-5 h-5 text-emerald-400" />
            </div>
            <div className="space-y-1">
              <span className="text-[11px] font-mono uppercase text-slate-400">College &amp; Department</span>
              <p className="text-xs font-bold text-slate-100 leading-snug">{identityConfig.COLLEGE_NAME}</p>
              <p className="text-[11px] text-slate-400">{identityConfig.DEPARTMENT}</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
