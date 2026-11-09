/* Arenly configuration
 *
 * Paste your Supabase project values here to switch on real accounts
 * (Supabase dashboard → Project Settings → API).
 * Leave them empty to run in LOCAL MODE (profile stored only on this device).
 *
 * The "anon" key is meant to be public: it is shipped to every browser and
 * protected by the Row Level Security policies in supabase/schema.sql.
 * NEVER put the "service_role" key here.
 */
window.ARENLY_CONFIG = {
  supabaseUrl: '',        // e.g. 'https://abcdefghijkl.supabase.co'
  supabaseAnonKey: '',    // the "anon public" key
  appleSignIn: false,     // true once "Sign in with Apple" is set up in Supabase → Authentication → Providers
};
