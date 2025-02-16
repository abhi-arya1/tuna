"use client";

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { ChevronLeft, ChevronRight } from 'lucide-react';

interface DatasetEntry {
  input: string;
  output: string;
}

interface DatasetViewerProps {
    onMove: () => void;
    data: string[];
    title?: string;
}

const DatasetViewer: React.FC<DatasetViewerProps> = ({
    onMove,
    data,
    title = "Dataset Preview"
}) => {
  console.log(data);
  const [currentPage, setCurrentPage] = useState(0);
  const entriesPerPage = 2;
  const totalPages = Math.ceil(data.length / entriesPerPage);

  const currentEntries = data.slice(
    currentPage * entriesPerPage,
    (currentPage + 1) * entriesPerPage
  );

  return (
    <div className="space-y-8">
      <div className="space-y-2">
        <div className="flex flex-row items-center justify-between">
          <div className="flex flex-col items-start justify-start gap-y-2">
            <motion.span
              className="text-gray-400 text-sm"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
            >
              Dataset Generation
            </motion.span>
            <motion.h2
              className="text-3xl font-normal"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              {title}
            </motion.h2>
          </div>
            <motion.button
              className="h-12 px-6 bg-accent hover:bg-accent-hover text-white
                          flex items-center gap-2 transition-colors duration-200"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              onClick={() => {
                const element = document.createElement('a');
                const file = new Blob([data.join('\n')], { type: 'application/json' });
                element.href = URL.createObjectURL(file);
                element.download = 'dataset.json';
                document.body.appendChild(element);
                element.click();
              }}
            >
              Download Dataset
            </motion.button>
        </div>
      </div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="border border-gray-700 bg-background overflow-hidden"
      >
        <div className="grid grid-cols-2 border-b border-gray-700">
          <div className="p-4 font-mono text-sm text-gray-400">Input</div>
          <div className="p-4 font-mono text-sm text-gray-400 border-l border-gray-700">Output</div>
        </div>

        <div className="divide-y divide-gray-700">
          {currentEntries.map((entry, index) => {
            const item = JSON.parse(entry);
            return (
            <div key={index} className="grid grid-cols-2 hover:bg-gray-800/50 transition-colors">
              <div className="p-6 font-mono text-sm text-white whitespace-pre-wrap">
                {item.input}
              </div>
              <div className="p-6 font-mono text-sm text-white whitespace-pre-wrap border-l border-gray-700">
                {item.output}
              </div>
            </div>
          )})}
        </div>

        <div className="border-t border-gray-700 p-4 flex items-center justify-between">
          <div className="text-sm text-gray-400">
            Showing {currentPage * entriesPerPage + 1} to {Math.min((currentPage + 1) * entriesPerPage, data.length)} of {data.length} entries
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setCurrentPage(Math.max(0, currentPage - 1))}
              disabled={currentPage === 0}
              className="p-2 text-gray-400 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="text-sm text-gray-400">
              Page {currentPage + 1} of {totalPages}
            </span>
            <button
              onClick={() => setCurrentPage(Math.min(totalPages - 1, currentPage + 1))}
              disabled={currentPage === totalPages - 1}
              className="p-2 text-gray-400 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
          <button className="h-12 px-6 bg-accent hover:bg-accent-hover text-white
                          flex items-center gap-2 transition-colors duration-200"
            onClick={onMove}
          >
            Continue
          </button>
        </div>
      </motion.div>
    </div>
  );
};

export default DatasetViewer;
