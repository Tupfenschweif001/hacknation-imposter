"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { toast } from "sonner";
import { Loader2, ArrowLeft } from "lucide-react";

export default function NewRequestPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    callback_number: "",
    number_to_call: "",
    preferred_time: "",
    radius_km: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const {
        data: { user },
      } = await supabase.auth.getUser();

      if (!user) {
        router.push("/login");
        return;
      }

      // 1. Get user profile for backend
      const { data: profile } = await supabase
        .from("profiles")
        .select("*")
        .eq("user_id", user.id)
        .single();

      // 2. Create request in Supabase
      const { data, error } = await supabase
        .from("requests")
        .insert([
          {
            user_id: user.id,
            title: formData.title,
            description: formData.description,
            callback_number: formData.callback_number,
            number_to_call: formData.number_to_call || null,
            preferred_time: formData.preferred_time,
            status: "queued",
          },
        ])
        .select()
        .single();

      if (error) throw error;

      toast.success("Request created successfully!");

      // 3. Send to backend for processing (non-blocking)
      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
      if (backendUrl) {
        fetch(`${backendUrl}/api/process-request`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            request_id: data.id,
            user_id: user.id,
            title: formData.title,
            description: formData.description,
            callback_number: formData.callback_number,
            number_to_call: formData.number_to_call || null,
            preferred_time: formData.preferred_time,
            user_profile: profile
              ? {
                  username: profile.username,
                  street: profile.street,
                  house_number: profile.house_number,
                  postal_code: profile.postal_code,
                  city: profile.city,
                  country: profile.country,
                }
              : null,
          }),
        }).catch((err) => {
          console.error("Backend call failed:", err);
          // Don't show error to user - request is already in DB
        });
      }

      // 4. Redirect to detail page
      router.push(`/requests/${data.id}`);
    } catch (error: any) {
      toast.error(error.message || "Failed to create request");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <Button
        variant="ghost"
        onClick={() => router.back()}
        className="mb-6 rounded-xl"
      >
        <ArrowLeft className="mr-2 h-4 w-4" />
        Back
      </Button>

      <Card className="rounded-2xl shadow-lg border-gray-200">
        <CardHeader>
          <CardTitle className="text-2xl">New Appointment Request</CardTitle>
          <CardDescription>
            Create a new request for the Voice AI Agent
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="title">
                Title <span className="text-red-500">*</span>
              </Label>
              <Input
                id="title"
                name="title"
                placeholder="e.g. Book dentist appointment"
                value={formData.title}
                onChange={handleChange}
                required
                disabled={loading}
                className="rounded-lg"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="description">
                Description <span className="text-red-500">*</span>
              </Label>
              <Textarea
                id="description"
                name="description"
                placeholder="Describe what the agent should do for you..."
                value={formData.description}
                onChange={handleChange}
                required
                disabled={loading}
                className="rounded-lg min-h-[120px]"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="number_to_call">
                Contact Number
              </Label>
              <Input
                id="number_to_call"
                name="number_to_call"
                type="tel"
                placeholder="+49 123 456789"
                value={formData.number_to_call}
                onChange={handleChange}
                disabled={loading}
                className="rounded-lg"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="preferred_time">
                Preferred Time Window <span className="text-red-500">*</span>
              </Label>
              <Input
                id="preferred_time"
                name="preferred_time"
                placeholder="e.g. next week, Monday 10-12 AM"
                value={formData.preferred_time}
                onChange={handleChange}
                required
                disabled={loading}
                className="rounded-lg"
              />
            </div>

            <div className="flex gap-3 pt-4">
              <Button
                type="button"
                variant="outline"
                onClick={() => router.back()}
                disabled={loading}
                className="flex-1 rounded-xl"
              >
                Cancel
              </Button>
              <Button
                type="submit"
                disabled={loading}
                className="flex-1 rounded-xl bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700"
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Creating...
                  </>
                ) : (
                  "Create Request"
                )}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
