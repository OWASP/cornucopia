import { json } from '@sveltejs/kit';

export function GET() {
    return json({
        meta: {
            edition: "OWASP Cornucopia Companion Edition",
            component: "cards",
            language: "en",
            languages: ["en"],
            version: "1.0"
        }
    });
}
