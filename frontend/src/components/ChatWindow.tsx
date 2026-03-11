import React from 'react';
import { useChat } from '../hooks/useChat';
import { Header } from './Header';
import { MessageList } from './MessageList';
import { InputBar } from './InputBar';

export const ChatWindow: React.FC = () => {
    const { messages, isLoading, error, sendMessage, clearChat } = useChat();

    return (
        <div className="flex flex-col h-screen bg-gray-50">
            <Header onClearChat={clearChat} />

            {error && (
                <div className="bg-red-50 border-b border-red-200 px-4 py-2 text-red-700 text-sm">
                    {error}
                </div>
            )}

            <MessageList messages={messages} isLoading={isLoading} />
            <InputBar onSend={sendMessage} disabled={isLoading} />
        </div>
    );
};
