"use client";

import React from 'react';
import { motion } from 'framer-motion';
import { Zap, Brain, Cloud, BookOpen, Database, Workflow, Stars, Cpu, Code } from 'lucide-react';

interface Feature {
  icon: React.ReactNode;
  label: string;
  title: string;
  description: string;
}

const features = [
  {
    icon: <Database className="w-4 h-4" />,
    label: "Smart Dataset Creation",
    title: "Tell us what you're building, and we'll generate the perfect dataset for your model.",
    description: "Describe your needs in plain English, and our AI will craft a comprehensive, high-quality dataset specifically for your use case."
  },
  {
    icon: <Brain className="w-4 h-4" />,
    label: "Model Intelligence",
    title: "Get matched with the ideal model architecture through natural conversation.",
    description: "Share your goals, and we'll recommend the perfect model based on your requirements, data, and performance needs."
  },
  {
    icon: <Cloud className="w-4 h-4" />,
    label: "Enterprise Training",
    title: "Train on cutting-edge hardware with simple English commands.",
    description: "Turn plain text into training jobs on enterprise-grade infrastructure. No configuration files or cloud expertise needed."
  },
  {
    icon: <Workflow className="w-4 h-4" />,
    label: "Natural Deployment",
    title: "Deploy production-ready models by describing what you need.",
    description: "Tell us your scaling, latency, and cost requirements, and we'll handle the infrastructure decisions automatically."
  },
  {
    icon: <Stars className="w-4 h-4" />,
    label: "End-to-End Experience",
    title: "Build complete AI solutions using natural conversation, from data to deployment.",
    description: "One cohesive experience for your entire AI development journey, powered by intelligent automation."
  },
  {
    icon: <Zap className="w-4 h-4" />,
    label: "State-of-the-Art Hardware",
    title: "Production-ready infrastructure, accessible through natural language.",
    description: "The same powerful tools used by industry leaders, but with a natural language interface anyone can use."
  }
];

const FeatureGrid = () => {
  return (
    <div className="w-full py-20">
      <div className="max-w-[1200px] mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="relative p-12 border-b border-[#333] mb-16"
        >
          <div className="absolute left-0 top-0 w-3 h-3">
            <div className="absolute left-0 top-0 w-[1px] h-3 bg-[#333]" />
            <div className="absolute left-0 top-0 h-[1px] w-3 bg-[#333]" />
          </div>
          <div className="absolute right-0 top-0 w-3 h-3">
            <div className="absolute right-0 top-0 w-[1px] h-3 bg-[#333]" />
            <div className="absolute right-0 top-0 h-[1px] w-3 bg-[#333]" />
          </div>

          <div className="max-w-3xl">
            <h1 className="text-[64px] leading-[1.1] font-normal text-white mb-6">
                Empowering the "citizen developer"
            </h1>
            <p className="text-[20px] leading-[1.6] text-[#888] mb-8">
              Create rich datasets, train production models, and deploy to enterprise infrastructure—all through natural language.
            </p>
            <div className="flex gap-4">
              <button className="px-6 py-3 bg-white text-black hover:bg-gray-200 transition-colors">
                Start Building
              </button>
              <button className="px-6 py-3 border border-[#333] text-white hover:bg-[#111] transition-colors">
                View Documentation
              </button>
            </div>
          </div>
        </motion.div>

        <div className="grid grid-cols-3 relative">
          {features.map((feature, index) => {
            const isLastInRow = (index + 1) % 3 === 0;
            const isFirstInRow = index % 3 === 0;
            const isTopRow = index < 3;

            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className={`
                  relative p-8 min-h-[280px]
                  ${!isLastInRow ? 'border-r border-[#333]' : ''}
                  ${isTopRow ? 'border-b border-[#333]' : ''}
                `}
              >
                {(index === 0 || index === 2 || index === 3 || index === 5) && (
                  <div className={`absolute ${index === 0 || index === 3 ? 'left-0' : 'right-0'}
                                 ${index < 3 ? 'top-0' : 'bottom-0'} w-3 h-3`}>
                    <div className={`absolute ${index === 0 || index === 3 ? 'left-0' : 'right-0'}
                                   ${index < 3 ? 'top-0' : 'bottom-0'} w-[1px] h-3 bg-[#333]`} />
                    <div className={`absolute ${index === 0 || index === 3 ? 'left-0' : 'right-0'}
                                   ${index < 3 ? 'top-0' : 'bottom-0'} h-[1px] w-3 bg-[#333]`} />
                  </div>
                )}

                <div className="space-y-4">
                  <div className="flex items-center gap-2 text-[#888]">
                    {feature.icon}
                    <span className="text-[14px] tracking-[-0.01em]">{feature.label}</span>
                  </div>
                  <h3 className="text-[20px] leading-[1.4] text-white font-normal pr-6">
                    {feature.title}
                  </h3>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default FeatureGrid;
