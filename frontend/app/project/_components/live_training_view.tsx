"use client";

import React, { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, ChevronUp } from 'lucide-react';

const LogSection = ({
  title,
  onToggle,
  children
}: {
  title: string;
  onToggle: () => void;
  children: React.ReactNode;
}) => (
  <div className="border border-gray-700 bg-background">
    <button
      onClick={onToggle}
      className="w-full px-4 py-2 flex items-center justify-between text-gray-300 hover:text-white border-b border-gray-700"
    >
      <span className="text-sm font-medium">{title}</span>
    </button>
    <AnimatePresence>
        <motion.div
            initial={{ height: 0 }}
            animate={{ height: "400px" }}
            exit={{ height: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
        >
            {children}
        </motion.div>
    </AnimatePresence>
  </div>
);

const LogContent = ({ lines }: { lines: string[] }) => {
  const logBoxRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (logBoxRef.current) {
      logBoxRef.current.scrollTop = logBoxRef.current.scrollHeight;
    }
  }, [lines]);

  const parseLogLine = (line: string) => {
    const timeMatch = line.match(/^<<(\d{2}:\d{2}:\d{2})>> (.+)$/);
    if (timeMatch) {
      const timestamp = timeMatch[1];
      const rawMessage = timeMatch[2];
      const isTunaLog = rawMessage.startsWith('[TUNA]');
      const isErrorLog = rawMessage.startsWith('[ERROR]');
      let message = rawMessage;

      if (isTunaLog) {
        message = rawMessage.replace('[TUNA] ', '');
      } else if (isErrorLog) {
        message = rawMessage.replace('[ERROR] ', '');
      }

      return {
        timestamp,
        message,
        isTunaLog,
        isErrorLog
      };
    }
    return {
      timestamp: "",
      message: line,
      isTunaLog: line.startsWith('[TUNA]'),
      isErrorLog: line.startsWith('[ERROR]')
    };
  };

  const validLines = lines.filter(line => line && line.trim().length > 0);

  return (
    <div
      ref={logBoxRef}
      className="h-full overflow-y-auto font-mono text-sm"
    >
      {validLines.map((line, index) => {
        const { timestamp, message, isTunaLog, isErrorLog } = parseLogLine(line);

        return (
          <div
            key={index}
            className={`
              text-gray-300 relative min-h-[32px] py-1
              ${isTunaLog ? 'bg-[#1F808D]/10' : ''}
              ${isErrorLog ? 'bg-[#440C13]' : ''}
            `}
          >
            <div className="w-full px-4 flex items-start">
              <span className="text-gray-500 shrink-0 w-[85px]">{timestamp}</span>
              <span className={`mr-2 shrink-0 ${isErrorLog ? 'text-red-400' : 'text-accent'}`}>→</span>
              <span className="break-words whitespace-pre-wrap">{message}</span>
            </div>
            {isTunaLog && (
              <div className="absolute inset-0 -left-2 bg-[#1F808D]/10 -z-10" />
            )}
            {isErrorLog && (
              <div className="absolute inset-0 -left-2 bg-[#440C13] -z-10" />
            )}
          </div>
        );
      })}
    </div>
  );
};

const LiveTrainingView = ({
    onMove,
    logContent,
    complete
}: {
    onMove: () => void;
    logContent: string;
    complete: boolean;
}) => {
  const [logOpen, setLogOpen] = useState(true);
  const logLines = (logContent || "").split('\n');

  return (
    <div className="space-y-8">
      <div className="space-y-2">
        <motion.span
          className="text-gray-400 text-sm"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          Train
        </motion.span>
        <motion.h2
          className="text-3xl font-normal"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          Training your model
        </motion.h2>
      </div>

      <motion.p
        className="text-gray-300 text-lg"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
        Spinning up a training instance...
      </motion.p>

      <motion.div
        className="space-y-2"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <LogSection
          title="Training Log"
          onToggle={() => setLogOpen(!logOpen)}
        >
          <LogContent lines={logLines} />
        </LogSection>
      </motion.div>

      <motion.div
        className="flex justify-end"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
      >
        <button
          className="h-12 px-6 bg-accent hover:bg-accent-hover text-white
                     flex items-center gap-2 transition-colors duration-200"
          onClick={() => onMove()}
        >
          Continue
          <span className="text-sm px-2 py-0.5 bg-black/20">⏎</span>
        </button>
      </motion.div>
    </div>
  );
};

export default LiveTrainingView;
