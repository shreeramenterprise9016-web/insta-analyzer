import React, { useState } from 'react';

function SearchBar({ onSearch, loading }) {
    const [username, setUsername] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (username.trim()) {
            onSearch(username.trim());
        }
    };

    return (
        <form onSubmit={handleSubmit} className="relative flex items-center">
            <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
            </div>
            <input
                type="text"
                className="block w-full p-4 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-white focus:ring-primary focus:border-primary shadow-sm transition-all"
                placeholder="Enter Instagram Username (e.g. instagram)"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                disabled={loading}
            />
            <button
                type="submit"
                disabled={loading}
                className="absolute right-2.5 bottom-2.5 bg-primary hover:bg-blue-600 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 text-white disabled:opacity-50 transition-colors"
            >
                {loading ? 'Analyzing...' : 'Analyze'}
            </button>
        </form>
    );
}

export default SearchBar;
