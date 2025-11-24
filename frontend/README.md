# Frontend - TechFirstSearch

React Native application with Web and iOS support.

## Quick Start

1. Install dependencies:
```bash
npm install
```

2. Configure API endpoint in `src/config.ts`:
```typescript
export const API_BASE_URL = 'http://localhost:8000';
```

3. Run development server:
```bash
npm start      # All platforms
npm run web    # Web only
npm run ios    # iOS only
```

## Project Structure

```
frontend/
├── App.tsx                          # Main app component
├── index.js                         # Entry point
├── src/
│   ├── components/
│   │   ├── ContentCard.tsx          # Content card component
│   │   └── SearchBar.tsx            # Search input component
│   ├── screens/
│   │   ├── FeedScreen.tsx           # Main feed screen
│   │   └── ContentViewerScreen.tsx  # Article viewer
│   ├── context/
│   │   └── ContentContext.tsx       # Global state management
│   ├── services/
│   │   └── api.ts                   # API client
│   ├── config.ts                    # Configuration
│   └── types.ts                     # TypeScript types
├── package.json
├── app.json
└── tsconfig.json
```

## Key Features

### Components

**ContentCard**
- Displays content with title, source, date, and type badge
- Color-coded by content type
- Thumbnail support
- Responsive design

**SearchBar**
- Real-time search with 300ms debounce
- Clear button
- Optimized performance

### Screens

**FeedScreen**
- Infinite scroll with pagination
- Pull-to-refresh
- Search integration
- Loading and error states

**ContentViewerScreen**
- Reader mode view (primary)
- WebView fallback
- Clean typography
- Source attribution

### State Management

Uses React Context for global state:
- Content list
- Loading states
- Search query
- Feed pagination

## Content Type Colors

- Papers: Blue (#3B82F6)
- Research: Purple (#8B5CF6)
- News: Red (#EF4444)
- Tutorial: Green (#10B981)
- Essay: Amber (#F59E0B)
- Article: Indigo (#6366F1)
- Post: Pink (#EC4899)

## Platform Support

### Web
Runs in any modern browser using React Native Web.

### iOS
Requires Xcode and macOS for development.

### Android
Can be added by configuring `app.json` and running `npm run android`.

## Building for Production

### Web
```bash
expo build:web
# Output in web-build/
```

### iOS
```bash
expo build:ios
```

## Customization

### Changing API Endpoint
Edit `src/config.ts`:
```typescript
export const API_BASE_URL = 'https://api.yourdomain.com';
```

### Styling
All styles use React Native StyleSheet API. Modify component styles in respective files.

### Adding Features
1. Create new component in `src/components/`
2. Add screen in `src/screens/`
3. Update navigation in `App.tsx`
4. Update types in `src/types.ts`

## Performance Optimization

- FlatList with virtualization for feed
- Image lazy loading
- Debounced search
- Memoized components (can be added with React.memo)
- Pull-to-refresh caching

## Troubleshooting

### Web not loading
Clear cache:
```bash
rm -rf .expo node_modules
npm install
npm run web
```

### iOS build issues
```bash
cd ios
pod install
cd ..
npm run ios
```

### TypeScript errors
```bash
npm run tsc --noEmit
```








<!-- 
- https://www.forerunnerventures.com/research
- https://www.forerunnerventures.com/perspectives


