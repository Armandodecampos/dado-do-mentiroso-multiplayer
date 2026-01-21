
import asyncio
import json
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.add_init_script(path="supabase_mock.js")

        await page.goto(f"file:///app/index.htm")

        await page.evaluate("""() => {
            window.testUtils.setCurrentUser({ id: 'user-123', email: 'jules@test.com' });
            window.testUtils.setCurrentRoom({ room_code: 'TEST1', creator_id: 'user-123' });
            window.testUtils.setGameStarted(true);
            window.testUtils.setPresences({
                'user-123': [{ name: 'Jules', email: 'jules@test.com' }],
                'user-456': [{ name: 'Agent', email: 'agent@test.com' }]
            });
            const gameState = {
                players: {
                    'user-123': { diceCount: 5, dice: [1, 2, 3, 4, 5] },
                    'user-456': { diceCount: 5, dice: [6, 6, 6, 6, 6] }
                },
                turnOrder: ['user-123', 'user-456'],
                currentPlayer: 'user-123',
                currentBid: { quantity: 2, face: 4 },
                lastBidder: 'user-456',
                turn: 2,
                round: 1,
                gameWinner: null,
                bidHistory: [{type: 'bid', playerId: 'user-456', quantity: 2, face: 4}],
                currentTurnMessage: 'É a vez de Jules.',
                roundInfo: { phase: 'bidding' }
            };
            window.testUtils.setGameState(gameState);
        }""")

        await page.evaluate("window.testUtils.showView('room-view')")
        await page.evaluate("window.testUtils.setRoomViewMode(true)")
        await page.evaluate("window.testUtils.renderRoomUI()")
        await page.evaluate("window.testUtils.renderGameUI()")

        await page.wait_for_timeout(1000)

        screenshot_path = "/home/jules/verification/12_history_width_fix.png"
        await page.screenshot(path=screenshot_path)
        print(f"Captura de tela salva em: {screenshot_path}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
