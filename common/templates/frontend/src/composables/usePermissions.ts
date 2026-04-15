/**
 * Permission checking composable.
 *
 * Wraps calls to the permissions backend API for checking
 * if the current user has access to specific resources.
 */

import { ref, type Ref } from "vue";
import { apiFetch } from "../lib/api";

interface PermissionCheckResult {
  allowed: boolean;
}

interface UsePermissions {
  checking: Ref<boolean>;
  check: (relation: string, object: string) => Promise<boolean>;
  listObjects: (relation: string, objectType: string) => Promise<string[]>;
}

export function usePermissions(permissionsApiUrl: string): UsePermissions {
  const checking = ref(false);

  async function check(relation: string, object: string): Promise<boolean> {
    checking.value = true;
    try {
      const result = await apiFetch<PermissionCheckResult>(
        `${permissionsApiUrl}/api/permissions/check`,
        {
          method: "POST",
          body: JSON.stringify({ relation, object }),
        }
      );
      return result.allowed;
    } catch {
      return false;
    } finally {
      checking.value = false;
    }
  }

  async function listObjects(
    relation: string,
    objectType: string
  ): Promise<string[]> {
    checking.value = true;
    try {
      const result = await apiFetch<{ objects: string[] }>(
        `${permissionsApiUrl}/api/permissions/list-objects`,
        {
          method: "POST",
          body: JSON.stringify({ relation, type: objectType }),
        }
      );
      return result.objects;
    } catch {
      return [];
    } finally {
      checking.value = false;
    }
  }

  return { checking, check, listObjects };
}
