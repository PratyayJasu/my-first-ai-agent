import React, { useRef, useEffect } from 'react';
import { Message } from '../types';
import { MessageBubble } from './MessageBubble';
import { TypingIndicator } from './TypingIndicator';

interface MessageListProps {
    messages: Message[];
    isLoading: boolean;
}

export const MessageList: React.FC<MessageListProps> = ({ messages, isLoading }) => {
    const bottomRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, isLoading]);

    if (messages.length === 0 && !isLoading) {
        return (
            <div className="flex-1 flex items-center justify-center text-gray-400">
                <div className="text-center">
                    <div className="text-6xl mb-4">🤖</div>
                    <p className="text-lg font-medium">AI Assistant</p>
                    <p className="text-sm mt-2">Ask me anything! I can help with:</p>
                    <ul className="text-sm mt-2 space-y-1">
                        <li>📅 Date & time</li>
                        <li>🔢 Calculations</li>
                        <li>🔍 Web search</li>
                        <li>📝 Note taking</li>
                        <li>💻 Shell commands</li>
                    </ul>
                </div>
            </div>
        );
    }

    return (
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message, index) => (
                <MessageBubble key={index} message={message} />
            ))}
            {isLoading && <TypingIndicator />}
            <div ref={bottomRef} />
        </div>
    );
};
