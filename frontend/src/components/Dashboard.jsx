// src/components/Dashboard.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
    const [quote, setQuote] = useState('');
    const [quotes, setQuotes] = useState([]);

    // Get JWT token from localStorage
    const token = localStorage.getItem('token');

    // Fetch quotes for the logged-in user
    useEffect(() => {
        const fetchQuotes = async () => {
            try {
                const response = await axios.get('http://localhost:5000/quotes', {
                    headers: {
                        Authorization: `Bearer ${token}`,  // Send JWT token in Authorization header
                    },
                });
                setQuotes(response.data);  // Set the fetched quotes
            } catch (error) {
                console.error('Error fetching quotes:', error);
            }
        };
        fetchQuotes();
    }, [token]);

    // Function to handle adding a new quote
    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            // Post a new quote to the backend
            await axios.post(
                'http://localhost:5000/quotes',
                { quote },
                {
                    headers: {
                        Authorization: `Bearer ${token}`,  // Send JWT token in Authorization header
                    },
                }
            );
            setQuotes([...quotes, { quote }]);  // Add the new quote to the quotes array
            setQuote('');  // Clear the input field
        } catch (error) {
            console.error('Error adding quote:', error);
        }
    };

    return (
        <div>
            <h2>Your Quotes</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Quote:</label>
                    <input
                        type="text"
                        value={quote}
                        onChange={(e) => setQuote(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Add Quote</button>
            </form>

            <h3>Saved Quotes</h3>
            <ul>
                {quotes.map((q, index) => (
                    <li key={index}>{q.quote}</li>  // Display each quote
                ))}
            </ul>
        </div>
    );
};

export default Dashboard;
