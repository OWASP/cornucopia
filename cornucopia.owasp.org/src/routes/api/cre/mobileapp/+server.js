import { json } from '@sveltejs/kit';

export function GET() {
    return json({
        meta: {
            edition: "OWASP Cornucopia Mobile App Edition",
            component: "cards",
            language: "all",
            languages: ["en"],
            version: "1.1"
        }
    });
}

