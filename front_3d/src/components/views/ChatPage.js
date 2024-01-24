import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { twilight } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { useNavigate, useLocation } from 'react-router-dom';
import React, { useState, useEffect, useRef } from 'react';
import TopBar from '../elements/TopBar';
import io from 'socket.io-client';
import hljs from 'highlight.js';
import './ChatPage.css'

const socket = io('https://www.darkdork.net'); // Replace with your server URL

const ChatPage = () => {
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState("");
    const navigate = useNavigate();
    const location = useLocation();
    const userDataFromLogin = location.state?.userData;
    // change it in prodaction
    const [userData, setUserData] = useState(userDataFromLogin);
    const lastMessageRef = useRef(null);

    const adjustTextareaHeight = (element) => {
        element.style.height = '1.35em';  // Reset the height
        element.style.height = element.scrollHeight  - 22 + 'px';  // Set to scroll height
    };

    const handleTextareaChange = (e) => {
        setNewMessage(e.target.value);
        adjustTextareaHeight(e.target);
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && e.ctrlKey) {
            e.preventDefault(); // Prevent default to avoid a new line being added
            sendMessage();
        } else if (e.key === 'Enter' && !e.ctrlKey) {
            // Insert a new line at the current cursor position
            const cursorPosition = e.target.selectionStart;
            const text = newMessage;
            const newText = text.slice(0, cursorPosition) + '\n' + text.slice(cursorPosition);
            setNewMessage(newText);
        }
    };

    useEffect(() => {
        // Adjust the height of the textarea if it has an initial value
        const textarea = document.getElementById('chatTextarea');
        if (textarea) {
            adjustTextareaHeight(textarea);
        }

        if (lastMessageRef.current) {
            lastMessageRef.current.scrollIntoView({ behavior: "smooth", block: "end" });
        }

        const fetchUserData = async () => {
            try {
                const response = await fetch('api/restore-session/user', {
                    credentials: 'include' // Important for cookies/session
                });
                if (response.ok) {
                    const data = await response.json();
                    setUserData(data);
                } else {
                    navigate('/login'); // Redirect to login if not authenticated
                }
            } catch (error) {
                console.error('Error fetching user data:', error);
                // navigate('/login');
            }
        };

        // Fetch user data only if userDataFromLogin is undefined
        if (!userDataFromLogin) {
            fetchUserData();
        }

        socket.on('receive_message', (message) => {
        setMessages(messages => [...messages, message]);
        });

        socket.on('token_usage', (tokenData) => {
            setUserData(userData => ({
                ...userData,
                incomingTokens: tokenData.incoming_tokens,
                outgoingTokens: tokenData.outgoing_tokens,
            }));
        });

        socket.on('error', (error) => {
            console.error("Error from server:", error.message);
            // Handle errors appropriately
        });

        return () => {
            socket.off('receive_message');
            socket.off('error');
        };    
        
    }, [messages]);

    const sendMessage = () => {
        if (newMessage.trim() !== '') {
            const messageData = { text: newMessage.trim() };
            socket.emit('send_message', messageData);  // Emitting the message to the server

            // Add the sent message to the messages state
            setMessages(messages => [...messages, { text: newMessage, sentByMe: true }]);

            setNewMessage("");  // Clearing the input field
        }
    };

    const handleLogout = async () => {
        const response = await fetch('api/session/logout', { method: 'POST' });
        const data = await response.json();

        if (response.ok) {
            setUserData(null); // Reset userData on logout
            navigate('/'); // Navigate to home or login page            navigate('/'); // or navigate.push('/') for index page
        } else {
            // Handle any errors
            console.error('Logout failed');
        }
    };

    const detectLanguage = (code) => {
        const detected = hljs.highlightAuto(code);
        return detected.language;
    };

    const isCodeBlock = (message) => {
        return message.startsWith('```') && message.endsWith('```');
    };

    const formatMessage = (message) => {
        if (isCodeBlock(message)) {
            const code = message.substring(3, message.length - 3).trim();
            const language = detectLanguage(code);
            return <SyntaxHighlighter language={language} style={twilight}>{code}</SyntaxHighlighter>;
        }
        return message;
    };

    return (
        <div className="chat-container">
            <TopBar 
                incomingTokens={userData.incomingTokens}
                outgoingTokens={userData.outgoingTokens}
                balance={userData.balance}
                onLogout={handleLogout} 
                user_id={userData.id}
            />
            <div className="chat-messages" >
                {messages.map((message, index) => (
                    <div 
                        key={index} 
                        className={message.sentByMe ? 'my-message' : 'other-message'}
                        ref={index === messages.length - 1 ? lastMessageRef : null}
                        id={index === messages.length - 1 ? 'lastMessage' : null}
                    >
                        {formatMessage(message.text)}
                    </div>
                ))}
            </div>
            <div className="chat-input">
                <textarea 
                    id="chatTextarea"
                    rows="1"
                    value={newMessage}
                    onChange={handleTextareaChange}
                    onKeyPress={handleKeyPress}
                    placeholder="Type a message..."
                ></textarea>
                <button className="sendMessage" onClick={sendMessage}>Send</button>
            </div>
        </div>    
    );

};

export default ChatPage;
