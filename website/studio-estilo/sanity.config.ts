import { defineConfig } from 'sanity';
import { structureTool } from 'sanity/structure';
import { schemaTypes } from './schemaTypes';

// Projekt-ID kommt aus der Umgebung (SANITY_STUDIO_PROJECT_ID), Datensatz "production".
export default defineConfig({
  name: 'estilo',
  title: 'ESTILO Website',
  projectId: process.env.SANITY_STUDIO_PROJECT_ID || 'bitte-eintragen',
  dataset: process.env.SANITY_STUDIO_DATASET || 'production',
  plugins: [
    structureTool({
      structure: (S) => S.list().title('Inhalte').items([
        S.listItem().title('Startseite').id('seite').child(S.document().schemaType('seite').documentId('seite')),
        S.listItem().title('Studio und Öffnungszeiten').id('studio').child(S.document().schemaType('studio').documentId('studio')),
        S.listItem().title('Bewertungen').id('stimmen').child(S.document().schemaType('stimmen').documentId('stimmen')),
      ]),
    }),
  ],
  schema: { types: schemaTypes },
});
