# Frontend Development

## UI Components and Pages

### Core Components
1. Navigation Bar
2. Sidebar Menu
3. Character Sheet Display
4. Map Viewer
5. AI Generation Interface
6. Form Components

### Pages
1. Dashboard
2. NPC Creator/Editor
3. Encounter Builder
4. Campaign Manager
5. Map Generator/Editor
6. Settings

## Component Examples

### NPC Form Component
```jsx
const NPCForm = ({ onSubmit, initialData }) => {
  // Form implementation with character creation fields
  // Integration with AI generation
  // Portrait upload/generation
};
```

### Map Viewer Component
```jsx
const MapViewer = ({ mapData }) => {
  // Interactive map display
  // Marker management
  // Zoom and pan controls
};
```

### AI Generation Interface
```jsx
const AIGenerator = ({ type, onGenerate }) => {
  // Type-specific generation controls
  // Parameter configuration
  // Results display
};
```

## State Management

### React Context Structure
```jsx
const AppContext = {
  campaign: CampaignContext,
  npcs: NPCContext,
  maps: MapContext,
  encounters: EncounterContext,
  ai: AIContext
};
```

### API Communication
- Axios for HTTP requests
- Request interceptors for authentication
- Response handling and error management
- Caching strategy

## Routing Structure
```jsx
<Router>
  <Routes>
    <Route path="/" element={<Dashboard />} />
    <Route path="/npcs/*" element={<NPCRoutes />} />
    <Route path="/encounters/*" element={<EncounterRoutes />} />
    <Route path="/campaigns/*" element={<CampaignRoutes />} />
    <Route path="/maps/*" element={<MapRoutes />} />
    <Route path="/settings" element={<Settings />} />
  </Routes>
</Router>
```
