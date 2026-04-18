// In-memory auth store — token never touches localStorage
// Lives only for the current browser session (tab)

const _state = {
  token: null,
  name: null,
  userId: null,
};

export const authStore = {
  save(token, name, userId) {
    _state.token = token;
    _state.name = name;
    _state.userId = userId;
  },

  getToken() {
    return _state.token;
  },

  getName() {
    return _state.name;
  },

  getUserId() {
    return _state.userId;
  },

  isLoggedIn() {
    return !!_state.token;
  },

  clear() {
    _state.token = null;
    _state.name = null;
    _state.userId = null;
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
