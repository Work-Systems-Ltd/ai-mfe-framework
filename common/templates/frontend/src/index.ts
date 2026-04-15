/**
 * MFE Frontend Common - shared utilities, composables, and components.
 */

export { cn } from "./lib/utils";
export { apiFetch, setTokenProvider, ApiError } from "./lib/api";
export { useAuth, type AuthUser } from "./composables/useAuth";
export { usePermissions } from "./composables/usePermissions";
