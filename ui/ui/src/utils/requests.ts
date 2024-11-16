export function get(url: string, params: any = {}) {
    const urlI = new URL(url)
    urlI.search = new URLSearchParams(params).toString();
    return fetch(urlI)
}