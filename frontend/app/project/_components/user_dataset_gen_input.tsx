"use client";

import React, { useState } from 'react';
import { motion } from 'framer-motion';

const UserDatasetGenInput: React.FC = () => {
  const [inputValue, setInputValue] = useState('');

  return (
    <div className="space-y-8 bg-transparent">
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
          className="text-4xl font-normal"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
            What should your model do?
        </motion.h2>
      </div>

      <motion.div
        className="w-full"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <div className="flex w-full items-center gap-3">
          <div className="relative flex-1">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              className="w-full h-12 bg-transparent border border-gray-700
                        text-white/90 placeholder-gray-600 px-4
                        focus:outline-none focus:border-accent
                        transition-all duration-200"
            />
            <div className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-600 text-sm">
              Press Enter
            </div>
          </div>
          <button className="h-12 px-6 bg-accent hover:bg-accent-hover text-white
                          flex items-center gap-2 transition-colors duration-200">
            Continue
            <span className="text-sm py-0.5 text-gray-200">⏎</span>
          </button>
        </div>
      </motion.div>
    </div>
  );
};

export default UserDatasetGenInput;
