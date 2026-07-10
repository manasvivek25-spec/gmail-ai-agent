import React from 'react';

import { Calendar, Clock, AlertCircle } from 'lucide-react';
import { Badge } from '../ui/badge';

interface DeadlineTrackerProps {
  emails: any[];
  onSelect: (id: string) => void;
  selectedId: string | null;
}

export const DeadlineTracker: React.FC<DeadlineTrackerProps> = ({ emails, onSelect, selectedId }) => {
  const organizeDeadlines = () => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const groups: Record<string, any[]> = {
      'Today': [],
      'Tomorrow': [],
      'This Week': [],
      'Later': []
    };

    emails.forEach(email => {
      if (!email.deadline || email.deadline === 'NONE') return;
      
      const deadline = new Date(email.deadline);
      const diffTime = deadline.getTime() - today.getTime();
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

      if (diffDays === 0) groups['Today'].push(email);
      else if (diffDays === 1) groups['Tomorrow'].push(email);
      else if (diffDays > 1 && diffDays <= 7) groups['This Week'].push(email);
      else if (diffDays > 7) groups['Later'].push(email);
    });

    Object.values(groups).forEach(items => {
      items.sort((a, b) => new Date(a.deadline).getTime() - new Date(b.deadline).getTime());
    });

    return groups;
  };

  const groups = organizeDeadlines();

  return (
    <div className="flex-1 overflow-y-auto custom-scrollbar p-6 space-y-10 bg-white">
      {Object.entries(groups).map(([title, items]) => (
        items.length > 0 && (
          <section key={title} className="space-y-4">
            <div className="flex items-center gap-3 border-b border-slate-100 pb-3">
              <h2 className="text-sm font-black text-slate-900 uppercase tracking-widest">{title}</h2>
              <Badge variant="secondary" className="bg-slate-50 text-slate-400 border-none">
                {items.length} Actions
              </Badge>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {items.map(email => (
                <div 
                  key={email.email_id}
                  onClick={() => onSelect(email.email_id)}
                  className={`p-6 rounded-2xl border transition-all cursor-pointer relative group ${
                    selectedId === email.email_id 
                      ? 'border-primary/20 bg-primary/5 shadow-md ring-1 ring-primary/10' 
                      : 'border-slate-100 bg-white hover:border-primary/20 hover:shadow-sm'
                  }`}
                >
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex items-center gap-2">
                      <div className="bg-orange-100 text-orange-600 p-1.5 rounded-lg">
                        <Calendar size={14} />
                      </div>
                      <span className="text-[10px] font-black text-orange-600 uppercase tracking-widest">
                        Due {email.deadline}
                      </span>
                    </div>
                    {email.priority === 'Critical' && (
                      <AlertCircle size={14} className="text-red-500" />
                    )}
                  </div>
                  
                  <h3 className="text-sm font-bold text-slate-900 mb-2 line-clamp-1 group-hover:text-primary transition-colors">
                    {email.subject}
                  </h3>
                  <p className="text-xs text-slate-500 line-clamp-2 leading-relaxed mb-4">
                    {email.summary}
                  </p>
                  
                  <div className="flex items-center justify-between pt-4 border-t border-slate-50">
                    <div className="flex items-center gap-1.5">
                      <Clock size={12} className="text-slate-300" />
                      <span className="text-[10px] text-slate-400 font-bold uppercase tracking-tighter">
                        {email.time}
                      </span>
                    </div>
                    <Badge variant="outline" className="text-[9px] font-bold uppercase border-slate-200 text-slate-400">
                      {email.category}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )
      ))}
      {emails.length === 0 && (
        <div className="h-full flex flex-col items-center justify-center py-20">
          <div className="w-16 h-16 bg-slate-50 rounded-3xl flex items-center justify-center mb-6">
            <Calendar size={32} className="text-slate-200" />
          </div>
          <h3 className="text-lg font-bold text-slate-900">No active deadlines</h3>
          <p className="text-sm text-slate-400 mt-1 text-center max-w-xs">Your AI agent has not detected any immediate actionable deadlines in your inbox.</p>
        </div>
      )}
    </div>
  );
};
