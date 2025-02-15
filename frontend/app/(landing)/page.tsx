"use client";

import React, { useEffect, useState} from 'react';
import SearchInput from './_components/search-input';

const LandingPage: React.FC = () => {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-12 md:p-24 overflow-x-hidden w-screen bg-background">
      <div className="-z-10 absolute h-[200vw] max-h-[2000px] md:max-h-[1000px] lg:max-h-[1000px] left-0 right-0 top-0 bg-[linear-gradient(to_right,#4f4f4f2e_1px,transparent_1px),linear-gradient(to_bottom,#4f4f4f2e_1px,transparent_1px)] bg-[size:14px_24px] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_0%,#000_70%,transparent_110%)]" />

      <div className="pointer-events-none mt-[4rem] md:mt-80">
        <div className="text-center mb-6">
          <h1 className="text-8xl md:text-8xl font-bold text-white mb-4">
              The Vercel for AI Models
          </h1>
        </div>
        {/* <div className="text-center max-w-3xl mx-auto">
          <p className="text-xl md:text-2xl text-gray-300">
            A deployment platform for your AI models
          </p>
        </div> */}

        <div className="pointer-events-auto px-4 max-w-[900px] w-full mx-auto">
            <SearchInput />
        </div>
      </div>
    </main>
  );
};

export default LandingPage;
