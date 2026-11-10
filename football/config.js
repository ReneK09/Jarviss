/* Arenly configuration
 *
 * Paste your Supabase project values here to switch on real accounts
 * (Supabase dashboard → Project Settings → API).
 * Leave them empty to run in LOCAL MODE (profile stored only on this device).
 *
 * The publishable / "anon" key is meant to be public: it is shipped to every browser and
 * protected by the Row Level Security policies in supabase/schema.sql.
 * NEVER put the "service_role" / secret (sb_secret_…) key here.
 */
window.ARENLY_CONFIG = {
  supabaseUrl: 'https://hyomumbaokxfqhhvrgpf.supabase.co',
  supabaseAnonKey: 'sb_publishable_XfrAXsi610cvNITj2x-ZOA_ZMz6aBn3',   // publishable (or legacy "anon public") key
  appleSignIn: false,
  vapidPublicKey: 'BGUmH9FuUqR7h-infJko2XjmK6OTBlpqO8qwWzbvy0-bt4Vo8x_7tgkfqWj2tbm8sQlrHdUy5-Zr91DjFsPCkU4',   // Web Push (public half; the private key lives only in Supabase secrets)     // true once "Sign in with Apple" is set up in Supabase → Authentication → Providers
};
