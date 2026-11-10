// Arenly push watcher – SINGLE-FILE version for the Supabase dashboard editor.
// Same code as index.ts + logic.ts (generated). Paste the whole file into the function `push-watch`.
import { createClient } from 'npm:@supabase/supabase-js@2.118.0';
import webpush from 'npm:web-push@3.6.7';


export const CUPS: Record<string, string[]> = {
  'ger.1': ['ger.dfb_pokal'], 'ger.2': ['ger.dfb_pokal'], 'eng.1': ['eng.fa', 'eng.league_cup'], 'eng.2': ['eng.fa', 'eng.league_cup'],
  'esp.1': ['esp.copa_del_rey'], 'ita.1': ['ita.coppa_italia'], 'fra.1': ['fra.coupe_de_france'], 'ned.1': ['ned.cup'],
  'por.1': ['por.taca.portugal'], 'sco.1': ['sco.tennents'], 'usa.1': ['usa.open'],
};
export const EURO = ['uefa.champions', 'uefa.europa', 'uefa.europa.conf'];
export const NATION = ['uefa.nations', 'fifa.friendly', 'fifa.worldq.uefa', 'uefa.euroq', 'fifa.world', 'uefa.euro'];

const COMP: Record<string, string> = {
  'ger.1': 'Bundesliga', 'ger.2': '2. Bundesliga', 'ger.dfb_pokal': 'DFB-Pokal', 'eng.1': 'Premier League', 'esp.1': 'LaLiga',
  'ita.1': 'Serie A', 'fra.1': 'Ligue 1', 'uefa.champions': 'Champions League', 'uefa.europa': 'Europa League',
  'uefa.europa.conf': 'Conference League', 'uefa.nations': 'Nations League', 'fifa.friendly': 'Testspiel',
  'fifa.worldq.uefa': 'WM-Quali', 'uefa.euroq': 'EM-Quali', 'fifa.world': 'WM', 'uefa.euro': 'EM',
};
const NAMES: Record<string, string> = {
  'Bayern Munich': 'Bayern München', 'Bayern': 'Bayern', 'Cologne': 'Köln', 'FC Cologne': '1. FC Köln', 'Nuremberg': 'Nürnberg',
  'Monchengladbach': 'Mönchengladbach', "M'gladbach": 'Gladbach', 'Dusseldorf': 'Düsseldorf', 'Greuther Furth': 'Greuther Fürth',
  'Inter Milan': 'Inter Mailand', 'AC Milan': 'AC Mailand', 'Napoli': 'Neapel', 'Roma': 'AS Rom', 'Lazio': 'Lazio Rom',
  'Germany': 'Deutschland', 'Austria': 'Österreich', 'Switzerland': 'Schweiz', 'Netherlands': 'Niederlande', 'Serbia': 'Serbien',
  'Greece': 'Griechenland', 'France': 'Frankreich', 'Spain': 'Spanien', 'Italy': 'Italien', 'Belgium': 'Belgien', 'Denmark': 'Dänemark',
  'Poland': 'Polen', 'Croatia': 'Kroatien', 'Turkey': 'Türkei', 'Türkiye': 'Türkei', 'Hungary': 'Ungarn', 'Scotland': 'Schottland',
  'Czechia': 'Tschechien', 'Czech Republic': 'Tschechien', 'Sweden': 'Schweden', 'Norway': 'Norwegen', 'Brazil': 'Brasilien',
  'Argentina': 'Argentinien', 'Slovakia': 'Slowakei', 'Northern Ireland': 'Nordirland', 'Ireland': 'Irland',
};
export const deName = (n: string) => NAMES[n] ?? n;
export const compLabel = (slug: string) => COMP[slug] ?? '';
const berlinTime = (ms: number) => new Date(ms).toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Berlin' });

export type Sent = { lineup?: boolean; kickoff?: boolean; ft?: boolean; goals?: string[] };
export type Kind = 'goals' | 'kickoff' | 'fulltime' | 'lineup';
export type Note = { kind: Kind; teamIds: string[]; payload: { title: string; body: string; url: string; tag: string } };

type Goal = { key: string; teamId: string; who: string; min: string; own: boolean; pen: boolean };
export function scoringPlays(c: any, homeId: string, awayId: string): Goal[] {
  return (c?.details ?? []).filter((x: any) => x.scoringPlay && !x.shootout).map((x: any) => {
    const own = !!x.ownGoal, scorerTeam = String(x.team?.id ?? '');
    // ESPN files an own goal under the player's team – the goal counts for the other side
    const teamId = own ? (scorerTeam === homeId ? awayId : homeId) : scorerTeam;
    const who = x.athletesInvolved?.[0]?.displayName ?? '';
    const min = x.clock?.displayValue ?? '';
    return { key: `${scorerTeam}|${min}|${who}`, teamId, who, min, own, pen: !!x.penaltyKick };
  });
}

