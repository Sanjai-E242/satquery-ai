'use client';

import React, { useState, useEffect } from 'react';
import { Header } from '@/components/layout/Header';
import { AboutSection } from '@/components/layout/AboutSection';
import { TechnologySection } from '@/components/layout/TechnologySection';
import { TeamSection } from '@/components/layout/TeamSection';
import { ContactSection } from '@/components/layout/ContactSection';
import { Footer } from '@/components/layout/Footer';
import { InputPanel } from '@/components/image-upload/InputPanel';
import { SatelliteViewer } from '@/components/satellite-viewer/SatelliteViewer';
import { AIChat } from '@/components/chat/AIChat';
import { ExecutionTrace } from '@/components/execution-trace/ExecutionTrace';
import { StatusPanels } from '@/components/dashboard/StatusPanels';
import { ProcessingPipeline } from '@/components/dashboard/ProcessingPipeline';
import { SystemStatus, ImageMetadata, ImageValidation, AnalysisResult } from '@/types';
import { fetchSystemStatus, fetchSampleDataset, fetchSEN12MSDataset, submitQuery, validateImages } from '@/lib/api';
import { identityConfig } from '@/lib/identityConfig';
import { MessageSquare, Target, GitCompare, Layers, Sparkles, Compass } from 'lucide-react';

