import { defineStore } from "pinia";
import { ref } from "vue";
import { useAuth, type AuthUser } from "@common/composables/useAuth";

export const useAuthStore = defineStore("auth", () => {
  const { isAuthenticated, user, token, init: authInit, logout: authLogout, getToken } = useAuth();

  const loading = ref(true);

  async function init(): Promise<void> {
    loading.value = true;
    try {
      await authInit({
        url: import.meta.env.VITE_KEYCLOAK_URL,
        realm: import.meta.env.VITE_KEYCLOAK_REALM,
        clientId: import.meta.env.VITE_KEYCLOAK_CLIENT_ID,
      });
    } finally {
      loading.value = false;
    }
  }

  async function logout(): Promise<void> {
    await authLogout();
  }

  return {
    isAuthenticated,
    user: user as ReturnType<typeof ref<AuthUser | null>>,
    token,
    loading,
    init,
    logout,
    getToken,
  };
});
