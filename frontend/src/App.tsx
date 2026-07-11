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
  const [userProfile, setUserProfile] = useState<{name: string, email: string} | null>(null);

  useEffect(() => {
    if (token) {
      api.getUserProfile().then(res => {
        if (res.data && typeof res.data === 'object' && 'name' in res.data) {
          setUserProfile(res.data);
        }
      }).catch(console.error);
    }
  }, [token]);

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
        <div className="w-[380px] border-r border-slate-200 flex flex-col bg-white z-10 transition-colors duration-300">
          <div className="p-4 flex flex-col border-b border-slate-100 bg-white">
            <div className="flex justify-between items-center mb-4">
              <h2 className="font-bold text-slate-800 text-xl tracking-tight capitalize">
                {currentView.split(':')[1] || currentView.replace(':', ' ')}
              </h2>
              <span className="text-[10px] bg-[#0EA5E9] text-white px-2 py-0.5 rounded-full font-bold shadow-sm">
                {emails.filter(e => !e.is_read).length || emails.length} new
              </span>
            </div>
            
            {/* Tabs */}
            <div className="flex items-center gap-1 bg-slate-50/50 p-1 rounded-lg border border-slate-100">
              <button className="flex-1 text-[11px] font-semibold bg-white text-[#0EA5E9] py-1.5 rounded-md shadow-sm border border-slate-200">All</button>
              <button className="flex-1 text-[11px] font-semibold text-slate-500 hover:text-slate-700 py-1.5 rounded-md">Unread</button>
              <button className="flex-1 text-[11px] font-semibold text-slate-500 hover:text-slate-700 py-1.5 rounded-md">Starred</button>
              <button className="flex-1 text-[11px] font-semibold text-slate-500 hover:text-slate-700 py-1.5 rounded-md">Attachments</button>
            </div>
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
        userProfile={userProfile}
      />

      <main className="flex-1 flex flex-col min-w-0 bg-white">
        <header className="h-16 border-b border-slate-100 bg-white flex items-center justify-between px-6 z-10">
          <div className="flex items-center gap-4 text-sm font-semibold text-slate-700 w-32">
            <span className="capitalize">{currentView.split(':')[1] || currentView.replace(':', ' ')}</span>
          </div>
          
          <div className="flex-1 max-w-lg mx-6 relative group">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-[#0EA5E9] transition-colors" size={16} />
            <input 
              type="text" 
              placeholder="Search emails..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && searchQuery.trim()) {
                  setCurrentView('search:' + searchQuery.trim());
                } else if (e.key === 'Enter' && !searchQuery.trim()) {
                  setCurrentView('inbox');
                }
              }}
              className="w-full bg-slate-50 border border-slate-200 rounded-full py-2 pl-12 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-[#0EA5E9]/20 focus:border-[#0EA5E9] transition-all placeholder:text-slate-400 font-medium text-slate-700"
            />
          </div>
          
          <div className="flex items-center gap-5 justify-end w-64">
            <div className="flex items-center gap-2 bg-green-50 px-3 py-1.5 rounded-full border border-green-100 hover-float cursor-pointer shadow-sm">
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
              <span className="text-[11px] font-bold text-green-700 uppercase tracking-tight">AI Active</span>
            </div>
            
            <button className="relative p-2 text-slate-400 hover:text-slate-600 transition-colors hover-float">
              <div className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full border border-white"></div>
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>
            </button>
            
            <div className="flex items-center gap-2 pl-5 border-l border-slate-200">
              <div className="w-8 h-8 rounded-full bg-[#0EA5E9] flex items-center justify-center text-white font-bold text-xs shadow-sm cursor-pointer hover-float">
                {userProfile ? userProfile.name.split(' ').map((n: string) => n[0]).join('').substring(0, 2).toUpperCase() : 'U'}
              </div>
              <div className="hidden xl:flex flex-col">
                <span className="text-[12px] font-bold text-slate-800 leading-tight truncate max-w-[120px]">{userProfile ? userProfile.name : 'User'}</span>
                <span className="text-[10px] text-slate-400 font-medium truncate max-w-[120px]">{userProfile ? userProfile.email : 'Loading...'}</span>
              </div>
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
