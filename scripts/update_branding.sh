#!/bin/bash

# Restaurant Name and Logo Update Script

echo "========================================="
echo "Restaurant Branding Update"
echo "========================================="
echo ""

# Get restaurant name
read -p "Enter your restaurant name (or press Enter to keep 'BistroFlow'): " RESTAURANT_NAME

if [ -z "$RESTAURANT_NAME" ]; then
    RESTAURANT_NAME="BistroFlow"
    echo "Keeping default name: BistroFlow"
else
    echo "Updating to: $RESTAURANT_NAME"
    
    # Update LoginPage
    sed -i "s/BistroFlow/$RESTAURANT_NAME/g" /app/frontend/src/pages/LoginPage.js
    
    # Update ReceptionDashboard (bill prints)
    sed -i "s/BistroFlow/$RESTAURANT_NAME/g" /app/frontend/src/pages/ReceptionDashboard.js
    
    echo "✓ Restaurant name updated in all files"
fi

echo ""
echo "========================================="
echo "Logo Options:"
echo "========================================="
echo ""
echo "Choose your logo option:"
echo "1) Upload a logo file"
echo "2) Use an external URL"
echo "3) Keep current icon"
echo ""
read -p "Enter choice (1-3): " LOGO_CHOICE

case $LOGO_CHOICE in
    1)
        echo ""
        echo "Please upload your logo file to: /app/frontend/public/logo.png"
        echo "You can use the file browser or run:"
        echo "cp /your/path/logo.png /app/frontend/public/logo.png"
        echo ""
        echo "Supported formats: PNG, JPG, SVG"
        echo "Recommended size: 200x200px or larger"
        ;;
    2)
        read -p "Enter your logo URL: " LOGO_URL
        if [ ! -z "$LOGO_URL" ]; then
            sed -i "s|src=\"/logo.png\"|src=\"$LOGO_URL\"|g" /app/frontend/src/pages/LoginPage.js
            echo "✓ Logo URL updated to: $LOGO_URL"
        fi
        ;;
    3)
        # Revert to icon
        echo "Keeping current icon design"
        ;;
    *)
        echo "Invalid choice, keeping current setup"
        ;;
esac

echo ""
echo "========================================="
echo "✓ Branding update complete!"
echo "========================================="
echo ""
echo "The app will auto-reload with your changes."
