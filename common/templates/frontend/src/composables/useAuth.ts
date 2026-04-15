/**
 * Keycloak authentication composable.
 *
 * Provides reactive auth state and methods for login/logout.
 * Initializes keycloak-js and manages token lifecycle.
 */

import Keycloak from "keycloak-js";
import { ref, type Ref } from "vue";
import { setTokenProvider } from "../lib/api";

export interface AuthUser {
  sub: string;
  username: string;
  email: string;
  firstName: string;
  lastName: string;
  roles: string[];
}

interface AuthState {
  isAuthenticated: Ref<boolean>;
  user: Ref<AuthUser | null>;
  token: Ref<string | undefined>;
  keycloak: Ref<Keycloak | null>;
  init: (config: KeycloakConfig) => Promise<void>;
  login: () => Promise<void>;
  logout: () => Promise<void>;
  getToken: () => string | undefined;
}

interface KeycloakConfig {
  url: string;
  realm: string;
  clientId: string;
}

const isAuthenticated = ref(false);
const user = ref<AuthUser | null>(null);
const token = ref<string | undefined>(undefined);
const keycloakInstance = ref<Keycloak | null>(null);

let _initialized = false;

function extractUser(kc: Keycloak): AuthUser {
  const parsed = kc.tokenParsed;
  return {
    sub: parsed?.sub ?? "",
    username: parsed?.preferred_username ?? "",
    email: parsed?.email ?? "",
    firstName: parsed?.given_name ?? "",
    lastName: parsed?.family_name ?? "",
    roles: parsed?.realm_access?.roles ?? [],
  };
}

export function useAuth(): AuthState {
  async function init(config: KeycloakConfig): Promise<void> {
    if (_initialized) return;

    const kc = new Keycloak({
      url: config.url,
      realm: config.realm,
      clientId: config.clientId,
    });

    const authenticated = await kc.init({
      onLoad: "login-required",
      checkLoginIframe: false,
      pkceMethod: "S256",
    });

    keycloakInstance.value = kc;
    isAuthenticated.value = authenticated;

    if (authenticated) {
      token.value = kc.token;
      user.value = extractUser(kc);
      setTokenProvider(() => kc.token);
    }

    // Auto-refresh token
    setInterval(async () => {
      try {
        const refreshed = await kc.updateToken(30);
        if (refreshed) {
          token.value = kc.token;
        }
      } catch {
        isAuthenticated.value = false;
        user.value = null;
      }
    }, 10000);

    _initialized = true;
  }

  async function login(): Promise<void> {
    await keycloakInstance.value?.login();
  }

  async function logout(): Promise<void> {
    await keycloakInstance.value?.logout();
    isAuthenticated.value = false;
    user.value = null;
    token.value = undefined;
  }

  function getToken(): string | undefined {
    return keycloakInstance.value?.token;
  }

  return {
    isAuthenticated,
    user,
    token,
    keycloak: keycloakInstance,
    init,
    login,
    logout,
    getToken,
  };
}
