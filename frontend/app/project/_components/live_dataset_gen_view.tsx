"use client";

import React, { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';

const DatasetGeneration = ({
  statusText,
  logContent,
  dataset,
  sources,
  complete
}: {
  statusText: string;
  logContent: string;
  dataset: any[];
  sources: string[];
  complete: boolean;
}) => {
  const logBoxRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (logBoxRef.current) {
      logBoxRef.current.scrollTop = logBoxRef.current.scrollHeight;
    }
  }, [logContent]);

  const mockLogContent = `<<10:20:39>> Initializing dataset generator...
<<10:20:40>> [TUNA] Starting your environment`;

  const logLines = (logContent || mockLogContent).split('\n');

  const parseLogLine = (line: string) => {
    const timeMatch = line.match(/^<<(\d{2}:\d{2}:\d{2})>> (.+)$/);
    if (timeMatch) {
      return {
        timestamp: timeMatch[1],
        message: timeMatch[2]
      };
    }
    return {
      timestamp: "",
      message: line
    };
  };

  return (
    <div className="space-y-8">
      <div className="space-y-2">
        <motion.span
          className="text-gray-400 text-sm"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          Dataset
        </motion.span>
        <motion.h2
          className="text-3xl font-normal"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          Building your Dataset
        </motion.h2>
      </div>

      <motion.p
        className="text-gray-300 text-lg"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
        {statusText || "Generating a dataset..."}
      </motion.p>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="border border-gray-700 h-[400px] rounded-none bg-background"
      >
        <div
          ref={logBoxRef}
          className="h-full overflow-y-auto font-mono text-sm"
        >
          {logLines.map((line, index) => {
            const { timestamp, message } = parseLogLine(line);
            const isTunaLog = message.startsWith('[TUNA]');

            return (
              <div
                key={index}
                className={`
                  text-gray-300 relative min-h-[32px] py-1
                  ${isTunaLog ? 'bg-[#1F808D]/10' : ''}
                `}
              >
                <div className="w-full px-4 flex items-start">
                  <span className="text-gray-500 shrink-0 w-[85px]">{timestamp}</span>
                  <span className="text-accent mr-2 shrink-0">→</span>
                  <span className="break-words whitespace-pre-wrap">{message}</span>
                </div>
                {isTunaLog && (
                  <div className="absolute inset-0 -left-2 bg-[#1F808D]/10 -z-10" />
                )}
              </div>
            );
          })}
        </div>
      </motion.div>

      <motion.div
        className="flex justify-end"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
      >
        <button className="h-12 px-6 bg-accent hover:bg-accent-hover text-white
                          flex items-center gap-2 transition-colors duration-200">
          Continue
          <span className="text-sm px-2 py-0.5 bg-black/20">⏎</span>
        </button>
      </motion.div>
    </div>
  );
};

export default DatasetGeneration;
