import type { Metadata } from 'next';
import Rechtsseite from '@/components/Rechtsseite';
import { firma } from '@/lib/content';

export const metadata: Metadata = { title: 'Impressum', robots: { index: true } };

// Angaben übernommen von estilo.at/impressum (Stand 25.11.2026): § 5 ECG, § 25 MedienG.
export default function Impressum() {
  return (
    <Rechtsseite titel="Impressum" stand="27. November 2026">
      <p>Informationen über die Anbieterin dieser Website und Offenlegung nach § 25 Mediengesetz.</p>
      <h2>Diensteanbieterin</h2>
      <p>{firma.name}<br />Inhaberin: {firma.inhaberin}<br />Rechtsform: Einzelunternehmen ohne Firmenbucheintragung<br />{firma.strasse}<br />{firma.ort}<br />{firma.land}</p>
      <p>Telefon: <a href={firma.telefonLink}>{firma.telefon}</a><br />E-Mail: <a href={`mailto:${firma.mail}`}>{firma.mail}</a><br />Website: estilo.at</p>
      <h2>Unternehmensangaben</h2>
      <table><tbody>
        <tr><th scope="row">UID-Nummer</th><td>ATU80845757</td></tr>
        <tr><th scope="row">Gewerbe- und Aufsichtsbehörde</th><td>Bezirkshauptmannschaft Feldkirch</td></tr>
        <tr><th scope="row">Kammerzugehörigkeit</th><td>Wirtschaftskammer Vorarlberg</td></tr>
        <tr><th scope="row">Berufsbezeichnung</th><td>Gewerbetreibende</td></tr>
        <tr><th scope="row">Verleihungsstaat</th><td>Österreich</td></tr>
        <tr><th scope="row">Anwendbare Rechtsvorschriften</th><td>Gewerbeordnung 1994 (GewO), abrufbar im <a href="https://www.ris.bka.gv.at" target="_blank" rel="noopener noreferrer">Rechtsinformationssystem des Bundes</a>, sowie Dienstleistungsgesetz (DLG)</td></tr>
      </tbody></table>
      <h2>Gewerbeberechtigungen</h2>
      <h3>Gestalterische Einrichtungsvorschläge</h3>
      <p>GISA-Zahl 37267223. Erstellung von Einrichtungsvorschlägen nach rein optischen und geschmacklichen Gesichtspunkten unter Ausschluss jeder Beratungs-, Vorplanungs- und Planungstätigkeit, betreffend den Grundriss von Räumlichkeiten und deren haustechnischen Ausstattung.</p>
      <h3>Handelsgewerbe</h3>
      <p>GISA-Zahl 37267285. Handelsgewerbe mit Ausnahme der reglementierten Handelsgewerbe und Handelsagent.</p>
      <h2>Offenlegung gemäß § 25 Mediengesetz</h2>
      <table><tbody>
        <tr><th scope="row">Medieninhaberin und Herausgeberin</th><td>{firma.inhaberin}</td></tr>
        <tr><th scope="row">Wohnort</th><td>Dornbirn, Österreich</td></tr>
        <tr><th scope="row">Unternehmensgegenstand</th><td>Handel mit Möbeln und Einrichtungsgegenständen sowie Erstellung von Einrichtungsvorschlägen</td></tr>
        <tr><th scope="row">Grundlegende Richtung</th><td>Präsentation des Unternehmens sowie Information über dessen Produkte, Leistungen und Referenzen</td></tr>
      </tbody></table>
      <h2>Bildnachweis 3D-Szene</h2>
      <p>Einzelne Modelle, Texturen und das Umgebungsbild der 3D-Wohnung stammen von Poly Haven (polyhaven.com) und stehen unter der Lizenz CC0.</p>
    </Rechtsseite>
  );
}
