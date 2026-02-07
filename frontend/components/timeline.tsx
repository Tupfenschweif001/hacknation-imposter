import { Event } from '@/lib/types';
import { Card } from '@/components/ui/card';
import { formatDistanceToNow } from 'date-fns';
import { Circle } from 'lucide-react';

interface TimelineProps {
  events: Event[];
}

export function Timeline({ events }: TimelineProps) {
  if (events.length === 0) {
    return (
      <Card className="rounded-2xl border-dashed border-2 border-gray-200 bg-gray-50">
        <div className="p-8 text-center">
          <p className="text-sm text-gray-500">No events yet</p>
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {events.map((event, index) => {
        const timeAgo = formatDistanceToNow(new Date(event.created_at), {
          addSuffix: true,
        });

        return (
          <div key={event.id} className="flex gap-4">
            <div className="flex flex-col items-center">
              <div className="w-3 h-3 rounded-full bg-violet-600 flex-shrink-0 mt-1" />
              {index < events.length - 1 && (
                <div className="w-0.5 h-full bg-gray-200 mt-2" />
              )}
            </div>
            <Card className="flex-1 rounded-xl border-gray-200 mb-2">
              <div className="p-4">
                <div className="flex items-start justify-between gap-2 mb-2">
                  <span className="font-medium text-gray-900">{event.type}</span>
                  <span className="text-xs text-gray-500 whitespace-nowrap">
                    {timeAgo}
                  </span>
                </div>
                <p className="text-sm text-gray-600">{event.message}</p>
              </div>
            </Card>
          </div>
        );
      })}
    </div>
  );
}