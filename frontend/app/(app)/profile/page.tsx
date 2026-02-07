'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { supabase } from '@/lib/supabase';
import { Profile } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { Skeleton } from '@/components/ui/skeleton';
import { toast } from 'sonner';
import { Loader2, Calendar } from 'lucide-react';

export default function ProfilePage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [profile, setProfile] = useState<Profile>({
    user_id: '',
    username: '',
    default_callback_number: '',
    street: '',
    house_number: '',
    postal_code: '',
    city: '',
    country: 'Germany',
    calendar_connected: false,
  });

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      
      if (!user) {
        router.push('/login');
        return;
      }

      const { data, error } = await supabase
        .from('profiles')
        .select('*')
        .eq('user_id', user.id)
        .single();

      if (error && error.code !== 'PGRST116') {
        throw error;
      }

      if (data) {
        setProfile(data);
      } else {
        // Create default profile
        setProfile({
          user_id: user.id,
          username: user.email?.split('@')[0] || '',
          default_callback_number: '',
          street: '',
          house_number: '',
          postal_code: '',
          city: '',
          country: 'Germany',
          calendar_connected: false,
        });
      }
    } catch (error: any) {
      toast.error('Failed to load profile');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);

    try {
      const { error } = await supabase
        .from('profiles')
        .upsert({
          user_id: profile.user_id,
          username: profile.username,
          default_callback_number: profile.default_callback_number,
          street: profile.street,
          house_number: profile.house_number,
          postal_code: profile.postal_code,
          city: profile.city,
          country: profile.country,
          calendar_connected: profile.calendar_connected,
          updated_at: new Date().toISOString(),
        });

      if (error) throw error;

      toast.success('Profile saved successfully!');
      setIsEditing(false);
      // Reload profile to get fresh data
      await fetchProfile();
    } catch (error: any) {
      toast.error(error.message || 'Failed to save profile');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    setIsEditing(false);
    // Reload original data
    fetchProfile();
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setProfile({
      ...profile,
      [e.target.name]: e.target.value,
    });
  };

  if (loading) {
    return (
      <div className="p-8 max-w-3xl mx-auto">
        <Skeleton className="h-10 w-48 mb-6" />
        <Skeleton className="h-96 w-full rounded-2xl" />
      </div>
    );
  }

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Profile</h1>
        <p className="text-gray-600 mt-1">Manage your personal information</p>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        <Card className="rounded-2xl shadow-lg border-gray-200">
          <CardHeader>
            <CardTitle>Personal Information</CardTitle>
            <CardDescription>
              This information will be used for your requests
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                name="username"
                placeholder="Your name"
                value={profile.username}
                onChange={handleChange}
                disabled={!isEditing || saving}
                className="rounded-lg"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="default_callback_number">My Callback Number</Label>
              <Input
                id="default_callback_number"
                name="default_callback_number"
                type="tel"
                placeholder="+49 123 456789"
                value={profile.default_callback_number}
                onChange={handleChange}
                disabled={!isEditing || saving}
                className="rounded-lg"
              />
              <p className="text-xs text-gray-500">
                This number will be used automatically for new requests
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="street">Street</Label>
              <Input
                id="street"
                name="street"
                placeholder="Musterstraße"
                value={profile.street}
                onChange={handleChange}
                disabled={!isEditing || saving}
                className="rounded-lg"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="house_number">House Number</Label>
                <Input
                  id="house_number"
                  name="house_number"
                  placeholder="123"
                  value={profile.house_number}
                  onChange={handleChange}
                  disabled={!isEditing || saving}
                  className="rounded-lg"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="postal_code">Postal Code</Label>
                <Input
                  id="postal_code"
                  name="postal_code"
                  placeholder="12345"
                  value={profile.postal_code}
                  onChange={handleChange}
                  disabled={!isEditing || saving}
                  className="rounded-lg"
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="city">City</Label>
              <Input
                id="city"
                name="city"
                placeholder="Berlin"
                value={profile.city}
                onChange={handleChange}
                disabled={!isEditing || saving}
                className="rounded-lg"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="country">Country</Label>
              <Input
                id="country"
                name="country"
                placeholder="Germany"
                value={profile.country}
                onChange={handleChange}
                disabled={!isEditing || saving}
                className="rounded-lg"
              />
            </div>
          </CardContent>
        </Card>

        <Card className="rounded-2xl shadow-lg border-gray-200">
          <CardHeader>
            <CardTitle>Calendar Integration</CardTitle>
            <CardDescription>
              Connect your calendar for automatic appointment entries
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-violet-100 flex items-center justify-center">
                  <Calendar className="w-5 h-5 text-violet-600" />
                </div>
                <div>
                  <p className="font-medium text-gray-900">Google Calendar</p>
                  <p className="text-sm text-gray-500">
                    {profile.calendar_connected ? 'Connected' : 'Not connected'}
                  </p>
                </div>
              </div>
              <Button
                type="button"
                variant="outline"
                disabled
                className="rounded-xl"
              >
                Coming soon
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="rounded-2xl shadow-lg border-gray-200">
          <CardHeader>
            <CardTitle>Security</CardTitle>
            <CardDescription>
              Manage your security settings
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button
              type="button"
              variant="outline"
              disabled
              className="rounded-xl"
            >
              Change Password (Coming soon)
            </Button>
          </CardContent>
        </Card>

        <div className="flex gap-3">
          {!isEditing ? (
            <>
              <Button
                type="button"
                variant="outline"
                onClick={() => router.push('/dashboard')}
                className="flex-1 rounded-xl"
              >
                Back to Dashboard
              </Button>
              <Button
                type="button"
                onClick={() => setIsEditing(true)}
                className="flex-1 rounded-xl bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700"
              >
                Edit Profile
              </Button>
            </>
          ) : (
            <>
              <Button
                type="button"
                variant="outline"
                onClick={handleCancel}
                disabled={saving}
                className="flex-1 rounded-xl"
              >
                Cancel
              </Button>
              <Button
                type="submit"
                disabled={saving}
                className="flex-1 rounded-xl bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700"
              >
                {saving ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Saving...
                  </>
                ) : (
                  'Save Changes'
                )}
              </Button>
            </>
          )}
        </div>
      </form>
    </div>
  );
}