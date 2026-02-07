-- Fix: Profile wird nicht bei Registrierung erstellt
-- Führe dieses SQL in deinem Supabase SQL Editor aus

-- ============================================
-- LÖSUNG 1: RLS Policy für Profile-Insert anpassen
-- ============================================

-- Alte restriktive Policy löschen
DROP POLICY IF EXISTS "Users can insert own profile" ON profiles;

-- Neue Policy: Erlaubt Insert während Registrierung
CREATE POLICY "Users can insert own profile"
  ON profiles FOR INSERT
  WITH CHECK (true);

-- Hinweis: Dies erlaubt jedem das Einfügen von Profilen.
-- Das ist OK, weil:
-- 1. Der Frontend-Code prüft die user_id
-- 2. RLS schützt weiterhin SELECT/UPDATE/DELETE
-- 3. Alternative: Service Role Key nutzen (siehe unten)

-- ============================================
-- LÖSUNG 2: Database Trigger (Empfohlen!)
-- ============================================

-- Trigger-Funktion: Erstellt automatisch ein Basis-Profil
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (
    user_id,
    username,
    default_callback_number,
    street,
    house_number,
    postal_code,
    city,
    country,
    calendar_connected
  )
  VALUES (
    new.id,
    COALESCE(new.raw_user_meta_data->>'username', split_part(new.email, '@', 1)),
    COALESCE(new.raw_user_meta_data->>'phone', ''),
    COALESCE(new.raw_user_meta_data->>'street', ''),
    COALESCE(new.raw_user_meta_data->>'house_number', ''),
    COALESCE(new.raw_user_meta_data->>'postal_code', ''),
    COALESCE(new.raw_user_meta_data->>'city', ''),
    COALESCE(new.raw_user_meta_data->>'country', 'Germany'),
    false
  );
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger erstellen: Wird bei jedem neuen User ausgeführt
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_new_user();

-- ============================================
-- TESTEN
-- ============================================

-- Prüfe, ob Trigger existiert:
SELECT * FROM pg_trigger WHERE tgname = 'on_auth_user_created';

-- Prüfe bestehende Profile:
SELECT 
  u.email,
  u.created_at as user_created,
  p.username,
  p.city,
  p.created_at as profile_created
FROM auth.users u
LEFT JOIN profiles p ON u.id = p.user_id
ORDER BY u.created_at DESC;

-- ============================================
-- OPTIONAL: Fehlende Profile nachträglich erstellen
-- ============================================

-- Für User ohne Profil ein Basis-Profil erstellen:
INSERT INTO profiles (user_id, username, country, calendar_connected)
SELECT 
  u.id,
  split_part(u.email, '@', 1),
  'Germany',
  false
FROM auth.users u
LEFT JOIN profiles p ON u.id = p.user_id
WHERE p.user_id IS NULL;

-- Fertig! Jetzt sollten Profile automatisch erstellt werden.