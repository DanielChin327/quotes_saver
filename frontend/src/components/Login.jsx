// src/components/Login.jsx
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();  // Used to programmatically navigate to the dashboard

    // Function to handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();  // Prevent page refresh

        try {
            const response = await axios.post('http://localhost:5000/login', {
                username,
                password,
            });

            // Store JWT token in localStorage
            localStorage.setItem('token', response.data.access_token);

            // Redirect to the dashboard after successful login
            navigate('/dashboard');
        } catch (error) {
            // Display error message if login fails
            setError('Invalid username or password');
        }
    };

    return (
        <div>
            <h2>Login</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Username:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default Login;
