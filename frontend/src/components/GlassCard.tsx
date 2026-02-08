
import React, { useRef } from 'react';
import { motion, useMotionValue, useSpring, useTransform } from 'framer-motion';

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  isProcessing?: boolean;
  theme?: 'dark' | 'light';
}

export const GlassCard: React.FC<GlassCardProps> = ({ children, className = "", isProcessing = false, theme = 'dark' }) => {
  const cardRef = useRef<HTMLDivElement>(null);
  
  const x = useMotionValue(0);
  const y = useMotionValue(0);

  const mouseXSpring = useSpring(x, { stiffness: 100, damping: 20 });
  const mouseYSpring = useSpring(y, { stiffness: 100, damping: 20 });

  const rotateX = useTransform(mouseYSpring, [-0.5, 0.5], ["3deg", "-3deg"]);
  const rotateY = useTransform(mouseXSpring, [-0.5, 0.5], ["-3deg", "3deg"]);

  const handleMouseMove = (e: React.MouseEvent) => {
    if (isProcessing || !cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    const width = rect.width;
    const height = rect.height;
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;
    const xPct = mouseX / width - 0.5;
    const yPct = mouseY / height - 0.5;
    x.set(xPct);
    y.set(yPct);
  };

  const handleMouseLeave = () => {
    x.set(0);
    y.set(0);
  };

  return (
    <motion.div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{
        rotateX: isProcessing ? 0 : rotateX,
        rotateY: isProcessing ? 0 : rotateY,
        transformStyle: "preserve-3d",
      }}
      className={`
        relative overflow-hidden glass-card-inner
        transition-all duration-1000 ease-[cubic-bezier(0.65,0,0.35,1)]
        ${theme === 'dark' 
          ? 'bg-white/[0.03] backdrop-blur-3xl border-white/[0.08] shadow-[0_40px_80px_-15px_rgba(0,0,0,0.8)]' 
          : 'bg-white/70 backdrop-blur-3xl border-slate-200/50 shadow-[0_40px_80px_-20px_rgba(0,0,0,0.06)]'}
        rounded-[40px] ${className}
      `}
    >
      <div className={`absolute inset-0 pointer-events-none transition-opacity duration-1000 ${theme === 'dark' ? 'bg-gradient-to-br from-white/[0.05] to-transparent opacity-50' : 'bg-gradient-to-br from-indigo-50/30 to-white/10 opacity-100'}`} />
      
      <div className="relative z-10 p-12" style={{ transform: "translateZ(30px)" }}>
        {children}
      </div>
    </motion.div>
  );
};
