import React from 'react';
import { cn } from '@/lib/utils';
import { EmailMetadata } from '@/types';
import { Badge } from '../ui/badge';
import { Clock, Archive, Star, CheckCircle } from 'lucide-react';
interface EmailCardProps {
  email: EmailMetadata;
  isActive: boolean;
  onClick: () => void;
}

export const EmailCard: React.FC<EmailCardProps> = ({ email, isActive, onClick }) => {
  const getImportanceIndicator = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'critical': return { icon: '🚨', label: 'Critical', variant: 'destructive' as const };
      case 'high': return { icon: '🔥', label: 'High', variant: 'destructive' as const };
      case 'medium': return { icon: '⚡', label: 'Medium', variant: 'ai' as const };
      default: return { icon: '📄', label: 'Low', variant: 'secondary' as const };
    }
  };

  const importance = getImportanceIndicator(email.priority);

  return (
    <div
      onClick={onClick}
      className={cn(
        "p-4 cursor-pointer transition-all duration-300 border-b border-border flex flex-col gap-3 relative overflow-hidden group hover:scale-[1.01] hover:shadow-lg hover:z-10",
        isActive ? "bg-accent/30 shadow-md ring-1 ring-primary/30 z-10" : "hover:bg-accent/10 bg-transparent"
      )}
    >
      {isActive && <div className="absolute left-0 top-0 bottom-0 w-1 bg-primary" />}
      
      <div className="flex gap-3 items-start w-full">
        <div className="w-10 h-10 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center text-primary font-bold shrink-0 text-lg shadow-inner">
          {email.subject ? email.subject.charAt(0).toUpperCase() : '?'}
        </div>
        
        <div className="flex-1 min-w-0 flex flex-col gap-1">
          <div className="flex justify-between items-start">
            <h3 className={cn(
              "text-sm font-semibold truncate pr-2",
              isActive ? "text-primary drop-shadow-[0_0_8px_rgba(59,130,246,0.5)]" : "text-foreground"
            )}>
              {email.subject}
            </h3>
            <div className="flex items-center gap-1 text-[10px] text-muted-foreground font-medium shrink-0 pt-1">
              <Clock size={10} />
              <span>{email.time}</span>
            </div>
          </div>

          <p className="text-xs text-muted-foreground line-clamp-2 leading-relaxed pr-8">
            {email.summary}
          </p>

          <div className="flex items-center gap-2 mt-2">
            <div className="px-2 py-0.5 rounded-full bg-primary/10 text-[9px] font-bold text-primary uppercase tracking-tighter border border-primary/20">
              {email.category || 'UNKNOWN'}
            </div>
            {email.priority && (
              <Badge variant={importance.variant} className="text-[9px] uppercase tracking-tighter px-1.5 py-0">
                {importance.icon} {importance.label}
              </Badge>
            )}
            <div className="flex-1" />
            {email.relevance !== undefined && (
              <div className="flex items-center gap-1 text-[10px] font-bold text-orange-500 bg-orange-50 px-1.5 py-0.5 rounded">
                <span className="text-[10px]">🔥</span> {email.relevance}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Hover Actions */}
      <div className="absolute right-4 top-1/2 -translate-y-1/2 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-all duration-300 bg-background/90 backdrop-blur-md shadow-lg shadow-black/5 rounded-lg border border-border p-1 translate-x-2 group-hover:translate-x-0">
        <button className="p-1.5 hover:bg-accent rounded text-muted-foreground hover:text-green-500 transition-colors" title="Archive">
          <Archive size={14} />
        </button>
        <button className="p-1.5 hover:bg-accent rounded text-muted-foreground hover:text-yellow-500 transition-colors" title="Star">
          <Star size={14} />
        </button>
        <button className="p-1.5 hover:bg-accent rounded text-muted-foreground hover:text-blue-500 transition-colors" title="Mark Read">
          <CheckCircle size={14} />
        </button>
      </div>
    </div>
  );
};
