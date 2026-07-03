import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { EmailMetadata, CategoryCounts } from '../types';

export function useEmails(view: string) {
  const [emails, setEmails] = useState<EmailMetadata[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchEmails = async () => {
    setIsLoading(true);
    try {
      let res;
      if (view === 'inbox') res = await api.getEmails();
      else if (view === 'starred') res = await api.getStarred();
      else if (view === 'recommended') res = await api.getRecommended();
      else if (view === 'deadlines') res = await api.getDeadlines();
      else if (view.startsWith('category:')) res = await api.getCategoryEmails(view.split(':')[1]);
      else if (view.startsWith('label:')) res = await api.getLabelEmails(view.split(':')[1]);
      else if (view.startsWith('search:')) res = await api.search(view.substring(7));
      
      setEmails(res?.data || []);
    } catch (error) {
      console.error('Error fetching emails:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchEmails();
  }, [view]);

  return { emails, isLoading, refetch: fetchEmails };
}

export function useInitialData() {
  const [categories, setCategories] = useState<CategoryCounts>({});
  const [labels, setLabels] = useState<string[]>([]);

  const fetchData = async () => {
    try {
      const [catRes, labelRes] = await Promise.all([
        api.getCategories(),
        api.getLabels()
      ]);
      setCategories(catRes.data);
      setLabels(labelRes.data);
    } catch (error) {
      console.error('Error fetching initial data:', error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return { categories, labels, refetch: fetchData };
}
