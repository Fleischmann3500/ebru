import { defineCliConfig } from 'sanity/cli';
export default defineCliConfig({ api: { projectId: process.env.SANITY_STUDIO_PROJECT_ID || 'bitte-eintragen', dataset: process.env.SANITY_STUDIO_DATASET || 'production' } });
