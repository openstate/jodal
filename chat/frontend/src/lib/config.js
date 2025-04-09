const envApiUrl = import.meta.env.PUBLIC_API_URL;
console.debug('Environment API URL:', envApiUrl);

export const API_BASE_URL = envApiUrl || 'https://api.chat.bron.live';
console.debug('Using API URL:', API_BASE_URL);
