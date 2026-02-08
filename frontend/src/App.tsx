
import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Layout } from './components/Layout';
import { UploadState } from './components/UploadState';
import { ProcessingState } from './components/ProcessingState';
import { ResultState } from './components/ResultState';

export enum AppState {
  IDLE = 'idle',
  PROCESSING = 'processing',
  READY = 'ready'
}

const App: React.FC = () => {
  const [appState, setAppState] = useState<AppState>(AppState.IDLE);
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [isSettling, setIsSettling] = useState(false);

  const [pdfUrl, setPdfUrl] = useState<string>('');

  useEffect(() => {
    document.documentElement.classList.toggle('light', theme === 'light');
  }, [theme]);

  const toggleTheme = () => {
    setIsTransitioning(true);
    setIsSettling(true);

    // Theme swap happens during the sweep
    setTimeout(() => {
      setTheme(prev => prev === 'dark' ? 'light' : 'dark');
    }, 350);

    // End transition wave
    setTimeout(() => {
      setIsTransitioning(false);
      // Brief settle window before final crisp lock
      setTimeout(() => {
        setIsSettling(false);
      }, 150);
    }, 850);
  };

  const handleUpload = async (file: File | null) => {
    if (!file) return;
    setAppState(AppState.PROCESSING);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/upload-resume', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Upload failed: ${errorText}`);
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setPdfUrl(url);
      setAppState(AppState.READY);
    } catch (error) {
      console.error("Upload error:", error);
      alert("Failed to process resume. Please try again.");
      setAppState(AppState.IDLE);
    }
  };

  const reset = () => {
    if (pdfUrl) URL.revokeObjectURL(pdfUrl);
    setAppState(AppState.IDLE);
    setPdfUrl('');
  };

  return (
    <Layout
      theme={theme}
      onToggleTheme={toggleTheme}
      isTransitioning={isTransitioning}
      isSettling={isSettling}
    >
      <AnimatePresence mode="wait">
        {appState === AppState.IDLE && (
          <motion.div
            key="idle"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0, scale: 1.05, filter: 'blur(20px)', transition: { duration: 0.8 } }}
            className="w-full max-w-xl"
          >
            <UploadState onUpload={handleUpload} theme={theme} />
          </motion.div>
        )}

        {appState === AppState.PROCESSING && (
          <motion.div
            key="processing"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, filter: 'blur(10px)', transition: { duration: 0.5 } }}
            className="w-full max-w-2xl px-6"
          >
            <ProcessingState theme={theme} />
          </motion.div>
        )}

        {appState === AppState.READY && (
          <motion.div
            key="ready"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ type: 'spring', damping: 25, stiffness: 120 }}
            className="w-full max-w-2xl px-6"
          >
            <ResultState onReset={reset} theme={theme} pdfUrl={pdfUrl} />
          </motion.div>
        )}
      </AnimatePresence>
    </Layout>
  );
};

export default App;
