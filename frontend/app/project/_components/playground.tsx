"use client";


import React, { useState, useCallback, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Send, Loader2 } from 'lucide-react';
import type { KeyboardEvent } from 'react';
import OpenAI from "openai";
import { pinwheel } from 'ldrs'

pinwheel.register();


interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface PlaygroundProps {
  modelId: string;
  onError?: (error: string) => void;
}

const MessageBubble = ({ message }: { message: Message }) => (
  <motion.div
    initial={{ opacity: 0, y: 10 }}
    animate={{ opacity: 1, y: 0 }}
    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
  >
    <div
      className={`max-w-[80%] px-4 py-2 ${
        message.role === 'user'
          ? 'bg-accent text-white border-gray-400 border-2'
          : 'bg-gray-800 text-gray-100'
      }`}
    >
      <p className="whitespace-pre-wrap">{message.content}</p>
    </div>
  </motion.div>
);

const Playground = ({ modelId, onError }: PlaygroundProps) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);


  const handleSubmit = useCallback(async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: input.trim()
    };

    const inputMessages = [...messages, userMessage];

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const openai = new OpenAI({
        apiKey: "runway_key",
        baseURL: "http://localhost:8000/v1",
        dangerouslyAllowBrowser: true
      });

      const response = await openai.chat.completions.create({
        model: "runway_base",
        messages: inputMessages
      });

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.choices[0].message.content || ""
      }]);
    } catch (error) {
      console.error(error);
      onError?.(error instanceof Error ? error.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  }, [input, isLoading, messages, modelId, onError]);

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="space-y-8 bg-transparent">
      <div className="space-y-2">
        <motion.span
          className="text-gray-400 text-sm"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          Model Playground
        </motion.span>
        <motion.h2
          className="text-4xl font-normal"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          Chat with your model
        </motion.h2>
      </div>

      <motion.div
        className="w-full h-[600px] flex flex-col"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <div className="flex-1 overflow-y-auto space-y-4 p-4 border border-gray-700">
          {messages.map((message, index) => (
            <MessageBubble key={index} message={message} />
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <motion.div
                className="bg-gray-800 rounded-lg px-4 py-2"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                <Loader2 className="animate-spin" size={24} />
              </motion.div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="border border-gray-700 border-t-0 p-4">
          <div className="flex items-start gap-3">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Send a message..."
              disabled={isLoading}
              className="flex-1 h-12 max-h-48 bg-transparent border border-gray-700
                       text-white/90 placeholder-gray-600 px-4 py-2 resize-none
                       focus:outline-none focus:border-accent
                       transition-all duration-200
                       disabled:opacity-50 disabled:cursor-not-allowed"
              style={{ minHeight: '48px' }}
            />
            <button
              onClick={handleSubmit}
              disabled={!input.trim() || isLoading}
              className="h-12 px-6 bg-accent hover:bg-accent-hover text-white
                        flex items-center gap-2 transition-colors duration-200
                        disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                  <Loader2 className="animate-spin" size={20} />
                  // <PinwheelLoader />
              ) : (
                <Send size={20} />
              )}
            </button>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Playground;
