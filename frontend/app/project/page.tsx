"use client";

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import UserInitialInput from './_components/user_initial_input_form';
import UserDatasetGenInput from './_components/user_dataset_gen_input';
import ModelAdvice from './_components/user_model_advice';
import { HFModel, ProjectMakeStatus } from '@/lib/dtypes';

const ProjectPage = () => {
  const [step, setStep] = useState<ProjectMakeStatus>(ProjectMakeStatus.USER_INPUT);

  const wsRef = useRef<WebSocket | null>(null);
  const [connectionState, setConnectionState] = useState<"CONNECTING" | "OPEN" | "CLOSED">("CONNECTING");
  const [recommendationModel, setRecommendationModel] = useState<HFModel | null>(null);
  const [models, setModels] = useState<HFModel[]>([]);
  const [modelText, setModelText] = useState<string>("");
  const [inputValue, setInputValue] = useState('');

  const sendMessage = useCallback(
    (type: string, text?: string, button_reply?: any) => {
      if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return;
      const message = { type, text, button: button_reply };
      wsRef.current.send(JSON.stringify(message));
    },
    []
  );


  const connect = useCallback(() => {
    setConnectionState("CONNECTING");

    const ws = new WebSocket(`${process.env.NEXT_PUBLIC_API_URL_WS!}/wsc`);

    ws.onopen = () => {
      setConnectionState("OPEN");
    };

    ws.onclose = () => {
      setConnectionState("CLOSED");
    };

    ws.onerror = () => {
      setConnectionState("CLOSED");
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);

        switch (msg.type) {
          case "model_advice":
            setRecommendationModel(msg?.recommendation || null);
            setModelText((prev) => (prev + (msg?.text || "")));
            setModels(msg?.model_list || []);
            break;
          default:
            break;
        }
      } catch (err) {
        console.error("Error parsing WebSocket message:", err);
      }
    };

    wsRef.current = ws;
  }, []);

  useEffect(() => {
    connect();
    return () => {
      wsRef.current?.close();
    };
  }, [connect]);

  useEffect(() => {
    console.log(modelText)
  }, [modelText])

  const handleReconnect = () => {
    wsRef.current?.close();
    connect();
  };

  const handleUserInitialInput = () => {
    setStep(ProjectMakeStatus.MODEL_ADVICE);
    sendMessage("idea_input", inputValue);
  }

  return (
    <main className="min-h-screen bg-background text-white overflow-hidden">
      {/* <div className="fixed top-0 left-0 right-0 h-1 bg-gray-800">
        <div className="h-full w-[16.67%] bg-accent transition-all duration-300" />
      </div> */}

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
            {
              step === ProjectMakeStatus.USER_INPUT && (
                <UserInitialInput 
                  onMove={handleUserInitialInput} 
                  inputValue={inputValue}
                  setInputValue={setInputValue}
                />
              )
            }
            {
              step === ProjectMakeStatus.MODEL_ADVICE && (
                <ModelAdvice 
                  models={models} 
                  modelText={modelText} 
                  recommendationModel={recommendationModel}
                  // onMove={handleUserInitialInput}
                />
              )
            }
            {
              step === ProjectMakeStatus.DS_GENERATION && (
                <UserDatasetGenInput />
              )
            }
          </motion.div>
        </AnimatePresence>
      </div>
    </main>
  );
};

export default ProjectPage;
