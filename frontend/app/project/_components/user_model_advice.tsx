"use client";

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { HFModel } from '@/lib/dtypes';


const ModelAdvice = ({
  models,
  modelText,
  recommendationModel
}: {
  models: HFModel[];
  modelText: string;
  recommendationModel: HFModel | null;
}) => {
  const [selectedModel, setSelectedModel] = useState('gpt-4-turbo');

  return (
    <div className="space-y-8">
      <div className="space-y-2">
        <motion.span
          className="text-gray-400 text-sm"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
            Model Advice
        </motion.span>
        <motion.h2
          className="text-3xl font-normal"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          Select your preferred Model
        </motion.h2>
      </div>

      <motion.p
        className="text-gray-300 text-lg"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
        {modelText ? modelText : "LOADING"}
      </motion.p>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="border border-accent p-4"
      >
        <label className="flex items-start space-x-4 cursor-pointer">
          <input
            type="checkbox"
            checked={selectedModel === recommendationModel?.id}
            // onChange={() => setSelectedModel(recommendationModel?.id)}
            onChange={() => {}}
            className="mt-1.5 h-4 w-4 border-gray-700 rounded-sm checked:bg-accent hover:border-accent focus:ring-accent"
          />
          <div className="flex-1">
            <div className="flex items-center justify-between">
            <span className="text-lg font-medium">{recommendationModel?.id}</span>
            <span className="text-accent text-sm border border-accent px-2 py-0.5 ml-2">Recommended</span>
            </div>
            <div className="text-gray-400 text-sm">{recommendationModel?.created_at} · {recommendationModel?.downloads}</div>
          </div>
        </label>
      </motion.div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
        className="border border-gray-700 max-h-[300px] overflow-y-auto"
      >
        <div className="p-2 space-y-2">
          {models.map((HFModel) => (
            <label
              key={HFModel.id}
              className="flex items-start space-x-4 p-2 cursor-pointer hover:bg-white/5 transition-colors duration-200"
            >
              <input
                type="checkbox"
                checked={selectedModel === HFModel.id}
                onChange={() => setSelectedModel(HFModel.id)}
                className="mt-1.5 h-4 w-4 border-gray-700 rounded-sm checked:bg-accent hover:border-accent focus:ring-accent"
              />
              <div className="flex-1">
                <div className="text-lg">{HFModel.id}</div>
                <div className="text-gray-400 text-sm">{HFModel.created_at} · {HFModel.downloads}</div>
              </div>
            </label>
          ))}
        </div>
      </motion.div>

      <motion.div
        className="flex justify-end"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.7 }}
      >
        <button className="h-12 px-6 bg-accent hover:bg-accent-hover text-white
                          flex items-center gap-2 transition-colors duration-200">
          Continue
          <span className="text-sm px-2 py-0.5 bg-black/20">⏎</span>
        </button>
      </motion.div>
    </div>
  );
};

export default ModelAdvice;
