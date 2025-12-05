# CopilotKit AG-UI Integration for ADK Agents

This guide explains how to integrate Google ADK agents with CopilotKit's AG-UI protocol to create a modern, user-facing chat interface.

## Overview

**AG-UI (Agent-to-User Interface)** is a protocol that allows AI agents to communicate with frontend applications. CopilotKit provides official support for ADK agents via this protocol.

### Architecture

```
┌──────────────────────┐         AG-UI Protocol         ┌─────────────────────┐
│                      │────────────────────────────────▶│                     │
│  Next.js + CopilotKit│        Tool calls, messages     │  ADK Agent          │
│  (Port 3000)         │◀────────────────────────────────│  (Port 8000)        │
└──────────────────────┘                                 └─────────────────────┘
```

**Key Benefits:**
- Modern chat UI out of the box
- Real-time tool execution visualization
- No need for custom API proxy layer
- Native ADK agent support

## Prerequisites

- Existing ADK agent (see `02_python_development.md`)
- Node.js 18+ installed
- Basic knowledge of React/Next.js

## Quick Start

### 1. Create Next.js Frontend

```bash
# Create new Next.js project
npx -y create-next-app@latest my-agent-ui --typescript --tailwind --app --no-src-dir

# Navigate to project
cd my-agent-ui

# Install CopilotKit dependencies
npm install @copilotkit/react-core @copilotkit/react-ui
```

### 2. Configure CopilotKit Provider

**File:** `app/layout.tsx`

```typescript
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { CopilotKit } from '@copilotkit/react-core';
import '@copilotkit/react-ui/styles.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'ADK Agent Chat',
  description: 'Chat interface for ADK agent',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <CopilotKit runtimeUrl="http://localhost:8000/copilotkit">
          {children}
        </CopilotKit>
      </body>
    </html>
  );
}
```

### 3. Add Chat Interface

**File:** `app/page.tsx`

```typescript
'use client';

import { CopilotChat } from '@copilotkit/react-ui';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="w-full max-w-4xl">
        <h1 className="text-3xl font-bold mb-8">ADK Agent Chat</h1>
        <div className="h-[600px] border rounded-lg shadow-lg">
          <CopilotChat
            labels={{
              title: "Product Assistant",
              initial: "Hi! I can help you find products. What are you looking for?",
            }}
          />
        </div>
      </div>
    </main>
  );
}
```

### 4. Start Both Servers

```bash
# Terminal 1: Start ADK agent
cd path/to/your-agent
adk web --port 8000

# Terminal 2: Start Next.js frontend
cd my-agent-ui
npm run dev
```

### 5. Test the Integration

1. Open browser to `http://localhost:3000`
2. You should see the CopilotKit chat interface
3. Test agent functionality through the chat
4. Verify tool calls execute correctly

## ADK Agent Endpoint

ADK agents running with `adk web` automatically expose an AG-UI compatible endpoint. The default endpoint path is:

```
http://localhost:8000/copilotkit
```

**Important:** Verify this endpoint path matches your ADK version. Check the ADK documentation or inspect the running agent's routes.

## Advanced Configuration

### Custom Styling

```typescript
<CopilotChat
  className="h-full"
  labels={{
    title: "Your Agent Name",
    initial: "Custom welcome message",
    placeholder: "Ask me anything...",
  }}
  makeSystemMessage={(message) => {
    // Customize system messages
    return message;
  }}
/>
```

### Using CopilotSidebar

For a sidebar layout instead of full-page chat:

```typescript
import { CopilotSidebar } from '@copilotkit/react-ui';

<CopilotSidebar>
  <YourMainContent />
</CopilotSidebar>
```

### CORS Configuration

If you encounter CORS issues during development, you may need to configure your ADK agent to allow requests from `http://localhost:3000`.

## Deployment

### Option 1: Local Development
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Simple for testing and iteration

### Option 2: Cloud Deployment
1. Deploy ADK agent to Cloud Run (see `04_advanced_topics.md`)
2. Update `runtimeUrl` in `layout.tsx` to your Cloud Run URL
3. Deploy Next.js to Vercel, Netlify, or Cloud Run

**Example for production:**
```typescript
<CopilotKit runtimeUrl="https://your-agent.run.app/copilotkit">
```

## Troubleshooting

### Issue: "Cannot connect to runtime"

**Solution:**
1. Verify ADK agent is running: `adk web --port 8000`
2. Check endpoint path is correct (default: `/copilotkit`)
3. Verify no CORS errors in browser console
4. Ensure both servers are running on expected ports

### Issue: Tools not executing

**Solution:**
1. Check that tools are properly defined in `agent.py`
2. Verify tool docstrings are clear and descriptive
3. Check ADK agent logs for errors
4. Test tools directly via `adk run` first

### Issue: Messages not appearing

**Solution:**
1. Check browser console for JavaScript errors
2. Verify `@copilotkit/react-ui/styles.css` is imported
3. Ensure CopilotKit provider wraps your entire app

## Testing Workflow

1. **Start ADK agent** with `adk web --port 8000`
2. **Start frontend** with `npm run dev`
3. **Test basic chat** - verify connection
4. **Test tool calls** - verify tools execute correctly
5. **Test error handling** - verify graceful error messages
6. **Review agent logs** - check for any backend issues

## Best Practices

1. **Clear Tool Documentation** - Write descriptive docstrings for all tools
2. **Error Handling** - Implement proper error responses in tools
3. **Structured Outputs** - Format tool responses clearly
4. **User Feedback** - Use CopilotKit's built-in message formatting
5. **Testing** - Test agent behavior thoroughly before deployment

## Resources

- [CopilotKit ADK Documentation](https://docs.copilotkit.ai/adk)
- [CopilotKit Quickstart](https://docs.copilotkit.ai/adk/quickstart)
- [ADK Development Workflow](./adk_development_workflow.md)
- [Google ADK Documentation](https://cloud.google.com/agent-developer-kit)

## Example Project Structure

```
my-adk-project/
├── my-agent/                    # ADK agent
│   ├── agent.py
│   ├── tools.py
│   └── requirements.txt
└── my-agent-ui/                 # Next.js frontend
    ├── app/
    │   ├── layout.tsx           # CopilotKit provider
    │   └── page.tsx             # Chat interface
    ├── package.json
    └── next.config.js
```

## Next Steps

After setting up the integration:
1. Customize the chat interface styling
2. Add custom components for rich tool responses
3. Implement user authentication if needed
4. Deploy to production environments
5. Monitor agent performance and user interactions
