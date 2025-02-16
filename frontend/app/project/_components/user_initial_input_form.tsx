"use client";

import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useEnterSubmit } from '@/components/hooks/enter-submit';
import { haloGrotesk } from '@/app/fonts';

const UserInitialInput = ({
  onMove,
  inputValue,
  setInputValue
}: {
  onMove: (input: string) => void;
  inputValue: string;
  setInputValue: (input: string) => void;
}) => {
  const [error, setError] = useState("");
  const [showEnterHint, setShowEnterHint] = useState(true);
  const inputRef = useRef<HTMLInputElement>(null);

  useEnterSubmit(() => {
    if (inputValue) {
      onMove(inputValue);
    } else {
      setError("Please enter details on your ideal model...."); // FIXME: LATER
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
    <div className="space-y-8 bg-transparent">
      <div className="space-y-2">
        <motion.span
          className="text-gray-400 text-sm"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          Models
        </motion.span>
        <motion.h2
          className={`${haloGrotesk.className} text-4xl font-normal`}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          What are you using your model for?
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
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              className="w-full h-12 bg-transparent border border-gray-700
                        text-white/90 placeholder-gray-600 px-4
                        focus:outline-none focus:border-accent
                        transition-all duration-200"
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
            onClick={() => {
              if(inputValue) {
                onMove(inputValue);
              } else {
                setError("Please enter details on your ideal model....") // FIXME: LATER
              }
            }}
          >
            Continue
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
      </motion.div>
    </div>
  );
};

export default UserInitialInput;
