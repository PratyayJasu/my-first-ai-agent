import { ChatRequest, ChatResponse, ConversationHistory, ToolInfo } from '../types';

// Use environment variable for production, fallback to /api for local dev (proxied by Vite)
const API_BASE = import.meta.env.VITE_API_URL || '/api';

export const api = {
    async sendMessage(message: string): Promise<ChatResponse> {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message } as ChatRequest),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return response.json();
    },

    async getHistory(): Promise<ConversationHistory> {
        const response = await fetch(`${API_BASE}/chat/history`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return response.json();
    },

    async clearHistory(): Promise<void> {
        const response = await fetch(`${API_BASE}/chat/history`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
    },

    async getTools(): Promise<ToolInfo[]> {
        const response = await fetch(`${API_BASE}/chat/tools`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return response.json();
    },

    async healthCheck(): Promise<boolean> {
        try {
            const response = await fetch(`${API_BASE}/health`);
            return response.ok;
        } catch {
            return false;
        }
    },
};