/** Decide what to send for one match. `prev` is the stored state (or null the first time we see the match). */
export function decide(input: { id: string; slug: string; c: any; prev: { sent?: Sent; home_score?: number; away_score?: number } | null;
                                hasLineup?: boolean; now?: number }) {
  const { id, slug, c, prev } = input;
  const now = input.now ?? Date.now();
  const st = c?.status?.type ?? {};
  const state: string = st.state ?? 'pre';
  const H = c.competitors.find((x: any) => x.homeAway === 'home'), A = c.competitors.find((x: any) => x.homeAway === 'away');
  const homeId = String(H.team.id), awayId = String(A.team.id);
  const hn = deName(H.team.shortDisplayName ?? H.team.displayName), an = deName(A.team.shortDisplayName ?? A.team.displayName);
  const hs = Number(H.score ?? 0) || 0, as = Number(A.score ?? 0) || 0;
  const teamIds = [homeId, awayId];
  const url = `#/match/${slug}/${id}`;
  const kickoff = new Date(c.date).getTime();
  const sent: Sent = structuredClone(prev?.sent ?? {});
  const goals = scoringPlays(c, homeId, awayId);
  const notes: Note[] = [];
  const comp = compLabel(slug);

  if (!prev){
    // first sighting: remember silently what already happened – never send back-dated messages
    if (state !== 'pre'){ sent.kickoff = true; sent.lineup = true; }
    if (state === 'post') sent.ft = true;
    sent.goals = goals.map(g => g.key);
  }

  // line-ups: about an hour before kick-off, once ESPN has the starting XI
  if (state === 'pre' && !sent.lineup && input.hasLineup && kickoff - now < 75 * 60e3 && kickoff - now > -15 * 60e3){
    sent.lineup = true;
    notes.push({ kind: 'lineup', teamIds, payload: { title: `📋 Aufstellung: ${hn} – ${an}`,
      body: `Die Startelf ist da. Anpfiff um ${berlinTime(kickoff)} Uhr${comp ? ' · ' + comp : ''}.`, url: url + '/lineups', tag: `${id}-lineup` } });
  }
  if ((state === 'in' || state === 'post') && !sent.kickoff){
    sent.kickoff = true;
    if (state === 'in') notes.push({ kind: 'kickoff', teamIds, payload: { title: `🟢 Anpfiff: ${hn} – ${an}`,
      body: comp ? `${comp} – das Spiel läuft.` : 'Das Spiel läuft.', url, tag: `${id}-kickoff` } });
  }
  if (state === 'in' || state === 'post'){
    const known = new Set(sent.goals ?? []);
    const fresh = goals.filter(g => !known.has(g.key));
    for (const g of fresh){
      known.add(g.key);
      const team = g.teamId === homeId ? hn : an;
      notes.push({ kind: 'goals', teamIds, payload: {
        title: `⚽ TOR für ${team}!${g.own ? ' (Eigentor)' : g.pen ? ' (Elfmeter)' : ''}`,
        body: `${hn} ${hs}:${as} ${an}${g.who ? ' · ' + g.who : ''}${g.min ? ` (${g.min})` : ''}`, url, tag: `${id}-goal-${g.key}` } });
    }
    // the score moved but ESPN has no scorer detail yet → still tell people
    const prevTotal = (prev?.home_score ?? hs) + (prev?.away_score ?? as);
    if (prev && !fresh.length && hs + as > prevTotal){
      const team = hs > (prev.home_score ?? 0) ? hn : an;
      notes.push({ kind: 'goals', teamIds, payload: { title: `⚽ TOR für ${team}!`, body: `${hn} ${hs}:${as} ${an}`, url, tag: `${id}-score-${hs}-${as}` } });
    }
    sent.goals = [...known];
  }
  if (state === 'post' && st.completed && !sent.ft){
    sent.ft = true;
    notes.push({ kind: 'fulltime', teamIds, payload: { title: `🏁 Abpfiff: ${hn} ${hs}:${as} ${an}`,
      body: [comp, st.detail && /AET|PEN/i.test(st.detail) ? (/PEN/i.test(st.detail) ? 'nach Elfmeterschießen' : 'nach Verlängerung') : ''].filter(Boolean).join(' · ') || 'Endstand',
      url, tag: `${id}-ft` } });
  }
  return { notes, row: { event_id: id, slug, state, home_score: hs, away_score: as, sent, kickoff: new Date(kickoff).toISOString(), updated_at: new Date(now).toISOString() } };
}

export const PREF: Record<Kind, string> = { goals: 'goals', kickoff: 'matchday', fulltime: 'matchday', lineup: 'lineup' };

// Arenly push watcher – Supabase Edge Function, triggered every minute by pg_cron (see ../../push.sql).
// Looks at today's matches of every subscribed club / national team on ESPN and sends Web Push
// notifications for line-ups, kick-off, goals and full time.

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
