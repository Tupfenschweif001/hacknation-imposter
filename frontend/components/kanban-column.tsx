import { Request } from '@/lib/types';
import { RequestCard } from '@/components/request-card';
import { Card } from '@/components/ui/card';

interface KanbanColumnProps {
  title: string;
  requests: Request[];
  emptyMessage?: string;
}

export function KanbanColumn({ title, requests, emptyMessage = 'No requests' }: KanbanColumnProps) {
  return (
    <div className="flex flex-col h-full">
      <div className="mb-4">
        <h2 className="text-lg font-semibold text-foreground">{title}</h2>
        <p className="text-sm text-muted-foreground">{requests.length} request{requests.length !== 1 ? 's' : ''}</p>
      </div>
      <div className="flex-1 space-y-3 overflow-y-auto pr-2">
        {requests.length === 0 ? (
          <Card className="rounded-2xl border-dashed border-2 border-border bg-muted/30">
            <div className="p-8 text-center">
              <p className="text-sm text-muted-foreground">{emptyMessage}</p>
            </div>
          </Card>
        ) : (
          requests.map((request) => (
            <RequestCard key={request.id} request={request} />
          ))
        )}
      </div>
    </div>
  );
}