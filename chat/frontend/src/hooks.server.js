/** @type {import('@sveltejs/kit').Handle} */
export async function handle({ event, resolve }) {
    const response = await resolve(event, {
        transformPageChunk: ({ html }) => {
            if (process.env.NODE_ENV === 'production') {
                const host = event.url.host;
                return html.replace(
                    '</head>',
                    `<script defer data-domain="${host}" src="https://plausible.io/js/script.js"></script></head>`
                );
            }
            return html;
        }
    });
    
    return response;
} 