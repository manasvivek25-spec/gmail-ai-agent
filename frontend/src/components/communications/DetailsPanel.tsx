import React from 'react';
import { 
  Star, 
  Lightbulb, 
  Share2, 
  MoreHorizontal,
  Mail,
  Zap,
  Calendar,
  Loader2
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { EmailDetails } from '@/types';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { Card, CardContent } from '../ui/card';
import { useState, useEffect } from 'react';
import { api } from '@/services/api';

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
  const [rawEmailData, setRawEmailData] = useState<any>(null);
  const [isLoadingRaw, setIsLoadingRaw] = useState(false);

  useEffect(() => {
    if (showRawEmail && !rawEmailData && email?.email_id) {
      setIsLoadingRaw(true);
      api.getRawEmail(email.email_id)
        .then(res => setRawEmailData(res.data))
        .catch(err => console.error(err))
        .finally(() => setIsLoadingRaw(false));
    }
  }, [showRawEmail, email, rawEmailData]);
  if (!email) {
    return (
      <div className="flex-1 flex items-center justify-center bg-white text-slate-500 transition-colors duration-300 relative">
        <div className="text-center max-w-sm px-6 flex flex-col items-center">
          <div className="relative">
            <div className="w-24 h-24 bg-blue-50 rounded-[28px] flex items-center justify-center mx-auto mb-6 shadow-sm border border-blue-100/50 hover-float">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#0EA5E9" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/><line x1="8" y1="16" x2="8" y2="16"/><line x1="16" y1="16" x2="16" y2="16"/></svg>
            </div>
            <div className="absolute -top-2 -right-2 bg-green-500 rounded-full p-1 border-2 border-white shadow-sm animate-pulse">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><path d="m5 12 5 5L20 7"/></svg>
            </div>
          </div>
          <h2 className="text-[22px] font-bold text-slate-800 mb-2 tracking-tight">Select an email to read</h2>
          <p className="text-[13px] text-slate-500 mb-8">Mail Agent will surface AI insights automatically</p>
          
          <button className="flex items-center gap-2 px-4 py-2 bg-blue-50/50 text-[#0EA5E9] rounded-full border border-blue-100 text-[12px] font-semibold hover:bg-blue-50 transition-colors shadow-sm">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
            2 emails need your attention today
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col bg-card overflow-hidden h-screen transition-colors duration-300">
      <header className="px-8 py-6 border-b border-border flex justify-between items-start bg-card/80 backdrop-blur-md sticky top-0 z-10 transition-colors duration-300">
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
          <h1 className="text-2xl font-bold text-foreground leading-tight tracking-tight">
            {email.subject}
          </h1>
          
          <div className="flex items-center mt-6 gap-4">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-full bg-accent flex items-center justify-center text-muted-foreground font-bold uppercase shadow-inner">
                {email.category ? email.category.charAt(0) : '?'}
              </div>
              <div>
                <div className="text-xs text-muted-foreground font-medium">Category</div>
                <div className="text-sm font-semibold text-foreground">{email.category || 'Unknown'}</div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon" onClick={onToggleBookmark}>
            <Star size={20} className={isBookmarked ? "text-yellow-400 fill-yellow-400" : "text-muted-foreground"} />
          </Button>
          <Button variant="ghost" size="icon">
            <Share2 size={20} className="text-muted-foreground hover:text-foreground" />
          </Button>
          <Button variant="ghost" size="icon">
            <MoreHorizontal size={20} className="text-muted-foreground hover:text-foreground" />
          </Button>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-8 space-y-10 custom-scrollbar pb-20">
        <section className="space-y-4">
          <div className="flex items-center gap-2">
            <Zap size={16} className="text-primary" />
            <h2 className="text-xs font-bold text-primary uppercase tracking-widest">AI BRIEF</h2>
          </div>
          
          <div className="bg-gradient-to-br from-primary/10 to-primary/5 p-6 rounded-2xl border border-primary/20 shadow-sm relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-primary/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
            <p className="text-[15px] text-foreground leading-relaxed font-medium relative z-10">
              {email.summary}
            </p>
            <div className="relative z-10 mt-6 pt-5 border-t border-primary/10">
              <div className="flex items-center gap-2 mb-2">
                <Calendar size={14} className="text-red-500" />
                <h3 className="text-[10px] font-bold text-red-500 uppercase tracking-widest">Actionable Deadline</h3>
              </div>
              <p className={cn(
                "text-[15px] font-bold",
                (!email.deadline || email.deadline === 'NONE') ? "text-muted-foreground" : "text-foreground"
              )}>
                {(!email.deadline || email.deadline === 'NONE') ? "NIL" : email.deadline}
              </p>
            </div>
          </div>

          <div className="mt-6">
            <Card className="bg-accent/50 border-border shadow-sm hover:shadow-md transition-shadow">
              <CardContent className="p-6 flex items-start gap-4">
                <div className="bg-card p-2 rounded-lg shadow-sm border border-border">
                  <Lightbulb size={18} className="text-yellow-500 drop-shadow-[0_0_8px_rgba(234,179,8,0.5)]" />
                </div>
                <div>
                  <h3 className="text-[10px] font-bold text-foreground uppercase tracking-widest mb-2">Importance ({email.relevance}/10)</h3>
                  <p className="text-xs text-muted-foreground italic leading-relaxed">
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
            <h2 className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-4">Neural Tags</h2>
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
            <div className="flex items-center justify-between mb-6 border-b border-border pb-4">
              <h2 className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">Original Gmail Correspondence</h2>
            </div>
            
            {isLoadingRaw ? (
              <div className="flex items-center justify-center p-12 text-muted-foreground">
                <Loader2 className="w-8 h-8 animate-spin" />
              </div>
            ) : rawEmailData ? (
              <div className="bg-white text-black p-8 rounded-xl border border-slate-200 shadow-sm font-sans">
                {/* Authentic Gmail Header */}
                <div className="flex items-start justify-between mb-8 pb-6 border-b border-slate-100">
                  <div className="flex gap-4">
                    <div className="w-12 h-12 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold text-xl uppercase shadow-md">
                      {rawEmailData.sender ? rawEmailData.sender.charAt(0).replace(/[^A-Za-z]/, 'A') : '?'}
                    </div>
                    <div>
                      <div className="font-semibold text-base mb-1 text-slate-800">
                        {rawEmailData.sender}
                      </div>
                      <div className="text-xs text-slate-500 flex items-center gap-1">
                        <span>to {rawEmailData.recipient || 'me'}</span>
                        <span className="text-slate-300 mx-1">•</span>
                        <span>{rawEmailData.date || 'Unknown date'}</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Email Body */}
                <div 
                  className="text-sm leading-relaxed max-w-none prose prose-sm prose-slate"
                  dangerouslySetInnerHTML={{ __html: rawEmailData.html }}
                />
              </div>
            ) : (
              <div className="text-[13px] text-muted-foreground whitespace-pre-wrap leading-relaxed font-sans bg-accent/30 p-8 rounded-xl border border-dashed border-border shadow-inner">
                {email.body}
              </div>
            )}
          </section>
        )}

      </div>
      
      <footer className="px-8 py-4 border-t border-border bg-accent/30 flex items-center justify-between text-[10px] font-bold text-muted-foreground uppercase tracking-widest backdrop-blur-sm transition-colors duration-300">
        <span>Email AI Agent Engine v1.0</span>
        <span className="flex items-center gap-1"><Zap size={10} className="text-primary" /> Secured Encryption</span>
      </footer>
    </div>
  );
};
