// Auth store — token lives in sessionStorage (survives redirects, clears on tab close)

export const authStore = {
  save(token, name, userId) {
    sessionStorage.setItem('token', token);
    sessionStorage.setItem('name', name);
    sessionStorage.setItem('userId', userId);
  },

  getToken() {
    return sessionStorage.getItem('token');
  },

  getName() {
    return sessionStorage.getItem('name');
  },

  getUserId() {
    return sessionStorage.getItem('userId');
  },

  isLoggedIn() {
    return !!sessionStorage.getItem('token');
  },

  clear() {
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('name');
    sessionStorage.removeItem('userId');
  },

  logout() {
    this.clear();
    window.location.href = 'login.html';
  }
};

// Auto-redirect to login if token is missing on protected pages
export function requireAuth() {
  if (!authStore.isLoggedIn()) {
    window.location.href = 'login.html';
  }
}

// Helper: get auth headers for fetch calls
export function authHeaders() {
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${authStore.getToken()}`
  };
}
