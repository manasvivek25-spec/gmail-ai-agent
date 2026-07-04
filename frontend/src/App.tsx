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
  const [token, setToken] = useState<string | null>(localStorage.getItem('jwt_token'));
  const [currentView, setCurrentView] = useState('inbox');
  const [selectedEmailId, setSelectedEmailId] = useState<string | null>(null);
  const [selectedEmailDetails, setSelectedEmailDetails] = useState<EmailDetails | null>(null);
  const [isAssistantOpen, setIsAssistantOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [isSyncing, setIsSyncing] = useState(false);
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    const url = new URL(window.location.href);
    const callbackToken = url.searchParams.get('token');
    if (callbackToken) {
      localStorage.setItem('jwt_token', callbackToken);
      setToken(callbackToken);
      window.history.replaceState({}, document.title, '/');
    }
  }, []);

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDark]);

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
        <div className="w-[380px] border-r border-border flex flex-col bg-card shadow-[4px_0_24px_-12px_rgba(0,0,0,0.05)] z-10 transition-colors duration-300">
          <div className="p-4 flex justify-between items-center border-b border-border bg-card/50 backdrop-blur-sm">
            <h2 className="font-bold text-foreground text-[11px] uppercase tracking-[0.2em]">{currentView.replace(':', ' ')}</h2>
            <span className="text-[10px] bg-accent px-2 py-0.5 rounded text-muted-foreground font-bold">{emails.length} Items</span>
          </div>
          
          <div className="flex-1 overflow-y-auto custom-scrollbar">
            {isLoading ? (
              <div className="h-full flex flex-col items-center justify-center space-y-4">
                <Loader2 className="text-primary animate-spin" size={24} />
                <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">Updating Stream...</p>
              </div>
            ) : (
              <div className="divide-y divide-border">
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
                    <p className="text-sm font-bold text-foreground">End of stream</p>
                    <p className="text-xs text-muted-foreground mt-1">No communications found in this view.</p>
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
  if (!token) {
    return (
      <div className="flex h-screen w-full items-center justify-center bg-background text-foreground transition-colors duration-300">
        <div className="max-w-md p-10 text-center bg-card rounded-[2rem] border border-border shadow-2xl flex flex-col items-center relative overflow-hidden group">
          <div className="absolute inset-0 bg-gradient-to-br from-primary/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700" />
          <div className="w-24 h-24 bg-accent rounded-full flex items-center justify-center mb-8 relative shadow-inner">
            <div className="absolute inset-0 rounded-full bg-primary/20 scale-0 group-hover:scale-[1.8] transition-transform duration-1000 ease-out opacity-0 group-hover:opacity-100 blur-xl" />
            <Bot className="text-primary w-12 h-12 relative z-10" />
          </div>
          <h1 className="text-4xl font-bold tracking-tight mb-3">Mail Agent</h1>
          <p className="text-muted-foreground mb-10 text-sm leading-relaxed">
            Welcome to the future of email. Sign in with Google to securely sync your inbox with your personal AI assistant.
          </p>
          <Button 
            onClick={async () => {
              const res = await fetch('http://localhost:8000/auth/google/url');
              const data = await res.json();
              window.location.href = data.url;
            }} 
            className="w-full font-bold h-14 text-sm shadow-lg hover:shadow-primary/25 hover:-translate-y-1 transition-all rounded-xl relative z-10"
          >
            Sign In with Google
          </Button>
        </div>
      </div>
    );
  }
  const handleSignOut = () => {
    localStorage.removeItem('jwt_token');
    setToken(null);
    window.location.href = '/';
  };

  return (
    <div className="flex h-screen w-full bg-background overflow-hidden font-sans text-foreground antialiased transition-colors duration-300">
      <NavigationSidebar 
        currentView={currentView} 
        setCurrentView={setCurrentView} 
        categories={categories} 
        labels={labels} 
        onSync={handleSync}
        isSyncing={isSyncing}
        isDark={isDark}
        toggleTheme={() => setIsDark(!isDark)}
        onSignOut={handleSignOut}
      />

      <main className="flex-1 flex flex-col min-w-0 bg-card">
        <header className="h-16 border-b border-border bg-card/80 backdrop-blur flex items-center justify-between px-8 z-10 transition-colors duration-300">
          <div className="flex-1 max-w-xl relative group">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground group-focus-within:text-primary transition-colors" size={16} />
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
              className="w-full bg-accent/50 border border-transparent rounded-lg py-2 pl-10 pr-4 text-xs focus:outline-none focus:ring-1 focus:ring-primary/50 focus:bg-background focus:border-primary/20 transition-all placeholder:text-muted-foreground font-medium text-foreground"
            />
            <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-1 text-muted-foreground/50">
              <Command size={10} />
              <span className="text-[10px] font-bold">K</span>
            </div>
          </div>
          
          <div className="flex items-center gap-4 ml-8">
            <div className="hidden md:flex flex-col items-end mr-2">
              <span className="text-[10px] font-bold text-foreground uppercase tracking-tighter">Secure Engine</span>
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
