/**
 * HTTP client wrapper with automatic auth token injection.
 */

let _getToken: (() => string | undefined) | null = null;

/**
 * Set the function used to retrieve the current auth token.
 * Called once during app initialization (e.g., from useAuth composable).
 */
export function setTokenProvider(provider: () => string | undefined): void {
  _getToken = provider;
}

/**
 * Fetch wrapper that automatically injects the Authorization header.
 */
export async function apiFetch<T>(
  url: string,
  options: RequestInit = {}
): Promise<T> {
  const headers = new Headers(options.headers);

  if (_getToken) {
    const token = _getToken();
    if (token) {
      headers.set("Authorization", `Bearer ${token}`);
    }
  }

  if (!headers.has("Content-Type") && options.body) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(url, { ...options, headers });

  if (!response.ok) {
    throw new ApiError(response.status, response.statusText, await response.text());
  }

  return response.json() as Promise<T>;
}

export class ApiError extends Error {
  constructor(
    public status: number,
    public statusText: string,
    public body: string
  ) {
    super(`API Error ${status}: ${statusText}`);
    this.name = "ApiError";
  }
}
