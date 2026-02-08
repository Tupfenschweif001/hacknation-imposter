'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { supabase } from '@/lib/supabase';
import { Request } from '@/lib/types';
import { KanbanColumn } from '@/components/kanban-column';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Plus } from 'lucide-react';
import { toast } from 'sonner';

export default function DashboardPage() {
  const router = useRouter();
  const [requests, setRequests] = useState<Request[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRequests();
  }, []);

  const fetchRequests = async () => {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      
      if (!user) {
        router.push('/login');
        return;
      }

      const { data, error } = await supabase
        .from('requests')
        .select('*')
        .eq('user_id', user.id)
        .order('updated_at', { ascending: false });

      if (error) throw error;

      setRequests(data || []);
    } catch (error: any) {
      toast.error('Failed to load requests');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const openRequests = requests.filter((r) =>
    ['queued', 'outside_business_hours'].includes(r.status)
  );

  const inProgressRequests = requests.filter((r) =>
    ['calling', 'in_progress', 'waiting_for_callback'].includes(r.status)
  );

  const completedRequests = requests.filter((r) =>
    ['booked', 'failed', 'canceled'].includes(r.status)
  );

  if (loading) {
    return (
      <div className="p-8">
        <div className="flex items-center justify-between mb-8">
          <Skeleton className="h-10 w-48" />
          <Skeleton className="h-10 w-40" />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[1, 2, 3].map((i) => (
            <div key={i} className="space-y-4">
              <Skeleton className="h-8 w-32" />
              <Skeleton className="h-48 w-full rounded-2xl" />
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 h-full flex flex-col">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
          <p className="text-muted-foreground mt-1">Manage your appointment requests</p>
        </div>
        <Button
          onClick={() => router.push('/new')}
          className="rounded-xl bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700"
        >
          <Plus className="mr-2 h-4 w-4" />
          New Request
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 flex-1 min-h-0">
        <KanbanColumn
          title="Open"
          requests={openRequests}
          emptyMessage="No open requests"
        />
        <KanbanColumn
          title="In Progress"
          requests={inProgressRequests}
          emptyMessage="No requests in progress"
        />
        <KanbanColumn
          title="Completed"
          requests={completedRequests}
          emptyMessage="No completed requests"
        />
      </div>
    </div>
  );
}