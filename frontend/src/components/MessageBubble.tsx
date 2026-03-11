import React from 'react';
import { Message } from '../types';

interface MessageBubbleProps {
    message: Message;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
    const isUser = message.role === 'user';

    return (
        <div
            className={`flex ${isUser ? 'justify-end' : 'justify-start'} message-enter`}
        >
            <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 ${isUser
                        ? 'bg-primary-600 text-white rounded-br-md'
                        : 'bg-gray-100 text-gray-800 rounded-bl-md'
                    }`}
            >
                <p className="whitespace-pre-wrap break-words text-sm leading-relaxed">
                    {message.content}
                </p>
            </div>
        </div>
    );
};
