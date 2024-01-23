import React from 'react';
import './TopBar.css'; // CSS file for styling
import { logout } from '../../services/logoutService';


const TopBar = ({ incomingTokens, outgoingTokens, balance, onLogout, user_id }) => {
    
    return (
        <div className="top-bar">
            <div className="token-info">
                <span>Incoming Tokens: {incomingTokens}</span>
                <span>Outgoing Tokens: {outgoingTokens}</span>
                <span>Total cost: {balance}€</span>
            </div>
            <div className="user-info">
                <a href={`/dashboard?userId=${user_id}`}>Dashboard</a>
                <button onClick={onLogout}>Logout</button>
            </div>
        </div>
    );
};

export default TopBar;

