"use client";
import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { EC2Instance } from '@/lib/dtypes';
import { EC2_G4DN, EC2_P5 } from '@/lib/dtypes';

const InstanceSelect = ({
    onMove,
}: {
    onMove: (inst: EC2Instance) => void;
}) => {
    const [selectedInstance, setSelectedInstance] = useState<EC2Instance | null>(null);

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <motion.span
          className="text-gray-400 text-sm"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          Training Hardware
        </motion.span>
        <motion.h2
          className="text-3xl font-normal"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          Select the Training Hardware
        </motion.h2>
      </div>

      <motion.div
        className="relative min-h-[100px]"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
          <p className="text-gray-300 text-lg">
            {"Next, select the ideal hardware for training your model. We recommend the H100 for the speed and performance it offers, especially with larger datasets."}
          </p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
          <div className="border border-accent p-4">
            <label className="flex items-start space-x-4 cursor-pointer">
              <input
                type="checkbox"
                checked={selectedInstance === EC2_P5}
                onChange={() => setSelectedInstance(EC2_P5)}
                className="mt-1.5 h-4 w-4 border-gray-700 rounded-sm checked:bg-accent hover:border-accent focus:ring-accent"
              />
              <div className="flex-1">
                <div className="flex items-center justify-between">
                    <div className="flex flex-row gap-x-2 items-center justify-center pb-3">
                        <img src="/nvidia.png" className="h-8" />
                        <span className="text-lg font-medium">NVIDIA H100</span>
                    </div>
                  <span className="text-accent text-sm border border-accent px-2 py-0.5 self-center">Recommended</span>
                </div>
                <div className="text-gray-400 text-sm">{EC2_P5.memory_gb} GB Memory · {EC2_P5.vcpus} vCPUs · {EC2_P5.storage_gb} GB Storage</div>
              </div>
            </label>
          </div>
      </motion.div>

      <div className="space-y-2">
        <span className="text-sm text-gray-400">Otherwise, we offer another instance:</span>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="border border-gray-700 max-h-[300px] overflow-y-auto"
        >
          <div className="p-2 space-y-2">
                <label
                  className="flex items-start space-x-4 p-2 cursor-pointer hover:bg-white/5 transition-colors duration-200"
                >
                  <input
                    type="checkbox"
                    checked={selectedInstance === EC2_G4DN}
                    onChange={() => setSelectedInstance(EC2_G4DN)}
                    className="mt-1.5 h-4 w-4 border-gray-700 rounded-sm checked:bg-accent hover:border-accent focus:ring-accent"
                  />
                  <div className="flex-1 justify-start items-start flex flex-col">
                     <div className="flex flex-row gap-x-2 items-center justify-center pb-3">
                        <img src="/nvidia.png" className="h-8" />
                        <span className="text-lg font-medium">NVIDIA A100</span>
                    </div>
                    <div className="text-gray-400 text-sm">{EC2_G4DN.memory_gb} GB Memory · {EC2_G4DN.vcpus} vCPUs · {EC2_G4DN.storage_gb} GB Storage</div>
                  </div>
                </label>
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
                          onClick={() => onMove(selectedInstance || EC2_P5)}>
          Continue
        </button>
      </motion.div>
    </div>
  );
};

export default InstanceSelect;
