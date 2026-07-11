import React from 'react';
import { cn } from '@/lib/utils';
import { EmailMetadata } from '@/types';
import { Badge } from '../ui/badge';
import { Clock, Archive, Star, CheckCircle, Paperclip } from 'lucide-react';

interface EmailCardProps {
  email: EmailMetadata;
  isActive: boolean;
  onClick: () => void;
}

export const EmailCard: React.FC<EmailCardProps> = ({ email, isActive, onClick }) => {
  const getInitials = (subject: string, sender: string) => {
    // Attempt to extract initials from sender if available, else subject
    const text = sender || subject || '?';
    const words = text.trim().split(/\s+/);
    if (words.length >= 2) {
      return (words[0][0] + words[1][0]).toUpperCase();
    }
    return text.substring(0, 2).toUpperCase();
  };

  const getAvatarColor = (initials: string) => {
    const colors = [
      'bg-orange-500', 
      'bg-green-600', 
      'bg-blue-500', 
      'bg-pink-500', 
      'bg-purple-500',
      'bg-teal-500'
    ];
    let sum = 0;
    for (let i = 0; i < initials.length; i++) {
      sum += initials.charCodeAt(i);
    }
    return colors[sum % colors.length];
  };

  const getImportanceIndicator = (priority: string) => {
    switch (priority?.toLowerCase()) {
      case 'critical': return { icon: '🚨', label: 'Critical', variant: 'destructive' as const };
      case 'high': return { icon: '🔥', label: 'High', variant: 'destructive' as const };
      case 'medium': return { icon: '⚡', label: 'Medium', variant: 'ai' as const };
      default: return null;
    }
  };

  const importance = getImportanceIndicator(email.priority);
  const initials = getInitials(email.subject, email.sender || '');
  const avatarColor = getAvatarColor(initials);

  return (
    <div
      onClick={onClick}
      className={cn(
        "p-4 cursor-pointer bg-white border-b border-slate-100 flex flex-col gap-3 relative group hover-float rounded-xl mx-2 my-1",
        isActive ? "shadow-md ring-1 ring-[#0EA5E9]/20 z-10" : "hover:bg-slate-50"
      )}
    >
      {isActive && <div className="absolute left-0 top-1/2 -translate-y-1/2 h-8 w-1 bg-[#0EA5E9] rounded-r-md" />}
      
      <div className="flex gap-4 items-start w-full">
        <div className={cn("w-10 h-10 rounded-full flex items-center justify-center text-white font-bold shrink-0 text-sm shadow-sm", avatarColor)}>
          {initials}
        </div>
        
        <div className="flex-1 min-w-0 flex flex-col gap-1 mt-0.5">
          <div className="flex justify-between items-start">
            <h3 className={cn(
              "text-[13px] font-semibold truncate pr-2",
              isActive ? "text-[#0EA5E9]" : "text-slate-800"
            )}>
              {email.subject || '(No Subject)'}
            </h3>
            <div className="flex items-center gap-1 text-[10px] text-slate-400 font-medium shrink-0">
              {email.time}
            </div>
          </div>

          <p className="text-[12px] text-slate-500 line-clamp-2 leading-relaxed pr-8">
            {email.summary || 'No content preview available.'}
          </p>

          <div className="flex items-center gap-2 mt-2">
            {email.category && (
              <div className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-blue-50/50 text-[10px] font-semibold text-[#0EA5E9] border border-blue-100/50">
                {email.category}
                <Paperclip size={10} className="ml-0.5" />
              </div>
            )}
            
            {importance && (
              <Badge variant={importance.variant} className="text-[9px] uppercase tracking-tighter px-1.5 py-0 shadow-sm">
                {importance.icon} {importance.label}
              </Badge>
            )}
            
            <div className="flex-1" />
            
            {email.is_starred && (
              <Star size={12} className="text-yellow-400 fill-yellow-400" />
            )}
            
            {email.relevance !== undefined && (
              <div className="flex items-center gap-1 text-[10px] font-bold text-orange-500 bg-orange-50 px-1.5 py-0.5 rounded shadow-sm">
                <span className="text-[10px]">🔥</span> {email.relevance}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Hover Actions */}
      <div className="absolute right-4 top-1/2 -translate-y-1/2 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-all duration-300 bg-white/90 backdrop-blur-md shadow-lg rounded-lg border border-slate-200 p-1 translate-x-2 group-hover:translate-x-0">
        <button className="p-1.5 hover:bg-slate-100 rounded text-slate-400 hover:text-green-500 transition-colors" title="Archive">
          <Archive size={14} />
        </button>
        <button className="p-1.5 hover:bg-slate-100 rounded text-slate-400 hover:text-yellow-500 transition-colors" title="Star">
          <Star size={14} />
        </button>
        <button className="p-1.5 hover:bg-slate-100 rounded text-slate-400 hover:text-blue-500 transition-colors" title="Mark Read">
          <CheckCircle size={14} />
        </button>
      </div>
    </div>
  );
};
