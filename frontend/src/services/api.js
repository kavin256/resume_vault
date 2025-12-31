/**
 * API Service Module
 * Centralized API calls for Resume Vault frontend
 */

// Use environment variable or fallback to production URL
const API_BASE_URL = import.meta.env.VITE_API_URL || "https://resume-vault.fly.dev";

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
    method: "POST",
    headers: {
      Authorization: `Bearer ${clerkToken}`,
      "Content-Type": "application/json",
    },
    body: userData ? JSON.stringify(userData) : undefined,
  });

  if (!response.ok) {
    let errorMessage = "Failed to sync user";
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

/**
 * Get or create user's master profile
 *
 * This function fetches the authenticated user's master profile.
 * If the profile doesn't exist, the backend automatically creates one
 * with default values populated from the user's account.
 *
 * @param {string} clerkToken - Clerk session token (JWT)
 * @returns {Promise<Object>} Profile response with status and profile data
 * @throws {Error} If the request fails or returns an error
 */
export async function getMasterProfile(clerkToken) {
  const response = await fetch(`${API_BASE_URL}/profiles/me`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${clerkToken}`,
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    let errorMessage = "Failed to fetch master profile";
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

/**
 * Update user's master profile
 *
 * @param {string} clerkToken - Clerk session token (JWT)
 * @param {Object} profileData - Profile data to update
 * @returns {Promise<Object>} Updated profile response
 * @throws {Error} If the request fails or returns an error
 */
export async function updateMasterProfile(clerkToken, profileData) {
  const response = await fetch(`${API_BASE_URL}/profiles/me`, {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${clerkToken}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(profileData),
  });

  if (!response.ok) {
    let errorMessage = "Failed to update master profile";
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
