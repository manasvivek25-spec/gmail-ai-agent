import React from 'react';
import { Sparkles, TrendingUp, Target } from 'lucide-react';
import { Badge } from '../ui/badge';

interface RecommendationFeedProps {
  emails: any[];
  onSelect: (id: string) => void;
  selectedId: string | null;
}

export const RecommendationFeed: React.FC<RecommendationFeedProps> = ({ emails, onSelect, selectedId }) => {
  return (
    <div className="flex-1 overflow-y-auto custom-scrollbar p-10 space-y-12 bg-white">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-black text-slate-900 tracking-tight">Priority Intelligence</h1>
          <p className="text-sm text-slate-500 mt-2 font-medium">Neural engine analysis of your most critical communications.</p>
        </div>
        <div className="bg-secondary/10 text-secondary px-4 py-2 rounded-2xl flex items-center gap-2 border border-secondary/20">
          <Sparkles size={16} />
          <span className="text-[11px] font-black uppercase tracking-wider">AI Optimized</span>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {emails.map((email, index) => (
          <div 
            key={email.email_id}
            onClick={() => onSelect(email.email_id)}
            className={`p-8 rounded-[32px] border transition-all cursor-pointer relative overflow-hidden flex flex-col md:flex-row gap-8 items-center ${
              selectedId === email.email_id 
                ? 'border-primary/20 bg-primary/5 shadow-xl ring-1 ring-primary/10 scale-[1.01]' 
                : 'border-slate-100 bg-white hover:border-secondary/20 hover:shadow-lg'
            }`}
          >
            {index === 0 && (
              <div className="absolute top-0 left-0 bg-secondary text-white px-6 py-1 text-[9px] font-black uppercase tracking-widest rounded-br-2xl shadow-lg">
                Top Priority
              </div>
            )}
            
            <div className="flex flex-col items-center gap-3 shrink-0">
              <div className="w-16 h-16 rounded-[24px] bg-slate-50 border border-slate-100 flex items-center justify-center text-2xl shadow-inner">
                {email.priority === 'Critical' ? '🚨' : email.priority === 'High' ? '🔥' : '⚡'}
              </div>
              <div className="flex flex-col items-center">
                <span className="text-[10px] font-black text-slate-400 uppercase tracking-tighter">Score</span>
                <span className="text-xl font-black text-slate-900">{email.importance}</span>
              </div>
            </div>

            <div className="flex-1 space-y-4">
              <div className="flex items-center gap-3">
                <Badge variant="ai" className="bg-primary/10 text-primary border-none uppercase text-[9px] px-3">
                  {email.category}
                </Badge>
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
                  Received {email.time}
                </span>
              </div>

              <h2 className="text-xl font-bold text-slate-900 leading-tight">
                {email.subject}
              </h2>
              
              <p className="text-sm text-slate-500 leading-relaxed line-clamp-2">
                {email.summary}
              </p>

              <div className="flex flex-wrap gap-2 pt-2">
                <div className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-50 rounded-full text-[10px] font-bold text-slate-600 border border-slate-100">
                  <TrendingUp size={12} className="text-secondary" />
                  High Relevance
                </div>
                <div className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-50 rounded-full text-[10px] font-bold text-slate-600 border border-slate-100">
                  <Target size={12} className="text-primary" />
                  Interest Match
                </div>
              </div>
            </div>

            <div className="shrink-0 flex flex-col gap-2 w-full md:w-auto">
              <button className="px-6 py-3 bg-primary text-white text-xs font-black uppercase tracking-widest rounded-2xl hover:bg-primary/90 transition-all shadow-lg shadow-primary/20 active:scale-95">
                Focus
              </button>
              <button className="px-6 py-3 bg-white text-slate-900 text-xs font-black uppercase tracking-widest rounded-2xl border border-slate-200 hover:bg-slate-50 transition-all active:scale-95">
                Dismiss
              </button>
            </div>
          </div>
        ))}
        {emails.length === 0 && (
          <div className="py-20 text-center">
            <div className="w-20 h-20 bg-secondary/10 rounded-[40px] flex items-center justify-center mx-auto mb-8">
              <Sparkles size={40} className="text-secondary/50" />
            </div>
            <h3 className="text-2xl font-black text-slate-900">Neural Feed Empty</h3>
            <p className="text-sm text-slate-500 mt-2 max-w-sm mx-auto font-medium">The agent hasn't found any high-priority recommendations in your current workspace.</p>
          </div>
        )}
      </div>
    </div>
  );
};
