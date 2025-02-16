"use client";

import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
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
  const inputRef = useRef<HTMLInputElement>(null);

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
          Model Selection
        </motion.span>
        <motion.h2
          className={`${haloGrotesk.className} text-4xl font-normal`}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          Tell us about your ideal model. Inputs, outputs, etc.
        </motion.h2>
      </div>

      <motion.div
        className="w-full"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <div className="flex w-full items-center gap-3 mb-6">
          <div className="relative flex-1">
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder='Describe your ideal model...'
              className="w-full h-12 bg-transparent border border-gray-700
                        text-white/90 placeholder-gray-600 px-4
                        focus:outline-none focus:border-accent
                        transition-all duration-200"
            />
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
          <span className="text-muted-foreground text-sm">Suggestions</span>
          <button
            className="w-full px-6 py-3 border-b-2 border-b-muted-foreground/20 self-start text-start hover:bg-muted-foreground/20 text-white
                      flex items-center gap-2 transition-colors duration-200"
            onClick={() => setInputValue("A user can describe a graph, and get Python Matplotlib code as the output, prioritzing code generation.")}
          >
            A user can describe a graph, and get Python Matplotlib code as the output, prioritzing code generation.
          </button>
          <button
            className="w-full px-6 py-3 my-3 border-b-2 border-b-muted-foreground/20 self-start text-start hover:bg-muted-foreground/20 text-white
                      flex items-center gap-2 transition-colors duration-200"
            onClick={() => setInputValue("A user can ask for recent news on Stanford University, and recieve a summary as the output.")}
          >
            A user can ask for recent news on Stanford University, and recieve a summary as the output.
          </button>
      </motion.div>
    </div>
  );
};

export default UserInitialInput;
