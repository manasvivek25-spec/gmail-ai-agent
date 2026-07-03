
import React from 'react';
import { Inbox, Star, Flame, Calendar, RefreshCw, Tag, Mail, ShieldCheck } from 'lucide-react';
import { api } from '../services/api';

interface SidebarProps {
  currentView: string;
  setCurrentView: (view: string) => void;
  categories: Record<string, number>;
  labels: string[];
}

const Sidebar: React.FC<SidebarProps> = ({ currentView, setCurrentView, categories, labels }) => {
  const navItem = (name: string, icon: React.ReactNode, id: string) => (
    <button
      onClick={() => setCurrentView(id)}
      className={`flex items-center space-x-3 w-full px-4 py-2.5 rounded-xl transition-all duration-200 ${
        currentView === id 
          ? 'bg-blue-50 text-blue-700 shadow-sm shadow-blue-100/50' 
          : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
      }`}
    >
      <span className={`${currentView === id ? 'text-blue-600' : 'text-slate-400'}`}>
        {icon}
      </span>
      <span className="font-semibold text-sm">{name}</span>
    </button>
  );

  return (
    <div className="w-72 bg-white h-screen flex flex-col border-r border-slate-200/80 p-6 z-10 shadow-sm">
      <div className="mb-10 flex items-center space-x-3 px-2">
        <div className="bg-blue-600 p-2 rounded-xl shadow-lg shadow-blue-200">
          <Mail className="text-white" size={24} />
        </div>
        <div>
          <h1 className="text-lg font-black text-slate-900 leading-none">EMAIL AI</h1>
          <p className="text-[10px] font-bold text-blue-600 tracking-tighter uppercase">Professional Agent</p>
        </div>
      </div>

      <div className="space-y-8 overflow-y-auto custom-scrollbar pr-1">
        <section>
          <h2 className="px-4 text-[11px] font-bold text-slate-400 uppercase tracking-[0.2em] mb-3">Workspace</h2>
          <div className="space-y-1.5">
            {navItem('Inbox', <Inbox size={18} />, 'inbox')}
            {navItem('Starred', <Star size={18} />, 'starred')}
          </div>
        </section>

        <section>
          <h2 className="px-4 text-[11px] font-bold text-slate-400 uppercase tracking-[0.2em] mb-3">AI Intelligence</h2>
          <div className="space-y-1.5">
            {navItem('Priority Feed', <Flame size={18} />, 'recommended')}
            {navItem('Deadlines', <Calendar size={18} />, 'deadlines')}
          </div>
        </section>

        <section>
          <h2 className="px-4 text-[11px] font-bold text-slate-400 uppercase tracking-[0.2em] mb-3">Smart Groups</h2>
          <div className="space-y-1.5">
            {Object.entries(categories).map(([name, count]) => (
              <button
                key={name}
                onClick={() => setCurrentView(`category:${name}`)}
                className={`flex items-center justify-between w-full px-4 py-2.5 rounded-xl transition-all duration-200 ${
                  currentView === `category:${name}` 
                    ? 'bg-green-50 text-green-700' 
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                }`}
              >
                <div className="flex items-center space-x-3 truncate">
                  <ShieldCheck size={18} className={currentView === `category:${name}` ? 'text-green-600' : 'text-slate-400'} />
                  <span className="font-semibold text-sm truncate">{name}</span>
                </div>
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                  currentView === `category:${name}` ? 'bg-green-100 text-green-700' : 'bg-slate-100 text-slate-500'
                }`}>
                  {count}
                </span>
              </button>
            ))}
          </div>
        </section>

        <section>
          <h2 className="px-4 text-[11px] font-bold text-slate-400 uppercase tracking-[0.2em] mb-3">Labels</h2>
          <div className="space-y-1.5">
            {labels.map((label) => (
              <button
                key={label}
                onClick={() => setCurrentView(`label:${label}`)}
                className={`flex items-center space-x-3 w-full px-4 py-2.5 rounded-xl transition-all duration-200 ${
                  currentView === `label:${label}` 
                    ? 'bg-slate-100 text-slate-900 border border-slate-200' 
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                }`}
              >
                <Tag size={16} className="text-slate-400" />
                <span className="font-semibold text-sm truncate">{label}</span>
              </button>
            ))}
          </div>
        </section>
      </div>

      <div className="mt-auto pt-6 border-t border-slate-100">
        <button 
          onClick={() => api.refresh()}
          className="flex items-center justify-center space-x-2 w-full px-4 py-3 rounded-xl bg-slate-900 text-white hover:bg-slate-800 transition-all shadow-lg shadow-slate-200"
        >
          <RefreshCw size={18} />
          <span className="font-bold text-sm">Sync Agent</span>
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
