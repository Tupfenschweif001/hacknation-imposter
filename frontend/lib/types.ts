export type RequestStatus =
  | 'queued'
  | 'outside_business_hours'
  | 'calling'
  | 'in_progress'
  | 'waiting_for_callback'
  | 'booked'
  | 'failed'
  | 'canceled';

export interface Request {
  id: string;
  user_id: string;
  title: string;
  description: string;
  callback_number: string;
  number_to_call?: string | null;
  preferred_time: string;
  status: RequestStatus;
  summary?: string | null;
  created_at: string;
  updated_at: string;
}

export interface Event {
  id: string;
  request_id: string;
  created_at: string;
  type: string;
  message: string;
}

export interface Profile {
  user_id: string;
  username: string;
  default_callback_number: string;
  street: string;
  house_number: string;
  postal_code: string;
  city: string;
  country: string;
  calendar_connected: boolean;
}
