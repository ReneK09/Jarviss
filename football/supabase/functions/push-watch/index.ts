// Arenly push watcher – Supabase Edge Function, triggered every minute by pg_cron (see ../../push.sql).
// Looks at today's matches of every subscribed club / national team on ESPN and sends Web Push
// notifications for line-ups, kick-off, goals and full time.
import { createClient } from 'npm:@supabase/supabase-js@2.118.0';
import webpush from 'npm:web-push@3.6.7';
import { CUPS, EURO, NATION, PREF, decide, type Note } from './logic.ts';

const ESPN = 'https://site.api.espn.com/apis/site/v2/sports/soccer';
const json = (o: unknown, status = 200) => new Response(JSON.stringify(o), { status, headers: { 'content-type': 'application/json' } });
const ymd = (d: Date) => d.toISOString().slice(0, 10).replace(/-/g, '');

Deno.serve(async (req) => {
  const secret = Deno.env.get('CRON_SECRET');
  if (!secret || req.headers.get('x-cron-secret') !== secret) return json({ error: 'forbidden' }, 403);
  webpush.setVapidDetails(Deno.env.get('VAPID_SUBJECT') ?? 'mailto:info@arenly.app',
    Deno.env.get('VAPID_PUBLIC_KEY')!, Deno.env.get('VAPID_PRIVATE_KEY')!);
  const sb = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!, { auth: { persistSession: false } });

  const { data: subs, error } = await sb.from('push_subscriptions').select('endpoint,p256dh,auth,club_id,club_slug,nation_id,prefs,app_url');
  if (error) return json({ error: error.message }, 500);
  if (!subs?.length) return json({ ok: true, subscriptions: 0 });

  // competitions to look at and the team ids that matter there
  const watch = new Map<string, Set<string>>();
  const add = (slug: string, id: string) => (watch.get(slug) ?? watch.set(slug, new Set()).get(slug)!).add(String(id));
  for (const s of subs){
    if (s.club_id && s.club_slug) [s.club_slug, ...(CUPS[s.club_slug] ?? []), ...EURO].forEach(sl => add(sl, s.club_id));
    if (s.nation_id) NATION.forEach(sl => add(sl, s.nation_id));
  }
  const now = new Date(), days = [ymd(new Date(now.getTime() - 864e5)), ymd(now)];
  const events = new Map<string, { c: any; slug: string }>();
  await Promise.all([...watch.entries()].flatMap(([slug, ids]) => days.map(async d => {
    try {
      const r = await fetch(`${ESPN}/${slug}/scoreboard?dates=${d}`);
      if (!r.ok) return;
      for (const e of (await r.json()).events ?? []){
        const c = e.competitions?.[0];
        if ((c?.competitors ?? []).some((x: any) => ids.has(String(x.team?.id)))) events.set(String(e.id), { c: { ...c, date: c.date ?? e.date }, slug });
      }
    } catch { /* one competition failing must not stop the rest */ }
  })));
  if (!events.size) return json({ ok: true, subscriptions: subs.length, events: 0 });

  const { data: rows } = await sb.from('push_state').select('event_id,home_score,away_score,sent').in('event_id', [...events.keys()]);
  const prev = new Map((rows ?? []).map((r: any) => [r.event_id, r]));
  const outbox: Note[] = [], upserts: unknown[] = [];

  for (const [id, { c, slug }] of events){
    const p = prev.get(id) ?? null;
    let hasLineup = false;
    const kickoff = new Date(c.date).getTime();
    if (c.status?.type?.state === 'pre' && !p?.sent?.lineup && kickoff - now.getTime() < 75 * 60e3){
      try {
        const s = await (await fetch(`${ESPN}/${slug}/summary?event=${id}`)).json();
        hasLineup = (s.rosters ?? []).some((r: any) => (r.roster ?? []).some((x: any) => x.starter));
      } catch { /* try again next minute */ }
    }
    const { notes, row } = decide({ id, slug, c, prev: p, hasLineup, now: now.getTime() });
    outbox.push(...notes); upserts.push(row);
  }
  if (upserts.length) await sb.from('push_state').upsert(upserts);

  // deliver
  let sent = 0; const gone = new Set<string>();
  await Promise.all(outbox.flatMap(n => subs
    .filter(s => (n.teamIds.includes(String(s.club_id)) || n.teamIds.includes(String(s.nation_id))) && (s.prefs?.[PREF[n.kind]] ?? true))
    .map(async s => {
      const payload = { ...n.payload, url: (s.app_url ?? '') + n.payload.url };
      try {
        await webpush.sendNotification({ endpoint: s.endpoint, keys: { p256dh: s.p256dh, auth: s.auth } }, JSON.stringify(payload), { TTL: 900, urgency: 'high' });
        sent++;
      } catch (err: any) {
        if (err?.statusCode === 404 || err?.statusCode === 410) gone.add(s.endpoint);   // device unsubscribed
        else console.error('push failed', err?.statusCode, err?.body);
      }
    })));
  if (gone.size) await sb.from('push_subscriptions').delete().in('endpoint', [...gone]);
  // housekeeping: forget old matches
  await sb.from('push_state').delete().lt('updated_at', new Date(now.getTime() - 3 * 864e5).toISOString());

  return json({ ok: true, subscriptions: subs.length, events: events.size, notifications: outbox.length, delivered: sent, removed: gone.size });
});
