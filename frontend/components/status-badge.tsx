import { Badge } from '@/components/ui/badge';
import { RequestStatus } from '@/lib/types';
import { Clock, Phone, CheckCircle, XCircle, Ban, PhoneOff } from 'lucide-react';

interface StatusBadgeProps {
  status: RequestStatus;
}

export function StatusBadge({ status }: StatusBadgeProps) {
  const statusConfig: Record<
    RequestStatus,
    { label: string; variant: 'default' | 'secondary' | 'destructive' | 'outline'; icon: any; className: string }
  > = {
    queued: {
      label: 'Queued',
      variant: 'secondary',
      icon: Clock,
      className: 'bg-gray-100 text-gray-700 hover:bg-gray-100',
    },
    outside_business_hours: {
      label: 'Outside Business Hours',
      variant: 'secondary',
      icon: Clock,
      className: 'bg-blue-100 text-blue-700 hover:bg-blue-100',
    },
    calling: {
      label: 'Calling',
      variant: 'default',
      icon: Phone,
      className: 'bg-violet-100 text-violet-700 hover:bg-violet-100',
    },
    in_progress: {
      label: 'In Progress',
      variant: 'default',
      icon: Phone,
      className: 'bg-violet-100 text-violet-700 hover:bg-violet-100',
    },
    waiting_for_callback: {
      label: 'Waiting for Callback',
      variant: 'outline',
      icon: PhoneOff,
      className: 'bg-yellow-100 text-yellow-700 hover:bg-yellow-100 border-yellow-300',
    },
    booked: {
      label: 'Booked',
      variant: 'default',
      icon: CheckCircle,
      className: 'bg-green-100 text-green-700 hover:bg-green-100',
    },
    failed: {
      label: 'Failed',
      variant: 'destructive',
      icon: XCircle,
      className: 'bg-red-100 text-red-700 hover:bg-red-100',
    },
    canceled: {
      label: 'Canceled',
      variant: 'outline',
      icon: Ban,
      className: 'bg-gray-100 text-gray-700 hover:bg-gray-100',
    },
  };

  const config = statusConfig[status];
  const Icon = config.icon;

  return (
    <Badge variant={config.variant} className={`rounded-full ${config.className}`}>
      <Icon className="w-3 h-3 mr-1" />
      {config.label}
    </Badge>
  );
}