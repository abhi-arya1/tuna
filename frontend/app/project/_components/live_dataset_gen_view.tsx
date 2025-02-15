"use client";

import React, { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';

const DatasetGeneration = ({
  statusText,
  logContent
}: {
  statusText: string;
  logContent: string;
}) => {
  const logBoxRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (logBoxRef.current) {
      logBoxRef.current.scrollTop = logBoxRef.current.scrollHeight;
    }
  }, [logContent]);

  const mockStatusText = "Generating a synthetic dataset based on your model requirements. This process will take a few minutes.";
  const mockLogContent = `Initializing dataset generator...
[TUNA] Setting up environment variables
Loading base templates...
[TUNA] Configuring data pipelines
Generating sample data structures...
Validating data format...
[TUNA] Optimizing memory allocation
Applying transformations...
Creating training splits...
[TUNA] Validating data integrity
Optimizing data distribution...
[TUNA] Finalizing system checks
Completing dataset generation...`;

  const logLines = (logContent || mockLogContent).split('\n');

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
        {statusText || mockStatusText}
      </motion.p>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="border border-gray-700 h-[400px] rounded-none bg-background"
      >
        <div
          ref={logBoxRef}
          className="h-full overflow-y-auto font-mono text-sm whitespace-pre-wrap"
        >
          {logLines.map((line, index) => {
            const isTunaLog = line.startsWith('[TUNA]');
            return (
              <div
                key={index}
                className={`
                  text-gray-300 relative h-8 flex items-center
                  ${isTunaLog ? 'bg-[#1F808D]/10' : ''}
                `}
              >
                <div className="w-full px-4 flex items-center">
                  <span className="text-accent mr-2">→</span>
                  {line}
                </div>
                {isTunaLog && (
                  <div className="absolute inset-0 -left-4 bg-[#1F808D]/10 -z-10" />
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
