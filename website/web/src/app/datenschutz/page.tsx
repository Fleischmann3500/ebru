import type { Metadata } from 'next';
import Rechtsseite from '@/components/Rechtsseite';
import { firma } from '@/lib/content';

export const metadata: Metadata = { title: 'Datenschutz' };

// Grundlage: Datenschutzinformation von estilo.at (Stand 25.11.2026), angepasst an die neue Seite:
// Hosting Vercel statt Netlify, Formular über Resend, keine Karte, keine Cookies, kein Browser-Speicher.
// VOR LIVEGANG PRÜFEN: Anbieterangaben und Auftragsverarbeitungsverträge von Vercel und Resend (siehe Projekt.md).
export default function Datenschutz() {
  return (
    <Rechtsseite titel="Datenschutz" stand="27. November 2026">
      <p>Diese Information beschreibt die Verarbeitung personenbezogener Daten beim Besuch der ESTILO-Website und bei einer Kontaktaufnahme.</p>

      <h2>1. Verantwortliche</h2>
      <p>{firma.inhaberin}<br />{firma.name}<br />{firma.strasse}<br />{firma.ort}, {firma.land}<br />Telefon: <a href={firma.telefonLink}>{firma.telefon}</a><br />E-Mail: <a href={`mailto:${firma.mail}`}>{firma.mail}</a></p>

      <h2>2. Bereitstellung und Hosting</h2>
      <p>Die Website wird über Vercel Inc., USA, bereitgestellt. Zur Auslieferung und Absicherung verarbeitet die Hosting-Infrastruktur insbesondere IP-Adresse, Datum und Uhrzeit, aufgerufene Adresse, Datenmenge, HTTP-Status, Referrer sowie Browser- und Geräteinformationen. Zweck ist ein sicherer, stabiler Betrieb und die Abwehr von Missbrauch. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO; unser berechtigtes Interesse besteht in der sicheren Bereitstellung des Webangebots.</p>
      <p>Vercel verarbeitet diese Daten für uns als Auftragsverarbeiter auf Grundlage eines Auftragsverarbeitungsvertrags. Eine Verarbeitung in den USA ist möglich; Vercel stützt Übermittlungen auf das EU-US Data Privacy Framework beziehungsweise auf EU-Standardvertragsklauseln. Weitere Informationen: <a href="https://vercel.com/legal/privacy-policy" target="_blank" rel="noopener noreferrer">Datenschutzinformation von Vercel</a>.</p>

      <h2>3. Kontaktformular und direkte Kontaktaufnahme</h2>
      <p>Wenn Sie das Formular absenden, werden Name, E-Mail-Adresse, die freiwillige Telefonnummer, das gewählte Thema und Ihre Nachricht an unseren Server bei Vercel übertragen und von dort über den E-Mail-Versanddienst Resend (USA) als E-Mail an {firma.mail} zugestellt. Sie erhalten eine Bestätigung an die angegebene Adresse. Name, E-Mail-Adresse und Nachricht sind Pflichtangaben; ohne sie können wir Ihre Anfrage nicht beantworten.</p>
      <p>Zum Schutz vor automatisierten Anfragen verwenden wir ein unsichtbares Zusatzfeld, eine Mindestausfülldauer und eine Begrenzung der Anfragen je IP-Adresse. Die IP-Adresse wird dafür nur kurzzeitig im Arbeitsspeicher des Servers gehalten und nicht dauerhaft gespeichert.</p>
      <p>Resend verarbeitet die Nachrichten für uns als Auftragsverarbeiter und speichert Versandprotokolle für einen begrenzten Zeitraum. Eine Verarbeitung in den USA ist möglich; die Übermittlung wird auf das EU-US Data Privacy Framework beziehungsweise EU-Standardvertragsklauseln gestützt. Weitere Informationen: <a href="https://resend.com/legal/privacy-policy" target="_blank" rel="noopener noreferrer">Datenschutzinformation von Resend</a>.</p>
      <p>Bei Kontaktaufnahme über das Formular, per E-Mail oder Telefon verarbeiten wir die mitgeteilten Kontakt- und Nachrichteninhalte zur Bearbeitung und Beantwortung. Für vertragliche und vorvertragliche Anfragen gilt Art. 6 Abs. 1 lit. b DSGVO, für sonstige Anfragen Art. 6 Abs. 1 lit. f DSGVO; unser berechtigtes Interesse ist die sachgerechte Kommunikation.</p>
      <p>Unser geschäftliches E-Mail-Postfach wird von World4You Internet Services GmbH, Wolfgang-Pauli-Straße 2, BT3, 4020 Linz, Österreich, als Auftragsverarbeiter betrieben.</p>
      <p>Kundenanfragen und Korrespondenz speichern wir nur so lange, wie dies für Bearbeitung, Geschäftsbeziehungen, gesetzliche Pflichten oder die Geltendmachung, Ausübung oder Verteidigung von Rechtsansprüchen erforderlich ist. Gespeicherte Anfragen werden mindestens jährlich überprüft. Steuerlich relevante Unterlagen werden nach den gesetzlichen Aufbewahrungspflichten aufbewahrt, grundsätzlich sieben Jahre gemäß § 132 BAO (Art. 6 Abs. 1 lit. c DSGVO).</p>

      <h2>4. Links zu Google</h2>
      <p>Die Website bindet keine Karte ein. Die Links „Route planen“, „Alle Bewertungen auf Google“ und „ESTILO auf Google bewerten“ stellen erst beim Anklicken eine Verbindung zum jeweiligen Google-Dienst her (Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland). Ab diesem Zeitpunkt gelten die Datenschutzbestimmungen von Google.</p>

      <h2>5. Cookies, Browser-Speicher und Statistik</h2>
      <p>Die Website setzt keine Cookies, legt keine Einträge im Browser-Speicher an und verwendet kein Besuchertracking oder Analysewerkzeug. Deshalb fragen wir auch keine Einwilligung dafür ab.</p>

      <h2>6. Schriften, Bilder und 3D-Inhalte</h2>
      <p>Schriften, Bilder und die Daten der 3D-Wohnung werden von unserem eigenen Webspace geladen. Es wird keine Verbindung zu einem externen Schrift-, Bild- oder Inhaltsdienst hergestellt.</p>

      <h2>7. Kundenbewertungen</h2>
      <p>Die dargestellten Bewertungen stammen aus unserem Google-Unternehmensprofil. Wir veröffentlichen eine Auswahl mit Erlaubnis der Verfasser und ohne Namen; Kürzungen sind mit […] gekennzeichnet. Eine Wiedererkennung anhand des Wortlauts der ursprünglichen Google-Bewertung kann weiterhin möglich sein. Rechtsgrundlage ist unser berechtigtes Interesse, Interessierten authentische Erfahrungen zugänglich zu machen (Art. 6 Abs. 1 lit. f DSGVO). Betroffene können unter <a href={`mailto:${firma.mail}`}>{firma.mail}</a> widersprechen; die Entfernung von unserer Website verändert die ursprüngliche Google-Bewertung nicht.</p>

      <h2>8. Rechte betroffener Personen</h2>
      <p>Nach Maßgabe der gesetzlichen Voraussetzungen bestehen insbesondere Rechte auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch. Zur Ausübung dieser Rechte genügt eine Nachricht an die oben genannte E-Mail-Adresse.</p>
      <p>Widerspruchsrecht: Soweit eine Verarbeitung auf Art. 6 Abs. 1 lit. f DSGVO beruht, können Sie aus Gründen, die sich aus Ihrer besonderen Situation ergeben, jederzeit Widerspruch einlegen.</p>
      <p>Sie haben außerdem das Recht auf Beschwerde bei der Österreichischen Datenschutzbehörde, Barichgasse 40–42, 1030 Wien, E-Mail: <a href="mailto:dsb@dsb.gv.at">dsb@dsb.gv.at</a>.</p>

      <h2>9. Automatisierte Entscheidungen</h2>
      <p>Es findet keine ausschließlich automatisierte Entscheidungsfindung einschließlich Profiling im Sinne von Art. 22 DSGVO statt.</p>
    </Rechtsseite>
  );
}
