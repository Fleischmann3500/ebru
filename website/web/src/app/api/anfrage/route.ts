import { NextResponse } from 'next/server';
import { Resend } from 'resend';
import { firma } from '@/lib/content';

// Anfrage -> zwei Mails: an ESTILO und eine Bestätigung an die Person. Schutz: Honeypot, Mindestzeit, IP-Limit.
const LIMIT = new Map<string, number[]>();
const esc = (s: string) => s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]!);

export async function POST(req: Request) {
  const ip = req.headers.get('x-forwarded-for')?.split(',')[0]?.trim() || 'unbekannt';
  const jetzt = Date.now();
  const liste = (LIMIT.get(ip) || []).filter((t) => jetzt - t < 60 * 60 * 1000);
  if (liste.length >= 5) return NextResponse.json({ fehler: 'Zu viele Anfragen in kurzer Zeit.' }, { status: 429 });

  let d: Record<string, unknown>;
  try { d = await req.json(); } catch { return NextResponse.json({ fehler: 'Ungültige Anfrage.' }, { status: 400 }); }
  const text = (k: string, max = 200) => String(d[k] ?? '').trim().slice(0, max);
  const name = text('name'), email = text('email'), telefon = text('telefon', 60), thema = text('thema', 60), nachricht = text('nachricht', 4000);

  // Bot-Falle und Mindestzeit (unter 3 Sekunden ausgefüllt = Bot): still bestätigen, nichts senden
  if (text('website') || Number(d.dauer) < 3000) return NextResponse.json({ ok: true });
  if (!name || !nachricht || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return NextResponse.json({ fehler: 'Bitte Name, E-Mail und Nachricht ausfüllen.' }, { status: 400 });

  const key = process.env.RESEND_API_KEY;
  const von = process.env.ANFRAGE_VON || 'ESTILO Website <anfrage@estilo.at>';
  const an = process.env.ANFRAGE_AN || firma.mail;
  if (!key) return NextResponse.json({ fehler: 'Das Formular ist gerade nicht eingerichtet.' }, { status: 503 });

  liste.push(jetzt); LIMIT.set(ip, liste);
  const resend = new Resend(key);
  const zeilen = [['Name', name], ['E-Mail', email], ['Telefon', telefon || '–'], ['Thema', thema]];
  const html = `<p style="font:16px/1.5 sans-serif">${zeilen.map(([k, v]) => `<b>${k}:</b> ${esc(v)}`).join('<br>')}</p><p style="font:16px/1.5 sans-serif;white-space:pre-wrap">${esc(nachricht)}</p>`;
  try {
    const a = await resend.emails.send({ from: von, to: an, replyTo: email, subject: `Anfrage: ${thema} (${name})`, html });
    if (a.error) throw new Error(a.error.message);
    await resend.emails.send({
      from: von, to: email, replyTo: an, subject: 'Ihre Anfrage bei ESTILO',
      html: `<p style="font:16px/1.6 sans-serif">Guten Tag ${esc(name)},<br><br>danke für Ihre Nachricht. Ich melde mich bei Ihnen.<br><br>Ebru Filiz<br>ESTILO Einrichtungsstudio<br>${firma.strasse}, ${firma.ort}<br>${firma.telefon}</p><hr><p style="font:14px/1.5 sans-serif;color:#555;white-space:pre-wrap">${esc(nachricht)}</p>`,
    });
    return NextResponse.json({ ok: true });
  } catch (e) {
    console.error('Resend', e);
    return NextResponse.json({ fehler: 'Senden hat nicht geklappt.' }, { status: 502 });
  }
}
