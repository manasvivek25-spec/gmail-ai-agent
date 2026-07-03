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
        "p-4 cursor-pointer transition-all border-b border-slate-100 flex flex-col gap-3 relative overflow-hidden group",
        isActive ? "bg-primary/5 shadow-sm ring-1 ring-primary/20 z-10" : "hover:bg-slate-50/80 bg-white"
      )}
    >
      {isActive && <div className="absolute left-0 top-0 bottom-0 w-1 bg-primary" />}
      
      <div className="flex gap-3 items-start w-full">
        <div className="w-10 h-10 rounded-full bg-blue-50 border border-blue-100 flex items-center justify-center text-blue-600 font-bold shrink-0 text-lg shadow-sm">
          {email.subject ? email.subject.charAt(0).toUpperCase() : '?'}
        </div>
        
        <div className="flex-1 min-w-0 flex flex-col gap-1">
          <div className="flex justify-between items-start">
            <h3 className={cn(
              "text-sm font-semibold truncate pr-2",
              isActive ? "text-primary" : "text-slate-900"
            )}>
              {email.subject}
            </h3>
            <div className="flex items-center gap-1 text-[10px] text-slate-400 font-medium shrink-0 pt-1">
              <Clock size={10} />
              <span>{email.time}</span>
            </div>
          </div>

          <p className="text-xs text-slate-500 line-clamp-2 leading-relaxed pr-8">
            {email.summary}
          </p>

          <div className="flex items-center gap-2 mt-2">
            <div className="px-2 py-0.5 rounded-full bg-blue-50 text-[9px] font-bold text-blue-700 uppercase tracking-tighter">
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
      <div className="absolute right-4 top-1/2 -translate-y-1/2 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity bg-white/90 backdrop-blur shadow-sm rounded-lg border border-slate-200 p-1">
        <button className="p-1.5 hover:bg-slate-100 rounded text-slate-500 hover:text-green-600 transition-colors" title="Archive">
          <Archive size={14} />
        </button>
        <button className="p-1.5 hover:bg-slate-100 rounded text-slate-500 hover:text-yellow-500 transition-colors" title="Star">
          <Star size={14} />
        </button>
        <button className="p-1.5 hover:bg-slate-100 rounded text-slate-500 hover:text-blue-600 transition-colors" title="Mark Read">
          <CheckCircle size={14} />
        </button>
      </div>
    </div>
  );
};
