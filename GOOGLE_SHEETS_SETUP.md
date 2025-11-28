# 📊 Google Sheets Integration Guide

## Overview
Connect your **Google Sheets** to the app for **live, real-time data**. Update your data in Google Sheets → App updates instantly!

---

## ✅ Step 1: Create Google Sheets

### Create 3 Sheets (or use existing ones):

1. **Reviews Sheet** - Customer reviews and ratings
2. **POS/Sales Sheet** - Daily sales data
3. **Inventory Sheet** - Stock levels

**Go to:** https://sheets.google.com → **"New Spreadsheet"**

---

## 📝 Step 2: Format Your Data

### Reviews Sheet Example:
| date | review_text | rating | source |
|------|-------------|--------|--------|
| 2025-11-28 | Amazing food! | 5 | Google |
| 2025-11-28 | Great service | 5 | Facebook |
| 2025-11-27 | Could be better | 3 | Yelp |

**Required columns:**
- `review_text` (or `text`) - What customers said
- Others optional: `date`, `rating`, `source`

---

### POS/Sales Sheet Example:
| date | item | qty | price |
|------|------|-----|-------|
| 2025-11-28 | Pizza | 5 | 12.99 |
| 2025-11-28 | Pasta | 3 | 9.99 |
| 2025-11-27 | Burger | 2 | 8.99 |

**Required columns:**
- `item` - Dish name
- `qty` - Quantity sold
- `price` - Price per item
- `date` - Sale date

---

### Inventory Sheet Example:
| item | qty_on_hand | unit_cost | sku |
|------|------------|-----------|-----|
| Pizza Base | 50 | 2.00 | SKU001 |
| Cheese | 30 | 3.00 | SKU002 |
| Pasta | 25 | 1.50 | SKU003 |

**Required columns:**
- `item` - Item name
- `qty_on_hand` - Current stock
- `unit_cost` - Cost per unit
- `sku` (optional)

---

## 🔗 Step 3: Make Sheets Public

For each sheet:

1. Click **"Share"** (top right)
2. Click **"Change to anyone with link"**
3. Make sure it says **"Viewer"** access
4. Click **"Share"**

---

## 🔑 Step 4: Get Sheet IDs

**Sheet URL format:**
```
https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit#gid=0
```

**Extract the `{SHEET_ID}`** - it's the long string in the URL.

**Example:**
- URL: `https://docs.google.com/spreadsheets/d/1a2b3c4d5e6f7g8h9i0j/edit#gid=0`
- SHEET_ID: `1a2b3c4d5e6f7g8h9i0j`

---

## ⚙️ Step 5: Add to Streamlit Cloud

1. **Go to your Streamlit Cloud app**
2. **Click "Manage app"** (bottom right)
3. **Click "Settings" → "Secrets"**
4. **Add these 3 lines:**

```
GOOGLE_REVIEWS_SHEET_ID=your_reviews_sheet_id_here
GOOGLE_POS_SHEET_ID=your_pos_sheet_id_here
GOOGLE_INVENTORY_SHEET_ID=your_inventory_sheet_id_here
```

**Replace** `your_reviews_sheet_id_here` with actual IDs from Step 4.

5. **Click "Save"**
6. **App auto-restarts** ✨

---

## 🚀 Step 6: Use It!

1. **Go to your app**
2. **In sidebar**, select: **"📊 Google Sheets"**
3. **Data loads from Google Sheets** instead of CSV files!
4. **Update your Google Sheets → Refreshes in app** (within 5 minutes)

---

## 💡 How It Works

- **Caching**: Data is cached for 5 minutes (to save API calls)
- **Auto-refresh**: Refresh page or wait 5 minutes for updates
- **Live data**: As soon as you update Google Sheets, app reflects changes

---

## 🔄 Real-Time Updates

To see changes **immediately**:
1. Update Google Sheet
2. Go to your app
3. Click **"Rerun"** (top right of Streamlit)
4. New data loads instantly!

Or simply **refresh the page** (Ctrl+R).

---

## ❓ Troubleshooting

### "❌ Google Sheets not configured"
- Check Sheet IDs are correct in Secrets
- Make sure sheets are **public** (anyone with link)
- Wait 2 minutes for Streamlit to restart

### "⚠️ Could not load from Google Sheets"
- Check internet connection
- Verify Sheet ID is correct
- Make sure sheet name matches (restaurant_reviews, pos_sales, inventory)
- Try with local CSV files first

### Data not updating
- Wait 5 minutes (cache expires)
- Refresh the page
- Click "Rerun" in Streamlit

### Access denied error
- Sheet must be **public** (anyone with link can view)
- Check sharing settings in Google Sheets

---

## 🎯 Sheet Name Requirements

Your sheet tabs must be named exactly:
- `restaurant_reviews` - For reviews data
- `pos_sales` - For sales data  
- `inventory` - For inventory data

⚠️ **Names are case-sensitive!**

---

## 📚 Quick Reference

| Item | Value |
|------|-------|
| Google Sheets | https://sheets.google.com |
| Required Format | CSV compatible (table format) |
| Public Sheets | Must be "Anyone with link can view" |
| Update Frequency | Every 5 minutes (cached) |
| Column Names | Must match exactly (case-sensitive) |

---

## 🔐 Security

✅ **Safe to use:**
- Google Sheets are read-only for the app
- Only Sheet IDs needed (not API keys)
- Data is public (you control sharing)

❌ **Don't share:**
- Sheet IDs should not be private
- Keep sharing settings to "Anyone with link"

---

## 🎉 Next Steps

1. Create 3 Google Sheets
2. Add sample data
3. Make them public
4. Get Sheet IDs
5. Add to Streamlit Cloud Secrets
6. Switch to "Google Sheets" mode in app
7. Enjoy live data! 🎊

---

## 📞 Need Help?

- **Google Sheets not loading?** Check if sheets are public
- **Wrong data showing?** Verify column names match exactly
- **Slow updates?** That's the 5-minute cache (working as designed)

**You're all set!** 🚀
