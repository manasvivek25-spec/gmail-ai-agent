import React, { useState } from 'react';
import { Bot, Send, User, X, Loader2, Command } from 'lucide-react';
import { api } from '../services/api';
import { Button } from './ui/button';

interface AIAssistantProps {
  isOpen: boolean;
  onClose: () => void;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const AIAssistant: React.FC<AIAssistantProps> = ({ isOpen, onClose }) => {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!query.trim()) return;

    const userMsg: Message = { role: 'user', content: query };
    setMessages(prev => [...prev, userMsg]);
    setQuery('');
    setIsLoading(true);

    try {
      const response = await api.ask(query);
      const assistantMsg: Message = { role: 'assistant', content: response.data.response };
      setMessages(prev => [...prev, assistantMsg]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error processing your request.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-white/40 backdrop-blur-md flex items-center justify-center z-50 p-4 animate-in fade-in duration-300">
      <div className="bg-white border border-slate-200 w-full max-w-2xl h-[700px] rounded-[32px] shadow-2xl flex flex-col overflow-hidden relative">
        <header className="px-8 py-6 border-b border-slate-100 flex justify-between items-center bg-white/80 sticky top-0 z-10">
          <div className="flex items-center space-x-4">
            <div className="p-2.5 bg-primary rounded-2xl text-white shadow-lg shadow-primary/20">
              <Bot size={28} />
            </div>
            <div>
              <h2 className="text-xl font-black text-slate-900 tracking-tight">Neural Engine</h2>
              <p className="text-[10px] text-primary uppercase tracking-widest font-black">Professional Assistant Active</p>
            </div>
          </div>
          <Button variant="ghost" size="icon" onClick={onClose} className="rounded-full hover:bg-slate-50">
            <X size={24} className="text-slate-400" />
          </Button>
        </header>

        <div className="flex-1 overflow-y-auto p-8 space-y-8 custom-scrollbar bg-slate-50/30">
          {messages.length === 0 && (
            <div className="h-full flex flex-col items-center justify-center text-slate-400 space-y-8 text-center max-w-md mx-auto">
              <div className="w-24 h-24 bg-white rounded-[40px] shadow-sm flex items-center justify-center border border-slate-100">
                <Bot size={48} className="text-primary opacity-20" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-slate-900 mb-2">How can the agent help?</h3>
                <p className="text-sm">I can analyze your deadlines, prioritize tasks, or search through your communication history using natural language.</p>
              </div>
              <div className="flex flex-wrap justify-center gap-3">
                {['What are my top priorities?', 'List upcoming deadlines', 'Summarize recent emails'].map(suggestion => (
                  <button 
                    key={suggestion}
                    onClick={() => setQuery(suggestion)}
                    className="px-4 py-2 bg-white hover:bg-primary/10 hover:border-primary/20 hover:text-primary text-[11px] font-bold text-slate-600 rounded-2xl transition-all border border-slate-200 shadow-sm"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-in slide-in-from-bottom-2 duration-300`}>
              <div className={`flex max-w-[85%] gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                <div className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 shadow-sm ${
                  msg.role === 'user' ? 'bg-slate-900 text-white' : 'bg-primary text-white'
                }`}>
                  {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                </div>
                <div className={`p-5 rounded-2xl text-sm leading-relaxed shadow-sm ${
                  msg.role === 'user' 
                    ? 'bg-slate-900 text-white rounded-tr-none' 
                    : 'bg-white text-slate-700 border border-slate-100 rounded-tl-none font-medium'
                }`}>
                  {msg.content}
                </div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start animate-pulse">
              <div className="bg-white border border-slate-100 p-5 rounded-2xl rounded-tl-none text-primary flex items-center space-x-3 shadow-sm">
                <Loader2 size={16} className="animate-spin" />
                <span className="text-[10px] font-black uppercase tracking-widest">Synthesizing Response...</span>
              </div>
            </div>
          )}
        </div>

        <div className="p-8 bg-white border-t border-slate-100">
          <div className="flex items-center gap-3 bg-slate-50 border border-slate-200 rounded-[24px] p-2 pl-6 focus-within:ring-2 focus-within:ring-primary/20 focus-within:border-primary/30 transition-all">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Query the neural engine..."
              className="flex-1 bg-transparent border-none focus:outline-none text-sm text-slate-900 placeholder:text-slate-400 font-medium"
            />
            <div className="flex items-center gap-1 px-3 py-1 bg-white border border-slate-200 rounded-lg text-[10px] font-bold text-slate-300">
              <Command size={10} />
              <span>K</span>
            </div>
            <Button 
              onClick={handleSend}
              disabled={isLoading || !query.trim()}
              variant="ai"
              size="icon"
              className="rounded-2xl shrink-0"
            >
              <Send size={18} />
            </Button>
          </div>
          <p className="mt-4 text-[10px] text-center text-slate-400 font-bold uppercase tracking-widest">
            Privacy Protected • Local Inference Only
          </p>
        </div>
      </div>
    </div>
  );
};

export default AIAssistant;
