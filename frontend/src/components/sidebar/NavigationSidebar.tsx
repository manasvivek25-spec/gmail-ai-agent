import React from 'react';
import { 
  Inbox, 
  Flame, 
  Calendar, 
  BarChart2, 
  MessageSquare, 
  Tag, 
  RefreshCw,
  Mail,
  Smartphone,
  MessageCircle,
  Plus,
  Moon,
  Sun,
  LogOut,
  Send,
  Star,
  Archive,
  Trash2,
  Edit3,
  Settings
} from 'lucide-react';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { cn } from '@/lib/utils';
import { CategoryCounts } from '@/types';

interface SidebarProps {
  currentView: string;
  setCurrentView: (view: string) => void;
  categories: CategoryCounts;
  labels: string[];
  onSync: () => void;
  isSyncing: boolean;
  isDark: boolean;
  toggleTheme: () => void;
  onSignOut?: () => void;
  userProfile?: {name: string, email: string} | null;
}

export const NavigationSidebar: React.FC<SidebarProps> = ({ 
  currentView, 
  setCurrentView, 
  categories, 
  labels,
  onSync,
  isSyncing,
  isDark,
  toggleTheme,
  onSignOut,
  userProfile
}) => {
  const NavItem = ({ id, label, icon: Icon, badge }: { id: string, label: string, icon: any, badge?: number }) => (
    <Button
      variant="ghost"
      className={cn(
        "w-full justify-between px-4 py-2.5 hover-float rounded-xl transition-all duration-300 text-sm",
        currentView === id 
          ? "bg-[#0EA5E9] text-white font-semibold shadow-lg shadow-sky-500/30" 
          : "text-slate-400 hover:text-slate-200 hover:bg-white/5"
      )}
      onClick={() => setCurrentView(id)}
    >
      <div className="flex items-center gap-3">
        <Icon size={18} className={currentView === id ? "text-white" : "text-slate-400"} />
        <span>{label}</span>
      </div>
      {badge !== undefined && badge > 0 && (
        <Badge className={cn(
          "font-bold text-[10px] px-1.5 py-0 h-4 min-w-[16px] flex items-center justify-center rounded-full",
          currentView === id ? "bg-white text-[#0EA5E9]" : "bg-white/10 text-slate-300"
        )}>
          {badge}
        </Badge>
      )}
    </Button>
  );

  const getLabelColor = (index: number) => {
    const colors = ['bg-blue-500', 'bg-green-500', 'bg-orange-500', 'bg-purple-500', 'bg-pink-500'];
    return colors[index % colors.length];
  };

  return (
    <div className="w-[280px] h-screen bg-[#0B1120] border-r border-[#1e293b] flex flex-col p-4 shadow-2xl z-20 transition-colors duration-300">
      <div className="flex items-center justify-between px-2 pt-2 pb-6">
        <div className="flex items-center gap-3">
          <div className="bg-[#0EA5E9] p-2 rounded-full shadow-lg shadow-sky-500/20">
            <Mail className="text-white" size={20} />
          </div>
          <div>
            <h1 className="font-bold text-white tracking-tight text-lg leading-tight">Mail Agent</h1>
            <p className="text-[9px] text-slate-400 font-medium tracking-widest uppercase">AI-Powered Inbox</p>
          </div>
        </div>
      </div>
      
      {/* New Email Button */}
      <div className="px-2 mb-6">
        <Button className="w-full justify-center gap-2 bg-[#0EA5E9] hover:bg-[#0284C7] text-white rounded-xl py-6 font-semibold shadow-lg shadow-sky-500/20 hover-float">
          <Edit3 size={18} />
          New Email
        </Button>
      </div>

      <div className="flex-1 overflow-y-auto space-y-6 sidebar-scrollbar pr-2">
        <div className="space-y-1">
          <NavItem id="inbox" label="Inbox" icon={Inbox} badge={12} />
          <NavItem id="sent" label="Sent" icon={Send} />
          <NavItem id="starred" label="Starred" icon={Star} badge={3} />
          <NavItem id="archive" label="Archive" icon={Archive} />
          <NavItem id="trash" label="Trash" icon={Trash2} />
        </div>

        <div>
          <h2 className="px-4 text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-3">AI Tools</h2>
          <div className="space-y-1">
            <NavItem id="assistant" label="AI Compose" icon={MessageSquare} />
            <NavItem id="analytics" label="Analytics" icon={BarChart2} />
            <NavItem id="recommended" label="Automation" icon={Flame} />
          </div>
        </div>

        <div>
          <h2 className="px-4 text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-3">Labels</h2>
          <div className="space-y-1">
            {labels.length > 0 ? labels.map((label, index) => (
              <Button
                key={label}
                variant="ghost"
                className={cn(
                  "w-full justify-start gap-3 px-4 py-2 hover-float rounded-xl transition-all duration-300 text-sm",
                  currentView === `label:${label}` 
                    ? "bg-[#0EA5E9] text-white font-semibold shadow-lg shadow-sky-500/30" 
                    : "text-slate-400 hover:text-slate-200 hover:bg-white/5"
                )}
                onClick={() => setCurrentView(`label:${label}`)}
              >
                <div className={`w-2 h-2 rounded-full ${getLabelColor(index)}`}></div>
                <span className="truncate">{label}</span>
              </Button>
            )) : (
              <Button
                variant="ghost"
                className="w-full justify-start gap-3 px-4 py-2 hover-float rounded-xl transition-all duration-300 text-sm text-slate-400 hover:text-slate-200 hover:bg-white/5"
                onClick={async () => {
                  const name = window.prompt("Enter new label name:");
                  if (name) {
                    await fetch("http://localhost:8000/api/labels/create", {
                      method: "POST",
                      headers: { "Content-Type": "application/json" },
                      body: JSON.stringify({ name })
                    });
                    onSync();
                  }
                }}
              >
                <Plus size={16} />
                <span>Create Label</span>
              </Button>
            )}
            
            <NavItem id="deadlines" label="Deadlines" icon={Calendar} />
          </div>
        </div>
      </div>

      <div className="mt-4 pt-4 border-t border-[#1e293b] flex items-center justify-between px-2">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-[#0EA5E9] flex items-center justify-center text-white font-bold text-sm shadow-inner">
            {userProfile ? userProfile.name.split(' ').map((n: string) => n[0]).join('').substring(0, 2).toUpperCase() : 'U'}
          </div>
          <div className="flex flex-col">
            <span className="text-white text-sm font-semibold leading-tight truncate max-w-[130px]">{userProfile ? userProfile.name : 'User'}</span>
            <span className="text-slate-400 text-[10px] truncate max-w-[130px]">{userProfile ? userProfile.email : 'Loading...'}</span>
          </div>
        </div>
        {onSignOut && (
          <Button 
            variant="ghost" 
            size="icon"
            className="text-slate-400 hover:text-white hover:bg-white/10 rounded-full hover-float"
            onClick={onSignOut}
          >
            <Settings size={16} />
          </Button>
        )}
      </div>
    </div>
  );
};