export default function Home() {
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [analysisMode, setAnalysisMode] = useState<'single' | 'bi_temporal' | 'optical_sar'>('single');
  const [primaryImage, setPrimaryImage] = useState<ImageMetadata | null>(null);
  const [secondaryImage, setSecondaryImage] = useState<ImageMetadata | null>(null);
  const [validation, setValidation] = useState<ImageValidation | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [statusMessage, setStatusMessage] = useState<string>('');

  useEffect(() => {
    fetchSystemStatus()
      .then(setSystemStatus)
      .catch((err) => console.error('Error fetching system status:', err));
  }, []);

  // Load real verified Sentinel-2 optical & Sentinel-1 SAR dataset patches from backend
  const handleLoadDemoDataset = async () => {
    try {
      setLoading(true);
      setStatusMessage('Loading verified BigEarthNet Sentinel-2 optical & Sentinel-1 SAR satellite patches...');
      
      const data = await fetchSampleDataset();
      setPrimaryImage(data.primary_image);
      setSecondaryImage(data.secondary_image);

      const val = await validateImages(data.primary_image.id, data.secondary_image.id);
      setValidation(val);
    } catch (err: any) {
      alert('Failed to load real sample satellite dataset: ' + (err.message || err));
    } finally {
      setLoading(false);
      setStatusMessage('');
    }
  };

  // Load paired SEN12MS-CR dataset sample
  const handleLoadSEN12MSDataset = async (sampleId: string) => {
    try {
      setLoading(true);
      setStatusMessage(`Loading SEN12MS-CR paired optical & SAR sample '${sampleId}'...`);

      const data = await fetchSEN12MSDataset(sampleId);
      setPrimaryImage(data.primary_image);
      setSecondaryImage(data.secondary_image);

      const val = await validateImages(data.primary_image.id, data.secondary_image.id);
      setValidation(val);
    } catch (err: any) {
      alert(`Failed to load SEN12MS-CR sample '${sampleId}': ` + (err.message || err));
    } finally {
      setLoading(false);
      setStatusMessage('');
    }
  };

  // Submit natural language query to agentic controller
  const handleSendQuery = async (queryText: string) => {
    if (!primaryImage) {
      alert('Please upload or select a primary satellite image first.');
      return;
    }

    if ((analysisMode === 'bi_temporal' || analysisMode === 'optical_sar') && !secondaryImage) {
      alert(`Please select or upload a secondary image for ${analysisMode === 'bi_temporal' ? 'Bi-Temporal Change Detection' : 'Optical+SAR Multimodal Fusion'}.`);
      return;
    }

    try {
      setLoading(true);
      setStatusMessage('Executing PyTorch AI inference pipeline...');
      const res = await submitQuery(
        queryText,
        analysisMode,
        primaryImage.id,
        secondaryImage ? secondaryImage.id : undefined
      );
      setResult(res);
    } catch (err: any) {
      console.error('Query execution error:', err);
      alert('Query Execution Error: ' + (err.message || err));
    } finally {
      setLoading(false);
      setStatusMessage('');
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-space-950 bg-grid-pattern bg-spatial-glow">
      <Header systemStatus={systemStatus} />

      <main className="flex-1 max-w-[1600px] w-full mx-auto p-4 sm:p-6 space-y-6">
        {/* SIH Landing Banner & Capability Feature Selector */}
        {!primaryImage && (
          <div className="glass-panel rounded-2xl p-6 border border-cyan-500/20 space-y-4 text-center radar-sweep shadow-2xl">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-cyan-950/80 border border-cyan-500/30 text-cyan-400 text-xs font-mono font-bold tracking-wider uppercase">
              <Sparkles className="w-3.5 h-3.5" />
              <span>{identityConfig.COLLEGE_NAME} — {identityConfig.TEAM_NAME}</span>
            </div>

            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-100 tracking-tight">
              Agentic Multimodal Satellite Intelligence Workstation
            </h2>

            <p className="text-xs sm:text-sm text-slate-400 max-w-2xl mx-auto leading-relaxed">
              Analyze satellite imagery using genuine PyTorch AI models: Florence-2 VQA, sequence-to-sequence phrase grounding, ResNet-18 Siamese bi-temporal change detection, and Sentinel-1 SAR cross-modal channel attention fusion.
            </p>

            {/* AI Capabilities Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5 pt-2 max-w-4xl mx-auto text-left">
              <div className="p-3.5 rounded-xl bg-space-950/80 border border-slate-800 glass-panel-hover">
                <div className="w-8 h-8 rounded-lg bg-cyan-950 border border-cyan-500/30 flex items-center justify-center mb-2">
                  <MessageSquare className="w-4 h-4 text-cyan-400" />
                </div>
                <h4 className="text-xs font-bold text-slate-200">1. Satellite VQA</h4>
                <p className="text-[11px] text-slate-400 mt-1">Natural-language visual question answering via fine-tuned Florence-2 LoRA model.</p>
              </div>

              <div className="p-3.5 rounded-xl bg-space-950/80 border border-slate-800 glass-panel-hover">
                <div className="w-8 h-8 rounded-lg bg-indigo-950 border border-indigo-500/30 flex items-center justify-center mb-2">
                  <Target className="w-4 h-4 text-indigo-400" />
                </div>
                <h4 className="text-xs font-bold text-slate-200">2. Phrase Grounding</h4>
                <p className="text-[11px] text-slate-400 mt-1">Text-guided phrase localization, dynamic bounding boxes, and segmentation masks.</p>
              </div>

              <div className="p-3.5 rounded-xl bg-space-950/80 border border-emerald-500/30 flex items-center justify-center mb-2">
                <div className="w-8 h-8 rounded-lg bg-emerald-950 border border-emerald-500/30 flex items-center justify-center mb-2">
                  <GitCompare className="w-4 h-4 text-emerald-400" />
                </div>
                <h4 className="text-xs font-bold text-slate-200">3. Change Detection</h4>
                <p className="text-[11px] text-slate-400 mt-1">Siamese ResNet-18 feature cosine distance change map and changed percentage.</p>
              </div>

              <div className="p-3.5 rounded-xl bg-space-950/80 border border-slate-800 glass-panel-hover">
                <div className="w-8 h-8 rounded-lg bg-amber-950 border border-amber-500/30 flex items-center justify-center mb-2">
                  <Layers className="w-4 h-4 text-amber-400" />
                </div>
                <h4 className="text-xs font-bold text-slate-200">4. Optical + SAR Fusion</h4>
                <p className="text-[11px] text-slate-400 mt-1">Sentinel-1 SAR radar backscatter + Sentinel-2 optical dynamic channel attention fusion.</p>
              </div>
            </div>
          </div>
        )}

        {/* Processing Stage Indicator */}
        <ProcessingPipeline loading={loading} mode={analysisMode} />

        {/* Main Grid Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Column: Input Control Panel */}
          <div className="lg:col-span-3 space-y-5">
            <InputPanel
              analysisMode={analysisMode}
              setAnalysisMode={setAnalysisMode}
              primaryImage={primaryImage}
              setPrimaryImage={setPrimaryImage}
              secondaryImage={secondaryImage}
              setSecondaryImage={setSecondaryImage}
              validation={validation}
              setValidation={setValidation}
              onLoadDemoDataset={handleLoadDemoDataset}
              onLoadSEN12MSDataset={handleLoadSEN12MSDataset}
            />
          </div>

          {/* Center Column: Satellite Imagery Viewer */}
          <div className="lg:col-span-5 flex flex-col">
            <SatelliteViewer
              primaryImage={primaryImage}
              secondaryImage={secondaryImage}
              evidence={result?.evidence || []}
              mode={analysisMode}
            />
          </div>

          {/* Right Column: AI Assistant Chat */}
          <div className="lg:col-span-4 flex flex-col">
            <AIChat
              onSendQuery={handleSendQuery}
              loading={loading}
              result={result}
              mode={analysisMode}
            />
          </div>
        </div>

        {/* Observable Agent Execution Trace */}
        {result && (
          <ExecutionTrace
            steps={result.execution_steps}
            modelsUsed={result.models_used}
            toolsUsed={result.tools_used}
            totalDurationMs={result.duration_ms}
            executionId={result.execution_id}
          />
        )}

        {/* System & BigEarthNet Dataset Status Footer Panels */}
        <StatusPanels systemStatus={systemStatus} />

        {/* Permanent Informational Sections */}
        <AboutSection />
        <TechnologySection />
        <TeamSection />
        <ContactSection />
      </main>

      {/* Professional Footer with Prominent Developer Credit */}
      <Footer />
    </div>
  );
}
