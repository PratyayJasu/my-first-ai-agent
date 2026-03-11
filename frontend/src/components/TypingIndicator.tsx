import React from 'react';

export const TypingIndicator: React.FC = () => {
    return (
        <div className="flex justify-start message-enter">
            <div className="bg-gray-100 rounded-2xl rounded-bl-md px-4 py-3">
                <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
                </div>
            </div>
        </div>
    );
};
