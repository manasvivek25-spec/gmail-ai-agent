import React from 'react';
import { 
  Star, 
  Lightbulb, 
  Share2, 
  MoreHorizontal,
  Mail,
  Zap,
  Calendar
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
      <div className="flex-1 flex items-center justify-center bg-card text-muted-foreground transition-colors duration-300">
        <div className="text-center max-w-sm px-6">
          <div className="w-24 h-24 bg-accent rounded-full flex items-center justify-center mx-auto mb-6 shadow-inner relative group">
            <div className="absolute inset-0 rounded-full bg-primary/20 scale-0 group-hover:scale-150 transition-transform duration-700 ease-out opacity-0 group-hover:opacity-100" />
            <Mail size={36} className="text-primary relative z-10 drop-shadow-sm" />
          </div>
          <h2 className="text-xl font-bold text-foreground mb-2 tracking-tight">Select a communication</h2>
          <p className="text-sm">Choose an email from the list to see AI insights and full conversation details.</p>
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
            
            {email.deadline && email.deadline !== 'NONE' && (
              <div className="relative z-10 mt-6 pt-5 border-t border-primary/10">
                <div className="flex items-center gap-2 mb-2">
                  <Calendar size={14} className="text-red-500" />
                  <h3 className="text-[10px] font-bold text-red-500 uppercase tracking-widest">Actionable Deadline</h3>
                </div>
                <p className="text-[15px] font-bold text-foreground">
                  {email.deadline}
                </p>
              </div>
            )}
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
              <h2 className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">Original Correspondence</h2>
            </div>
            
            <div className="text-[13px] text-muted-foreground whitespace-pre-wrap leading-relaxed font-sans bg-accent/30 p-8 rounded-xl border border-dashed border-border shadow-inner">
              {email.body}
            </div>
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
