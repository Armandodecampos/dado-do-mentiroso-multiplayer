
import asyncio
import json
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.add_init_script(path="supabase_mock.js")

        await page.goto(f"file:///app/index.htm")

        # Define the complete state in a Python dictionary
        state = {
            "currentUser": {"id": "user-123", "email": "jules@test.com"},
            "currentRoom": {"room_code": "TEST1", "creator_id": "user-123"},
            "gameStarted": True,
            "presences": {
                "user-123": [{"name": "Jules", "email": "jules@test.com"}],
                "user-456": [{"name": "Agent", "email": "agent@test.com"}]
            },
            "gameState": {
                "players": {
                    "user-123": {"diceCount": 5, "dice": [1, 2, 3, 4, 5]},
                    "user-456": {"diceCount": 5, "dice": [6, 6, 6, 6, 6]}
                },
                "turnOrder": ["user-123", "user-456"],
                "currentPlayer": "user-123",
                "currentBid": {"quantity": 2, "face": 4},
                "lastBidder": "user-456",
                "turn": 2,
                "round": 1,
                "gameWinner": None,
                "bidHistory": [{"type": "bid", "playerId": "user-456", "quantity": 2, "face": 4}],
                "currentTurnMessage": "É a vez de Jules.",
                "roundInfo": {"phase": "bidding"}
            }
        }

        # Serialize the state to JSON and set it in the browser context
        state_json = json.dumps(state)
        await page.evaluate(f"window.testUtils.setState({state_json})")

        # Render the UI
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
