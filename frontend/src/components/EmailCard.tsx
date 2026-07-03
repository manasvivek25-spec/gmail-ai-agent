
import React from 'react';
import { AlertCircle, Zap, FileText, Star, Clock } from 'lucide-react';

interface EmailMetadata {
  email_id: string;
  subject: string;
  summary: string;
  time: string;
  relevance: number;
  importance: number;
  is_starred: boolean;
  category: string;
  priority: string;
}

interface EmailCardProps {
  email: EmailMetadata;
  isActive: boolean;
  onClick: () => void;
}

const EmailCard: React.FC<EmailCardProps> = ({ email, isActive, onClick }) => {
  const getPriorityInfo = () => {
    switch (email.priority.toLowerCase()) {
      case 'critical': return { icon: <AlertCircle size={14} />, color: 'text-red-600', bg: 'bg-red-50' };
      case 'high': return { icon: <Zap size={14} />, color: 'text-orange-600', bg: 'bg-orange-50' };
      case 'medium': return { icon: <Zap size={14} />, color: 'text-yellow-600', bg: 'bg-yellow-50' };
      default: return { icon: <FileText size={14} />, color: 'text-blue-600', bg: 'bg-blue-50' };
    }
  };

  const priority = getPriorityInfo();

  return (
    <div
      onClick={onClick}
      className={`p-5 cursor-pointer transition-all duration-200 border-b border-slate-100 relative ${
        isActive 
          ? 'bg-white shadow-md z-10 scale-[1.02] rounded-xl mx-2 my-1 border-blue-100' 
          : 'bg-transparent hover:bg-slate-50/80'
      }`}
    >
      {isActive && <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-blue-600 rounded-r-full" />}
      
      <div className="flex justify-between items-start mb-3">
        <div className="flex items-center space-x-2">
          <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider bg-slate-100 text-slate-600`}>
            {email.category || 'Direct'}
          </span>
          <div className={`flex items-center space-x-1 px-2 py-0.5 rounded-full ${priority.bg} ${priority.color}`}>
            {priority.icon}
            <span className="text-[10px] font-black uppercase tracking-tighter">{email.priority}</span>
          </div>
        </div>
        <div className="flex items-center text-slate-400 space-x-1">
          <Clock size={10} />
          <span className="text-[10px] font-medium">{email.time}</span>
        </div>
      </div>
      
      <h3 className={`text-sm font-bold mb-1.5 line-clamp-1 ${isActive ? 'text-slate-900' : 'text-slate-700'}`}>
        {email.subject}
      </h3>
      
      <p className="text-xs text-slate-500 line-clamp-2 leading-relaxed mb-3">
        {email.summary}
      </p>
      
      <div className="flex items-center justify-between mt-auto">
        <div className="flex -space-x-1">
          {/* Avatar placeholders for professional look */}
          <div className="w-5 h-5 rounded-full bg-blue-100 border border-white flex items-center justify-center text-[8px] font-bold text-blue-600">AI</div>
          <div className="w-5 h-5 rounded-full bg-green-100 border border-white flex items-center justify-center text-[8px] font-bold text-green-600">S</div>
        </div>
        
        {email.is_starred && <Star size={14} className="text-yellow-400 fill-yellow-400" />}
      </div>
    </div>
  );
};

export default EmailCard;
