
import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const statuses = [
  "Extracting data...",
  "Analyzing structure...",
  "Rewriting content...",
  "Optimizing for ATS...",
  "Applying layout...",
  "Generating PDF..."
];

interface ProcessingStateProps {
  theme: 'dark' | 'light';
}

export const ProcessingState: React.FC<ProcessingStateProps> = ({ theme }) => {
  const [statusIndex, setStatusIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setStatusIndex((prev) => (prev + 1) % statuses.length);
    }, 1200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center w-full relative">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className={`text-4xl font-black tracking-tighter mb-16 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}
      >
        Perfecting<span className="animate-pulse">...</span>
      </motion.div>

      {/* Liquid Light Progress Bar */}
      {/* Liquid Light Progress Bar */}
      <div className={`relative w-full h-2 rounded-full overflow-hidden mb-10 max-w-lg ${theme === 'dark' ? 'bg-white/5' : 'bg-slate-200'}`}>
        <div className="absolute inset-0 blur-md opacity-30 iridescent-gradient" />
        <motion.div
          className="absolute left-0 top-0 h-full iridescent-gradient"
          initial={{ width: "0%" }}
          animate={{ width: "100%" }}
          transition={{ duration: 120, ease: "linear" }}
        />
        <motion.div
          className="absolute inset-0 bg-gradient-to-r from-transparent via-white/50 to-transparent w-[50%]"
          animate={{ left: ["-50%", "150%"] }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
        />
      </div>

      <div className="h-6 relative w-full flex justify-center overflow-hidden">
        <AnimatePresence mode="wait">
          <motion.p
            key={statusIndex}
            initial={{ y: 24, opacity: 0, filter: 'blur(4px)' }}
            animate={{ y: 0, opacity: 1, filter: 'blur(0px)' }}
            exit={{ y: -24, opacity: 0, filter: 'blur(4px)' }}
            transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
            className={`text-xs uppercase tracking-[0.4em] font-black ${theme === 'dark' ? 'text-white/30' : 'text-slate-400'}`}
          >
            {statuses[statusIndex]}
          </motion.p>
        </AnimatePresence>
      </div>

      <motion.div
        animate={{ scale: [1, 1.2, 1], opacity: [0.3, 0.6, 0.3] }}
        transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
        className={`absolute w-[500px] h-[500px] blur-[120px] rounded-full pointer-events-none -z-10 ${theme === 'dark' ? 'bg-indigo-500/10' : 'bg-indigo-500/5'}`}
      />
    </div>
  );
};
