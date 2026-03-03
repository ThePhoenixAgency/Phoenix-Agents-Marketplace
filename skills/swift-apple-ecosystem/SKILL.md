---
name: swift-apple-ecosystem
description: SwiftUI, MVVM, async/await, Combine, HIG, Xcode
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---
# Swift & Apple Ecosystem
## SwiftUI + MVVM
```swift
// Model
struct User: Identifiable, Codable {
    let id: UUID
    var name: String
    var email: String
}
// ViewModel
@Observable
final class UserViewModel {
    private(set) var users: [User] = []
    private(set) var isLoading = false
    private let service: UserService

    init(service: UserService = .init()) {
        self.service = service
    }

    func loadUsers() async {
        isLoading = true
        defer { isLoading = false }
        do {
            users = try await service.fetchUsers()
        } catch {
            // handle error
        }
    }
}
// View
struct UserListView: View {
    @State private var viewModel = UserViewModel()

    var body: some View {
        NavigationStack {
            List(viewModel.users) { user in
                NavigationLink(user.name) {
                    UserDetailView(user: user)
                }
            }
            .navigationTitle("Users")
            .task { await viewModel.loadUsers() }
            .overlay {
                if viewModel.isLoading { ProgressView() }
            }
        }
    }
}
```
## Async/Await
```swift
func fetchData() async throws -> [Item] {
    let (data, response) = try await URLSession.shared.data(from: url)
    guard let httpResponse = response as? HTTPURLResponse,
          httpResponse.statusCode == 200 else {
        throw APIError.invalidResponse
    }
    return try JSONDecoder().decode([Item].self, from: data)
}
```
## Conventions
- Structs par defaut, classes uniquement si reference semantics necessaire
- guard let pour les sorties anticipees
- Extensions pour organiser les conformites aux protocoles
- Nommage expressif : fetchUserData(for: userID)
- [weak self] dans les closures pour eviter les retain cycles
## HIG obligatoires
- Dark Mode natif
- SF Symbols pour les icones
- Dynamic Type pour les tailles de texte
- VoiceOver accessibility labels
- Navigation native (NavigationStack, TabView)
