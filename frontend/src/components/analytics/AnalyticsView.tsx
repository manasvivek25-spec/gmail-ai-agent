import React, { useState, useEffect } from 'react';
import { api } from '@/services/api';

import { Badge } from '@/components/ui/badge';
import { BarChart, Tag, Target, Calendar, Database } from 'lucide-react';

export const AnalyticsView: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const res = await api.getAnalytics();
        setData(res.data);
      } catch (e) {
        console.error("Failed to fetch analytics", e);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (loading) return (
    <div className="flex-1 flex items-center justify-center bg-white">
      <div className="text-center animate-pulse">
        <BarChart className="mx-auto mb-4 text-slate-200" size={48} />
        <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Synthesizing Neural Data...</p>
      </div>
    </div>
  );

  if (!data) return <div className="p-20 text-center text-slate-400">No telemetry data available.</div>;

  const MetricCard = ({ title, value, icon: Icon, color }: any) => {
    const colorClasses: Record<string, string> = {
      blue: 'bg-primary/10 text-primary',
      emerald: 'bg-secondary/10 text-secondary',
      purple: 'bg-purple-50 text-purple-600',
      orange: 'bg-orange-50 text-orange-600'
    };
    
    return (
    <div className="bg-white border border-slate-100 p-6 rounded-2xl shadow-sm flex items-center gap-4">
      <div className={`p-3 rounded-xl ${colorClasses[color] || 'bg-slate-50 text-slate-600'}`}>
        <Icon size={24} />
      </div>
      <div>
        <h3 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{title}</h3>
        <p className="text-2xl font-black text-slate-900">{value}</p>
      </div>
    </div>
  )};

  return (
    <div className="flex-1 bg-white overflow-y-auto p-10 space-y-12 custom-scrollbar">
      <div>
        <h1 className="text-3xl font-black text-slate-900 tracking-tight">Intelligence Telemetry</h1>
        <p className="text-sm text-slate-500 mt-2 font-medium">Real-time metrics from your local neural engine.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard title="Processed" value={data.emails_processed} icon={Database} color="blue" />
        <MetricCard title="Deadlines" value={data.deadlines_count} icon={Calendar} color="emerald" />
        <MetricCard title="Label Rules" value={data.labels_count} icon={Tag} color="purple" />
        <MetricCard title="Interests" value={data.top_interests?.length || 0} icon={Target} color="orange" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
        <section className="space-y-6">
          <h2 className="text-xs font-bold text-slate-900 uppercase tracking-[0.2em] flex items-center gap-2">
            <Target size={16} className="text-orange-500" />
            Top Neural Interests
          </h2>
          <div className="space-y-3">
            {data.top_interests?.map((interest: string, i: number) => (
              <div key={interest} className="flex items-center justify-between p-4 bg-slate-50 rounded-xl border border-slate-100">
                <span className="text-sm font-bold text-slate-700">{interest}</span>
                <Badge variant="secondary" className="bg-white border-slate-200">#{i + 1} Rank</Badge>
              </div>
            ))}
          </div>
        </section>

        <section className="space-y-6">
          <h2 className="text-xs font-bold text-slate-900 uppercase tracking-[0.2em] flex items-center gap-2">
            <Tag size={16} className="text-purple-500" />
            Common AI Tags
          </h2>
          <div className="flex flex-wrap gap-2">
            {data.top_tags?.map((tag: string) => (
              <Badge key={tag} variant="outline" className="px-4 py-2 text-xs font-bold border-slate-200 bg-white">
                {tag}
              </Badge>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
};
