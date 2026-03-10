import { useState, useCallback, useEffect } from 'react';
import { Message } from '../types';
import { api } from '../services/api';

export function useChat() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Load conversation history on mount
    useEffect(() => {
        const loadHistory = async () => {
            try {
                const history = await api.getHistory();
                if (history.messages.length > 0) {
                    setMessages(history.messages as Message[]);
                }
            } catch (err) {
                console.error('Failed to load history:', err);
            }
        };
        loadHistory();
    }, []);

    const sendMessage = useCallback(async (content: string) => {
        if (!content.trim()) return;

        const userMessage: Message = {
            role: 'user',
            content: content.trim(),
            timestamp: new Date().toISOString(),
        };

        setMessages(prev => [...prev, userMessage]);
        setIsLoading(true);
        setError(null);

        try {
            const response = await api.sendMessage(content);

            const assistantMessage: Message = {
                role: 'assistant',
                content: response.response,
                timestamp: response.timestamp,
            };

            setMessages(prev => [...prev, assistantMessage]);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred');
            // Remove the user message if request failed
            setMessages(prev => prev.slice(0, -1));
        } finally {
            setIsLoading(false);
        }
    }, []);

    const clearChat = useCallback(async () => {
        try {
            await api.clearHistory();
            setMessages([]);
            setError(null);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to clear chat');
        }
    }, []);

    return {
        messages,
        isLoading,
        error,
        sendMessage,
        clearChat,
    };
}
