-- ============================================
-- KOMPLETTER FIX: Profile-Erstellung & RLS
-- Führe dieses komplette Script in Supabase aus
-- ============================================

-- ============================================
-- SCHRITT 1: Alte Policies löschen
-- ============================================

DROP POLICY IF EXISTS "Users can view own profile" ON profiles;
DROP POLICY IF EXISTS "Users can insert own profile" ON profiles;
DROP POLICY IF EXISTS "Users can update own profile" ON profiles;
DROP POLICY IF EXISTS "Enable read access for users" ON profiles;
DROP POLICY IF EXISTS "Enable insert for authenticated users" ON profiles;
DROP POLICY IF EXISTS "Enable update for users" ON profiles;

-- ============================================
-- SCHRITT 2: Neue, funktionierende RLS Policies
-- ============================================

-- SELECT: User kann eigenes Profil lesen
CREATE POLICY "profiles_select_policy"
  ON profiles FOR SELECT
  USING (auth.uid() = user_id);

-- INSERT: Authentifizierte User können Profile erstellen
CREATE POLICY "profiles_insert_policy"
  ON profiles FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

-- UPDATE: User kann eigenes Profil aktualisieren
CREATE POLICY "profiles_update_policy"
  ON profiles FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- DELETE: User kann eigenes Profil löschen (optional)
CREATE POLICY "profiles_delete_policy"
  ON profiles FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);

-- ============================================
-- SCHRITT 3: Database Trigger für automatische Profile-Erstellung
-- ============================================

-- Alte Trigger/Funktion löschen falls vorhanden
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
DROP FUNCTION IF EXISTS public.handle_new_user();

-- Neue Trigger-Funktion erstellen
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER
SECURITY DEFINER
SET search_path = public
LANGUAGE plpgsql
AS $$
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
    NEW.id,
    COALESCE(NEW.raw_user_meta_data->>'username', split_part(NEW.email, '@', 1)),
    COALESCE(NEW.raw_user_meta_data->>'phone', ''),
    COALESCE(NEW.raw_user_meta_data->>'street', ''),
    COALESCE(NEW.raw_user_meta_data->>'house_number', ''),
    COALESCE(NEW.raw_user_meta_data->>'postal_code', ''),
    COALESCE(NEW.raw_user_meta_data->>'city', ''),
    COALESCE(NEW.raw_user_meta_data->>'country', 'Germany'),
    false
  );
  RETURN NEW;
EXCEPTION
  WHEN others THEN
    -- Log error but don't fail user creation
    RAISE WARNING 'Could not create profile for user %: %', NEW.id, SQLERRM;
    RETURN NEW;
END;
$$;

-- Trigger erstellen
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_new_user();

-- ============================================
-- SCHRITT 4: Fehlende Profile für bestehende User erstellen
-- ============================================

-- Erstelle Profile für alle User ohne Profil
INSERT INTO profiles (
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
SELECT 
  u.id,
  COALESCE(u.raw_user_meta_data->>'username', split_part(u.email, '@', 1)),
  COALESCE(u.raw_user_meta_data->>'phone', ''),
  COALESCE(u.raw_user_meta_data->>'street', ''),
  COALESCE(u.raw_user_meta_data->>'house_number', ''),
  COALESCE(u.raw_user_meta_data->>'postal_code', ''),
  COALESCE(u.raw_user_meta_data->>'city', ''),
  COALESCE(u.raw_user_meta_data->>'country', 'Germany'),
  false
FROM auth.users u
LEFT JOIN profiles p ON u.id = p.user_id
WHERE p.user_id IS NULL;

-- ============================================
-- SCHRITT 5: Prüfungen
-- ============================================

-- Prüfe ob Trigger existiert
SELECT 
  tgname as trigger_name,
  tgenabled as enabled
FROM pg_trigger 
WHERE tgname = 'on_auth_user_created';

-- Prüfe User mit/ohne Profile
SELECT 
  u.email,
  u.created_at as user_created,
  p.username,
  p.city,
  p.created_at as profile_created,
  CASE 
    WHEN p.user_id IS NULL THEN '❌ KEIN PROFIL'
    ELSE '✅ Profil vorhanden'
  END as status
FROM auth.users u
LEFT JOIN profiles p ON u.id = p.user_id
ORDER BY u.created_at DESC;

-- Prüfe RLS Policies
SELECT 
  schemaname,
  tablename,
  policyname,
  permissive,
  roles,
  cmd
FROM pg_policies
WHERE tablename = 'profiles'
ORDER BY policyname;

-- ============================================
-- FERTIG!
-- ============================================

-- Wenn alles funktioniert, solltest du sehen:
-- 1. Trigger "on_auth_user_created" ist enabled
-- 2. Alle User haben Profile (✅ Profil vorhanden)
-- 3. 4 RLS Policies für profiles (SELECT, INSERT, UPDATE, DELETE)