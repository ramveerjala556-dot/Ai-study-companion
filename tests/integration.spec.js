const { test, expect } = require('@playwright/test');

test('E2E Study Flow: Dashboard and Chat', async ({ page }) => {
  // 1. Visit the dashboard
  await page.goto('http://localhost:5173/');
  await expect(page).toHaveTitle(/frontend/);
  await expect(page.locator('h1')).toContainText('Study Dashboard');

  // 2. Navigate to Chat
  await page.click('button:has-text("Chat with AI")');
  await expect(page.locator('.bg-blue-600.text-white.p-4.font-bold:has-text("AI Study Companion")')).toBeVisible();

  // 3. Send a message in Chat
  const input = page.locator('input[placeholder="Ask me anything about your studies..."]');
  await input.fill('I want to learn about Computer Science');
  await page.click('button[type="submit"]');

  // 4. Check for AI response
  // Note: This requires the backend to be running and have at least one topic for ID=1
  // or a mock that returns a response.
  await expect(page.locator('.max-w-\\[80\\%\\]:has-text("learn about")')).toBeVisible({ timeout: 15000 });

  // 5. Go back to Dashboard
  await page.click('button:has-text("Dashboard")');
  await expect(page.locator('h1')).toContainText('Study Dashboard');
});
