// app/projects/components/ModelAdvice.tsx
"use client";

import React, { useState } from 'react';
import { motion } from 'framer-motion';

interface Model {
  id: string;
  name: string;
  provider: string;
  type: string;
}

const ModelAdvice: React.FC = () => {
  const [selectedModel, setSelectedModel] = useState('gpt-4-turbo');

  const recommendationRationale = "Based on your use case, we recommend a model with strong instruction-following capabilities and high accuracy.";
  const recommendedModel: Model = {
    id: 'gpt-4-turbo',
    name: 'GPT-4 Turbo',
    provider: 'OpenAI',
    type: 'Large Language Model'
  };

  const modelList: Model[] = [
    { id: 'gpt-3.5-turbo', name: 'GPT-3.5 Turbo', provider: 'OpenAI', type: 'Language Model' },
    { id: 'claude-3-opus', name: 'Claude 3 Opus', provider: 'Anthropic', type: 'Language Model' },
    { id: 'claude-3-sonnet', name: 'Claude 3 Sonnet', provider: 'Anthropic', type: 'Language Model' },
    { id: 'gemini-pro', name: 'Gemini Pro', provider: 'Google', type: 'Language Model' },
    { id: 'mistral-large', name: 'Mistral Large', provider: 'Mistral AI', type: 'Language Model' },
    { id: 'mixtral-8x7b', name: 'Mixtral 8x7B', provider: 'Mistral AI', type: 'Language Model' },
    { id: 'llama-2-70b', name: 'LLaMA 2 70B', provider: 'Meta', type: 'Language Model' },
    { id: 'cohere-command', name: 'Command', provider: 'Cohere', type: 'Language Model' },
    { id: 'palm-2', name: 'PaLM 2', provider: 'Google', type: 'Language Model' },
    { id: 'j2-ultra', name: 'J2-Ultra', provider: 'AI21', type: 'Language Model' },
  ];

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
          Select your preferred model
        </motion.h2>
      </div>

      <motion.p
        className="text-gray-300 text-lg"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
        {recommendationRationale}
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
            checked={selectedModel === recommendedModel.id}
            onChange={() => setSelectedModel(recommendedModel.id)}
            className="mt-1.5 h-4 w-4 border-gray-700 rounded-sm checked:bg-accent hover:border-accent focus:ring-accent"
          />
          <div className="flex-1">
            <div className="text-lg font-medium flex items-center gap-2">
              {recommendedModel.name}
              <span className="text-accent text-sm border border-accent px-2 py-0.5">Recommended</span>
            </div>
            <div className="text-gray-400 text-sm">{recommendedModel.provider} · {recommendedModel.type}</div>
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
          {modelList.map((model) => (
            <label
              key={model.id}
              className="flex items-start space-x-4 p-2 cursor-pointer hover:bg-white/5 transition-colors duration-200"
            >
              <input
                type="checkbox"
                checked={selectedModel === model.id}
                onChange={() => setSelectedModel(model.id)}
                className="mt-1.5 h-4 w-4 border-gray-700 rounded-sm checked:bg-accent hover:border-accent focus:ring-accent"
              />
              <div className="flex-1">
                <div className="text-lg">{model.name}</div>
                <div className="text-gray-400 text-sm">{model.provider} · {model.type}</div>
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
