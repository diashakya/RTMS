# Django Admin Usage Guide - Restaurant Management System

## 🗑️ **How to Delete Items from Admin Panel**

### **Method 1: Individual Item Deletion**
1. **Navigate** to the item list (Foods, Orders, Customers, etc.)
2. **Click on the item title** to open the edit page
3. **Scroll to bottom** and click the red **"Delete"** button
4. **Confirm deletion** on the confirmation page

### **Method 2: Bulk Deletion (Multiple Items)**
1. **Select items** using checkboxes on the left of each row
2. **Choose delete action** from the dropdown at the bottom:
   - `Delete selected foods` (for food items)
   - `Delete selected specials` (for special items)
   - `⚠️ Delete selected orders (permanent)` (for orders)
   - `Delete selected categories` (for categories)
3. **Click "Go"** to execute the action
4. **Confirm** on the confirmation page

### **Method 3: Alternative Actions (Non-Destructive)**
Instead of permanent deletion, you can:

#### **For Food Items:**
- `Mark selected items as unavailable` - Hides items without deleting
- Individual edit to change status

#### **For Specials:**
- `Deactivate selected specials` - Turns off specials temporarily
- `Activate selected specials` - Re-enables deactivated specials

#### **For Orders:**
- `Mark selected orders as completed` - Changes status instead of deleting
- `Cancel selected orders` - Marks as cancelled with email notification

## 🛡️ **Safety Features**

### **Confirmation Required**
- All delete actions require confirmation
- Shows count of items being deleted
- Lists affected items before deletion

### **Success Messages**
- Admin displays confirmation after successful deletion
- Shows count of deleted items

### **⚠️ Warning Indicators**
- Destructive actions marked with warning symbols
- Clear labeling of permanent vs temporary actions

## 📋 **Best Practices**

### **Before Deleting:**
1. **Backup important data** if needed
2. **Consider marking as inactive** instead of deleting
3. **Check for related data** (orders, favorites, etc.)

### **For Orders:**
- **Prefer cancellation** over deletion for audit trails
- **Keep completed orders** for reporting and analytics
- **Only delete test/spam orders**

### **For Food Items:**
- **Mark as unavailable** instead of deleting popular items
- **Keep for reordering history** and customer preferences
- **Delete only test/duplicate items**

## 🔍 **Finding Items to Delete**

### **Search Functionality:**
- Use the **search box** at the top to find specific items
- Search by name, category, customer, etc.

### **Filtering:**
- Use **filters on the right** to narrow down items
- Filter by category, status, date, etc.

### **Sorting:**
- Click **column headers** to sort by different criteria
- Find oldest/newest items easily

## 📊 **Admin Dashboard Features**

### **Quick Stats:**
- View item counts in the main admin dashboard
- Monitor active vs inactive items
- Track order statuses

### **Batch Operations:**
- Select multiple items for bulk operations
- Efficient management of large datasets

## 🚨 **Emergency Recovery**

### **If You Accidentally Delete:**
1. **Check Django admin logs** (if logging is enabled)
2. **Restore from database backup** (if available)
3. **Recreate critical items** manually
4. **Contact system administrator** for help

### **Prevention:**
- **Regular backups** of the database
- **Test deletions** on staging environment first
- **Train admin users** on proper procedures

---

## 📞 **Need Help?**
- Check Django admin documentation
- Contact system administrator
- Review application logs for errors