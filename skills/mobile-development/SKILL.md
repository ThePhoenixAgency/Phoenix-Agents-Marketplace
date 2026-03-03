---
name: mobile-development
description: React Native, Flutter, responsive layouts
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---
# Mobile Development
## React Native
```typescript
import { View, Text, FlatList, StyleSheet } from 'react-native';
function UserList({ users }: { users: User[] }) {
  return (
    <FlatList
      data={users}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => (
        <View style={styles.card}>
          <Text style={styles.name}>{item.name}</Text>
        </View>
      )}
    />
  );
}
const styles = StyleSheet.create({
  card: { padding: 16, borderBottomWidth: 1, borderColor: '#eee' },
  name: { fontSize: 16, fontWeight: '600' },
});
```
## Flutter
```dart
class UserList extends StatelessWidget {
  final List<User> users;
  const UserList({required this.users});
  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: users.length,
      itemBuilder: (context, index) => ListTile(
        title: Text(users[index].name),
        subtitle: Text(users[index].email),
      ),
    );
  }
}
```
## Responsive
- Utiliser Dimensions / MediaQuery
- Flexbox pour les layouts
- Tester sur plusieurs tailles d'ecran
- Safe area pour les encoches
