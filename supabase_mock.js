window.supabase = {
  createClient: () => ({
    auth: {
      onAuthStateChange: (callback) => {
        // **FIXED**: Simulate an authenticated user by default.
        // This aligns with the test script's goal of verifying in-game functionality.
        const mockSession = {
          user: { id: 'user-123', email: 'jules@test.com' }
        };
        callback('INITIAL_SESSION', mockSession);

        return { data: { subscription: { unsubscribe: () => {} } } };
      },
      getSession: () => ({
        data: {
          session: { user: { id: 'user-123', email: 'jules@test.com' } }
        }
      }),
      signInWithPassword: () => ({ data: {}, error: null }),
      signUp: () => ({ data: {}, error: null }),
      signOut: () => ({ error: null }),
    },
    channel: (channelName) => ({
      on: () => ({
        subscribe: (callback) => {
          // Immediately confirm subscription
          if (callback) {
            callback('SUBSCRIBED');
          }
          return {};
        }
      }),
      // Mock the track function to do nothing
      track: () => Promise.resolve('ok'),
      // Mock the untrack function to do nothing
      untrack: () => Promise.resolve('ok'),
      // Mock presenceState to return an empty object
      presenceState: () => ({})
    }),
    from: () => ({
      // **FIXED**: Mock the profile lookup to return a valid profile.
      // This prevents errors inside the handleUserLoggedIn function.
      select: () => ({
          eq: () => ({
              single: () => Promise.resolve({
                  data: { name: 'Jules', last_room: null },
                  error: null
              })
          })
      }),
      insert: () => ({ data: [{}], error: null }),
      update: () => ({ data: [{}], error: null }),
    }),
    removeChannel: () => Promise.resolve('ok')
  }),
};
