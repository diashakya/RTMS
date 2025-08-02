# Restaurant Management System (RTMS) - Testing Documentation

## 📋 Overview

This document provides comprehensive testing guidelines, test cases, and debugging utilities for the Restaurant Management System (RTMS). The system includes user authentication, menu management, cart functionality, order processing, real-time tracking, and administrative features.

## 🏗️ System Architecture

The RTMS is built using:
- **Backend**: Django 5.2 with Python 3.12.6
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Real-time**: Django Channels with WebSocket
- **Authentication**: Django built-in authentication
- **Security**: CSRF protection, session management

## 🧪 Test Environment Setup

### Prerequisites

```bash
# Ensure Python 3.12+ is installed
python --version

# Activate virtual environment
source myenvi/bin/activate  # Linux/Mac
# OR
myenvi\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Create test data
python manage.py loaddata test_data.json

# Run development server
python manage.py runserver
```

### Test Environment Specifications

| Component | Version/Details |
|-----------|----------------|
| **Operating System** | Windows 11 / Linux / macOS |
| **Python** | 3.12.6 |
| **Django** | 5.2 |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **Browsers** | Chrome 120+, Firefox 118+, Edge 118+ |
| **WebSocket** | Django Channels 4.0+ |
| **Node.js** | 18+ (for frontend tools) |

## 📝 Test Cases Overview

### Module Coverage

| Module | Test Cases | Coverage |
|--------|------------|----------|
| **User Authentication** | 5 test cases | Login, Registration, Logout |
| **Menu Management** | 5 test cases | Display, Filtering, Search, Images |
| **Cart Management** | 5 test cases | Add, Update, Remove, Persistence |
| **Checkout Process** | 5 test cases | Delivery, Dine-in, Validation |
| **Favorites Management** | 5 test cases | Add, Remove, Authentication |
| **Order History** | 5 test cases | View, Status, Receipt, Reorder |
| **Real-time Tracking** | 4 test cases | WebSocket, Updates, Recovery |
| **Admin Dashboard** | 4 test cases | Access, Management, Notifications |
| **Form Validation** | 4 test cases | Real-time, Success, Required fields |
| **Loading Indicators** | 3 test cases | Button states, AJAX feedback |
| **CSRF Security** | 2 test cases | Token presence, Validation |
| **Image Handling** | 3 test cases | Display, Fallback, Validation |

**Total: 50 comprehensive test cases**

## 🧪 Detailed Test Cases

### User Authentication Module

| Test ID | Scenario | Test Type | Priority |
|---------|----------|-----------|----------|
| TC_Auth_01 | Valid user login | Positive | High |
| TC_Auth_02 | Invalid password | Negative | High |
| TC_Auth_03 | Empty credentials | Negative | Medium |
| TC_Auth_04 | Password masking | UI | Low |
| TC_Auth_05 | User logout | Functional | Medium |

### Menu Management Module

| Test ID | Scenario | Test Type | Priority |
|---------|----------|-----------|----------|
| TC_Menu_01 | View menu items | Positive | High |
| TC_Menu_02 | Category filtering | Functional | High |
| TC_Menu_03 | Missing image fallback | UI | Medium |
| TC_Menu_04 | Quick view modal | UI | Medium |
| TC_Menu_05 | Search functionality | Functional | High |

### Cart Management Module

| Test ID | Scenario | Test Type | Priority |
|---------|----------|-----------|----------|
| TC_Cart_01 | Add item to cart | Positive | Critical |
| TC_Cart_02 | Update cart quantity | Functional | High |
| TC_Cart_03 | Remove item from cart | Functional | High |
| TC_Cart_04 | Empty cart display | UI | Low |
| TC_Cart_05 | Cart persistence | Functional | Medium |

### Checkout Process Module

| Test ID | Scenario | Test Type | Priority |
|---------|----------|-----------|----------|
| TC_Checkout_01 | Valid delivery checkout | Positive | Critical |
| TC_Checkout_02 | Valid dine-in checkout | Positive | Critical |
| TC_Checkout_03 | Missing customer details | Negative | High |
| TC_Checkout_04 | Invalid phone number | Validation | Medium |
| TC_Checkout_05 | Order type selection | UI | Medium |

## 🔧 Debugging Utilities

### Available Debug Scripts

```bash
# Debug favorites functionality
python debug_favorites_buttons.py

# Test cart operations
python test_cart_buttons.py

# Comprehensive favorites testing
python test_favorites_comprehensive.py

# Authentication testing
python test_favorites_auth.py

# User creation for testing
python create_test_user.py

# Cart data setup
python create_test_carts.py
```

### Debug Script: `debug_favorites_buttons.py`

This script performs comprehensive debugging of the favorites functionality:

```python
# Key features:
- CSRF token validation
- Page load verification  
- HTML element detection
- JavaScript function checking
- API endpoint testing
- Detailed error reporting
```

**Usage:**
```bash
python debug_favorites_buttons.py
```

**Output Analysis:**
- ✅ Green checkmarks: Feature working correctly
- ❌ Red X marks: Issues found that need attention
- Detailed suggestions for fixing common problems

## 🚀 Running Tests

### Manual Testing Steps

1. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

2. **Open browser and navigate to:**
   ```
   http://127.0.0.1:8000/
   ```

