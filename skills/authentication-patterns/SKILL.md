---
name: authentication-patterns
description: JWT, OAuth2 PKCE, RBAC, session management
---
# Authentication Patterns
## JWT
```typescript
const token = jwt.sign(
  { userId: user.id, role: user.role },
  process.env.JWT_SECRET,
  { expiresIn: '15m', algorithm: 'HS256' }
);
// Refresh token: long-lived, stored in httpOnly cookie
const refreshToken = jwt.sign(
  { userId: user.id },
  process.env.REFRESH_SECRET,
  { expiresIn: '7d' }
);
```
## OAuth2 PKCE
```
1. Client genere code_verifier (random string)
2. Client genere code_challenge = SHA256(code_verifier)
3. Client redirige vers /authorize?code_challenge=...
4. User se connecte, serveur renvoie authorization_code
5. Client echange code + code_verifier pour un access_token
```
## RBAC
```typescript
const permissions = {
  admin: ['read', 'write', 'delete', 'manage'],
  editor: ['read', 'write'],
  viewer: ['read'],
};
function authorize(user, permission) {
  const userPerms = permissions[user.role] || [];
  if (!userPerms.includes(permission)) {
    throw new ForbiddenError('Insufficient permissions');
  }
}
```
## Checklist securite auth
- [ ] Passwords hashes avec bcrypt/argon2 (jamais MD5/SHA1)
- [ ] Access tokens courts (15min)
- [ ] Refresh tokens en httpOnly secure cookie
- [ ] Rate limiting sur /login
- [ ] Lockout apres N tentatives echouees
- [ ] CSRF protection sur les formulaires
- [ ] MFA recommande pour les admins
