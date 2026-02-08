
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Download, RefreshCw, CheckCircle2, ChevronLeft, ChevronRight } from 'lucide-react';

interface ResultStateProps {
  onReset: () => void;
  theme: 'dark' | 'light';
  pdfUrl?: string; // Changed from latex
}

export const ResultState: React.FC<ResultStateProps> = ({ onReset, theme, pdfUrl }) => {
  const handleDownload = () => {
    if (!pdfUrl) return;
    const a = document.createElement('a');
    a.href = pdfUrl;
    a.download = 'resume.pdf';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
    <div className="flex flex-col items-center w-full">
      <motion.div
        initial={{ scale: 0, rotate: -45 }}
        animate={{ scale: 1, rotate: 0 }}
        transition={{ type: "spring", stiffness: 300, damping: 20, delay: 0.2 }}
        className={`w-20 h-20 rounded-full flex items-center justify-center mb-8 transition-all duration-1000 ${theme === 'dark' ? 'bg-green-500/20 text-green-400 shadow-[0_0_40px_rgba(34,197,94,0.3)]' : 'bg-green-100 text-green-600 shadow-lg shadow-green-200'}`}
      >
        <CheckCircle2 size={40} strokeWidth={2.5} />
      </motion.div>

      <div className="text-center mb-12">
        <h1 className={`text-5xl md:text-6xl font-black tracking-tight mb-4 transition-colors duration-1000 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>Resume Optimized.</h1>
        <p className={`text-base font-medium transition-colors duration-1000 ${theme === 'dark' ? 'text-white/40' : 'text-slate-500'}`}>Reformatted for absolute clarity and maximum impact.</p>
      </div>

      <div className="flex flex-col sm:flex-row gap-6 w-full justify-center mb-16 px-4">
        <button
          onClick={handleDownload}
          disabled={!pdfUrl}
          className="relative group flex-1 max-w-[280px] h-16 rounded-2xl font-black text-lg overflow-hidden transition-all duration-300 hover:scale-[1.03] active:scale-[0.97] shadow-xl shadow-indigo-500/20 disabled:opacity-50 disabled:cursor-not-allowed">
          <div className="absolute inset-0 iridescent-gradient opacity-100" />
          <div className="absolute inset-0 shadow-[inset_0_1px_1px_rgba(255,255,255,0.4)]" />
          <div className="relative flex items-center justify-center gap-3 text-white">
            <Download size={22} />
            Download PDF
          </div>
        </button>

        <button
          onClick={onReset}
          className={`flex-1 max-w-[280px] h-16 rounded-2xl font-bold text-lg border transition-all duration-1000 flex items-center justify-center gap-3 ${theme === 'dark' ? 'bg-white/5 border-white/10 hover:bg-white/10 text-white/80 hover:text-white' : 'bg-white border-slate-200 hover:bg-slate-50 text-slate-600 hover:text-slate-900 shadow-sm'}`}
        >
          <RefreshCw size={20} />
          Upload another
        </button>
      </div>

      {pdfUrl && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="w-full h-[800px] max-w-4xl rounded-2xl overflow-hidden border border-white/10 shadow-2xl bg-white"
        >
          <iframe src={pdfUrl} className="w-full h-full" title="Resume Preview" />
        </motion.div>
      )}
    </div>
  );
};
