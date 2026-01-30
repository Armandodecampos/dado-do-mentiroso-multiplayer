from playwright.sync_api import sync_playwright, expect
import os

def verify_initial_view():
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
                            // Trigger with no session after a short delay
                            setTimeout(() => cb('INITIAL_SESSION', null), 100);
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
                    from: () => ({
                        select: () => ({
                            eq: () => ({
                                single: () => Promise.resolve({ data: null, error: { message: 'Not found' } }),
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

        # 1. Check Initial View
        initial_view = page.locator("#initial-view")
        expect(initial_view).to_be_visible()
        page.screenshot(path="verification/1_initial_view.png")
        print("Initial view visible.")

        # 2. Check "Como Jogar"
        page.click("#initial-how-to-play-btn")
        how_to_play_view = page.locator("#how-to-play-view")
        expect(how_to_play_view).to_be_visible()
        page.screenshot(path="verification/2_how_to_play.png")
        print("How to Play view visible.")

        # 3. Check "Voltar" returns to Initial View
        page.click("#back-to-lobby-from-how-to-play-btn")
        expect(initial_view).to_be_visible()
        print("Returned to Initial View.")

        # 4. Check "Prosseguir"
        page.click("#proceed-btn")
        auth_view = page.locator("#auth-view")
        expect(auth_view).to_be_visible()
        page.screenshot(path="verification/3_auth_view.png")
        print("Auth view (Login) visible after Prosseguir.")

        # 5. Check "Como Jogar" from Lobby (mocking login for a moment)
        # Actually, let's just check the "Como Jogar" button in Auth view if it exists (it doesn't, it's in Lobby)

        browser.close()

if __name__ == "__main__":
    if not os.path.exists("verification"):
        os.makedirs("verification")
    verify_initial_view()
