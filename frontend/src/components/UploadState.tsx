
import React, { useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, Sparkles, Link as LinkIcon } from 'lucide-react';
import { GlassCard } from './GlassCard';

interface UploadStateProps {
  onUpload: (file: File | null) => void;
  theme: 'dark' | 'light';
}

export const UploadState: React.FC<UploadStateProps> = ({ onUpload, theme }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const [isFocused, setIsFocused] = useState(false);
  const [jobText, setJobText] = useState('');

  // The input is visible if hovered, focused, or contains text
  const isVisible = isHovered || isFocused || jobText.trim().length > 0;

  return (
    <div className="text-center">
      <motion.div>
        <motion.h1 
          initial={{ opacity: 0, y: 20, filter: 'blur(10px)' }}
          animate={{ opacity: 1, y: 0, filter: 'blur(0px)' }}
          transition={{ duration: 1.2, delay: 0.6, ease: [0.22, 1, 0.36, 1] }}
          className={`text-5xl md:text-6xl font-black tracking-tight mb-4 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}
        >
          Upload your resume
        </motion.h1>
        <motion.p 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 1.2 }}
          className={`text-sm md:text-base font-medium mb-12 ${theme === 'dark' ? 'text-white/40' : 'text-slate-500'}`}
        >
          We’ll reformat it into a cleaner, ATS-friendly layout.
        </motion.p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 40, scale: 0.98 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 1.5, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
      >
        <GlassCard theme={theme} className="group">
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.8, duration: 1 }}
            onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
            onDragLeave={() => setIsDragging(false)}
            onDrop={(e) => {
              e.preventDefault();
              setIsDragging(false);
              const file = e.dataTransfer.files?.[0];
              if (file?.type === 'application/pdf') onUpload(file);
            }}
            onClick={() => fileInputRef.current?.click()}
            className={`
              relative cursor-pointer border-2 border-dashed rounded-[24px] p-16 transition-all duration-700 overflow-hidden
              ${isDragging 
                ? 'border-indigo-500 bg-indigo-500/5 scale-[0.98]' 
                : theme === 'dark' ? 'border-white/10 hover:border-white/20' : 'border-slate-200 hover:border-indigo-200'}
            `}
          >
            {/* Shimmer effect inside zone */}
            <div className="absolute inset-0 shimmer pointer-events-none opacity-30" />
            
            <input type="file" ref={fileInputRef} onChange={(e) => {
              const file = e.target.files?.[0];
              if (file?.type === 'application/pdf') onUpload(file);
            }} accept=".pdf" className="hidden" />
            
            <div className="flex flex-col items-center">
              <motion.div 
                animate={isDragging ? { y: -8, scale: 1.1 } : { y: 0, scale: 1 }}
                className={`w-20 h-20 rounded-full flex items-center justify-center mb-6 transition-colors duration-700 ${isDragging ? 'bg-indigo-600 text-white shadow-xl shadow-indigo-500/20' : theme === 'dark' ? 'bg-white/5 text-white/40' : 'bg-slate-100 text-slate-400'}`}
              >
                <Upload size={36} />
              </motion.div>
              <p className={`text-xl font-bold mb-1 ${theme === 'dark' ? 'text-white' : 'text-slate-800'}`}>Click or drag PDF here</p>
              <p className={`text-[10px] font-bold tracking-[0.2em] uppercase ${theme === 'dark' ? 'text-white/20' : 'text-slate-400'}`}>PDF only • Max 10MB</p>
            </div>
          </motion.div>

          <div className="mt-8 flex flex-col items-center">
            {/* Hover Interaction Zone */}
            <div 
              onMouseEnter={() => setIsHovered(true)}
              onMouseLeave={() => setIsHovered(false)}
              className="w-full flex flex-col items-center group/jobzone"
            >
              <button
                type="button"
                className={`text-[11px] uppercase tracking-[0.2em] font-bold transition-all flex items-center gap-2 mb-2 outline-none ${isVisible || isHovered ? (theme === 'dark' ? 'text-indigo-400' : 'text-indigo-600') : (theme === 'dark' ? 'text-white/20 hover:text-indigo-400' : 'text-slate-300 hover:text-indigo-600')}`}
              >
                <LinkIcon size={12} />
                Submit job listing (optional)
              </button>

              <AnimatePresence>
                {isVisible && (
                  <motion.div
                    initial={{ opacity: 0, height: 0, marginTop: 0 }}
                    animate={{ opacity: 1, height: 'auto', marginTop: 8 }}
                    exit={{ opacity: 0, height: 0, marginTop: 0 }}
                    transition={{ duration: 0.45, ease: [0.65, 0, 0.35, 1] }}
                    className="w-full overflow-hidden"
                  >
                    <textarea
                      placeholder="Paste job description or link (optional)"
                      value={jobText}
                      onFocus={() => setIsFocused(true)}
                      onBlur={() => setIsFocused(false)}
                      onChange={(e) => setJobText(e.target.value)}
                      className={`
                        w-full p-4 rounded-xl text-sm font-medium transition-all outline-none resize-none h-24 mb-6
                        ${theme === 'dark' 
                          ? 'bg-white/5 border border-white/10 text-white placeholder:text-white/20 focus:border-white/20 shadow-inner' 
                          : 'bg-slate-50 border border-slate-200 text-slate-800 placeholder:text-slate-400 focus:border-indigo-300 shadow-inner'}
                      `}
                    />
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 2.2 }}
              className="flex items-center justify-center mt-2"
            >
              <button 
                onClick={(e) => { e.stopPropagation(); onUpload(null); }}
                className={`text-[11px] uppercase tracking-[0.2em] font-bold transition-all flex items-center gap-2 group/btn ${theme === 'dark' ? 'text-white/30 hover:text-indigo-400' : 'text-slate-400 hover:text-indigo-600'}`}
              >
                <Sparkles size={14} />
                Use sample resume
              </button>
            </motion.div>
          </div>
        </GlassCard>
      </motion.div>
    </div>
  );
};
