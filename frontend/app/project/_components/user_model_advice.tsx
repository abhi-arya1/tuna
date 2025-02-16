"use client";
import React, { useState, useCallback, useEffect } from 'react';
import { motion } from 'framer-motion';
import { HFModel } from '@/lib/dtypes';

const ModelSkeleton = () => (
  <div className="flex items-start space-x-4 p-2">
    <div className="mt-1.5 h-4 w-4 bg-gray-800 rounded-sm animate-pulse" />
    <div className="flex-1 space-y-2">
      <div className="h-6 bg-gray-800 rounded w-1/2 animate-pulse" />
      <div className="h-4 bg-gray-800 rounded w-1/3 animate-pulse" />
    </div>
  </div>
);

const RecommendedModelSkeleton = () => (
  <div className="border border-accent p-4">
    <div className="flex items-start space-x-4">
      <div className="mt-1.5 h-4 w-4 bg-gray-800 rounded-sm animate-pulse" />
      <div className="flex-1 space-y-2">
        <div className="flex items-center justify-between">
          <div className="h-6 bg-gray-800 rounded w-1/3 animate-pulse" />
          <div className="h-6 w-24 bg-gray-800 rounded animate-pulse" />
        </div>
        <div className="h-4 bg-gray-800 rounded w-1/4 animate-pulse" />
      </div>
    </div>
  </div>
);

const ModelAdvice = ({
    onMove,
    models,
    modelText,
    recommendationModel
}: {
    onMove: (model: string) => void;
    models: HFModel[];
    modelText: string;
    recommendationModel: HFModel | null;
}) => {
  const [selectedModel, setSelectedModel] = useState('gpt-4-turbo');


  const filteredModels = models?.filter(model => model.id !== recommendationModel?.id) ?? [];

  return (
    <div className="space-y-8">
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
          className="text-3xl font-normal"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          Select your preferred Model
        </motion.h2>
      </div>

      <motion.div
        className="relative min-h-[100px]"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
        {modelText === null ? (
          <div className="space-y-2 absolute inset-0">
            <div className="h-5 bg-gray-800 rounded-sm w-full animate-pulse" />
            <div className="h-5 bg-gray-800 rounded-sm w-11/12 animate-pulse" />
            <div className="h-5 bg-gray-800 rounded-sm w-2/3 animate-pulse" />
          </div>
        ) : (
          <p className="text-gray-300 text-lg">
            {modelText}
          </p>
        )}
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        {recommendationModel === null ? (
          <RecommendedModelSkeleton />
        ) : (
          <div className="border border-accent p-4">
            <label className="flex items-start space-x-4 cursor-pointer">
              <input
                type="checkbox"
                checked={selectedModel === recommendationModel.id}
                onChange={() => setSelectedModel(recommendationModel.id)}
                className="mt-1.5 h-4 w-4 border-gray-700 rounded-sm checked:bg-accent hover:border-accent focus:ring-accent"
              />
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <span className="text-lg font-medium">{recommendationModel.id}</span>
                  <span className="text-accent text-sm border border-accent px-2 py-0.5 self-center">Recommended</span>
                </div>
                <div className="text-gray-400 text-sm">Created on {new Date(recommendationModel.created_at).toDateString()} · {recommendationModel.downloads} Downloads</div>
              </div>
            </label>
          </div>
        )}
      </motion.div>

      <div className="space-y-2">
        <span className="text-sm text-gray-400">More models</span>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="border border-gray-700 max-h-[300px] overflow-y-auto"
        >
          <div className="p-2 space-y-2">
            {models === null || models.length === 0 ? (
              <>
                <ModelSkeleton />
                <ModelSkeleton />
                <ModelSkeleton />
                <ModelSkeleton />
              </>
            ) : (
              filteredModels.map((HFModel) => (
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
                    <div className="text-gray-400 text-sm">Created on {new Date(HFModel.created_at).toDateString()} · {HFModel.downloads} Downloads</div>
                  </div>
                </label>
              ))
            )}
          </div>
        </motion.div>
      </div>

      <motion.div
        className="flex justify-end"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.7 }}
      >
        <button className="h-12 px-6 bg-accent hover:bg-accent-hover text-white
                          flex items-center gap-2 transition-colors duration-200"
                          onClick={() => onMove(selectedModel)}>
          Continue
        </button>
      </motion.div>
    </div>
  );
};

export default ModelAdvice;
