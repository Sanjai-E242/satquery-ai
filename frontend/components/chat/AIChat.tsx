'use client';

import React, { useState } from 'react';
import { Send, Bot, User, Sparkles, Download, FileText, CheckCircle2, ShieldAlert } from 'lucide-react';
import { AnalysisResult } from '@/types';
import { generateReport, getReportDownloadUrl } from '@/lib/api';

interface AIChatProps {
  onSendQuery: (query: string) => void;
  loading: boolean;
  result: AnalysisResult | null;
  mode: 'single' | 'bi_temporal' | 'optical_sar';
}

export const AIChat: React.FC<AIChatProps> = ({
  onSendQuery,
  loading,
  result,
  mode
}) => {
  const [inputText, setInputText] = useState('');
  const [generatingReport, setGeneratingReport] = useState(false);

  const samplePrompts = {
    single: [
      "What is the dominant land cover class?",
      "Locate the water body in this image.",
      "Are there built-up urban structures visible?"
    ],
    bi_temporal: [
      "Identify land cover changes between T1 and T2 images.",
      "Has the built-up urban area increased?",
      "Show spatial change map overlay."
    ],
    optical_sar: [
      "Perform cross-modal Sentinel-2 Optical + Sentinel-1 SAR feature alignment and dynamic channel attention fusion.",
      "Extract multimodal water bodies using SAR radar backscatter.",
      "Analyze cross-modal feature alignment."
    ]
  };

  const currentPrompts = samplePrompts[mode] || samplePrompts.single;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim() || loading) return;
    onSendQuery(inputText.trim());
    setInputText('');
  };

  const handleDownload = async (format: 'pdf' | 'json') => {
    if (!result) return;
    try {
      setGeneratingReport(true);
      await generateReport(result.execution_id, format);
      const downloadUrl = getReportDownloadUrl(result.execution_id, format);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = `satquery_report_${result.execution_id}.${format}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (err: any) {
      alert(err.message || 'Failed to download report');
    } finally {
      setGeneratingReport(false);
    }
  };

  return (
    <div className="glass-panel rounded-2xl border border-slate-800 flex flex-col h-full min-h-[480px]">
      {/* Header */}
      <div className="p-4 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-cyan-950/80 border border-cyan-500/30 flex items-center justify-center">
            <Bot className="w-4 h-4 text-cyan-400" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-slate-200">SatQuery Assistant</h3>
            <p className="text-[10px] text-slate-400 font-mono">Agentic Multimodal VLM</p>
          </div>
        </div>

        {/* Download Report Buttons */}
        {result && (
          <div className="flex items-center space-x-2">
            <button
              onClick={() => handleDownload('pdf')}
              disabled={generatingReport}
              className="px-2.5 py-1 rounded-lg bg-cyan-950/80 hover:bg-cyan-900 border border-cyan-500/40 text-cyan-300 text-xs font-medium flex items-center space-x-1.5 transition-all shadow-md hover:shadow-cyan-500/20"
            >
              <FileText className="w-3.5 h-3.5" />
              <span>{generatingReport ? 'Generating...' : 'PDF Report'}</span>
            </button>
            <button
              onClick={() => handleDownload('json')}
              disabled={generatingReport}
              className="px-2 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 text-xs font-mono"
            >
              JSON
            </button>
          </div>
        )}
      </div>

      {/* Chat Messages Body */}
      <div className="flex-1 p-4 overflow-y-auto space-y-4 text-xs">
        {/* Welcome message */}
        <div className="flex items-start space-x-3">
          <div className="w-7 h-7 rounded-lg bg-cyan-950 border border-cyan-500/30 flex items-center justify-center flex-shrink-0 mt-0.5">
            <Bot className="w-3.5 h-3.5 text-cyan-400" />
          </div>
          <div className="p-3 rounded-2xl bg-space-950 border border-slate-800 text-slate-300 max-w-[85%] space-y-2">
            <p className="font-medium text-slate-200">
              Welcome to SATQUERY AI. Upload satellite images and ask natural language queries.
            </p>
            <p className="text-slate-400 text-[11px]">
              The agentic controller will parse your query intent, route to specialist models, generate visual evidence, and produce confidence metrics.
            </p>
          </div>
        </div>

        {/* Latest Result Display */}
        {result && (
          <div className="space-y-3">
            {/* User Query Bubble */}
            <div className="flex items-start justify-end space-x-2">
              <div className="p-3 rounded-2xl bg-cyan-950/60 border border-cyan-500/30 text-cyan-100 max-w-[85%]">
                {result.query}
              </div>
              <div className="w-7 h-7 rounded-lg bg-slate-800 flex items-center justify-center flex-shrink-0 mt-0.5">
                <User className="w-3.5 h-3.5 text-slate-300" />
              </div>
            </div>

            {/* AI Answer Bubble */}
            <div className="flex items-start space-x-3">
              <div className="w-7 h-7 rounded-lg bg-cyan-950 border border-cyan-500/30 flex items-center justify-center flex-shrink-0 mt-0.5">
                <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
              </div>
              <div className="p-4 rounded-2xl bg-space-950 border border-slate-800 text-slate-200 max-w-[90%] space-y-3 shadow-xl">
                {/* Identified Task & Models Banner */}
                <div className="flex items-center justify-between text-[10px] font-mono pb-2 border-b border-slate-800">
                  <span className="text-cyan-400 uppercase font-semibold">TASK: {result.task}</span>
                  <span className="text-slate-400">{result.models_used[0]}</span>
                </div>

                {/* Answer text */}
                <p className="leading-relaxed font-sans text-slate-100 whitespace-pre-wrap">
                  {result.answer}
                </p>

                {/* Confidence Bar */}
                <div className="pt-2 border-t border-slate-800 flex items-center justify-between text-[11px]">
                  <span className="text-slate-400 font-mono">Confidence Level:</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-24 h-2 bg-slate-800 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-cyan-500 to-emerald-400 rounded-full"
                        style={{ width: `${result.confidence.value * 100}%` }}
                      ></div>
                    </div>
                    <span className="font-mono font-bold text-cyan-400">
                      {(result.confidence.value * 100).toFixed(0)}%
                    </span>
                    <span className="text-[10px] text-slate-500 font-mono">({result.confidence.type})</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Loading Indicator */}
        {loading && (
          <div className="flex items-center space-x-3 text-cyan-400 py-3">
            <div className="w-4 h-4 rounded-full border-2 border-cyan-400 border-t-transparent animate-spin"></div>
            <span className="font-mono text-xs animate-pulse">Agent routing and executing specialist workflow...</span>
          </div>
        )}
      </div>

      {/* Pre-populated Sample Prompt Chips */}
      <div className="px-4 py-2.5 border-t border-slate-800/80 bg-space-950/60 overflow-x-auto flex items-center space-x-2">
        <span className="text-[10px] uppercase font-mono text-slate-500 flex-shrink-0">Try:</span>
        {currentPrompts.map((prompt, idx) => (
          <button
            key={idx}
            onClick={() => onSendQuery(prompt)}
            disabled={loading}
            className="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-slate-850 border border-slate-800 hover:border-cyan-500/40 text-slate-300 hover:text-cyan-300 text-[11px] font-medium whitespace-nowrap transition-all flex-shrink-0"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Chat Input Bar */}
      <form onSubmit={handleSubmit} className="p-3 border-t border-slate-800 flex items-center space-x-2">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Ask anything about your satellite imagery..."
          disabled={loading}
          className="flex-1 bg-space-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500/60 placeholder-slate-500"
        />
        <button
          type="submit"
          disabled={loading || !inputText.trim()}
          className="p-2.5 rounded-xl bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 disabled:opacity-50 text-white shadow-lg shadow-cyan-500/20 transition-all"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
};
