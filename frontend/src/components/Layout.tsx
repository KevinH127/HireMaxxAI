
import React from 'react';
import { motion } from 'framer-motion';
import { Sun, Moon } from 'lucide-react';

interface LayoutProps {
  children: React.ReactNode;
  theme: 'dark' | 'light';
  onToggleTheme: () => void;
  isTransitioning: boolean;
  isSettling: boolean;
}

export const Layout: React.FC<LayoutProps> = ({ children, theme, onToggleTheme, isTransitioning, isSettling }) => {
  return (
    <div className={`relative min-h-screen w-full flex flex-col items-center justify-center overflow-hidden ${isSettling ? 'is-settling' : ''}`}>
      <div className="absolute inset-0 bg-noise pointer-events-none" />
      
      {/* Liquid Sweep Overlay - Now a localized ring blur */}
      <div className={`theme-sweep-bloom ${isTransitioning ? 'active' : ''}`} />
      
      {/* Background Blurs */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div 
          animate={{ 
            opacity: theme === 'dark' ? 0.15 : 0.05,
            scale: theme === 'dark' ? 1 : 0.85,
          }}
          transition={{ duration: 1.2, ease: [0.65, 0, 0.35, 1] }}
          className="absolute top-[-15%] right-[-10%] w-[70%] h-[70%] bg-blue-600 blur-[180px] rounded-full" 
        />
        <motion.div 
          animate={{ 
            opacity: theme === 'dark' ? 0.15 : 0.05,
            scale: theme === 'dark' ? 1 : 0.85,
          }}
          transition={{ duration: 1.2, ease: [0.65, 0, 0.35, 1] }}
          className="absolute bottom-[-15%] left-[-10%] w-[70%] h-[70%] bg-purple-600 blur-[180px] rounded-full" 
        />
      </div>
      
      <header className="absolute top-0 left-0 w-full p-8 flex justify-between items-center z-50">
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="text-xl font-bold tracking-tighter flex items-center gap-2"
        >
          <div className="w-6 h-6 iridescent-gradient rounded-full shadow-lg" />
          <span className={`transition-colors duration-1000 ${theme === 'dark' ? 'text-white' : 'text-slate-900'}`}>
            HireMaxx<span className="opacity-40">AI</span>
          </span>
        </motion.div>
        
        <div className="flex items-center gap-8">
          <motion.button
            onClick={onToggleTheme}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className={`p-2.5 rounded-full border transition-all duration-1000 ${theme === 'dark' ? 'border-white/10 text-white hover:bg-white/5' : 'border-slate-200 text-slate-800 hover:bg-slate-50 shadow-sm'}`}
          >
            {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
          </motion.button>
          
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className={`text-xs uppercase tracking-[0.2em] font-medium transition-colors duration-1000 ${theme === 'dark' ? 'text-white/30' : 'text-slate-400'}`}
          >
            <a href="#" className="hover:text-indigo-500 transition-colors">Demo</a>
          </motion.div>
        </div>
      </header>

      <main className="relative z-10 w-full flex items-center justify-center clarity-settle">
        {children}
      </main>

      <footer className={`absolute bottom-8 text-[10px] tracking-widest uppercase pointer-events-none transition-colors duration-1000 font-medium ${theme === 'dark' ? 'text-white/10' : 'text-slate-300'}`}>
        made with python
      </footer>
    </div>
  );
};
