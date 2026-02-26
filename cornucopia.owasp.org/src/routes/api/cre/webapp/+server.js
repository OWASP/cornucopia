import { json } from '@sveltejs/kit';

export function GET() {
    return json({
        meta: {
            edition: "OWASP Cornucopia Website App Edition",
            component: "cards",
            language: "all",
            languages: ["en", "es", "fr", "nl", "no_nb", "pt_br", "pt_pt", "it", "ru"],
            version: "2.2"
        }
    });
}
