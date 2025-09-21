# JavaScript Frontend Stack Trait

## Description
Modern JavaScript/TypeScript frontend development toolchain including build tools, testing frameworks, and code quality tools. This trait standardizes frontend development environments across agents.

## Content

### Frontend Development Tools

**Build Tools:**
- Vite ^5.0.0 - Fast build tool with hot module replacement and optimized production builds
- Webpack ^5.89.0 - Module bundler with advanced optimization and plugin ecosystem
- Parcel ^2.10.0 - Zero-configuration build tool for rapid development
- Rollup ^4.0.0 - Module bundler optimized for libraries and tree-shaking

**Testing Tools:**
- Jest ^29.7.0 - Comprehensive testing framework with snapshot testing and mocking
- Vitest ^1.0.0 - Fast unit testing framework with native ES modules support
- Cypress ^13.0.0 - End-to-end testing with real browser automation
- Playwright ^1.40.0 - Cross-browser testing with powerful automation capabilities
- React Testing Library ^14.0.0 - Component testing with user-centric approach

**Code Quality Tools:**
- ESLint ^8.55.0 - JavaScript/TypeScript linting with customizable rules
- Prettier ^3.1.0 - Code formatting with consistent style enforcement
- TypeScript ^5.3.0 - Static type checking for JavaScript with advanced type features
- Husky ^8.0.0 - Git hooks for automated code quality checks

**Framework-Specific Tools:**
- React Developer Tools - Browser extension for React debugging
- Vue DevTools - Browser extension for Vue.js debugging
- Angular CLI - Command-line interface for Angular development
- Storybook ^7.6.0 - Component development and documentation tool

### Tool Configurations

**Package.json Scripts:**
```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "test:e2e": "playwright test",
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
    "lint:fix": "eslint . --ext .js,.jsx,.ts,.tsx --fix",
    "format": "prettier --write .",
    "type-check": "tsc --noEmit"
  }
}
```

**Vite Configuration (vite.config.ts):**
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom']
        }
      }
    }
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts']
  }
})
```

**ESLint Configuration (.eslintrc.json):**
```json
{
  "extends": [
    "eslint:recommended",
    "@typescript-eslint/recommended",
    "react-hooks/recommended"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module",
    "ecmaFeatures": {
      "jsx": true
    }
  },
  "plugins": ["react-refresh", "@typescript-eslint"],
  "rules": {
    "react-refresh/only-export-components": [
      "warn",
      { "allowConstantExport": true }
    ],
    "@typescript-eslint/no-unused-vars": "error",
    "react-hooks/exhaustive-deps": "warn"
  }
}
```

**Prettier Configuration (.prettierrc):**
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false
}
```

**TypeScript Configuration (tsconfig.json):**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### Testing Execution Strategy

**Jest/Vitest Projects:**
- Detection: Look for jest.config.js, vitest.config.ts, or testing framework in package.json
- Primary command: `npm test` or `yarn test`
- Coverage command: `npm run test:coverage`
- Watch mode: `npm test -- --watch`
- UI mode (Vitest): `npm run test:ui`

**Cypress E2E Testing:**
- Detection: Look for cypress.config.js or cypress/ directory
- Interactive mode: `npx cypress open`
- Headless command: `npx cypress run`
- Component testing: `npx cypress run --component`

**Playwright E2E Testing:**
- Detection: Look for playwright.config.ts or @playwright/test in dependencies
- Primary command: `npx playwright test`
- UI mode: `npx playwright test --ui`
- Debug mode: `npx playwright test --debug`

### Development Workflow

**Setup Commands:**
```bash
# Install dependencies
npm install
# or
yarn install

# Setup git hooks
npx husky install

# Start development server
npm run dev
```

**Development Commands:**
```bash
# Run tests
npm test

# Run tests with coverage
npm run test:coverage

# Run linting
npm run lint

# Fix linting issues
npm run lint:fix

# Format code
npm run format

# Type checking
npm run type-check

# Build for production
npm run build
```

### Quality Gates

**Code Quality:**
- ESLint passing with no errors
- Prettier formatting enforced
- TypeScript strict mode with no errors
- Import organization with proper dependency separation

**Testing:**
- Unit test coverage > 80% for component logic
- E2E tests covering critical user journeys
- Component tests with user interaction validation
- Visual regression testing for UI components

**Performance:**
- Bundle size optimization with tree shaking
- Code splitting for optimal loading
- Lighthouse scores: Performance > 90, Accessibility > 95
- Core Web Vitals within acceptable thresholds

## Usage Notes

- **Which agents should use this trait**: frontend-engineer, mobile-engineer (for React Native), any agent working with JavaScript/TypeScript frontend code
- **Customization guidance**: Framework-specific configurations can be added (e.g., Next.js specific tools for SSR projects)
- **Compatibility requirements**: Node.js 18+ with modern package managers (npm 9+ or yarn 3+)

## Implementation Priority
**MEDIUM-HIGH** - This trait affects 3-4 frontend-focused agents and provides comprehensive frontend development standardization