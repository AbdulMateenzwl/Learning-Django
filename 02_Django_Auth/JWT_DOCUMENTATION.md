# JWT Authentication with djangorestframework-simplejwt

## Overview

This project demonstrates JWT (JSON Web Token) authentication implementation using Django REST Framework and the `djangorestframework-simplejwt` package.

## What is JWT?

JWT (JSON Web Token) is a compact, URL-safe token format used for securely transmitting information between parties. JWTs are self-contained and include all necessary information about the user, eliminating the need for server-side session storage.

### JWT Structure

A JWT consists of three parts separated by dots (.):

1. **Header**: Contains token type (JWT) and signing algorithm (HS256)
2. **Payload**: Contains claims (user data, expiration time, etc.)
3. **Signature**: Ensures token integrity and authenticity

Example JWT:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

### Benefits of JWT

- **Stateless**: No server-side session storage required
- **Scalable**: Works well in distributed systems and microservices
- **Cross-domain**: Can be used across different domains
- **Self-contained**: All user information is encoded in the token
- **Mobile-friendly**: Perfect for mobile and SPA applications

## Implementation Details

### 1. Packages Used

- `djangorestframework`: Django REST Framework for API development
- `djangorestframework-simplejwt`: JWT implementation for Django REST Framework

### 2. Key Configuration

#### Settings Configuration (`settings.py`)

```python
INSTALLED_APPS = [
    # ... other apps
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',  # For token blacklisting
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),     # Access token expires in 1 hour
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),        # Refresh token expires in 7 days
    'ROTATE_REFRESH_TOKENS': True,                      # Generate new refresh token on refresh
    'BLACKLIST_AFTER_ROTATION': True,                   # Blacklist old refresh tokens
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}
```

### 3. API Endpoints

#### Authentication Endpoints

- `POST /api/register/` - Register new user
- `POST /api/token/` - Login and get tokens
- `POST /api/token/refresh/` - Refresh access token
- `POST /api/token/verify/` - Verify token validity
- `POST /api/logout/` - Logout and blacklist token

#### User Management Endpoints

- `GET /api/profile/` - Get user profile
- `PUT /api/profile/update/` - Update user profile

### 4. Token Types

#### Access Token
- **Purpose**: Used for API authentication
- **Lifetime**: 60 minutes (configurable)
- **Usage**: Include in Authorization header as `Bearer <token>`

#### Refresh Token
- **Purpose**: Used to obtain new access tokens
- **Lifetime**: 7 days (configurable)
- **Usage**: Send to `/api/token/refresh/` endpoint

## API Usage Examples

### 1. User Registration

```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "SecurePassword123!",
    "password2": "SecurePassword123!",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

**Response:**
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "username": "newuser",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

### 2. User Login

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "SecurePassword123!"
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "newuser",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### 3. Get User Profile

```bash
curl -X GET http://127.0.0.1:8000/api/profile/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### 4. Refresh Access Token

```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'
```

### 5. Update Profile

```bash
curl -X PUT http://127.0.0.1:8000/api/profile/update/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Updated",
    "email": "updated@example.com"
  }'
```

### 6. Logout

```bash
curl -X POST http://127.0.0.1:8000/api/logout/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'
```

## Frontend Integration

### JavaScript/AJAX Example

```javascript
// Store tokens in localStorage
localStorage.setItem('access_token', data.access);
localStorage.setItem('refresh_token', data.refresh);

// Make authenticated requests
async function makeAuthenticatedRequest(url, options = {}) {
  const token = localStorage.getItem('access_token');
  
  const config = {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    }
  };
  
  let response = await fetch(url, config);
  
  // If token expired, try to refresh
  if (response.status === 401) {
    const refreshed = await refreshToken();
    if (refreshed) {
      // Retry request with new token
      config.headers['Authorization'] = `Bearer ${localStorage.getItem('access_token')}`;
      response = await fetch(url, config);
    }
  }
  
  return response;
}

// Refresh token function
async function refreshToken() {
  const refreshToken = localStorage.getItem('refresh_token');
  
  try {
    const response = await fetch('/api/token/refresh/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        refresh: refreshToken
      })
    });
    
    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('access_token', data.access);
      return true;
    } else {
      // Refresh token is invalid, logout user
      logout();
      return false;
    }
  } catch (error) {
    logout();
    return false;
  }
}
```

## Security Considerations

### 1. Token Storage
- **Frontend**: Store tokens in memory or secure httpOnly cookies
- **Avoid**: localStorage for sensitive applications (XSS vulnerable)
- **Mobile**: Use secure storage mechanisms

### 2. Token Rotation
- Enabled `ROTATE_REFRESH_TOKENS` to generate new refresh tokens
- Enabled `BLACKLIST_AFTER_ROTATION` to invalidate old tokens

### 3. Token Expiration
- Short access token lifetime (60 minutes)
- Longer refresh token lifetime (7 days)
- Implement automatic token refresh

### 4. HTTPS
- Always use HTTPS in production
- Prevents token interception

### 5. CORS Configuration
```python
# Add to settings.py for frontend apps
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React app
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True
```

## Testing

### 1. Automated Testing
Run the provided test script:
```bash
python test_jwt_api.py
```

### 2. Manual Testing
Visit the JWT demo page:
```
http://127.0.0.1:8000/jwt-demo
```

### 3. API Testing Tools
- **Postman**: Import API collection
- **curl**: Command-line testing
- **HTTPie**: User-friendly HTTP client

## Production Deployment

### 1. Environment Variables
```python
# settings.py
import os
from datetime import timedelta

SECRET_KEY = os.environ.get('SECRET_KEY')

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.environ.get('ACCESS_TOKEN_MINUTES', 15))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.environ.get('REFRESH_TOKEN_DAYS', 7))),
    # ... other settings
}
```

### 2. Database
- Use PostgreSQL or MySQL instead of SQLite
- Regular backups of token blacklist tables

### 3. Monitoring
- Monitor token usage patterns
- Set up alerts for suspicious activity
- Log authentication events

### 4. Rate Limiting
```python
# Add to settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

## Common Issues and Solutions

### 1. Token Expiration
**Problem**: Access token expired
**Solution**: Implement automatic token refresh

### 2. CORS Issues
**Problem**: Browser blocks API requests
**Solution**: Configure CORS properly in Django settings

### 3. Token Blacklisting
**Problem**: Logout doesn't work properly
**Solution**: Ensure token blacklist app is installed and migrated

### 4. Clock Skew
**Problem**: Tokens expire unexpectedly
**Solution**: Synchronize server clocks, add clock skew tolerance

## Advanced Features

### 1. Custom Claims
Add custom data to JWT tokens:

```python
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.groups.first().name if user.groups.exists() else 'user'
        token['permissions'] = list(user.user_permissions.values_list('codename', flat=True))
        return token
```

### 2. Multiple Token Types
Implement different tokens for different purposes:

```python
SIMPLE_JWT = {
    # ... other settings
    'AUTH_TOKEN_CLASSES': (
        'rest_framework_simplejwt.tokens.AccessToken',
        'rest_framework_simplejwt.tokens.RefreshToken',
    ),
}
```

### 3. Social Authentication
Integrate with social login providers:

```bash
pip install djoser
pip install social-auth-app-django
```

## Conclusion

This JWT implementation provides:
- Secure, stateless authentication
- Token rotation and blacklisting
- Comprehensive API endpoints
- Frontend integration examples
- Production-ready configuration

The system is scalable, secure, and follows Django best practices for authentication and authorization.
