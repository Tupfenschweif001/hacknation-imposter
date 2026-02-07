import Link from 'next/link';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { StatusBadge } from '@/components/status-badge';
import { Request } from '@/lib/types';
import { formatDistanceToNow } from 'date-fns';

interface RequestCardProps {
  request: Request;
}

export function RequestCard({ request }: RequestCardProps) {
  const timeAgo = formatDistanceToNow(new Date(request.updated_at), {
    addSuffix: true,
  });

  return (
    <Link href={`/requests/${request.id}`}>
      <Card className="rounded-2xl hover:shadow-md transition-shadow cursor-pointer border-gray-200">
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between gap-2">
            <h3 className="font-semibold text-gray-900 line-clamp-2">
              {request.title}
            </h3>
            <StatusBadge status={request.status} />
          </div>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-gray-600 line-clamp-2 mb-3">
            {request.description}
          </p>
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Updated {timeAgo}</span>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}