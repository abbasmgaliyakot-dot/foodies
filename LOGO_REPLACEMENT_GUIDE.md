# Logo & Branding Replacement Guide

## Quick Methods

### Method 1: Use the Interactive Script (Easiest)
```bash
bash /app/scripts/update_branding.sh
```
This script will guide you through:
- Changing restaurant name
- Uploading or using logo URL

### Method 2: Manual Logo Replacement

#### A. Upload Your Logo File
1. Place your logo in: `/app/frontend/public/logo.png`
   ```bash
   cp /path/to/your-logo.png /app/frontend/public/logo.png
   ```

2. The app is already configured to use `/logo.png`

#### B. Use External Logo URL
Edit `/app/frontend/src/pages/LoginPage.js` (around line 32):

Change:
```javascript
src="/logo.png"
```

To:
```javascript
src="https://your-website.com/your-logo.png"
```

### Method 3: Change Restaurant Name Only

Replace "BistroFlow" with your restaurant name in these files:
- `/app/frontend/src/pages/LoginPage.js`
- `/app/frontend/src/pages/ReceptionDashboard.js`

Or use find & replace:
```bash
cd /app/frontend/src
find . -name "*.js" -type f -exec sed -i 's/BistroFlow/YourRestaurantName/g' {} +
```

## Logo Specifications

**Recommended:**
- Format: PNG with transparent background
- Size: 200x200px minimum
- Aspect ratio: Square or horizontal
- File size: Under 500KB for fast loading

**Supported formats:**
- PNG (recommended)
- JPG/JPEG
- SVG
- WebP

## Logo Locations in the App

1. **Login Page** - Main logo display
2. **Printed Bills** - Appears on customer receipts
3. **Printed Kitchen Orders** - Company branding on kitchen tickets

## Example: Replace with Your Logo

### Using a local file:
```bash
# 1. Copy your logo
cp ~/Downloads/my-restaurant-logo.png /app/frontend/public/logo.png

# 2. The app will auto-reload and show your logo
```

### Using a URL:
Edit `/app/frontend/src/pages/LoginPage.js`:
```javascript
<img 
  src="https://example.com/my-logo.png" 
  alt="Restaurant Logo" 
  className="w-24 h-24 object-contain"
/>
```

## Customize Logo Size

In `/app/frontend/src/pages/LoginPage.js`, adjust the className:

```javascript
className="w-24 h-24 object-contain"  // Current size (96px × 96px)
className="w-32 h-32 object-contain"  // Larger (128px × 128px)
className="w-16 h-16 object-contain"  // Smaller (64px × 64px)
```

## Need Help?

Run the guide script:
```bash
bash /app/scripts/logo_guide.sh
```

Or use the interactive updater:
```bash
bash /app/scripts/update_branding.sh
```

## After Making Changes

The app uses hot reload - your changes will appear automatically within seconds!
No need to restart servers.
