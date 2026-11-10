// Arenly push watcher – pure decision logic (no network, no database).
// Given the current ESPN scoreboard entry of a match and what was already sent,
// decide which notifications to send and what to remember.

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
