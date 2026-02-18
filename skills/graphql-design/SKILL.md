---
name: graphql-design
description: Schema, DataLoader, subscriptions, pagination
---
# GraphQL Design
## Schema
```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts(first: Int, after: String): PostConnection!
}
type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}
type PostEdge {
  node: Post!
  cursor: String!
}
type PageInfo {
  hasNextPage: Boolean!
  endCursor: String
}
```
## DataLoader (N+1 prevention)
```typescript
const userLoader = new DataLoader(async (ids: string[]) => {
  const users = await db.users.findMany({ where: { id: { in: ids } } });
  return ids.map(id => users.find(u => u.id === id));
});
```
## Subscriptions
```typescript
const typeDefs = gql`
  type Subscription {
    messageAdded(channelId: ID!): Message!
  }
`;
const resolvers = {
  Subscription: {
    messageAdded: {
      subscribe: (_, { channelId }) => pubsub.asyncIterator(`MESSAGE_${channelId}`),
    },
  },
};
```
