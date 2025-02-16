"use client";

import React, { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, ChevronUp, Globe } from 'lucide-react';

interface SourceInfo {
  name: string;
  favicon: string;
}

const LogSection = ({
  title,
  isOpen,
  onToggle,
  otherSectionOpen,
  children
}: {
  title: string;
  isOpen: boolean;
  onToggle: () => void;
  otherSectionOpen: boolean;
  children: React.ReactNode;
}) => (
  <div className="border border-gray-700 bg-background">
    <button
      onClick={onToggle}
      className="w-full px-4 py-2 flex items-center justify-between text-gray-300 hover:text-white border-b border-gray-700"
    >
      <span className="text-sm font-medium">{title}</span>
      {isOpen ?
        <ChevronUp className="h-4 w-4" /> :
        <ChevronDown className="h-4 w-4" />
      }
    </button>
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ height: 0 }}
          animate={{ height: otherSectionOpen ? "200px" : "400px" }}
          exit={{ height: 0 }}
          transition={{ duration: 0.2 }}
          className="overflow-hidden"
        >
          {children}
        </motion.div>
      )}
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
      const message = isTunaLog ? rawMessage.replace('[TUNA] ', '') : rawMessage;

      return {
        timestamp,
        message,
        isTunaLog
      };
    }
    return {
      timestamp: "",
      message: line,
      isTunaLog: line.startsWith('[TUNA]')
    };
  };

  const validLines = lines.filter(line => line && line.trim().length > 0);

  return (
    <div
      ref={logBoxRef}
      className="h-full overflow-y-auto font-mono text-sm"
    >
      {validLines.map((line, index) => {
        const { timestamp, message, isTunaLog } = parseLogLine(line);

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
  );
};

const getSourceInfo = async (url: string): Promise<SourceInfo> => {
  try {
    const response = await fetch(url, { method: 'HEAD' });
    const title = response.headers.get('title') || new URL(url).hostname.split('.')[0];
    return {
      name: title.charAt(0).toUpperCase() + title.slice(1),
      favicon: `https://${new URL(url).hostname}/favicon.ico`
    };
  } catch (error) {
    return {
      name: new URL(url).hostname.split('.')[0],
      favicon: ''
    };
  }
}

const SourceButton = ({ source }: { source: string }) => {
  const [sourceInfo, setSourceInfo] = useState<SourceInfo>({
    name: new URL(source).hostname.split('.')[0],
    favicon: ''
  });
  const [imageError, setImageError] = useState(false);

  useEffect(() => {
    getSourceInfo(source).then(setSourceInfo);
  }, [source]);

  return (
    <a
      href={source}
      target="_blank"
      rel="noopener noreferrer"
      className="group flex items-center gap-3 p-3 border border-gray-700
                 hover:bg-gray-800/50 transition-all duration-200"
    >
      <div className="w-8 h-8 shrink-0 rounded-full overflow-hidden border border-gray-700
                    group-hover:border-accent transition-colors duration-200 bg-gray-800
                    flex items-center justify-center">
        {(!sourceInfo.favicon || imageError) ? (
          <Globe className="w-4 h-4 text-gray-400 group-hover:text-accent transition-colors duration-200" />
        ) : (
          <img
            src={sourceInfo.favicon}
            alt={sourceInfo.name}
            className="w-full h-full object-cover"
            onError={() => setImageError(true)}
          />
        )}
      </div>
      <div className="flex-1 min-w-0">
        <div className="font-medium text-gray-300 truncate group-hover:text-white transition-colors duration-200">
          {sourceInfo.name}
        </div>
        <div className="text-sm text-gray-500 truncate">
          {new URL(source).hostname}
        </div>
      </div>
    </a>
  );
};

const SourcesContent = ({ sources }: { sources: string[] }) => {
  return (
    <div className="h-full overflow-y-auto p-4">
      <div className="grid grid-cols-1 gap-3">
        {sources.map((source, index) => (
          <SourceButton key={index} source={source} />
        ))}
      </div>
    </div>
  );
};


const DatasetGeneration = ({
    onMove,
    statusText,
    logContent,
    dataset,
    sources,
    complete
}: {
    onMove: () => void;
    statusText: string;
    logContent: string;
    dataset: any[];
    sources: string[];
    complete: boolean;
}) => {
  const [mainLogOpen, setMainLogOpen] = useState(true);
  const [sourcesLogOpen, setSourcesLogOpen] = useState(false);

  const logLines = (logContent || "").split('\n');

  const toggleMainLog = () => {
    setMainLogOpen(!mainLogOpen);
    if (!mainLogOpen && sourcesLogOpen) {
      setSourcesLogOpen(false);
    }
  };

  const toggleSourcesLog = () => {
    setSourcesLogOpen(!sourcesLogOpen);
    if (!sourcesLogOpen && mainLogOpen) {
      setMainLogOpen(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* Header and status text remain the same */}
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
        className="space-y-2"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <LogSection
          title="Dataset Log"
          isOpen={mainLogOpen}
          onToggle={toggleMainLog}
          otherSectionOpen={sourcesLogOpen}
        >
          <LogContent lines={logLines} />
        </LogSection>

        <LogSection
          title="Sources"
          isOpen={sourcesLogOpen}
          onToggle={toggleSourcesLog}
          otherSectionOpen={mainLogOpen}
        >
          <SourcesContent sources={sources} />
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

export default DatasetGeneration;
