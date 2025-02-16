"use client";

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import UserInitialInput from './_components/user_initial_input_form';
import UserDatasetGenInput from './_components/user_dataset_gen_input';
import ModelAdvice from './_components/user_model_advice';
import { HFModel, ProjectMakeStatus } from '@/lib/dtypes';
import DatasetGeneration from './_components/live_dataset_gen_view';
import DatasetViewer from './_components/dataset_visualization';
import InstanceSelect from './_components/instance_select';
import LiveTrainingView from './_components/live_training_view';
import { SendToBack } from 'lucide-react';

const ProjectPage = () => {
  const [step, setStep] = useState<ProjectMakeStatus>(ProjectMakeStatus.USER_INPUT);

  const wsRef = useRef<WebSocket | null>(null);
  const [connectionState, setConnectionState] = useState<"CONNECTING" | "OPEN" | "CLOSED">("CONNECTING");

  // Model Recommendation States
  const [recommendationModel, setRecommendationModel] = useState<HFModel | null>(null);
  const [models, setModels] = useState<HFModel[]>([]);
  const [modelText, setModelText] = useState<string>("");
  const [modelIValue, setModelIValue] = useState('');

  const [dsIValue, setDsIValue] = useState('');
  const [dsOValue, setDsOValue] = useState('');
  const [dataset, setDataset] = useState<string[]>([]);
  const [logContent, setLogContent] = useState<string>("");
  const [sources, setSources] = useState<string[]>([]);
  const [complete, setComplete] = useState(false);

  const sendMessage = useCallback(
    (type: string, text?: string, button_reply?: any) => {
      if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return;
      const message = { type, text, button: button_reply };
      wsRef.current.send(JSON.stringify(message));
    },
    []
  );

  useEffect(() => {
    if(localStorage.getItem('modelIValue')) {
      setModelIValue(localStorage.getItem('modelIValue')!);
      localStorage.removeItem('modelIValue');
    }
  }, [])

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

    // class DSGeneration(BaseModel):
    // type: str
    // text: str
    // dataset: list[dict]
    // log: str
    // sources: list[str]
    // complete: bool = False

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);

        switch (msg.type) {
            case "model_advice":
                setRecommendationModel(msg?.recommendation || null);
                setModelText((prev) => (prev + (msg?.text || "")));
                setModels(msg?.model_list || []);
                break;
            case "ds_generation":
                setDsOValue((prev) => prev + (msg?.text || ""));
                setDataset(msg?.dataset || []);
                setLogContent((prev) => prev + (msg?.log || ""));
                setSources(msg?.sources);
                setComplete(msg?.complete || false);
                break;
            case "ds_visualization":
                setComplete(false);
                break;
            case "train_details":
                setLogContent((prev) => prev + (msg?.log || ""));
                setComplete(msg?.complete || false);
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
    sendMessage("idea_input", modelIValue);
  }

  const handleModelSelection = (model: string) => {
    setStep(ProjectMakeStatus.DS_INPUT);
    sendMessage("model_choice", model);
  }

  const handleUserDatasetInput = () => {
    setStep(ProjectMakeStatus.DS_GENERATION);
    sendMessage("dataset_input", dsIValue);
  }

  const handleDatasetGeneration = () => {
      setStep(ProjectMakeStatus.DS_VISUALIZATION);
      fetch(`${process.env.NEXT_PUBLIC_API_URL!}/dataset`).then((data: Response) => {
          console.log(data);
          data.json().then((data: any) => {console.log(data); setDataset(data.dataset)})
      })
      setLogContent("");
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
                  inputValue={modelIValue}
                  setInputValue={setModelIValue}
                />
              )
            }
            {
              step === ProjectMakeStatus.MODEL_ADVICE && (
                <ModelAdvice
                    onMove={handleModelSelection}
                    models={models}
                    modelText={modelText}
                    recommendationModel={recommendationModel}
                />
              )
            }
            {
              step === ProjectMakeStatus.DS_INPUT && (
                <UserDatasetGenInput
                  onMove={handleUserDatasetInput}
                  inputValue={dsIValue}
                  setInputValue={setDsIValue}
                />
              )
            }
            {
              step === ProjectMakeStatus.DS_GENERATION && (
                <DatasetGeneration
                    onMove={handleDatasetGeneration}
                    statusText={dsOValue}
                    logContent={logContent}
                    dataset={[]}
                    sources={sources}
                    complete={complete}
                />
              )
            }
            {
              step === ProjectMakeStatus.DS_VISUALIZATION && (
                <DatasetViewer
                    onMove={() => setStep(ProjectMakeStatus.TRAIN_INST_SELECTION)}
                    data={dataset}
                />
              )
            }
            {
              step === ProjectMakeStatus.TRAIN_INST_SELECTION && (
                <InstanceSelect
                    onMove={() => {
                      sendMessage("train", "");
                      setStep(ProjectMakeStatus.TRAIN_DETAILS)
                    }}
                />
              )
            }
            {
              step === ProjectMakeStatus.TRAIN_DETAILS && (
                <LiveTrainingView
                    onMove={() => {setStep(ProjectMakeStatus.DEPLOYMENT)}}
                    logContent={logContent}
                    complete={complete}
                />
              )
            }

            {/* <LiveTrainingView
                onMove={() => {setStep(ProjectMakeStatus.DEPLOYMENT)}}
                logContent={logContent}
                complete={complete}
            /> */}

          </motion.div>
        </AnimatePresence>
      </div>
    </main>
  );
};

export default ProjectPage;
