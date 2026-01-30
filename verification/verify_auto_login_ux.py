from playwright.sync_api import sync_playwright, expect
import os

def verify_auto_login_ux():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Absolute path to index.htm
        path = os.path.abspath("index.htm")
        url = f"file://{path}"

        # Mock Supabase
        page.add_init_script("""
            window.supabase = {
                createClient: () => ({
                    auth: {
                        onAuthStateChange: (cb) => {
                            setTimeout(() => {
                                cb('SIGNED_IN', {
                                    user: {
                                        id: '123',
                                        email: 'test@example.com',
                                        user_metadata: { name: 'Test Player' }
                                    }
                                });
                            }, 200);
                            return { data: { subscription: { unsubscribe: () => {} } } };
                        },
                        signOut: async () => ({ error: null }),
                    },
                    channel: () => ({
                        on: function() { return this; },
                        subscribe: function() { return this; },
                        track: function() { return this; },
                        untrack: function() { return Promise.resolve(); }
                    }),
                    from: (table) => ({
                        select: () => ({
                            eq: () => ({
                                single: () => Promise.resolve({
                                    data: { name: 'Test Player', last_room: null },
                                    error: null
                                }),
                                maybeSingle: () => Promise.resolve({ data: null, error: null })
                            }),
                            update: () => ({ eq: () => Promise.resolve({ error: null }) })
                        }),
                        update: () => ({ eq: () => Promise.resolve({ error: null }) })
                    })
                })
            };
        """)

        page.goto(url)

        # We expect that eventually the loader is gone and we are in the lobby
        expect(page.locator("#lobby-view")).to_be_visible(timeout=10000)
        expect(page.get_by_text("Bem-vindo, Test Player")).to_be_visible()
        page.screenshot(path="verification/6_auto_login_success.png")
        print("Auto-login verified successfully.")

        browser.close()

if __name__ == "__main__":
    if not os.path.exists("verification"):
        os.makedirs("verification")
    verify_auto_login_ux()
