"use client";

import React, { useCallback, useEffect, useRef, useState } from 'react';
import SearchInput from './_components/search-input';
import EasyUse from './_components/easy_use';
import FeatureGrid from './_components/features';
import { ProjectMakeStatus } from '@/lib/dtypes';
import { haloGrotesk } from '@/app/fonts';
import { useRouter } from 'next/navigation';

const LandingPage: React.FC = () => {
  const router = useRouter();

  const wsRef = useRef<WebSocket | null>(null);
  const [connectionState, setConnectionState] = useState<"CONNECTING" | "OPEN" | "CLOSED">("CONNECTING");
  const [modelIValue, setModelIValue] = useState('');
  const [step, setStep] = useState<ProjectMakeStatus>(ProjectMakeStatus.USER_INPUT);

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
        console.log(msg.type)
        if (msg.type === "model_advice") {
          router.push('/project');
        }
      } catch (err) {
        console.error("Error parsing WebSocket message:", err);
      }
    };

    wsRef.current = ws;
  }, [router]);

  useEffect(() => {
    connect();
    return () => {
      wsRef.current?.close();
    };
  }, [connect]);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-12 md:p-24 overflow-x-hidden w-screen bg-background">
      <div className="-z-10 absolute h-[200vw] max-h-[2000px] md:max-h-[1000px] lg:max-h-[1000px] left-0 right-0 top-0 bg-[linear-gradient(to_right,#4f4f4f2e_1px,transparent_1px),linear-gradient(to_bottom,#4f4f4f2e_1px,transparent_1px)] bg-[size:14px_24px] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_0%,#000_70%,transparent_110%)]" />

      <div className="pointer-events-none mt-[4rem] md:mt-80">
        <div className="text-center mb-6">
          <h1 className={`${haloGrotesk.className} text-8xl md:text-8xl font-bold text-white mb-4`}>
            The Vercel for AI Models
          </h1>
        </div>

        <div className="pointer-events-auto px-4 max-w-[900px] w-full mx-auto">
          <SearchInput
            setStep={setStep}
            setModelIValue={setModelIValue}
            sendMessage={sendMessage}
          />
        </div>

        <div className="flex flex-col py-1 mt-20">
          <h3 className="text-gray-400 text-center">Powered By</h3>
          <div className="flex flex-row gap-x-4 justify-center items-center pt-4">
            <img src="/groq.png" alt="Hero Image" className="h-8" />
            <img src="/perplexity.png" alt="Hero Image" className="h-8" />
          </div>
        </div>

        <div className="mb-6 mt-20">
          <FeatureGrid />
        </div>
      </div>
    </main>
  );
};

export default LandingPage;