3. **Execute test cases systematically:**
   - Follow test steps in sequence
   - Record actual results
   - Compare with expected results
   - Report any deviations

### Automated Testing

```bash
# Run Django unit tests
python manage.py test

# Run specific test modules
python manage.py test main.tests.test_views
python manage.py test main.tests.test_models

# Run with coverage report
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Debug Testing Process

1. **Setup Test Environment:**
   ```bash
   # Create test user
   python create_test_user.py
   
   # Setup test data
   python create_test_carts.py
   ```

2. **Run Debug Scripts:**
   ```bash
   # Test favorites functionality
   python debug_favorites_buttons.py
   
   # Test comprehensive features
   python test_favorites_comprehensive.py
   ```

3. **Browser Debug Steps:**
   - Open Developer Tools (F12)
   - Check Console for JavaScript errors
   - Monitor Network tab for API calls
   - Verify CSRF tokens in requests

## 🐛 Common Issues & Solutions

### Issue 1: Favorites Buttons Not Working

**Symptoms:**
- Buttons appear but don't respond to clicks
- No network requests in browser dev tools
- JavaScript console shows errors

**Debug Steps:**
```bash
python debug_favorites_buttons.py
```

**Common Causes:**
- Missing JavaScript event listeners
- CSRF token not found
- User not authenticated
- Missing `{% block extra_js %}` in base template

**Solutions:**
1. Verify `{% block extra_js %}` exists in `base.html`
2. Check user authentication status
3. Ensure CSRF tokens are present
4. Verify JavaScript functions are loaded

### Issue 2: Image Display Errors

**Symptoms:**
- ValueError: 'image' attribute has no file associated
- Broken image icons on pages

**Debug Steps:**
- Check database for items without images
- Verify static files configuration
- Test image upload functionality

**Solutions:**
1. Add conditional image checks in templates:
   ```django
   {% if food.image %}
       <img src="{{ food.image.url }}" alt="{{ food.title }}">
   {% else %}
       <img src="{% static 'images/sample_food.jpg' %}" alt="{{ food.title }}">
   {% endif %}
   ```

### Issue 3: CSRF Verification Failed

**Symptoms:**
- 403 Forbidden errors on form submissions
- "CSRF verification failed" messages

**Debug Steps:**
- Check for `{% csrf_token %}` in forms
- Verify CSRF middleware is enabled
- Test CSRF token in AJAX requests

**Solutions:**
1. Add CSRF tokens to all POST forms
2. Include CSRF headers in AJAX calls:
   ```javascript
   headers: {
       'X-CSRFToken': getCookie('csrftoken')
   }
   ```

### Issue 4: Real-time Features Not Working

**Symptoms:**
- Order status doesn't update automatically
- WebSocket connection failures

**Debug Steps:**
- Check Django Channels configuration
- Verify WebSocket URL patterns
- Test connection in browser console

**Solutions:**
1. Ensure Django Channels is properly installed
2. Configure ASGI application correctly
3. Check WebSocket URL routing

## 📊 Test Reporting

### Test Execution Report Template

```markdown
## Test Execution Report - [Date]

### Test Summary
- **Total Test Cases**: 50
- **Executed**: X
- **Passed**: X  
- **Failed**: X
- **Blocked**: X
- **Pass Rate**: X%

### Failed Test Cases
| Test ID | Module | Issue | Status |
|---------|--------|-------|--------|
| TC_XXX_XX | Module Name | Description | Open/Fixed |

### Environment Details
- **Browser**: Chrome 120.0.6099.109
- **OS**: Windows 11
- **Django Version**: 5.2
- **Database**: SQLite

### Recommendations
1. Issue 1 - Description and suggested fix
2. Issue 2 - Description and suggested fix
```

## 📚 Best Practices

### Testing Guidelines

1. **Test Data Management**
   - Use separate test database
   - Create isolated test scenarios
   - Clean up test data after tests

2. **Browser Testing**
   - Test on multiple browsers
   - Check responsive design
   - Verify JavaScript compatibility

3. **Security Testing**
   - Verify CSRF protection
   - Test authentication boundaries
   - Check input validation

4. **Performance Testing**
   - Monitor page load times
   - Test with large datasets
   - Verify AJAX response times

### Code Quality

1. **Follow PEP 8** for Python code
2. **Use ESLint** for JavaScript
3. **Validate HTML** with W3C validator
4. **Test CSS** across browsers

## 🔄 Continuous Integration

### GitHub Actions Workflow

```yaml
name: RTMS Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.12
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python manage.py test
```

## 📞 Support & Contribution

### Getting Help

1. **Check this documentation** first
2. **Run debug scripts** to identify issues
3. **Review Django logs** for server-side errors
4. **Check browser console** for client-side issues

### Contributing Tests

1. Follow the test case template
2. Include both positive and negative scenarios
3. Add debug scripts for complex features
4. Update documentation for new test cases

### Contact Information

- **Project Repository**: [GitHub Link]
- **Documentation**: [Wiki Link]
- **Issue Tracker**: [Issues Link]

---

## 📄 License

This testing documentation is part of the Restaurant Management System project and follows the same license terms as the main project.

---

**Last Updated**: [Current Date]  
**Version**: 1.0  
**Maintainer**: RTMS Development Team