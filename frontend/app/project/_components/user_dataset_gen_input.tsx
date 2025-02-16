"use client";

import React, { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import type { KeyboardEvent } from 'react';

const UserDatasetGenInput = ({
  onMove,
  inputValue,
  setInputValue
}: {
  onMove: (input: string) => void;
  inputValue: string;
  setInputValue: (input: string) => void;
}) => {
  const [error, setError] = useState("");

  const handleSubmit = useCallback(() => {
    if (inputValue) {
      onMove(inputValue);
    } else {
      setError("Please enter details on your ideal dataset....");
    }
  }, [inputValue, onMove]);

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSubmit();
    }
  };

  return (
    <div className="space-y-8 bg-transparent">
      <div className="space-y-2">
        <motion.span
          className="text-gray-400 text-sm"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
            Dataset Generation
        </motion.span>
        <motion.h2
          className="text-4xl font-normal"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
            How do you want your input/output to look?
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
              onChange={(e) => {
                setInputValue(e.target.value);
                if (error) setError("");
              }}
              onKeyDown={handleKeyDown}
              className="w-full h-12 bg-transparent border border-gray-700
                        text-white/90 placeholder-gray-600 px-4
                        focus:outline-none focus:border-accent
                        transition-all duration-200"
              placeholder='Describe your ideal dataset. Inputs, outputs, etc...'
            />
          </div>
          <button
            className="h-12 px-6 bg-accent hover:bg-accent-hover text-white
                      flex items-center gap-2 transition-colors duration-200"
            onClick={handleSubmit}
          >
            Continue
          </button>
        </div>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: 5 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-red-500 mt-2 text-sm"
          >
            {error}
          </motion.div>
        )}
      </motion.div>
    </div>
  );
};

export default UserDatasetGenInput;
