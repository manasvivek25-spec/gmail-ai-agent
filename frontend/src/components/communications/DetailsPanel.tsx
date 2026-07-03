import React from 'react';
import { 
  Star, 
  Lightbulb, 
  Share2, 
  MoreHorizontal,
  Mail,
  Zap
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { EmailDetails } from '@/types';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { Card, CardContent } from '../ui/card';
import { useState } from 'react';

interface DetailsPanelProps {
  email: EmailDetails | null;
  onToggleBookmark: () => void;
  isBookmarked: boolean;
}

export const DetailsPanel: React.FC<DetailsPanelProps> = ({ 
  email, 
  onToggleBookmark, 
  isBookmarked 
}) => {
  const [showRawEmail, setShowRawEmail] = useState(false);
  if (!email) {
    return (
      <div className="flex-1 flex items-center justify-center bg-white text-slate-400">
        <div className="text-center max-w-sm px-6">
          <div className="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-6">
            <Mail size={32} className="text-slate-300" />
          </div>
          <h2 className="text-xl font-bold text-slate-900 mb-2">Select a communication</h2>
          <p className="text-sm">Choose an email from the list to see AI insights and full conversation details.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col bg-white overflow-hidden h-screen">
      <header className="px-8 py-6 border-b border-slate-100 flex justify-between items-start bg-white sticky top-0 z-10">
        <div className="flex-1 pr-8">
          <div className="flex items-center gap-2 mb-4">
            {email.labels && email.labels.map(l => (
              <Badge key={l} variant="ai" className="px-2 py-0.5 text-[10px]">
                {l}
              </Badge>
            ))}
            <Badge variant="outline" className="px-2 py-0.5 text-[10px]">
              ID: {email.email_id ? email.email_id.substring(0, 8) : 'Unknown'}
            </Badge>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 leading-tight tracking-tight">
            {email.subject}
          </h1>
          
          <div className="flex items-center mt-6 gap-4">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 font-bold uppercase">
                {email.category ? email.category.charAt(0) : '?'}
              </div>
              <div>
                <div className="text-xs text-slate-500 font-medium">Category</div>
                <div className="text-sm font-semibold text-slate-900">{email.category || 'Unknown'}</div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon" onClick={onToggleBookmark}>
            <Star size={20} className={isBookmarked ? "text-yellow-400 fill-yellow-400" : "text-slate-400"} />
          </Button>
          <Button variant="ghost" size="icon">
            <Share2 size={20} className="text-slate-400" />
          </Button>
          <Button variant="ghost" size="icon">
            <MoreHorizontal size={20} className="text-slate-400" />
          </Button>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-8 space-y-10 custom-scrollbar pb-20">
        <section className="space-y-4">
          <div className="flex items-center gap-2">
            <Zap size={16} className="text-primary" />
            <h2 className="text-xs font-bold text-primary uppercase tracking-widest">AI BRIEF</h2>
          </div>
          
          <div className="bg-primary/5 p-6 rounded-2xl border border-primary/20">
            <p className="text-[15px] text-slate-800 leading-relaxed font-medium">
              {email.summary}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
            <Card className="bg-secondary/5 border-secondary/20 shadow-none">
              <CardContent className="p-6">
                <h3 className="text-[10px] font-bold text-secondary uppercase tracking-widest mb-3">Actionable Deadline</h3>
                <p className={cn(
                  "text-base font-bold",
                  email.deadline && email.deadline !== 'NONE' ? "text-secondary" : "text-slate-400"
                )}>
                  {email.deadline && email.deadline !== 'NONE' ? email.deadline : 'No deadline detected'}
                </p>
              </CardContent>
            </Card>

            <Card className="bg-slate-50 border-slate-100 shadow-none">
              <CardContent className="p-6 flex items-start gap-4">
                <div className="bg-white p-2 rounded-lg shadow-sm">
                  <Lightbulb size={18} className="text-yellow-500" />
                </div>
                <div>
                  <h3 className="text-[10px] font-bold text-slate-900 uppercase tracking-widest mb-2">Importance ({email.relevance}/10)</h3>
                  <p className="text-xs text-slate-600 italic leading-relaxed">
                    {email.relevance > 7 
                      ? 'Identified as high-priority based on your current project focus and interest engine.' 
                      : 'System-categorized based on typical professional correspondence patterns.'}
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        </section>

        {email.tags && email.tags.length > 0 && (
          <section>
            <h2 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-4">Neural Tags</h2>
            <div className="flex flex-wrap gap-2">
              {email.tags.map(tag => (
                <Badge key={tag} variant="secondary" className="px-3 py-1 text-[10px]">
                  {tag}
                </Badge>
              ))}
            </div>
          </section>
        )}

        <div className="flex justify-center my-8">
          <Button 
            variant="outline" 
            className="rounded-full px-6 py-2"
            onClick={() => setShowRawEmail(!showRawEmail)}
          >
            {showRawEmail ? "Hide Original Mail" : "Read Original Full Mail"}
          </Button>
        </div>

        {showRawEmail && (
          <section className="animate-in fade-in slide-in-from-bottom-4 duration-300">
            <div className="flex items-center justify-between mb-6 border-b border-slate-100 pb-4">
              <h2 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Original Correspondence</h2>
            </div>
            
            <div className="text-[13px] text-slate-600 whitespace-pre-wrap leading-relaxed font-sans bg-slate-50/50 p-8 rounded-xl border border-dashed border-slate-200">
              {email.body}
            </div>
          </section>
        )}

      </div>
      
      <footer className="px-8 py-4 border-t border-slate-100 bg-slate-50/50 flex items-center justify-between text-[10px] font-bold text-slate-400 uppercase tracking-widest">
        <span>Email AI Agent Engine v1.0</span>
        <span className="flex items-center gap-1"><Zap size={10} className="text-primary" /> Secured Encryption</span>
      </footer>
    </div>
  );
};
