/**
 * User Sync Composable
 * Handles synchronization of Clerk user data to backend MongoDB
 */

import { ref } from 'vue';
import { useAuth, useUser } from '@clerk/vue';
import { syncUser } from '@/services/api';

// Module-level state to persist across component instances
let hasSyncedGlobal = false;

/**
 * Composable for managing user synchronization with backend
 *
 * This composable ensures that authenticated users are synced
 * to the backend database on their first login.
 *
 * @returns {Object} User sync state and functions
 */
export function useUserSync() {
  const auth = useAuth();
  const { user } = useUser();
  const isSyncing = ref(false);
  const syncError = ref(null);

  /**
   * Sync user with backend
   *
   * Only syncs once per session to avoid redundant calls.
   * Errors are logged but don't prevent app usage.
   *
   * @returns {Promise<Object|void>} Sync response or void if already synced
   */
  const performUserSync = async () => {
    console.log('[UserSync] performUserSync called, hasSyncedGlobal:', hasSyncedGlobal);

    // Skip if already synced in this session
    if (hasSyncedGlobal) {
      console.log('[UserSync] User already synced in this session');
      return;
    }

    // Skip if already syncing
    if (isSyncing.value) {
      console.log('[UserSync] Sync already in progress');
      return;
    }

    isSyncing.value = true;
    syncError.value = null;

    try {
      console.log('[UserSync] Getting Clerk token...');

      // Get Clerk session token
      // In Clerk Vue, getToken is a computed ref, so we need .value to access the function
      const token = await auth.getToken.value();

      if (!token) {
        throw new Error('No authentication token available');
      }

      // Extract user data from Clerk user object
      const userData = {
        email: user.value?.primaryEmailAddress?.emailAddress || user.value?.emailAddresses?.[0]?.emailAddress,
        first_name: user.value?.firstName,
        last_name: user.value?.lastName
      };

      console.log('[UserSync] User data:', userData);
      console.log('[UserSync] Token received, calling backend...');

      // Call backend sync endpoint with user data
      const response = await syncUser(token, userData);

      console.log(`[UserSync] User sync successful: ${response.status}`);
      hasSyncedGlobal = true;

      return response;
    } catch (error) {
      console.error('[UserSync] User sync failed:', error);
      syncError.value = error.message;
      // Don't throw - allow app to continue even if sync fails
    } finally {
      isSyncing.value = false;
    }
  };

  return {
    performUserSync,
    isSyncing,
    syncError
  };
}
