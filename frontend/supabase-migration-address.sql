-- Migration: Adress-Felder strukturieren
-- Führe dieses SQL in deinem Supabase SQL Editor aus

-- Schritt 1: Alte address Spalte umbenennen (als Backup)
ALTER TABLE profiles RENAME COLUMN address TO address_old;

-- Schritt 2: Neue strukturierte Adress-Spalten hinzufügen
ALTER TABLE profiles ADD COLUMN street text;
ALTER TABLE profiles ADD COLUMN house_number text;
ALTER TABLE profiles ADD COLUMN postal_code text;
ALTER TABLE profiles ADD COLUMN city text;
ALTER TABLE profiles ADD COLUMN country text DEFAULT 'Germany';

-- Schritt 3: Optional - Alte Daten migrieren (falls bereits User existieren)
-- Kommentiere diese Zeilen aus, wenn du bestehende Daten migrieren möchtest:
-- UPDATE profiles SET 
--   street = 'Musterstraße',
--   house_number = '1',
--   postal_code = '12345',
--   city = 'Berlin',
--   country = 'Germany'
-- WHERE address_old IS NOT NULL AND address_old != '';

-- Schritt 4: Optional - Alte Spalte löschen (erst nach erfolgreicher Migration!)
-- Führe dies erst aus, wenn du sicher bist, dass alles funktioniert:
-- ALTER TABLE profiles DROP COLUMN address_old;

-- Fertig! Die Tabelle hat jetzt strukturierte Adress-Felder.