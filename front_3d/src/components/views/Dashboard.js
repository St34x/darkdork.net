import { useNavigate, useParams } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import './Dashboard.css'

const Dashboard = () => {
    const [tokenPricing, setTokenPricing] = useState([]);
    // Define state variables for password fields
    const [oldPassword, setOldPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmNewPassword, setConfirmNewPassword] = useState('');
    const [successMessagePassword, setSuccessMessagePassword] = useState('');
    
    // Define state var for username fields
    const [newUsername, setNewUsername] = useState('');
    const [errorMessagePassword, setErrorMessagePassword] = useState('');
    const [successMessageUsername, setSuccessMessageUsername] = useState('');
    const [errorMessageUsername, setErrorMessageUsername] = useState('');
    
    // State for incoming and outgoing token prices
    const [incomingPrice, setIncomingPrice] = useState('');
    const [outgoingPrice, setOutgoingPrice] = useState('');
    const [successMessageTokenPrice, setSuccessMessageTokenPrice] = useState('');
    const [errorMessageTokenPrice, setErrorMessageTokenPrice] = useState('');

    // New states for showing forms
    const [showIncomingPriceForm, setShowIncomingPriceForm] = useState(false);
    const [showOutgoingPriceForm, setShowOutgoingPriceForm] = useState(false);

    const { userId } = useParams();

    const navigate = useNavigate();

    const goBack = () => {
        navigate(-1); // Goes back to the previous page
    };

    // Fetch token prices on component mount
    useEffect(() => {
        const fetchTokenPrices = async () => {
            try {
                const response = await fetch('/api/tokens/get-token-prices', {
                    method: 'POST',
                    headers: {
                        credentials: 'include'
                    }, // Important for cookies/session
                }); // Adjust URL as needed
                if (!response.ok) throw new Error('Failed to fetch token prices');

                const prices = await response.json();
                setIncomingPrice(prices.incomingPrice); // Adjust these according to your API response
                setOutgoingPrice(prices.outgoingPrice);
            } catch (error) {
                console.error('Error fetching token prices:', error);
                // Handle error
            }
        };

        fetchTokenPrices();
    }, []);

    const handleChangePassword = async (userId, oldPassword, newPassword) => {
        if (newPassword !== confirmNewPassword) {
            // Handle the case where the new password and confirmation do not match
            setErrorMessagePassword('New passwords do not match');
            setSuccessMessagePassword('');
            return;
        }

        try {
            const response = await fetch(`/api/change-password/user/${userId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    credentials: 'include' // Important for cookies/session
                },
                body: JSON.stringify({ old_password: oldPassword, new_password: newPassword })
            });

            if (!response.ok) {
                throw new Error('Password change failed');
            }

            // Handle success
            setSuccessMessagePassword('Password changed successfully');
            setErrorMessagePassword('');
        } catch (error) {
            setErrorMessagePassword(error.message);
            setSuccessMessagePassword('');
        }
    };

    const handleChangeUsername = async (userId, newUsername) => {
        try {
            const response = await fetch(`/api/change-username/user/${userId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    credentials: 'include' // Important for cookies/session
                },
                body: JSON.stringify({ new_username: newUsername })
            });

            if (!response.ok) {
                throw new Error('Username change failed');
            }

            // Handle success
            setSuccessMessageUsername('Username changed successfully');
            setErrorMessageUsername('')
        } catch (error) {
            setErrorMessageUsername(error.message);
            setSuccessMessageUsername('')
        }
    };

    const handlePriceUpdate = async (tokenType, newPrice) => {
        try {
            const response = await fetch(`/api/change-price/token-pricing/${tokenType}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    credentials: 'include' // Important for cookies/session
                },
                body: JSON.stringify({ price_per_million: newPrice })
            });

            if (!response.ok) {
                throw new Error('Price update failed');
            }

            // Handle success
            setSuccessMessageTokenPrice(`Price for ${tokenType} tokens was updated successfully`);
            setErrorMessageTokenPrice('');
            alert();
        } catch (error) {
            setErrorMessageTokenPrice(`Error updating price for ${tokenType} tokens: ${error.message}`);
            setSuccessMessageTokenPrice('')
        }
    };

    return (
        <>
        <button onClick={goBack} className="go-back-button">Go Back</button>
        <div className="dashboard-container">
            {successMessageTokenPrice && <div className="success-message">{successMessageTokenPrice}</div>}
            {errorMessageTokenPrice && <div className="error-message">{errorMessageTokenPrice}</div>}
            <div className="price-container">
                <p>Current incoming token price: {incomingPrice}€/1M</p>
                <button className="change-price" onClick={() => setShowIncomingPriceForm(!showIncomingPriceForm)}>
                    Change 
                </button>
            </div>
            {showIncomingPriceForm && (
                <form onSubmit={(e) => {
                    e.preventDefault();
                    handlePriceUpdate('incoming', incomingPrice);
                    setShowIncomingPriceForm(false);
                }}>
                    <input 
                        type="text" 
                        placeholder="New Incoming Price" 
                        value={incomingPrice} 
                        onChange={(e) => setIncomingPrice(e.target.value)} 
                    />
                    <button type="submit">Update Incoming Price</button>
                </form>
            )}
            <div className="price-container">
                <p>Current outgoing token price: {outgoingPrice}€/1M</p>
                <button className="change-price" onClick={() => setShowOutgoingPriceForm(!showOutgoingPriceForm)}>
                    Change 
                </button>
            </div>
            {showOutgoingPriceForm && (
                <form onSubmit={(e) => {
                    e.preventDefault();
                    handlePriceUpdate('outgoing', outgoingPrice);
                    setShowOutgoingPriceForm(false);
                }}>
                    <input 
                        type="text" 
                        placeholder="New Outgoing Price" 
                        value={outgoingPrice} 
                        onChange={(e) => setOutgoingPrice(e.target.value)} 
                    />
                    <button type="submit">Update Outgoing Price</button>
                </form>
            )}            
            

            <p>Change username:</p>
            {successMessageUsername && <div className="success-message">{successMessageUsername}</div>}
            {errorMessageUsername && <div className="error-message">{errorMessageUsername}</div>}
            <form onSubmit={(e) => {
                e.preventDefault();
                handleChangeUsername(userId, newUsername);
            }}>
                <input type="text" placeholder="New Username" onChange={(e) => setNewUsername(e.target.value)} />
                <button type="submit">Change Username</button>
            </form>

            <p>Change password:</p>
            {successMessagePassword && <div className="success-message">{successMessagePassword}</div>}
            {errorMessagePassword && <div className="error-message">{errorMessagePassword}</div>}
            <form onSubmit={(e) => {
                e.preventDefault();
                handleChangePassword(userId, oldPassword, newPassword);
            }}>
                <input type="password" placeholder="Old Password" onChange={(e) => setOldPassword(e.target.value)} />
                <input type="password" placeholder="New Password" onChange={(e) => setNewPassword(e.target.value)} />
                <input type="password" placeholder="Confirm New Password" onChange={(e) => setConfirmNewPassword(e.target.value)} />
                <button type="submit">Change Password</button>
            </form>
        </div>
        </>
    );
};

export default Dashboard;
