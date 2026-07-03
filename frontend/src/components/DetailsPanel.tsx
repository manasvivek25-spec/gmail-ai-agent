
import React from 'react';
import { Star, Calendar, MessageSquare, Info, Lightbulb, User, Share2, MoreHorizontal } from 'lucide-react';

interface EmailDetails {
  subject: string;
  summary: string;
  body: string;
  deadline: string;
  importance: number;
  relevance: number;
  tags: string[];
  labels: string[];
}

interface DetailsPanelProps {
  email: EmailDetails | null;
  onToggleBookmark: () => void;
  isBookmarked: boolean;
}

const DetailsPanel: React.FC<DetailsPanelProps> = ({ email, onToggleBookmark, isBookmarked }) => {
  if (!email) {
    return (
      <div className="flex-1 flex items-center justify-center bg-white text-slate-400">
        <div className="text-center max-w-sm px-6">
          <div className="w-20 h-20 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-6">
            <MessageSquare size={32} className="text-blue-500 opacity-50" />
          </div>
          <h2 className="text-xl font-bold text-slate-900 mb-2">Select a communication</h2>
          <p className="text-sm">Choose an email from the list to see AI insights and full conversation details.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col bg-white overflow-hidden h-screen">
      <header className="p-8 border-b border-slate-100 flex justify-between items-start bg-white sticky top-0 z-10">
        <div className="flex-1 pr-8">
          <div className="flex items-center space-x-2 mb-4">
            {email.labels.map(l => (
              <span key={l} className="px-2.5 py-1 bg-blue-50 text-blue-700 text-[10px] font-bold rounded-lg uppercase tracking-wider">
                {l}
              </span>
            ))}
          </div>
          <h1 className="text-2xl font-black text-slate-900 leading-tight tracking-tight">{email.subject}</h1>
          
          <div className="flex items-center mt-6 space-x-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-600">
                <User size={16} />
              </div>
              <div>
                <p className="text-xs font-bold text-slate-900 leading-none">Sender Identity</p>
                <p className="text-[10px] text-slate-500 font-medium">via Email AI Agent</p>
              </div>
            </div>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <button className="p-2.5 text-slate-400 hover:text-slate-600 hover:bg-slate-50 rounded-xl transition-all">
            <Share2 size={20} />
          </button>
          <button 
            onClick={onToggleBookmark}
            className={`p-2.5 rounded-xl transition-all ${
              isBookmarked ? 'text-yellow-500 bg-yellow-50 shadow-sm' : 'text-slate-400 hover:bg-slate-50'
            }`}
          >
            <Star size={20} fill={isBookmarked ? 'currentColor' : 'none'} />
          </button>
          <button className="p-2.5 text-slate-400 hover:text-slate-600 hover:bg-slate-50 rounded-xl transition-all">
            <MoreHorizontal size={20} />
          </button>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-8 space-y-10 custom-scrollbar">
        {/* AI Insight Section */}
        <section className="space-y-4">
          <h2 className="text-[11px] font-black text-blue-600 uppercase tracking-[0.2em] mb-4">Agent Intelligence</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-6 bg-blue-50/50 rounded-2xl border border-blue-100/50 relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:scale-110 transition-transform">
                <Info size={40} className="text-blue-600" />
              </div>
              <h3 className="text-xs font-bold text-blue-800 uppercase tracking-widest mb-3 flex items-center">
                Executive Summary
              </h3>
              <p className="text-sm text-slate-700 leading-relaxed font-medium">{email.summary}</p>
            </div>

            <div className="p-6 bg-green-50/50 rounded-2xl border border-green-100/50 relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:scale-110 transition-transform">
                <Calendar size={40} className="text-green-600" />
              </div>
              <h3 className="text-xs font-bold text-green-800 uppercase tracking-widest mb-3 flex items-center">
                Detected Deadline
              </h3>
              <p className={`text-base font-black ${email.deadline && email.deadline !== 'NONE' ? 'text-green-700' : 'text-slate-400'}`}>
                {email.deadline && email.deadline !== 'NONE' ? email.deadline : 'No immediate action required'}
              </p>
            </div>
          </div>

          <div className="p-6 bg-slate-50 rounded-2xl border border-slate-100 flex items-start space-x-4">
            <div className="bg-white p-2 rounded-xl shadow-sm">
              <Lightbulb size={20} className="text-yellow-500" />
            </div>
            <div>
              <h3 className="text-xs font-bold text-slate-900 uppercase tracking-widest mb-2">Relevance Score: {email.importance}/10</h3>
              <p className="text-sm text-slate-600 leading-relaxed italic">
                {email.relevance > 7 
                  ? 'This matches your priority patterns and requires your attention.' 
                  : 'Categorized as secondary communication based on historical interactions.'}
              </p>
            </div>
          </div>
        </section>

        {/* Original Content */}
        <section>
          <div className="flex items-center justify-between mb-6 border-b border-slate-100 pb-4">
            <h2 className="text-[11px] font-black text-slate-400 uppercase tracking-[0.2em]">Original Correspondence</h2>
            <span className="text-[10px] font-bold text-slate-400 bg-slate-50 px-3 py-1 rounded-full">Encrypted Content</span>
          </div>
          
          <div className="text-[13px] text-slate-600 whitespace-pre-wrap leading-relaxed font-sans bg-slate-50/30 p-8 rounded-2xl border border-dashed border-slate-200">
            {email.body}
          </div>
        </section>
      </div>
      
      <footer className="p-4 border-t border-slate-100 bg-slate-50/50 flex justify-center">
        <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Powered by Email AI Agent Neural Engine</p>
      </footer>
    </div>
  );
};

export default DetailsPanel;
