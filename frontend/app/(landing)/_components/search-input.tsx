import React, { useState, useEffect } from 'react';

const placeholders = [
  "Enter your OpenAI key...",
  "Enter your Anthropic key...",
  "Enter your Mistral key...",
  "Enter your Gemini key..."
];

const SearchInput: React.FC = () => {
  const [placeholder, setPlaceholder] = useState(placeholders[0]);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % placeholders.length);
      setPlaceholder(placeholders[(currentIndex + 1) % placeholders.length]);
    }, 3000);

    return () => clearInterval(interval);
  }, [currentIndex]);

  return (
      <div className="flex w-full items-center gap-3">
        <div className="relative flex-1">
          <input
            type="text"
            className="w-full h-12 bg-transparent border border-gray-700
                       text-white/90 placeholder-gray-600 px-4
                       focus:outline-none focus:border-accent
                       transition-all duration-200"
            placeholder="Enter your OpenAI key..."
          />
          <div className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-600 text-sm">
            Press Enter
          </div>
        </div>
        <button className="h-12 px-6 bg-accent hover:bg-accent-hover text-white
                         flex items-center gap-2 transition-colors duration-200">
          Run Now
          <span className="text-sm px-2 py-0.5 bg-black/20">⌘R</span>
        </button>
      </div>
    );
};

export default SearchInput;
