"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase";
import { Profile } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import { toast } from "sonner";
import { Loader2, Calendar } from "lucide-react";

export default function ProfilePage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [profile, setProfile] = useState<Profile>({
    user_id: "",
    username: "",
    default_callback_number: "",
    street: "",
    house_number: "",
    postal_code: "",
    city: "",
    country: "Germany",
    calendar_connected: false,
  });

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const {
        data: { user },
      } = await supabase.auth.getUser();

      if (!user) {
        router.push("/login");
        return;
      }

      const { data, error } = await supabase
        .from("profiles")
        .select("*")
        .eq("user_id", user.id);

      if (error) {
        throw error;
      }

      if (data && data.length > 0) {
        setProfile(data[0]);
      } else {
        // Create default profile
        setProfile({
          user_id: user.id,
          username: user.email?.split("@")[0] || "",
          default_callback_number: "",
          street: "",
          house_number: "",
          postal_code: "",
          city: "",
          country: "Germany",
          calendar_connected: false,
        });
      }
    } catch (error: any) {
      toast.error("Failed to load profile");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);

    try {
      const { error } = await supabase.from("profiles").upsert({
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

      toast.success("Profile saved successfully!");
      setIsEditing(false);
      // Reload profile to get fresh data
      await fetchProfile();
    } catch (error: any) {
      toast.error(error.message || "Failed to save profile");
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    setIsEditing(false);
    // Reload original data
    fetchProfile();
  };

  const validateField = (name: string, value: string): string => {
    const validationRules: Record<
      string,
      { pattern: RegExp; message: string }
    > = {
      house_number: {
        pattern: /^\d+[a-zA-Z]?(-\d+)?$/,
        message: "Nur Zahlen und optional Buchstaben (z.B. 12a)",
      },
      postal_code: {
        pattern: /^\d{5}$/,
        message: "PLZ muss genau 5 Ziffern haben",
      },
      city: {
        pattern: /^[a-zA-ZäöüÄÖÜß\s-]+$/,
        message: "Nur Buchstaben, Leerzeichen und Bindestriche erlaubt",
      },
      street: {
        pattern: /^[a-zA-ZäöüÄÖÜß0-9\s.-]+$/,
        message: "Nur Buchstaben, Zahlen, Leerzeichen und . - erlaubt",
      },
      country: {
        pattern: /^[a-zA-ZäöüÄÖÜß\s-]+$/,
        message: "Nur Buchstaben, Leerzeichen und Bindestriche erlaubt",
      },
      default_callback_number: {
        pattern: /^[\d\s\-+()]+$/,
        message: "Nur Zahlen, +, -, Leerzeichen und Klammern erlaubt",
      },
    };

    if (!value) return ""; // Empty is ok for optional fields

    const rule = validationRules[name];
    if (rule && !rule.pattern.test(value)) {
      return rule.message;
    }

    return "";
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;

    setProfile({
      ...profile,
      [name]: value,
    });

    // Validate field
    const error = validateField(name, value);
    setErrors({
      ...errors,
      [name]: error,
    });
  };

  const hasErrors = () => {
    return Object.values(errors).some((error) => error !== "");
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
        <h1 className="text-3xl font-bold text-foreground">Profile</h1>
        <p className="text-muted-foreground mt-1">
          Manage your personal information
        </p>
      </div>

      <div className="space-y-6">
        <Card className="rounded-2xl shadow-lg border-border">
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
              {errors.username && (
                <p className="text-xs text-red-600 dark:text-red-400">
                  {errors.username}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="default_callback_number">
                My Callback Number
              </Label>
              <Input
                id="default_callback_number"
                name="default_callback_number"
                type="tel"
                placeholder="+49 123 456789"
                value={profile.default_callback_number}
                onChange={handleChange}
                disabled={!isEditing || saving}
                className={`rounded-lg ${errors.default_callback_number ? "border-red-500" : ""}`}
              />
              {errors.default_callback_number && (
                <p className="text-xs text-red-600 dark:text-red-400">
                  {errors.default_callback_number}
                </p>
              )}
              <p className="text-xs text-muted-foreground">
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
                className={`rounded-lg ${errors.street ? "border-red-500" : ""}`}
              />
              {errors.street && (
                <p className="text-xs text-red-600 dark:text-red-400">
                  {errors.street}
                </p>
              )}
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
                  className={`rounded-lg ${errors.house_number ? "border-red-500" : ""}`}
                />
                {errors.house_number && (
                  <p className="text-xs text-red-600 dark:text-red-400">
                    {errors.house_number}
                  </p>
                )}
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
                  className={`rounded-lg ${errors.postal_code ? "border-red-500" : ""}`}
                  maxLength={5}
                />
                {errors.postal_code && (
                  <p className="text-xs text-red-600 dark:text-red-400">
                    {errors.postal_code}
                  </p>
                )}
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
                className={`rounded-lg ${errors.city ? "border-red-500" : ""}`}
              />
              {errors.city && (
                <p className="text-xs text-red-600 dark:text-red-400">
                  {errors.city}
                </p>
              )}
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
                className={`rounded-lg ${errors.country ? "border-red-500" : ""}`}
              />
              {errors.country && (
                <p className="text-xs text-red-600 dark:text-red-400">
                  {errors.country}
                </p>
              )}
            </div>
          </CardContent>
        </Card>

        <Card className="rounded-2xl shadow-lg border-border">
          <CardHeader>
            <CardTitle>Calendar Integration</CardTitle>
            <CardDescription>
              Connect your calendar for automatic appointment entries
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between p-4 bg-muted/50 dark:bg-muted rounded-xl">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-violet-100 dark:bg-violet-950 flex items-center justify-center">
                  <Calendar className="w-5 h-5 text-violet-600 dark:text-violet-400" />
                </div>
                <div>
                  <p className="font-medium text-foreground">Google Calendar</p>
                  <p className="text-sm text-muted-foreground">
                    {profile.calendar_connected ? "Connected" : "Not connected"}
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
      </div>
      <div>
        <br />
      </div>

      <div className="flex gap-3">
        {!isEditing ? (
          <>
            <Button
              variant="outline"
              onClick={() => router.push("/dashboard")}
              className="flex-1 rounded-xl"
            >
              Back to Dashboard
            </Button>
            <Button
              onClick={() => setIsEditing(true)}
              className="flex-1 rounded-xl bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700"
            >
              Edit Profile
            </Button>
          </>
        ) : (
          <>
            <Button
              variant="outline"
              onClick={handleCancel}
              disabled={saving}
              className="flex-1 rounded-xl"
            >
              Cancel
            </Button>
            <Button
              onClick={handleSave}
              disabled={saving || hasErrors()}
              className="flex-1 rounded-xl bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700"
            >
              {saving ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Saving...
                </>
              ) : (
                "Save Changes"
              )}
            </Button>
          </>
        )}
      </div>
    </div>
  );
}
