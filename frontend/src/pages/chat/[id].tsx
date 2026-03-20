import { useRouter } from 'next/router';
import Head from 'next/head';
import { Layout } from '@/components';
import { useState, useEffect, useRef } from 'react';

// Mock auth token extraction or service (in real app, we use context/store)
const getCurrentUserId = () => "mock-user-id"; 

interface Message {
    id: string;
    sender_id: string;
    content: string;
    created_at: string;
    is_read: boolean;
}

export default function ChatRoom() {
    const router = useRouter();
    const { id } = router.query;
    
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputText, setInputText] = useState("");
    const [isConnected, setIsConnected] = useState(false);
    
    const wsRef = useRef<WebSocket | null>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const mockUserId = getCurrentUserId();

    // Auto-scroll to bottom when messages change
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        if (!id) return;

        // Fetch initial message history
        const fetchHistory = async () => {
            try {
                // Mock history fetch for now if backend is not running, but theoretically this works:
                // const res = await fetch(`http://localhost:8000/chat/${id}/messages`);
                // const data = await res.json();
                // setMessages(data);
                
                // Add some dummy history for demonstration
                setMessages([
                    {
                        id: 'msg1',
                        sender_id: 'other-user',
                        content: 'Hey! I saw we matched. Are you hitting the gym tomorrow?',
                        created_at: new Date(Date.now() - 3600000).toISOString(),
                        is_read: true,
                    },
                    {
                        id: 'msg2',
                        sender_id: mockUserId,
                        content: 'Yeah definitely! Im planning to do legs around 7 AM.',
                        created_at: new Date(Date.now() - 3500000).toISOString(),
                        is_read: true,
                    }
                ]);
            } catch (err) {
                console.error("Failed to fetch messages", err);
            }
        };

        fetchHistory();

        // Connect WebSocket
        const ws = new WebSocket(`ws://localhost:8000/chat/ws/${id}`);
        
        ws.onopen = () => setIsConnected(true);
        ws.onclose = () => setIsConnected(false);
        ws.onerror = (e) => console.error("WebSocket error", e);
        
        ws.onmessage = (event) => {
            const newMsg = JSON.parse(event.data);
            setMessages(prev => [...prev, newMsg]);
        };
        
        wsRef.current = ws;

        return () => {
            ws.close();
        };
    }, [id]);

    const sendMessage = (e: React.FormEvent) => {
        e.preventDefault();
        if (!inputText.trim() || !wsRef.current) return;
        
        const payload = {
            sender_id: mockUserId,
            content: inputText.trim()
        };
        
        // In reality, this goes to WS server
        if (wsRef.current.readyState === WebSocket.OPEN) {
            wsRef.current.send(JSON.stringify(payload));
        } else {
            // For Demo Purposes if Server is offline: simulate it instantly
            setMessages(prev => [...prev, {
                id: Math.random().toString(),
                sender_id: mockUserId,
                content: payload.content,
                created_at: new Date().toISOString(),
                is_read: true
            }]);
        }
        
        setInputText("");
    };

    return (
        <>
            <Head>
                <title>Chat - GymBuddy</title>
            </Head>
            <Layout>
                <main className="pt-24 pb-8 px-4 h-screen flex flex-col">
                    <div className="max-w-2xl mx-auto w-full flex-1 flex flex-col bg-gray-900 border border-gray-800 rounded-2xl overflow-hidden shadow-2xl">
                        
                        {/* Header */}
                        <div className="flex items-center justify-between px-6 py-4 bg-gray-800/80 backdrop-blur border-b border-gray-700">
                            <div className="flex items-center space-x-4">
                                <button 
                                    onClick={() => router.back()}
                                    className="p-2 -ml-2 text-gray-400 hover:text-white rounded-full hover:bg-gray-700 transition"
                                >
                                    ←
                                </button>
                                <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-purple-500 to-pink-500 flex items-center justify-center text-xl">
                                    💪
                                </div>
                                <div>
                                    <h2 className="font-semibold text-white">Your Match</h2>
                                    <div className="flex items-center text-xs text-gray-400 space-x-1">
                                        <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></span>
                                        <span>{isConnected ? 'Online' : 'Offline'}</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Messages Area */}
                        <div className="flex-1 overflow-y-auto p-6 space-y-4">
                            {messages.map((msg) => {
                                const isMe = msg.sender_id === mockUserId;
                                return (
                                    <div key={msg.id} className={`flex ${isMe ? 'justify-end' : 'justify-start'}`}>
                                        <div className={`max-w-[75%] rounded-2xl px-5 py-3 ${
                                            isMe 
                                            ? 'bg-purple-600 text-white rounded-br-sm' 
                                            : 'bg-gray-800 text-gray-100 rounded-bl-sm border border-gray-700'
                                        }`}>
                                            <p className="block">{msg.content}</p>
                                            <span className="text-[10px] opacity-60 mt-2 block text-right">
                                                {new Date(msg.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                                            </span>
                                        </div>
                                    </div>
                                );
                            })}
                            <div ref={messagesEndRef} />
                        </div>

                        {/* Input Area */}
                        <div className="p-4 bg-gray-800/50 backdrop-blur border-t border-gray-700">
                            <form onSubmit={sendMessage} className="flex space-x-2">
                                <input
                                    type="text"
                                    value={inputText}
                                    onChange={(e) => setInputText(e.target.value)}
                                    placeholder="Type a message..."
                                    className="flex-1 bg-gray-900 border border-gray-700 text-white rounded-xl px-4 py-3 focus:outline-none focus:border-purple-500 transition shadow-inner"
                                />
                                <button
                                    type="submit"
                                    disabled={!inputText.trim()}
                                    className="bg-purple-600 text-white p-3 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed hover:bg-purple-500 transition-colors shadow-lg shadow-purple-900/20"
                                >
                                    <svg className="w-6 h-6 transform rotate-90" fill="currentColor" viewBox="0 0 20 20">
                                        <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
                                    </svg>
                                </button>
                            </form>
                        </div>

                    </div>
                </main>
            </Layout>
        </>
    );
}
