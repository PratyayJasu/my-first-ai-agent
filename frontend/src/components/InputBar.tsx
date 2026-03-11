import React, { useState, useRef, useEffect } from 'react';

interface InputBarProps {
    onSend: (message: string) => void;
    disabled: boolean;
}

export const InputBar: React.FC<InputBarProps> = ({ onSend, disabled }) => {
    const [input, setInput] = useState('');
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (input.trim() && !disabled) {
            onSend(input);
            setInput('');
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    // Auto-resize textarea
    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
            textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
        }
    }, [input]);

    return (
        <form onSubmit={handleSubmit} className="border-t bg-white p-4">
            <div className="flex items-end gap-3 max-w-4xl mx-auto">
                <div className="flex-1 relative">
                    <textarea
                        ref={textareaRef}
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Type a message..."
                        disabled={disabled}
                        rows={1}
                        className="w-full resize-none rounded-2xl border border-gray-200 px-4 py-3 pr-12 
                       focus:outline-none focus:border-primary-500 focus:ring-1 focus:ring-primary-500
                       disabled:bg-gray-50 disabled:text-gray-400
                       text-sm leading-relaxed"
                    />
                </div>
                <button
                    type="submit"
                    disabled={disabled || !input.trim()}
                    className="flex-shrink-0 w-10 h-10 rounded-full bg-primary-600 text-white
                     flex items-center justify-center
                     hover:bg-primary-700 transition-colors
                     disabled:bg-gray-300 disabled:cursor-not-allowed"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        fill="currentColor"
                        className="w-5 h-5"
                    >
                        <path d="M3.478 2.404a.75.75 0 0 0-.926.941l2.432 7.905H13.5a.75.75 0 0 1 0 1.5H4.984l-2.432 7.905a.75.75 0 0 0 .926.94 60.519 60.519 0 0 0 18.445-8.986.75.75 0 0 0 0-1.218A60.517 60.517 0 0 0 3.478 2.404Z" />
                    </svg>
                </button>
            </div>
            <p className="text-xs text-gray-400 text-center mt-2">
                Press Enter to send, Shift+Enter for new line
            </p>
        </form>
    );
};
