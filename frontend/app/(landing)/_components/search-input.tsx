"use client";

import React, { useState, useRef, useEffect } from 'react';
import { useEnterSubmit } from '@/components/hooks/enter-submit';
import { motion } from 'framer-motion';
import { ProjectMakeStatus } from '@/lib/dtypes';

interface SearchInputProps {
  setStep: (step: ProjectMakeStatus) => void;
  setModelIValue: (value: string) => void;
  sendMessage: (type: string, text?: string, button_reply?: any) => void;
}

const SearchInput: React.FC<SearchInputProps> = ({ setStep, setModelIValue, sendMessage }) => {
  const [inputValue, setInputValue] = useState('');
  const [error, setError] = useState('');
  const [showEnterHint, setShowEnterHint] = useState(true);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleMove = () => {
    if (inputValue) {
      setModelIValue(inputValue);
      setStep(ProjectMakeStatus.MODEL_ADVICE);
      sendMessage("idea_input", inputValue);
    } else {
      setError('Please tell us about your ideal model...');
    }
  };

  useEnterSubmit(() => {
    if (inputValue) {
      handleMove();
    } else {
      setError('Please tell us about your ideal model...');
    }
  });

  useEffect(() => {
    const checkOverlap = () => {
      const input = inputRef.current;
      if (!input) return;

      const span = document.createElement('span');
      span.style.visibility = 'hidden';
      span.style.position = 'absolute';
      span.style.whiteSpace = 'pre';
      span.style.font = window.getComputedStyle(input).font;
      span.textContent = inputValue;
      document.body.appendChild(span);

      const textWidth = span.offsetWidth;
      const inputWidth = input.offsetWidth;
      document.body.removeChild(span);

      setShowEnterHint(textWidth < inputWidth - 100);
    };

    checkOverlap();
  }, [inputValue]);

  return (
    <div className="w-full">
      <div className="flex w-full items-center gap-3">
        <div className="relative flex-1">
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            className="w-full h-12 bg-transparent border border-gray-700
                     text-white/90 placeholder-gray-600 px-4
                     focus:outline-none focus:border-accent
                     transition-all duration-200"
            placeholder="Tell us about your ideal model..."
          />
          {showEnterHint && (
            <div className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-600 text-sm transition-opacity duration-200">
              Press Enter
            </div>
          )}
        </div>
        <button
          className="h-12 px-6 bg-accent hover:bg-accent-hover text-white
                   flex items-center gap-2 transition-colors duration-200"
          onClick={handleMove}
        >
          Run Now
          <span className="text-sm px-2 py-0.5 bg-black/20">⏎</span>
        </button>
      </div>
      {error && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-red-500 text-sm mt-2"
        >
          {error}
        </motion.p>
      )}
    </div>
  );
};

export default SearchInput;
