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
  Plus
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
}

export const NavigationSidebar: React.FC<SidebarProps> = ({ 
  currentView, 
  setCurrentView, 
  categories, 
  labels,
  onSync,
  isSyncing
}) => {
  const NavItem = ({ id, label, icon: Icon }: { id: string, label: string, icon: any }) => (
    <Button
      variant="ghost"
      className={cn(
        "w-full justify-start gap-3 px-3 py-2 text-slate-600 hover:text-slate-900",
        currentView === id && "bg-slate-100 text-slate-900 font-semibold"
      )}
      onClick={() => setCurrentView(id)}
    >
      <Icon size={18} className={cn(currentView === id ? "text-blue-600" : "text-slate-400")} />
      <span>{label}</span>
    </Button>
  );

  return (
    <div className="w-[280px] h-screen bg-slate-50 border-r border-slate-200 flex flex-col p-4">
      <div className="flex items-center gap-3 px-3 pt-4 pb-2">
        <div className="bg-blue-600 p-2 rounded-lg shadow-sm">
          <Globe className="text-white" size={20} />
        </div>
        <h1 className="font-bold text-slate-900 tracking-tight text-lg">Omni Agent</h1>
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
          <NavItem id="recommended" label="Recommended" icon={Flame} />
          <NavItem id="deadlines" label="Deadlines" icon={Calendar} />
          <NavItem id="analytics" label="Analytics" icon={BarChart2} />
          <NavItem id="assistant" label="AI Assistant" icon={MessageSquare} />
        </div>

        <div>
          <h2 className="px-3 text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-2">Smart Categories</h2>
          <div className="space-y-1">
            {Object.entries(categories).map(([name, count]) => (
              <Button
                key={name}
                variant="ghost"
                className={cn(
                  "w-full justify-between px-3 py-2 text-slate-600 hover:text-slate-900 text-sm",
                  currentView === `category:${name}` && "bg-slate-100 text-slate-900 font-semibold"
                )}
                onClick={() => setCurrentView(`category:${name}`)}
              >
                <span className="truncate">{name}</span>
                <Badge variant="secondary" className="font-medium text-[10px] px-1.5 py-0">
                  {count}
                </Badge>
              </Button>
            ))}
          </div>
        </div>

        {labels.length > 0 && (
          <div>
            <h2 className="px-3 text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-2">Labels</h2>
            <div className="space-y-1">
              {labels.map((label) => (
                <Button
                  key={label}
                  variant="ghost"
                  className={cn(
                    "w-full justify-start gap-3 px-3 py-2 text-slate-600 hover:text-slate-900 text-sm",
                    currentView === `label:${label}` && "bg-slate-100 text-slate-900 font-semibold"
                  )}
                  onClick={() => setCurrentView(`label:${label}`)}
                >
                  <Tag size={16} className="text-slate-400" />
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

      <div className="mt-auto pt-4 border-t border-slate-200">
        <Button 
          variant="outline" 
          className="w-full justify-center gap-2 text-slate-600 bg-white"
          onClick={onSync}
          disabled={isSyncing}
        >
          <RefreshCw size={16} className={cn(isSyncing && "animate-spin")} />
          <span>{isSyncing ? "Syncing AI..." : "Sync Agent"}</span>
        </Button>
      </div>
    </div>
  );
};
