export interface Message {
    role: 'user' | 'assistant';
    content: string;
    timestamp?: string;
}

export interface ChatRequest {
    message: string;
}

export interface ChatResponse {
    response: string;
    conversation_length: number;
    timestamp: string;
}

export interface ConversationHistory {
    messages: Message[];
}

export interface ToolInfo {
    name: string;
    description: string;
    parameters: Record<string, unknown>;
}
