'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { supabase } from '@/lib/supabase';
import { Request, Event } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { Skeleton } from '@/components/ui/skeleton';
import { StatusBadge } from '@/components/status-badge';
import { Timeline } from '@/components/timeline';
import { ArrowLeft, Phone, MapPin, Calendar, AlertCircle, Trash2, Loader2 } from 'lucide-react';
import { toast } from 'sonner';

export default function RequestDetailPage() {
  const router = useRouter();
  const params = useParams();
  const requestId = params.id as string;

  const [request, setRequest] = useState<Request | null>(null);
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  useEffect(() => {
    fetchRequestData();

    // Polling alle 3 Sekunden
    const interval = setInterval(() => {
      fetchRequestData(true);
    }, 3000);

    return () => clearInterval(interval);
  }, [requestId]);

  const handleDelete = async () => {
    if (!request) return;
    
    setDeleting(true);
    try {
      const { error } = await supabase
        .from('requests')
        .delete()
        .eq('id', request.id);

      if (error) throw error;

      toast.success('Request deleted successfully');
      router.push('/dashboard');
    } catch (error: any) {
      toast.error(error.message || 'Failed to delete request');
    } finally {
      setDeleting(false);
      setShowDeleteConfirm(false);
    }
  };

  const fetchRequestData = async (silent = false) => {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      
      if (!user) {
        router.push('/login');
        return;
      }

      // Fetch request
      const { data: requestData, error: requestError } = await supabase
        .from('requests')
        .select('*')
        .eq('id', requestId)
        .eq('user_id', user.id)
        .single();

      if (requestError) throw requestError;

      setRequest(requestData);

      // Fetch events
      const { data: eventsData, error: eventsError } = await supabase
        .from('events')
        .select('*')
        .eq('request_id', requestId)
        .order('created_at', { ascending: false });

      if (eventsError) throw eventsError;

      setEvents(eventsData || []);
    } catch (error: any) {
      if (!silent) {
        toast.error('Failed to load request');
        console.error(error);
      }
    } finally {
      setLoading(false);
    }
  };

  const getStatusMessage = () => {
    if (!request) return null;

    const messages: Record<string, { text: string; icon: any; color: string }> = {
      queued: {
        text: 'Your request has been queued and will be processed soon.',
        icon: AlertCircle,
        color: 'text-gray-600',
      },
      outside_business_hours: {
        text: 'Your request will be processed outside business hours. Expected start at 08:00 AM.',
        icon: AlertCircle,
        color: 'text-blue-600',
      },
      calling: {
        text: 'The agent is calling...',
        icon: Phone,
        color: 'text-violet-600',
      },
      in_progress: {
        text: 'The agent is processing your request.',
        icon: Phone,
        color: 'text-violet-600',
      },
      waiting_for_callback: {
        text: 'The call was unsuccessful. The agent is waiting for a callback.',
        icon: AlertCircle,
        color: 'text-yellow-600',
      },
      booked: {
        text: 'Appointment successfully booked!',
        icon: AlertCircle,
        color: 'text-green-600',
      },
      failed: {
        text: 'The request could not be completed successfully.',
        icon: AlertCircle,
        color: 'text-red-600',
      },
      canceled: {
        text: 'The request has been canceled.',
        icon: AlertCircle,
        color: 'text-gray-600',
      },
    };

    const config = messages[request.status];
    if (!config) return null;

    const Icon = config.icon;

    return (
      <Card className="rounded-2xl border-blue-200 bg-blue-50">
        <CardContent className="pt-6">
          <div className="flex gap-3">
            <Icon className={`w-5 h-5 flex-shrink-0 mt-0.5 ${config.color}`} />
            <p className={`text-sm ${config.color}`}>{config.text}</p>
          </div>
        </CardContent>
      </Card>
    );
  };

  if (loading) {
    return (
      <div className="p-8 max-w-5xl mx-auto">
        <Skeleton className="h-10 w-32 mb-6" />
        <div className="space-y-6">
          <Skeleton className="h-48 w-full rounded-2xl" />
          <Skeleton className="h-64 w-full rounded-2xl" />
        </div>
      </div>
    );
  }

  if (!request) {
    return (
      <div className="p-8 max-w-5xl mx-auto">
        <Card className="rounded-2xl">
          <CardContent className="pt-6">
            <p className="text-center text-muted-foreground">Request not found</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-5xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <Button
          variant="ghost"
          onClick={() => router.push('/dashboard')}
          className="rounded-xl"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Dashboard
        </Button>

        {!showDeleteConfirm ? (
          <Button
            variant="outline"
            onClick={() => setShowDeleteConfirm(true)}
            className="rounded-xl text-red-600 hover:bg-red-50 hover:text-red-700 dark:hover:bg-red-950 border-red-200"
          >
            <Trash2 className="mr-2 h-4 w-4" />
            Delete Request
          </Button>
        ) : (
          <div className="flex gap-2">
            <Button
              variant="outline"
              onClick={() => setShowDeleteConfirm(false)}
              disabled={deleting}
              className="rounded-xl"
            >
              Cancel
            </Button>
            <Button
              variant="destructive"
              onClick={handleDelete}
              disabled={deleting}
              className="rounded-xl"
            >
              {deleting ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Deleting...
                </>
              ) : (
                <>
                  <Trash2 className="mr-2 h-4 w-4" />
                  Confirm Delete
                </>
              )}
            </Button>
          </div>
        )}
      </div>

      <div className="space-y-6">
        {/* Header */}
        <Card className="rounded-2xl shadow-lg border-gray-200">
          <CardHeader>
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1">
                <CardTitle className="text-2xl mb-2">{request.title}</CardTitle>
                <StatusBadge status={request.status} />
              </div>
            </div>
          </CardHeader>
        </Card>

        {/* Status Message */}
        {getStatusMessage()}

        {/* Details */}
        <Card className="rounded-2xl shadow-lg border-gray-200">
          <CardHeader>
            <CardTitle>Details</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h4 className="text-sm font-medium text-muted-foreground mb-1">Description</h4>
              <p className="text-foreground">{request.description}</p>
            </div>

            <Separator />

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h4 className="text-sm font-medium text-muted-foreground mb-1 flex items-center gap-2">
                  <Phone className="w-4 h-4" />
                  Callback Number
                </h4>
                <p className="text-foreground">{request.callback_number}</p>
              </div>

              {request.number_to_call && (
                <div>
                  <h4 className="text-sm font-medium text-muted-foreground mb-1 flex items-center gap-2">
                    <Phone className="w-4 h-4" />
                    Number to Call
                  </h4>
                  <p className="text-foreground">{request.number_to_call}</p>
                </div>
              )}

              <div>
                <h4 className="text-sm font-medium text-muted-foreground mb-1 flex items-center gap-2">
                  <Calendar className="w-4 h-4" />
                  Preferred Time Window
                </h4>
                <p className="text-foreground">{request.preferred_time}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Summary */}
        {request.summary && (
          <Card className="rounded-2xl shadow-lg border-gray-200">
            <CardHeader>
              <CardTitle>Summary</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-foreground whitespace-pre-wrap">{request.summary}</p>
            </CardContent>
          </Card>
        )}

        {/* Timeline */}
        <Card className="rounded-2xl shadow-lg border-gray-200">
          <CardHeader>
            <CardTitle>Timeline</CardTitle>
          </CardHeader>
          <CardContent>
            <Timeline events={events} />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}