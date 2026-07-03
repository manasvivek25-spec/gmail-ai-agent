import { useState, useEffect } from 'react';
import { Search, Loader2, Bot, Command } from 'lucide-react';
import { NavigationSidebar } from './components/sidebar/NavigationSidebar';
import { EmailCard } from './components/communications/EmailCard';
import { DetailsPanel } from './components/communications/DetailsPanel';
import AIAssistant from './components/AIAssistant';
import { api } from './services/api';
import { useEmails, useInitialData } from './hooks/useCommunications';
import { EmailDetails } from './types';
import { Button } from './components/ui/button';

import { AnalyticsView } from './components/analytics/AnalyticsView';
import { DeadlineTracker } from './components/intelligence/DeadlineTracker';
import { RecommendationFeed } from './components/intelligence/RecommendationFeed';

function App() {
  const [currentView, setCurrentView] = useState('inbox');
  const [selectedEmailId, setSelectedEmailId] = useState<string | null>(null);
  const [selectedEmailDetails, setSelectedEmailDetails] = useState<EmailDetails | null>(null);
  const [isAssistantOpen, setIsAssistantOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [isSyncing, setIsSyncing] = useState(false);

  const { emails, isLoading, refetch: refetchEmails } = useEmails(currentView);
  const { categories, labels, refetch: refetchInitialData } = useInitialData();

  const handleSync = async () => {
    setIsSyncing(true);
    try {
      await api.refresh();
      await refetchEmails();
      await refetchInitialData();
    } catch (error) {
      console.error('Failed to sync emails:', error);
    } finally {
      setIsSyncing(false);
    }
  };

  useEffect(() => {
    if (selectedEmailId) {
      fetchEmailDetails(selectedEmailId);
    } else {
      setSelectedEmailDetails(null);
    }
  }, [selectedEmailId]);

  // Reset selection when changing views
  useEffect(() => {
    setSelectedEmailId(null);
  }, [currentView]);

  // Auto-select first email when emails change
  useEffect(() => {
    if (emails.length > 0 && !selectedEmailId) {
      setSelectedEmailId(emails[0].email_id);
    }
  }, [emails]);

  const fetchEmailDetails = async (id: string) => {
    try {
      const res = await api.getEmailDetails(id);
      setSelectedEmailDetails(res.data);
    } catch (error) {
      console.error('Error fetching email details:', error);
    }
  };

  const toggleBookmark = async () => {
    if (selectedEmailId) {
      await api.toggleBookmark(selectedEmailId);
      refetchEmails();
    }
  };

  const renderMainContent = () => {
    if (currentView === 'analytics') {
      return <AnalyticsView />;
    }

    if (currentView === 'deadlines') {
      return (
        <div className="flex-1 flex overflow-hidden">
          <DeadlineTracker 
            emails={emails} 
            onSelect={setSelectedEmailId} 
            selectedId={selectedEmailId} 
          />
          <DetailsPanel 
            email={selectedEmailDetails} 
            onToggleBookmark={toggleBookmark}
            isBookmarked={selectedEmailId ? emails.find(e => e.email_id === selectedEmailId)?.is_starred || false : false}
          />
        </div>
      );
    }

    if (currentView === 'recommended') {
      return (
        <div className="flex-1 flex overflow-hidden">
          <RecommendationFeed 
            emails={emails} 
            onSelect={setSelectedEmailId} 
            selectedId={selectedEmailId} 
          />
          <DetailsPanel 
            email={selectedEmailDetails} 
            onToggleBookmark={toggleBookmark}
            isBookmarked={selectedEmailId ? emails.find(e => e.email_id === selectedEmailId)?.is_starred || false : false}
          />
        </div>
      );
    }

    return (
      <div className="flex-1 flex overflow-hidden">
        {/* Inbox List */}
        <div className="w-[380px] border-r border-slate-100 flex flex-col bg-slate-50/20">
          <div className="p-4 flex justify-between items-center border-b border-slate-100 bg-white/50">
            <h2 className="font-bold text-slate-900 text-[11px] uppercase tracking-[0.2em]">{currentView.replace(':', ' ')}</h2>
            <span className="text-[10px] bg-slate-100 px-2 py-0.5 rounded text-slate-500 font-bold">{emails.length} Items</span>
          </div>
          
          <div className="flex-1 overflow-y-auto custom-scrollbar">
            {isLoading ? (
              <div className="h-full flex flex-col items-center justify-center space-y-4">
                <Loader2 className="text-primary animate-spin" size={24} />
                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Updating Stream...</p>
              </div>
            ) : (
              <div className="divide-y divide-slate-100">
                {emails.map(email => (
                  <EmailCard 
                    key={email.email_id} 
                    email={email} 
                    isActive={selectedEmailId === email.email_id}
                    onClick={() => setSelectedEmailId(email.email_id)}
                  />
                ))}
                {emails.length === 0 && (
                  <div className="p-12 text-center">
                    <p className="text-sm font-bold text-slate-900">End of stream</p>
                    <p className="text-xs text-slate-400 mt-1">No communications found in this view.</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Details Pane */}
        <DetailsPanel 
          email={selectedEmailDetails} 
          onToggleBookmark={toggleBookmark}
          isBookmarked={selectedEmailId ? emails.find(e => e.email_id === selectedEmailId)?.is_starred || false : false}
        />
      </div>
    );
  };

  return (
    <div className="flex h-screen w-full bg-slate-50 overflow-hidden font-sans text-slate-900 antialiased">
      <NavigationSidebar 
        currentView={currentView} 
        setCurrentView={setCurrentView} 
        categories={categories} 
        labels={labels} 
        onSync={handleSync}
        isSyncing={isSyncing}
      />

      <main className="flex-1 flex flex-col min-w-0 bg-white">
        <header className="h-16 border-b border-slate-100 bg-white flex items-center justify-between px-8 z-10">
          <div className="flex-1 max-w-xl relative group">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-primary transition-colors" size={16} />
            <input 
              type="text" 
              placeholder="Search communications..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && searchQuery.trim()) {
                  setCurrentView('search:' + searchQuery.trim());
                } else if (e.key === 'Enter' && !searchQuery.trim()) {
                  setCurrentView('inbox');
                }
              }}
              className="w-full bg-slate-50 border-none rounded-lg py-2 pl-10 pr-4 text-xs focus:outline-none focus:ring-1 focus:ring-primary/20 transition-all placeholder:text-slate-400 font-medium"
            />
            <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-1 text-slate-300">
              <Command size={10} />
              <span className="text-[10px] font-bold">K</span>
            </div>
          </div>
          
          <div className="flex items-center gap-4 ml-8">
            <div className="hidden md:flex flex-col items-end mr-2">
              <span className="text-[10px] font-bold text-slate-900 uppercase tracking-tighter">Secure Engine</span>
              <span className="text-[10px] text-secondary font-bold uppercase tracking-tighter">Agent Active</span>
            </div>
            <Button 
              onClick={() => setIsAssistantOpen(true)}
              variant="ai"
              size="sm"
              className="gap-2 font-bold text-[11px] uppercase tracking-wider rounded-lg"
            >
              <Bot size={16} />
              <span>Assistant</span>
            </Button>
          </div>
        </header>

        {renderMainContent()}
      </main>

      <AIAssistant isOpen={isAssistantOpen} onClose={() => setIsAssistantOpen(false)} />
    </div>
  );
}


export default App;
