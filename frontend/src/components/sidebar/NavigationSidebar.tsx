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
  Globe,
  Plus,
  Moon,
  Sun,
  LogOut
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
  onSignOut
}) => {
  const NavItem = ({ id, label, icon: Icon }: { id: string, label: string, icon: any }) => (
    <Button
      variant="ghost"
      className={cn(
        "w-full justify-start gap-3 px-3 py-2 text-muted-foreground hover:text-foreground hover:bg-accent/50 hover:scale-[1.02] active:scale-95 transition-all duration-300",
        currentView === id && "bg-accent/80 text-foreground font-semibold shadow-sm"
      )}
      onClick={() => setCurrentView(id)}
    >
      <Icon size={18} className={cn(currentView === id ? "text-primary drop-shadow-[0_0_8px_rgba(59,130,246,0.5)]" : "text-muted-foreground")} />
      <span>{label}</span>
    </Button>
  );

  return (
    <div className="w-[280px] h-screen bg-background/60 backdrop-blur-2xl border-r border-border flex flex-col p-4 shadow-[4px_0_24px_-12px_rgba(0,0,0,0.1)] z-20 transition-colors duration-300">
      <div className="flex items-center justify-between px-3 pt-4 pb-2">
        <div className="flex items-center gap-3">
          <div className="bg-gradient-to-br from-blue-500 to-indigo-600 p-2 rounded-xl shadow-lg shadow-blue-500/20">
            <Mail className="text-white" size={20} />
          </div>
          <h1 className="font-bold text-foreground tracking-tight text-lg">Mail Agent</h1>
        </div>
        <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-foreground rounded-full" onClick={toggleTheme}>
          {isDark ? <Sun size={18} /> : <Moon size={18} />}
        </Button>
      </div>
      
      {/* Multi-Channel Switcher UI (Phase 6) */}
      <div className="px-3 pb-6 flex gap-1 overflow-x-auto custom-scrollbar">
        <button className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md bg-blue-100 text-blue-700 text-[10px] font-bold uppercase tracking-wider shrink-0 transition-colors">
          <Mail size={12} /> Gmail
        </button>
        <button className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-slate-400 hover:bg-slate-200 text-[10px] font-bold uppercase tracking-wider shrink-0 transition-colors cursor-not-allowed opacity-50" title="Coming Soon">
          <Mail size={12} /> Outlook
        </button>
        <button className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-slate-400 hover:bg-slate-200 text-[10px] font-bold uppercase tracking-wider shrink-0 transition-colors cursor-not-allowed opacity-50" title="Coming Soon">
          <MessageCircle size={12} /> WhatsApp
        </button>
        <button className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-slate-400 hover:bg-slate-200 text-[10px] font-bold uppercase tracking-wider shrink-0 transition-colors cursor-not-allowed opacity-50" title="Coming Soon">
          <Smartphone size={12} /> Telegram
        </button>
      </div>

      <div className="flex-1 overflow-y-auto space-y-6 custom-scrollbar pr-1">
        <div className="space-y-1">
          <NavItem id="inbox" label="Inbox" icon={Inbox} />
          <NavItem id="analytics" label="Analytics" icon={BarChart2} />
          <NavItem id="assistant" label="AI Assistant" icon={MessageSquare} />
        </div>

        <div>
          <h2 className="px-3 text-[11px] font-bold text-muted-foreground uppercase tracking-widest mb-2">Smart Categories</h2>
          <div className="space-y-1">
            <NavItem id="recommended" label="Recommended" icon={Flame} />
            <NavItem id="deadlines" label="Deadlines" icon={Calendar} />
            {Object.entries(categories).map(([name, count]) => (
              <Button
                key={name}
                variant="ghost"
                className={cn(
                  "w-full justify-between px-3 py-2 text-muted-foreground hover:text-foreground hover:bg-accent/50 hover:scale-[1.02] active:scale-95 transition-all duration-300 text-sm",
                  currentView === `category:${name}` && "bg-accent/80 text-foreground font-semibold shadow-sm"
                )}
                onClick={() => setCurrentView(`category:${name}`)}
              >
                <span className="truncate">{name}</span>
                <Badge variant="secondary" className="font-medium text-[10px] px-1.5 py-0 bg-background/50">
                  {count}
                </Badge>
              </Button>
            ))}
          </div>
        </div>

        {labels.length > 0 && (
          <div>
            <h2 className="px-3 text-[11px] font-bold text-muted-foreground uppercase tracking-widest mb-2">Labels</h2>
            <div className="space-y-1">
              {labels.map((label) => (
                <Button
                  key={label}
                  variant="ghost"
                  className={cn(
                    "w-full justify-start gap-3 px-3 py-2 text-muted-foreground hover:text-foreground hover:bg-accent/50 hover:scale-[1.02] active:scale-95 transition-all duration-300 text-sm",
                    currentView === `label:${label}` && "bg-accent/80 text-foreground font-semibold shadow-sm"
                  )}
                  onClick={() => setCurrentView(`label:${label}`)}
                >
                  <Tag size={16} className={currentView === `label:${label}` ? "text-primary" : "text-muted-foreground"} />
                  <span className="truncate">{label}</span>
                </Button>
              ))}
            </div>
          </div>
        )}
        
        {/* Actions Section */}
        <div>
          <h2 className="px-3 text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-2 mt-4">Actions</h2>
          <div className="space-y-1">
            <Button
              variant="ghost"
              className="w-full justify-start gap-3 px-3 py-2 text-slate-600 hover:text-blue-600 hover:bg-blue-50 text-sm font-medium"
              onClick={async () => {
                const name = window.prompt("Enter new label name:");
                if (name) {
                  await fetch("http://localhost:8000/api/labels/create", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ name })
                  });
                  onSync(); // Refresh data
                }
              }}
            >
              <Plus size={16} />
              <span>Create Label</span>
            </Button>
            <Button
              variant="ghost"
              className="w-full justify-start gap-3 px-3 py-2 text-slate-600 hover:text-blue-600 hover:bg-blue-50 text-sm font-medium"
              onClick={async () => {
                const label = window.prompt("Enter existing label to assign rule to:");
                if (!label) return;
                const keyword = window.prompt(`Enter keyword to route to '${label}':`);
                if (keyword) {
                  await fetch("http://localhost:8000/api/rules/create", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ label, keyword })
                  });
                  onSync(); // Refresh data
                }
              }}
            >
              <Plus size={16} />
              <span>Create Rule</span>
            </Button>
          </div>
        </div>
      </div>

      <div className="mt-auto pt-4 border-t border-slate-200 space-y-2">
        <Button 
          variant="outline" 
          className="w-full justify-center gap-2 text-slate-600 bg-white"
          onClick={onSync}
          disabled={isSyncing}
        >
          <RefreshCw size={16} className={cn(isSyncing && "animate-spin")} />
          <span>{isSyncing ? "Syncing AI..." : "Sync Agent"}</span>
        </Button>
        {onSignOut && (
          <Button 
            variant="ghost" 
            className="w-full justify-center gap-2 text-red-500 hover:text-red-600 hover:bg-red-50"
            onClick={onSignOut}
          >
            <LogOut size={16} />
            <span>Sign Out</span>
          </Button>
        )}
      </div>
    </div>
  );
};
