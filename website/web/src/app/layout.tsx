import type { Metadata, Viewport } from 'next';
import './globals.css';
import { firma } from '@/lib/content';

export const metadata: Metadata = {
  metadataBase: new URL('https://estilo.at'),
  title: { default: 'ESTILO Einrichtungsstudio in Götzis | Möbel und Einrichtungsberatung', template: '%s | ESTILO Einrichtungsstudio' },
  description: 'Polstermöbel, Betten, Schränke, Esszimmer und Büro, ausgesucht und abgestimmt von Ebru Filiz. ESTILO Einrichtungsstudio, Am Garnmarkt 17, 6840 Götzis.',
  openGraph: { locale: 'de_AT', type: 'website', siteName: 'ESTILO', images: ['/og.jpg'] },
  icons: { icon: '/favicon.png' },
};

export const viewport: Viewport = { themeColor: '#F3EEE7', colorScheme: 'light' };

const jsonLd = {
  '@context': 'https://schema.org', '@type': 'FurnitureStore', name: firma.name, url: 'https://estilo.at/',
  email: firma.mail, telephone: firma.telefon,
  address: { '@type': 'PostalAddress', streetAddress: firma.strasse, postalCode: '6840', addressLocality: 'Götzis', addressCountry: 'AT' },
  openingHoursSpecification: [
    { '@type': 'OpeningHoursSpecification', dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], opens: '09:00', closes: '18:00' },
    { '@type': 'OpeningHoursSpecification', dayOfWeek: 'Saturday', opens: '09:00', closes: '14:00' },
  ],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="de">
      <body>
        <a href="#inhalt" className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:bg-hell focus:px-4 focus:py-2">Zum Inhalt springen</a>
        {children}
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      </body>
    </html>
  );
}
