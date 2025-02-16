"use client";

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import UserInput from '../_components/user_initial_input_form';

const ProjectPage = () => {
  return (
    <main className="min-h-screen bg-background text-white overflow-hidden">
      <div className="fixed top-0 left-0 right-0 h-1 bg-gray-800">
        <div className="h-full w-[16.67%] bg-accent transition-all duration-300" />
      </div>

      <div className="max-w-4xl mx-auto min-h-screen flex items-center justify-center p-8">
        <AnimatePresence mode="wait">
          <motion.div
            key="user-input"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.5, ease: [0.23, 1, 0.32, 1] }}
            className="w-full"
          >
            {/* <UserInput /> */}
          </motion.div>
        </AnimatePresence>
      </div>
    </main>
  );
};

export default ProjectPage;
