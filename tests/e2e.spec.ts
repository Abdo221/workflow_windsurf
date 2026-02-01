import { test, expect } from '@playwright/test';

test.describe('News Fetcher E2E', () => {
  test.beforeEach(async ({ page }) => {
    // Start backend and frontend before each test
    // This assumes backend is running on localhost:8000 and frontend on localhost:5173
    await page.goto('http://localhost:5173');
  });

  test('should fetch news for science category', async ({ page }) => {
    // Fill category input
    await page.fill('input[placeholder="Enter category"]', 'science');
    
    // Click fetch button
    await page.click('button:has-text("Fetch")');
    
    // Wait for status to appear (FRESH, CACHED, or PARTIAL)
    await page.waitForSelector('.status');
    
    // Check status is one of expected values
    const statusElement = page.locator('.status');
    await expect(statusElement).toBeVisible();
    const statusText = await statusElement.textContent();
    expect(['FRESH', 'CACHED', 'PARTIAL']).toContain(statusText?.split(' ')[1]);
    
    // Wait for items to load
    await page.waitForSelector('.news-item', { timeout: 30000 });
    
    // Check that at least 1 item is rendered
    const newsItems = page.locator('.news-item');
    const itemCount = await newsItems.count();
    expect(itemCount).toBeGreaterThanOrEqual(1);
    expect(itemCount).toBeLessThanOrEqual(10);
    
    // Validate each item
    for (let i = 0; i < itemCount; i++) {
      const item = newsItems.nth(i);
      
      // Check title is visible and has a link
      const titleLink = item.locator('h3 a');
      await expect(titleLink).toBeVisible();
      const href = await titleLink.getAttribute('href');
      expect(href).toBeTruthy();
      expect(href?.startsWith('http')).toBeTruthy();
      
      // Check description is visible
      const description = item.locator('p');
      await expect(description).toBeVisible();
      const descText = await description.textContent();
      expect(descText).toBeTruthy();
      expect(descText?.length).toBeGreaterThan(0);
      
      // Check meta info (source and published date)
      const meta = item.locator('.meta');
      await expect(meta).toBeVisible();
      const metaText = await meta.textContent();
      expect(metaText).toContain('Source:');
      expect(metaText).toContain('Published:');
      
      // Validate published date is within last 7 days
      const publishedDateMatch = metaText?.match(/Published: (.+)/);
      if (publishedDateMatch) {
        const publishedDate = new Date(publishedDateMatch[1]);
        const sevenDaysAgo = new Date();
        sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
        expect(publishedDate.getTime()).toBeGreaterThanOrEqual(sevenDaysAgo.getTime());
      }
    }
  });

  test('should handle empty category', async ({ page }) => {
    // Don't fill category input
    await page.click('button:has-text("Fetch")');
    
    // Button should be disabled when input is empty
    const button = page.locator('button:has-text("Fetch")');
    await expect(button).toBeDisabled();
  });

  test('should handle invalid category gracefully', async ({ page }) => {
    // Fill with invalid category
    await page.fill('input[placeholder="Enter category"]', 'invalid@category');
    
    // Click fetch button
    await page.click('button:has-text("Fetch")');
    
    // Should show error message
    await page.waitForSelector('.error', { timeout: 10000 });
    const errorElement = page.locator('.error');
    await expect(errorElement).toBeVisible();
  });
});
