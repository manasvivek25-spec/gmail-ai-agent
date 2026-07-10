import { useState, useEffect } from 'react';
import { Search, Loader2, Bot, Command } from 'lucide-react';
import { NavigationSidebar } from './components/sidebar/NavigationSidebar';
import { EmailCard } from './components/communications/EmailCard';
import { DetailsPanel } from './components/communications/DetailsPanel';
import AIAssistant from './components/AIAssistant';
import { api } from './services/api';
import { useEmails, useInitialData } from './hooks/useCommunications';
import { EmailDetails } from './types';

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
      <div className="flex h-screen w-full items-center justify-center bg-[#09090B] text-white">
        <div className="max-w-md p-8 flex flex-col items-center w-full">
          <div className="w-[100px] h-[100px] flex items-center justify-center rounded-full bg-blue-500/10 border-2 border-blue-500/30 mb-8">
            <Bot className="text-blue-500 w-[50px] h-[50px]" />
          </div>
          
          <h1 className="text-4xl font-bold tracking-tight text-white mb-4 tracking-tighter">Mail Agent</h1>
          
          <p className="text-white/70 text-center text-sm leading-relaxed mb-12">
            Your intelligent, multi-tenant AI email assistant. Sign in to seamlessly sync your inbox across all platforms.
          </p>
          
          <button 
            onClick={async () => {
              try {
                const origin = window.location.origin;
                const res = await fetch(`https://gmail-ai-agent-ih4e.onrender.com/auth/google/url?platform=${encodeURIComponent(origin)}`);
                const data = await res.json();
                if (data.url) {
                  window.location.href = data.url;
                }
              } catch (e) {
                console.error('Login failed', e);
              }
            }} 
            className="flex items-center justify-center gap-4 w-auto px-6 h-14 bg-white hover:bg-gray-50 text-black rounded-[30px] border border-gray-300 transition-colors shadow-sm cursor-pointer"
          >
            <div className="w-6 h-6 rounded-full bg-white flex items-center justify-center">
              <span className="text-[#4285F4] font-bold text-xl leading-none">G</span>
            </div>
            <span className="text-base font-semibold text-gray-800">Continue with Google</span>
          </button>

          <p className="text-white/30 text-xs text-center leading-relaxed mt-8">
            By signing in, you agree to our Terms of Service and Privacy Policy.
          </p>
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
          </div>
        </header>

        {renderMainContent()}
      </main>

      {/* Floating Chatbot Button */}
      <button
        onClick={() => setIsAssistantOpen(true)}
        className="fixed bottom-8 right-8 z-40 bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-4 rounded-full shadow-2xl hover:scale-110 hover:shadow-[0_0_20px_rgba(79,70,229,0.5)] transition-all duration-300 group flex items-center justify-center"
        aria-label="Open AI Assistant"
      >
        <Bot size={28} className="group-hover:animate-pulse" />
      </button>

      <AIAssistant isOpen={isAssistantOpen} onClose={() => setIsAssistantOpen(false)} />
    </div>
  );
}


export default App;
