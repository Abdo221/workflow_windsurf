import { test, expect } from '@playwright/test';

test.describe('News Fetcher End-to-End Integration', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the app
    await page.goto('http://localhost:5173');
    
    // Wait for the app to load
    await page.waitForSelector('h1', { timeout: 10000 });
  });

  test('should load the application with correct UI elements', async ({ page }) => {
    // Check main heading
    await expect(page.locator('h1')).toContainText('News Fetcher');
    
    // Check input field
    const categoryInput = page.locator('input[placeholder*="category"]');
    await expect(categoryInput).toBeVisible();
    await expect(categoryInput).toHaveAttribute('placeholder', /Enter category/i);
    
    // Check fetch button
    const fetchButton = page.locator('button:has-text("Fetch")');
    await expect(fetchButton).toBeVisible();
    
    // Initially button should be disabled (empty input)
    await expect(fetchButton).toBeDisabled();
  });

  test('should handle category input and enable fetch button', async ({ page }) => {
    const categoryInput = page.locator('input[placeholder*="category"]');
    const fetchButton = page.locator('button:has-text("Fetch")');
    
    // Button should be disabled initially
    await expect(fetchButton).toBeDisabled();
    
    // Type in category
    await categoryInput.fill('science');
    
    // Button should now be enabled
    await expect(fetchButton).toBeEnabled();
    
    // Clear input
    await categoryInput.clear();
    
    // Button should be disabled again
    await expect(fetchButton).toBeDisabled();
  });

  test('should fetch news and display results', async ({ page }) => {
    const categoryInput = page.locator('input[placeholder*="category"]');
    const fetchButton = page.locator('button:has-text("Fetch")');
    
    // Fill category and click fetch
    await categoryInput.fill('science');
    await fetchButton.click();
    
    // Wait for loading state
    await expect(fetchButton).toHaveText(/Fetching/i);
    
    // Wait for status to appear (may take time due to API calls)
    await page.waitForSelector('.status', { timeout: 30000 });
    
    // Check status is displayed
    const statusElement = page.locator('.status');
    await expect(statusElement).toBeVisible();
    
    // Status should be one of expected values
    const statusText = await statusElement.textContent();
    expect(statusText).toMatch(/Status: (FRESH|CACHED|PARTIAL)/);
    
    // Extract item count from status
    const itemCountMatch = statusText?.match(/\((\d+) items\)/);
    const itemCount = itemCountMatch ? parseInt(itemCountMatch[1]) : 0;
    
    // Should have 0 items with demo API key, but structure should be correct
    expect(itemCount).toBeGreaterThanOrEqual(0);
    expect(itemCount).toBeLessThanOrEqual(10);
    
    console.log(`Test completed with ${itemCount} items and status: ${statusText}`);
  });

  test('should validate API response structure', async ({ page }) => {
    const categoryInput = page.locator('input[placeholder*="category"]');
    const fetchButton = page.locator('button:has-text("Fetch")');
    
    // Fill category and click fetch
    await categoryInput.fill('technology');
    await fetchButton.click();
    
    // Wait for status
    await page.waitForSelector('.status', { timeout: 30000 });
    
    // Check that we can make a direct API call to validate structure
    const apiResponse = await page.evaluate(async () => {
      try {
        const response = await fetch('/api/news/fetch', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ category: 'test' }),
        });
        
        if (!response.ok) {
          throw new Error(`API returned ${response.status}`);
        }
        
        return await response.json();
      } catch (error) {
        return { error: error.message };
      }
    });
    
    // Validate API response structure
    expect(apiResponse).toHaveProperty('status');
    expect(apiResponse).toHaveProperty('attempts');
    expect(apiResponse).toHaveProperty('category');
    expect(apiResponse).toHaveProperty('items');
    
    expect(['FRESH', 'CACHED', 'PARTIAL']).toContain(apiResponse.status);
    expect(typeof apiResponse.attempts).toBe('number');
    expect(apiResponse.attempts).toBeGreaterThanOrEqual(1);
    expect(apiResponse.attempts).toBeLessThanOrEqual(5);
    expect(Array.isArray(apiResponse.items)).toBe(true);
  });

  test('should handle invalid category gracefully', async ({ page }) => {
    const categoryInput = page.locator('input[placeholder*="category"]');
    const fetchButton = page.locator('button:has-text("Fetch")');
    
    // Try invalid category (too short)
    await categoryInput.fill('a');
    await fetchButton.click();
    
    // Should show error message
    await page.waitForSelector('.error', { timeout: 10000 });
    const errorElement = page.locator('.error');
    await expect(errorElement).toBeVisible();
    
    // Try invalid category (invalid characters)
    await categoryInput.fill('invalid@category');
    await fetchButton.click();
    
    // Should still show error
    await expect(errorElement).toBeVisible();
  });

  test('should validate backend health endpoint', async ({ page }) => {
    // Test backend health endpoint directly
    const healthResponse = await page.evaluate(async () => {
      try {
        const response = await fetch('/api/');
        return {
          status: response.status,
          ok: response.ok,
          data: await response.json()
        };
      } catch (error) {
        return { error: error.message };
      }
    });
    
    expect(healthResponse.status).toBe(200);
    expect(healthResponse.data).toHaveProperty('message', 'News Fetcher API');
  });

  test('should test keyboard interaction', async ({ page }) => {
    const categoryInput = page.locator('input[placeholder*="category"]');
    const fetchButton = page.locator('button:has-text("Fetch")');
    
    // Focus input and type category
    await categoryInput.focus();
    await categoryInput.fill('sports');
    
    // Press Enter to trigger fetch
    await page.keyboard.press('Enter');
    
    // Should trigger fetch (loading state)
    await expect(fetchButton).toHaveText(/Fetching/i);
    
    // Wait for completion
    await page.waitForSelector('.status', { timeout: 30000 });
    
    // Verify status appeared
    await expect(page.locator('.status')).toBeVisible();
  });
});
