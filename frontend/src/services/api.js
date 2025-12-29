/**
 * API Service Module
 * Centralized API calls for Resume Vault frontend
 */

const API_BASE_URL = 'http://localhost:8000';

/**
 * Sync user with backend after Clerk authentication
 *
 * This function calls the backend /users/sync endpoint to ensure
 * the authenticated user exists in our MongoDB database.
 *
 * @param {string} clerkToken - Clerk session token (JWT)
 * @param {Object} userData - User data from Clerk (optional for now)
 * @returns {Promise<Object>} Sync response with status and user info
 * @throws {Error} If the request fails or returns an error
 */
export async function syncUser(clerkToken, userData = null) {
  const response = await fetch(`${API_BASE_URL}/users/sync`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${clerkToken}`,
      'Content-Type': 'application/json'
    },
    body: userData ? JSON.stringify(userData) : undefined
  });

  if (!response.ok) {
    let errorMessage = 'Failed to sync user';
    try {
      const error = await response.json();
      errorMessage = error.detail || errorMessage;
    } catch (e) {
      // If error response is not JSON, use default message
    }
    throw new Error(errorMessage);
  }

  return await response.json();
}
